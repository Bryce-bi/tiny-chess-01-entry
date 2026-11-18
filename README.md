# tiny-chess-01 entry

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Bryce-bi/tiny-chess-01-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Bryce-bi/tiny-chess-01-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine for make.fun's ["Build the strongest chess engine in 4 KB of
Python"](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
bounty. `main.py` (3,348 bytes as committed) unpacks and execs a
compressed payload of the real engine, which is both allowed and counted
by the bounty's rules ("a `main.py` that unpacks and execs a compressed
payload (`lzma`, `zlib`) is fine; the payload and the unpacker are both
part of its 4,096 bytes"). It reads no other file at runtime.

## How it plays

Lazy-legality move generation (pseudo-legal, MVV-LVA ordered, with a pin
fast-path that skips the full king-safety recheck when a move plainly
can't expose the king and isn't already in check), negamax alpha-beta
with check-aware quiescence (evasions searched, not stand-pat, when in
check at the horizon) and a one-ply check extension in the main search,
iterative deepening bounded by a 20,000-node budget (never a clock, so a
replay matches), castling, and material + centre/pawn-advance/bishop-pair
eval.

## Why main.py is a compressed payload

The readable source (`engine_src.py`, not committed — `.gitignore`) is
~9.2 KB with quiescence and castling back in; too big to fit raw.
`main.py` is `engine_src.py` packed by the kit's own
`node cli/makefun.mjs compress`, as its README and rules describe. The
bundle for submission needs `--compress-source main.py=engine_src.py` so
the authorship checks read the real source, not the compressed bytes.

## Verifying it

Perft-checked before and after packing (startpos depths 1-4: 20, 400,
8902, 197281; Kiwipete depths 1-3: 48, 2039, 97862, castling included) —
exact match both times. See the submission's transcripts for the rest.

## Size rule

`main.py` is at most 4,096 bytes as committed; the whole repository is at
most 8,192 bytes, no file over 4,096. MIT licensed (see LICENSE).
