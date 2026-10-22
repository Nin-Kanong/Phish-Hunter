# JavaScript Frontend Migration

## Project name

Phish-Hunter Security Operations Platform

## What changed

- Converted the active TypeScript `.ts` and `.tsx` frontend sources to JavaScript `.js` and React JSX `.jsx`.
- Kept React and Vite; React is the UI library, while JavaScript is the programming language.
- Removed TypeScript compiler configuration, type-only declaration files, and TypeScript-specific build commands/dependencies.
- Fixed the React workbench entry file, which previously contained accidental shell heredoc text after its valid initial code.
- Fixed the Settings page's missing closing element so it can be parsed by the frontend bundler.
- Retained the Python/FastAPI backend, static website, analysis modules, templates, tests, configuration, and historical feature documentation.
- Renamed the frontend npm packages to `k4-phish-hunter-workbench` and `k4-phish-hunter-network-artifacts`.

## Build the browser applications

Requirements: Node.js 20 or newer and npm. An internet connection is needed to fetch npm dependencies the first time.

Linux, macOS, or Kali/WSL:

```bash
./scripts/build_frontends.sh
```

Windows PowerShell:

```powershell
.\scripts\build_frontends.ps1
```

The two builds write to `phishhunter/web/static/workbench` and `phishhunter/web/static/network-artifacts`; these are the asset directories consumed by the Python app.

## Python backend

The backend remains Python/FastAPI. It has not been converted to JavaScript. Set up a local environment using the included virtual-environment instructions in `README.md`, then start it with `python run.py`.

## Verification note

The JavaScript source was generated using the TypeScript transpiler's type-erasure and JSX-preservation mode, then reviewed with source/import checks. A full Vite rebuild was not possible in the editing environment because npm registry access returned DNS `EAI_AGAIN`; use the build helper in a network-enabled local environment before depending on a rebuilt React bundle. Existing packaged static bundles are retained.
