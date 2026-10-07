# Treasure Hunt

Explore a procedurally generated dungeon, collect the key, then open the chest.

## Getting Started

This game uses **pygame**. Install it before running:

```bash
pip install pygame-ce
python game.py
```

> **Note:** If you are on Python 3.12 or newer, use `pygame-ce` (Community Edition) instead of `pygame`. It is a drop-in replacement with the same API.


## Controls

| Key | Action |
|-----|--------|
| W/A/S/D or Arrows | Move |
| R | Restart |

## Before changing the code

Play through the dungeon and observe how movement, tile collision, and item collection are handled. Trace the flow from `GameEngine` through `Player` and back. Understand how the grid and player state interact before making any modifications.

## Task 1 — Traps

Add floor traps that send the player back to their starting position when stepped on.

**Done when:** the player is visibly reset to the start room on stepping a trap, and a clear status message is shown.

## Task 2 — Enemy Guard

Add a guard that patrols back and forth near the chest. Touching the guard resets the player to start.

**Done when:** the guard moves between two patrol points each frame and correctly resets the player on collision.

## Task 3 — Mini-map

Draw a small mini-map in a corner of the screen showing the dungeon layout.

**Done when:** the mini-map updates in real time, distinguishes walls from floor, and marks the player's current position.

## Task 4 — Inventory UI

Show a HUD inventory slot that is empty at the start and displays a key icon once the key is collected.

**Done when:** the slot renders correctly in both states and updates immediately on key pickup.

## Required testing

Collect the key then the chest, trigger every trap type, collide with the guard, verify the player resets correctly each time, check the mini-map reflects the actual grid, and confirm the inventory slot updates on collection. Test restarting mid-run.

## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.

## Submission checklist

- [ ] Tasks 1–4 completed and tested.
- [ ] Traps reset the player correctly.
- [ ] Guard patrol and collision reset work.
- [ ] Mini-map reflects the dungeon in real time.
- [ ] Inventory slot updates on key pickup.
- [ ] No unnecessary external dependencies added beyond pygame.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Submission

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes
- [ ] A 10-second video of gameplay **after** your changes, showing the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
