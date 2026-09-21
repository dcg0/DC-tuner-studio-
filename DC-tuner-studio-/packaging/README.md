# DCtuneRstudio releases

The GitHub Actions workflow builds the universal JAR on Linux and native installers on Windows, macOS, and ARM64 Linux. Each native installer bundles its matching Java runtime and therefore does not require Java to be preinstalled.

The Raspberry Pi package is built on a native ARM64 runner and targets Raspberry Pi OS 64-bit (`arm64`). An `armhf` package is not produced unless an ARMv7 runner and matching JDK are supplied; labeling an ARM64 package as `armhf` would make it unusable.

The release workflow overlays these branding files onto a fresh checkout of the official rusEFI source, so the small public repository can remain focused on the DCtuneRstudio distribution assets while the build still contains the complete technical source tree.
