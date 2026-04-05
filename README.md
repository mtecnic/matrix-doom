# Matrix Doom — ASCII FPS in Pygame

A Matrix-themed first-person shooter rendered entirely with ASCII/Unicode characters in a pygame monospace grid. Green phosphor on black, cascading character rain, raycasting corridors, particle physics — the whole aesthetic.

**This project was generated autonomously** by an experimental modular code-building agent as a research artifact. Every file — 32 across 10 modules — was planned, scaffolded, built, and validated without human edits.

## What's in here

- **Raycasting engine** — DDA-based 3D corridor rendering using Unicode block characters
- **Particle physics** — shell casings, debris with gravity, bounce, and fade
- **3 weapon types** with distinct particle effects
- **Enemy AI** with pathfinding
- **HUD** — ammo, health, minimap
- **5+ procedurally generated levels**
- **Matrix rain** — cascading green characters on menus and as gameplay overlay

## How it was built

This game is the output of a single autonomous build session testing a **modular decomposition pipeline** for an LLM-driven code generator. The pipeline:

1. **Architecture** — LLM designs the project, detects it needs 20+ files, triggers modular mode
2. **Modular manifest** — decomposes into dependency-sorted module waves (config first, then asset/utils, then weapon/player/input, etc.)
3. **Per-module build** — each module is scaffolded and built with a scoped context window (only its own files + dependency interface stubs), keeping token usage under 40K even for large projects
4. **Integration** — a separate phase wires modules together via `main.py`, resolves cross-module imports
5. **Validation** — syntax, imports, naming conventions, `--test` self-check, all automated

The full build took **94 LLM rounds across ~17 minutes** against a local Qwen3-Coder model. No cloud API, no human in the loop.

### Why this matters

Flat single-agent builds hit a wall around 15 files — the code map saturates the context window and the LLM loses coherence. The modular pipeline solves this by giving each module its own scoped build cycle (~10 files, ~20K tokens), then composing them. This test validated that the approach works end-to-end: plan, scope, build, integrate, validate.

## Run it

```bash
pip install pygame
python3 main.py
```

Self-test (headless-safe):
```bash
python3 main.py --test
```

## Project structure

```
config/          — settings, constants
asset/           — font loading, glyph cache
utils/           — math helpers, file I/O
weapon/          — weapon types, projectiles, particle effects
player/          — stats, controller, movement
input/           — key bindings, input handler
levelgen/        — procedural map generation
particle/        — particle physics engine
world/           — grid, collision detection
enemy/           — AI, pathfinding
renderer/        — ASCII raycasting, Matrix rain overlay
menu/            — menu state machine, manager
main.py          — game loop, CLI entry point
```

## Build metadata

| Metric | Value |
|--------|-------|
| Total files | 32 |
| Modules | 10 |
| LLM rounds | 94 |
| Build time | ~17 min |
| Model | Qwen3-Coder (local, 4-bit quantized) |
| Validation | All 6 checks passed (naming, imports, syntax, lint, run, tests) |
| Human edits | 0 |
