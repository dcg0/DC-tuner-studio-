# DCtuneRstudio Branding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create an independent DCtuneRstudio-branded distribution of the rusEFI console while preserving firmware, ECU protocols, calculations, data I/O, and GPLv3 licensing.

**Architecture:** Keep the existing Java console modules, package names, protocol code, and generated ECU resources unchanged. Add a small branding constants class, update only visible startup/window/menu copy and Swing theme defaults, replace brand assets at existing resource paths, and add a non-invasive top-level static `ui/` brand shell plus a Gradle compatibility aggregator.

**Tech Stack:** Java/Swing, Gradle/Shadow, PNG/ICO assets, static HTML/CSS.

**Spec:** User request in conversation, dated 2026-09-21.

## Global Constraints

- Do not modify firmware, communication protocols, autotune, maps, calculations, or data read/write logic.
- Preserve `license.txt` and internal rusEFI credits; show the rusEFI credit only in the About dialog for user-facing branding.
- Use DC colors: `#00ccff`, `#0099ff`, `#ff2244`, `#ff4466`, `#050508`, `#0f0f1a`, `#e8e8f0`, `#00ff99`, `#1a1a2e`.
- Do not modify the existing root `README.md` or any `media/` directory.
- Produce `java_console/build/libs/DCtuneRstudio.jar` through the existing Shadow packaging task.

## Review Focus

- Main window title must remain DCtuneRstudio across connected, offline, updating, and bootloader states.
- Startup screen must not expose rusEFI branding and must display the DC Laboratory identity.
- About must retain the GPLv3 rusEFI credit without leaking it into primary UI surfaces.
- Protocol/resource identifiers must remain untouched so ECU signatures and INI resolution still work.
- The requested Gradle command must resolve through a compatibility `:java_console` aggregator without changing module behavior.

## Tasks

- [ ] Add branding constants and visible UI copy updates.
- [ ] Apply the DC Swing theme and replace brand assets.
- [ ] Add the static `ui/` shell and Gradle compatibility task.
- [ ] Build the Shadow JAR and run focused regression checks.
