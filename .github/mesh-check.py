"""Checks that an unpacked MESH-Piper archive still works the way MESH runs it.

usage: python mesh-check.py <unpacked folder> <voice .onnx, its .onnx.json beside it>

This is MESH's side of the contract, kept in step with MESH's own code: PiperVoices.FindProgram, PiperVoices.JsonLine,
PiperRenderer.Start and SystemVoices.Finished. A check that fails here means MESH needs a change before it can pin the
release built. Every check runs, and each failure is said, then the script exits 1 where any failed.
"""
import json
import os
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile

WINDOWS = os.name == "nt"
# PiperVoices.ProgramNames: MESH looks for these, in this order, within three folders of where it unpacks.
PROGRAM_NAMES = ["piper_exe.exe", "piper.exe"] if WINDOWS else ["piper_exe", "piper"]
MAX_DEPTH = 3

failures = []


def check(ok, what):
    print(("ok    " if ok else "FAIL  ") + what)
    if not ok:
        failures.append(what)
    return ok


def find_program(root):
    """PiperVoices.FindProgram: the first name found within MAX_DEPTH folders, the newer program first."""
    for name in PROGRAM_NAMES:
        found = sorted(p for p in root.rglob(name) if p.is_file() and len(p.relative_to(root).parts) - 1 <= MAX_DEPTH)
        if found:
            return found[0]
    return None


def json_line(text, output):
    """PiperVoices.JsonLine: one JSON object a line, every character past plain ASCII escaped."""
    return json.dumps({"text": text.replace("\r", " ").replace("\n", " "), "output_file": output}, ensure_ascii=True)


def wave_format(path):
    """SystemVoices.Finished's reading: the fmt chunk's format and bits, the extensible form's sub-format first."""
    data = path.read_bytes()
    if len(data) < 44 or data[0:4] != b"RIFF" or data[8:12] != b"WAVE":
        return None
    pos = 12
    while pos + 8 <= len(data):
        cid, size = data[pos:pos + 4], struct.unpack_from("<I", data, pos + 4)[0]
        if cid == b"fmt ":
            fmt, _, _, _, _, bits = struct.unpack_from("<HHIIHH", data, pos + 8)
            if fmt == 0xFFFE and size >= 40:
                fmt = struct.unpack_from("<H", data, pos + 8 + 24)[0]
            return fmt, bits
        pos += 8 + size + (size & 1)
    return None


def main():
    root, voice = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()

    found = find_program(root)
    if not check(found is not None, f"MESH finds {' or '.join(PROGRAM_NAMES)} within {MAX_DEPTH} folders of the archive"):
        return
    check(found.name == PROGRAM_NAMES[0], f"the program MESH finds is the newer {PROGRAM_NAMES[0]}, not the 2023 program")

    # MESH keeps the program in its settings folder, which can be a long path, so the program is run from a copy
    # under a folder past 160 characters, as espeak-ng's data path once had to fit in, yet short enough that its data
    # files stay inside Windows' 260.
    # The folder's name is sized from the temporary folder's own length, which differs by system.
    base = pathlib.Path(tempfile.mkdtemp(prefix="mesh-check-"))
    tail = os.sep.join(["", "Voices", "Piper", "Program", "bin"])
    name = ("MESH Settings Folder " * 20)[:max(20, 175 - len(str(base)) - len(tail) - 1)].strip()
    deep = base / name / "Voices" / "Piper" / "Program"
    shutil.copytree(found.parent.parent if found.parent.name == "bin" else found.parent, deep)
    program = find_program(deep)
    check(len(str(program.parent)) > 160, f"the program runs from a folder path of {len(str(program.parent))} characters")

    out = deep.parent / "Speech"
    out.mkdir()
    lines = [("Button 1, Fire", out / "line1.wav"), ("Café crème, Ölfass, señor", out / "line2.wav")]
    stdin = "".join(json_line(text, str(path)) + "\n" for text, path in lines)

    for speed in (None, "0.8"):
        for _, path in lines:
            path.unlink(missing_ok=True)
        # PiperRenderer.Start: the model, the lines as JSON on its input, the speed as --length_scale, from the
        # program's own folder.
        args = [str(program), "--model", str(voice), "--json-input"] + (["--length_scale", speed] if speed else [])
        run = subprocess.run(args, cwd=program.parent, input=stdin.encode("utf-8"), capture_output=True, timeout=300)
        said = (run.stdout + run.stderr).decode("utf-8", "replace")
        how = "at the voice's own speed" if speed is None else f"with --length_scale {speed}"
        check(run.returncode == 0, f"the program ends without an error {how} (exit {run.returncode})")
        for text, path in lines:
            check(path.is_file() and path.stat().st_size > 44, f"it writes {path.name} {how}")
            fmt = wave_format(path) if path.is_file() else None
            check(fmt in ((1, 16), (3, 32)), f"{path.name} is 16-bit PCM or 32-bit float, the two MESH reads ({fmt})")
            check(path.name in said, f"it says {path.name}'s path as it writes it")
        if failures:
            print(said[-2000:])

    shutil.rmtree(deep.parents[3], ignore_errors=True)


if __name__ == "__main__":
    main()
    if failures:
        print(f"\n{len(failures)} check(s) failed. MESH needs a change before it can pin this build.")
        sys.exit(1)
    print("\nEvery check passed. MESH runs this build as it is.")
