# BC Small Claims Web Host

This directory contains the first web-host shell for the BC Small Claims assistant.

Its current job is narrow on purpose: present a BC Gov-oriented React host over the same
canonical Notice of Claim JSON contract already used by the plugin path. It is not a second
renderer, not a second intake architecture, and not yet a live filing client.

## Current Scope

- show the shared canonical case JSON core
- keep the downstream branches visible: guided intake, deterministic PDF generation, and mock filing adapter
- provide a clean base for later BC Gov design-system alignment and hosted workflow work

## Boundary Rules

- intake remains upstream and owns conversational guidance plus canonical JSON updates
- PDF generation remains deterministic and separate from the web UI
- filing-adapter behavior remains deterministic and separate from the web UI
- the web host should consume the same canonical JSON contract rather than inventing its own data model

## Commands

Run from `web/`:

```bash
npm install
npm run dev
npm run test -- src/App.test.tsx
npm run build
npm run lint
```

## Next Web Slices

1. Replace the read-only JSON preview with structured editors backed by the same canonical schema.
2. Introduce BC Gov design-system components and typography once the target package versions are chosen.
3. Add a thin API seam so the web host can call the deterministic renderer and mock filing-adapter without duplicating their logic.
