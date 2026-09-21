#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}"
: "${RUSEFI_COMMIT:?RUSEFI_COMMIT is required}"
BUILD_DIR="${GITHUB_WORKSPACE}/.build/rusefi-src"
OVERLAY="${GITHUB_WORKSPACE}/DC-tuner-studio-"

rm -rf "${BUILD_DIR}"
mkdir -p "${GITHUB_WORKSPACE}/.build"
git clone --filter=blob:none --no-checkout https://github.com/rusefi/rusefi.git "${BUILD_DIR}"
git -C "${BUILD_DIR}" fetch --depth=1 origin "${RUSEFI_COMMIT}"
git -C "${BUILD_DIR}" checkout --detach "${RUSEFI_COMMIT}"
git -C "${BUILD_DIR}" submodule update --init java_console/peak-can-basic java_console/luaformatter

copy_overlay() {
  local source="$1"
  local destination="${BUILD_DIR}/$1"
  mkdir -p "$(dirname "${destination}")"
  cp -f "${OVERLAY}/${source}" "${destination}"
}

copy_overlay LICENSE
copy_overlay settings.gradle
copy_overlay java_console/build.gradle
copy_overlay java_console/ui/build.gradle
copy_overlay java_console/shared_io/src/main/resources/shared_io.properties
copy_overlay java_console/autoupdate/src/main/resources/com/rusefi/logo.png
copy_overlay java_console/core_ui/src/main/resources/com/rusefi/appicon.png
copy_overlay java_console/trigger-ui/src/main/resources/com/rusefi/logo.png
copy_overlay java_console/trigger-ui/src/main/resources/com/rusefi/logo_alphax.png
copy_overlay java_console/trigger-ui/src/main/resources/com/rusefi/logo_mre.png
copy_overlay java_console/trigger-ui/src/main/resources/com/rusefi/logo_proteus.png
copy_overlay java_console/trigger-ui/src/main/resources/com/rusefi/logo_tutomo.png
copy_overlay java_console/ui/src/main/java/com/rusefi/DCtuneRstudioBrand.java
copy_overlay java_console/ui/src/main/java/com/rusefi/Launcher.java
copy_overlay java_console/ui/src/main/java/com/rusefi/StartupFrame.java
copy_overlay java_console/ui/src/main/java/com/rusefi/ui/basic/UiHelper.java
copy_overlay java_console/ui/src/main/java/com/rusefi/ui/console/MainFrame.java
copy_overlay java_console/ui/src/main/resources/com/rusefi/banner.png
copy_overlay java_console/ui/src/main/resources/com/rusefi/splash.png

echo "SOURCE_DIR=${BUILD_DIR}" >> "${GITHUB_ENV}"
