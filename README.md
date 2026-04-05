<br>
<p align="center">
  <pre align="center">
  ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗
  ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝
  ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝
  ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗
  ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗
  ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
              ██████╗  ██████╗  ██████╗ ███╗   ███╗
              ██╔══██╗██╔═══██╗██╔═══██╗████╗ ████║
              ██║  ██║██║   ██║██║   ██║██╔████╔██║
              ██║  ██║██║   ██║██║   ██║██║╚██╔╝██║
              ██████╔╝╚██████╔╝╚██████╔╝██║ ╚═╝ ██║
              ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝     ╚═╝
  </pre>
</p>

<p align="center">
  <strong>A first-person shooter rendered entirely in ASCII.</strong><br>
  <em>Green phosphor. Digital rain. Raycasting corridors. Particle physics.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-green?style=flat-square&logo=python&logoColor=white" alt="Python 3.12">
  <img src="https://img.shields.io/badge/pygame-2.5-green?style=flat-square&logo=python&logoColor=white" alt="Pygame">
  <img src="https://img.shields.io/badge/files-32-green?style=flat-square" alt="32 files">
  <img src="https://img.shields.io/badge/human%20edits-0-green?style=flat-square" alt="Zero human edits">
  <img src="https://img.shields.io/badge/built%20by-autonomous%20agent-black?style=flat-square" alt="Built by AI">
</p>

---

## What is this?

Matrix Doom is an ASCII-rendered FPS built in pygame — raycasting corridors drawn with Unicode block characters, particle physics for shell casings and debris, enemy AI with A* pathfinding, procedurally generated levels, and the full Matrix green-on-black aesthetic with cascading digital rain.

**Every line of code was written by an AI agent.** No human touched the source. This is a research artifact from building and testing a modular autonomous code generator.

---

## Features

| Feature | Details |
|---------|---------|
| **Raycasting Engine** | DDA-based 3D corridor rendering using Unicode block chars on a monospace grid |
| **Particle Physics** | Shell casings, debris — gravity, bounce, fade |
| **3 Weapon Types** | Each with distinct projectile behavior and particle effects |
| **Enemy AI** | A* pathfinding, state-based behavior |
| **Procedural Levels** | 5+ levels generated from room layouts with corridors |
| **Digital Rain** | Cascading Matrix character rain on menus and as gameplay overlay |
| **HUD** | Ammo, health, minimap — all in ASCII |

---

## Quick Start

```bash
pip install pygame
python3 main.py
```

Run the self-test suite (headless-safe):

```bash
python3 main.py --test
```

---

## Project Structure

```
matrix-doom/
├── main.py              # Game loop, CLI entry point
├── config/              # Settings, constants
├── asset/               # Font loading, glyph cache
├── renderer/            # ASCII raycasting, Matrix rain overlay
│   ├── ascii.py         # DDA raycaster, wall/floor rendering
│   └── rain.py          # Digital rain effect
├── weapon/              # Weapon registry, projectiles, particle FX
├── particle/            # Particle physics engine
├── player/              # Stats, first-person controller
├── enemy/               # AI manager, A* pathfinding
├── levelgen/            # Procedural map generation
├── world/               # Grid, collision detection
├── input/               # Key bindings, input handler
├── menu/                # Menu state machine
└── utils/               # Math helpers, file I/O
```

---

## How It Was Built

This game is the first successful output of a **modular autonomous build pipeline** — an LLM agent that decomposes large projects into dependency-sorted module waves and builds each one with a scoped context window.

### The problem

Single-agent code generators hit a wall around 15 files. The code map saturates the context window, the model loses coherence, and builds fail or produce broken spaghetti.

### The solution

Decompose the project into modules. Build each module in isolation with only its own files + dependency interface stubs in context. Then wire them together in an integration phase.

### The pipeline

```
PLAN ──> DEPS ──> MODULE WAVES ──> INTEGRATE ──> VALIDATE
                       │
            ┌──────────┼──────────┐
            ▼          ▼          ▼
         config    asset/utils   weapon/player/input ...
        (wave 1)   (wave 2)        (wave 3)
```

Each module gets ~20K tokens of context (vs 65K blown on a flat build). Modules in the same wave can run in parallel since they don't depend on each other.

### Build stats

| Metric | Value |
|--------|-------|
| **Total files** | 32 |
| **Modules** | 10 |
| **LLM rounds** | 94 |
| **Build time** | ~17 minutes |
| **Model** | Qwen3-Coder (local, 4-bit quantized) |
| **Validation** | 6/6 checks passed |
| **Human edits** | 0 |

The model ran locally on an RTX 4090. No cloud APIs were used.

---

## Why release this?

This is a proof-of-concept for **autonomous modular code generation**. The game itself is fun to look at, but the real result is that the pipeline works: an LLM can plan a 30+ file project, decompose it into modules, build each one in a scoped context, and integrate them into a working application — all without human intervention.

We're building toward agents that can construct real software, not just snippets. This is one step on that road.

---

<p align="center">
  <sub>Built autonomously by an experimental code agent. Research artifact — not production software.</sub>
</p>
