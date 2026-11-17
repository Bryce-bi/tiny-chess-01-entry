# tiny-chess-01 entry

A chess engine for make.fun's "Build the strongest chess engine in 4 KB of
Python" bounty. `main.py` is the whole engine (4,070 bytes as committed),
Python 3.13 standard library only, reading no other file.

## How it plays

- Lazy-legality move generation: pseudo-legal moves are generated, sorted
  by a simple MVV-LVA capture heuristic, and checked for king safety one
  at a time, so alpha-beta cutoffs skip legality checks on moves never
  tried.
- Negamax alpha-beta search with a quiescence extension on captures
  (4 plies), under iterative deepening.
- Deterministic by a node-count budget, never a clock: the same position
  and history always produce the same move, so a replay matches.
- Material + a small positional bonus (centre file/rank, pawn
  advancement) for evaluation.
- Does not castle. Dropping it kept the rest of the move generator (legal
  captures, promotions, en passant, check detection) inside the 4,096-byte
  cap with room to spare for search and evaluation.

## Verifying it

The move generator was checked against the standard perft reference
values (the start position to depth 4, and the "Kiwipete" test position)
before being minified into `main.py`; both matched exactly. See the
submission's transcripts for the development and verification sessions.

## Size rule

`main.py` is at most 4,096 bytes as committed; the whole repository is at
most 8,192 bytes, no file over 4,096. MIT licensed (see LICENSE).
