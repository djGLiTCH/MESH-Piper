# MESH-Piper

Builds of [Piper](https://github.com/OHF-Voice/piper1-gpl), the local text-to-speech program from the Open Home
Foundation, for Windows, macOS and Linux. [MESH](https://github.com/djGLiTCH/MESH) reads your arcade panel's control
labels aloud with Piper's voices, and it downloads one of these builds only when you press its Download button.

This repository is a fork of Piper. Its `mesh` branch is Piper's code, unchanged, with this folder's files added:
this page, `THIRD-PARTY.md`, `PIPER_COMMIT`, the workflow that makes the builds (`workflows/mesh-build.yml`) and the
one that follows Piper's main (`workflows/mesh-update.yml`), with `mesh-version.sh`, which gives a release's
version. Piper's own README is `README.md` at the top of the branch.

These are builds of Piper's own command-line program, `piper_exe` from Piper's `libpiper`. Piper itself publishes no
builds of that program, only its Python package.

MESH does not contain Piper, and Piper does not contain MESH. MESH starts this program as a separate program and
hands it text on its input, and the program writes sound files.

## What each build holds

Each release has one archive per platform: Windows x64, macOS on Apple silicon and on Intel, and Linux x64 and arm64.
Each holds:

- `piper_exe` (`piper_exe.exe` on Windows), Piper's command-line program
- the libraries it runs with: Piper's `libpiper`, espeak-ng, and ONNX Runtime
- on Windows, the Microsoft Visual C++ runtime's files, so nothing else needs installing
- `espeak-ng-data`, the data espeak-ng reads words with
- `COPYING` (GPL-3.0), `THIRD-PARTY.md` with every part's licence, and `SOURCE.md` naming the exact source of the
  build

Each release also has `SHA256SUMS.txt`, the SHA-256 sum of each archive and of `mesh-contract.txt`, which holds the
contract number below.

## MESH's check

`mesh-check.py` runs a build the way MESH runs Piper, and every build runs it, as does "Check a release with MESH"
on a published release. Its `CONTRACT` numbers that way of running Piper, and MESH carries the same number. When MESH
changes what it needs of the program, the number goes up in both.

MESH carries one release's archives by size and SHA-256. A newer release reaches MESH without a new MESH only through
a record the MESH developer signs, naming the release, its contract number and each archive's size and SHA-256. MESH
uses that release only where the record checks against the developer's keys, the release is newer than the one it
carries and the contract number is its own, and it checks each download against the record.

## macOS

The macOS builds are not signed. MESH clears the quarantine macOS puts on a download when it fetches Piper itself.
Where macOS still stops `piper_exe` on its first run, open System Settings > Privacy & Security and choose Open
Anyway beside its name.

## Source

The `mesh` branch at a release's tag is the complete source of that release's builds. The workflow also fetches
espeak-ng, ONNX Runtime and Open JTalk as Piper's own build does, at the versions Piper's build names.

Release v1.8.1-rc1 builds Piper at commit `46c3c71`, on Piper's main branch after its 1.8.0 release, which reads
the voices retrained since October 2026.

## Versions

A release takes the version of the Piper it builds. Where that Piper is a release of Piper's own, the tag is its
version. Where it is newer, as Piper's main often is, the tag is one patch step past Piper's last version with `-rc`
and a number, as `v1.8.1-rc1` follows 1.8.0, until Piper's own next release gives the version. A release candidate
is published as a pre-release. The program itself says Piper's own version when asked.

## Moving to a newer Piper

Each Monday the workflow `workflows/mesh-update.yml` looks at Piper's main. Where it has moved, it merges it into the
branch `piper-update`, moves `PIPER_COMMIT` on, builds and tests every platform there, and opens a pull request into
`mesh` that names the release it will make. Merging that pull request with a merge commit builds every platform
again and publishes the release, with its version as above. It can also be started by hand from the Actions tab.

`PIPER_COMMIT` names the Piper commit the branch builds, and each archive's `SOURCE.md` names it too.

Piper's own workflows are switched off in this fork. Syncing this fork's `main` runs nothing and leaves `mesh` as
it is.

## Licence

Piper is licensed under the GNU General Public License, version 3 (GPL-3.0), and so are these builds. See `COPYING`.
Every other part keeps its own licence, listed in `THIRD-PARTY.md`.

Piper's voices are not in these builds. Each voice carries its own licence, given in its MODEL_CARD on
[Piper's voices page](https://huggingface.co/rhasspy/piper-voices), and some voices are for non-commercial use only.

## Releasing

A push to `mesh` builds and tests every platform. A tag starting with `v`, pushed once that build is green, publishes
the archives and their sums as that tag's release.

## Building it yourself

The workflow's steps run on any machine with CMake and a C++ compiler. On Windows, clang-cl (from LLVM) also builds
it, once two clang errors in espeak-ng's own command-line tool, which Piper does not use, are made warnings.
