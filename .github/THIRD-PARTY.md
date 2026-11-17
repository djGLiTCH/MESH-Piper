# The parts of each build and their licences

Each build's archive carries every licence file named here, in its `licenses` folder unless the table says otherwise.

| Part | Where it comes from | Version | Licence | Its licence files |
|---|---|---|---|---|
| Piper (`piper_exe`, `libpiper`) | https://github.com/OHF-Voice/piper1-gpl | The Piper commit the `mesh` branch is built on, named in `SOURCE.md` | GPL-3.0 | `COPYING` |
| espeak-ng | https://github.com/espeak-ng/espeak-ng, fetched by Piper's build | The commit Piper's `libpiper/CMakeLists.txt` names | GPL-3.0, with parts under Apache-2.0, BSD-2-Clause and the Unicode licence | `licenses/espeak-ng-COPYING`, `-COPYING.APACHE`, `-COPYING.BSD2`, `-COPYING.UCD` |
| ONNX Runtime | https://github.com/microsoft/onnxruntime, its release fetched by Piper's build | The version Piper's `libpiper/CMakeLists.txt` names | MIT | `licenses/onnxruntime-LICENSE`, `licenses/onnxruntime-ThirdPartyNotices.txt` |
| Open JTalk, for Japanese voices | https://github.com/tsukumijima/open_jtalk, fetched by Piper's build | The commit Piper's `libpiper/CMakeLists.txt` names | Modified BSD | `licenses/open_jtalk-COPYING` |
| The Microsoft Visual C++ runtime, Windows only | The Visual Studio build tools on the build machine, the runtime's own files placed beside the program | As the build's compiler | Microsoft's terms for the Visual C++ Redistributable, which let a program carry these files | None carried |
