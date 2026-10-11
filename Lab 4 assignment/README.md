# Crack the Cipher Chip — ELCT918 Verilog Refresher Assignment

**Course:** Selected Topics in AI Accelerators Hardware Design (ELCT918), German University in Cairo
**Instructors:** Dr. Eman Azab, MSc Eng. Nour ElShahawy
**Students:** Shrouq Mohamed, BahaaElDin Hassan

## Links

- **EDA Playground:** https://edaplayground.com/x/BB5A
- Simulator: Icarus Verilog 12.0 (tick *Open EPWave after run* to see the waveforms)

## Password

```
6 3 B 9
```

Entered one nibble per enabled clock cycle right after reset, the chip outputs the ciphertext
`C A F E` (`dout` = `1c`, `2a`, `3f`, `4e`) and raises `flag` on the fourth nibble.

## Files

| File | Contents |
|------|----------|
| `mystery.sv` | The unchanged `mystery` netlist |
| `solution.sv` | our `module solution` |
| `tb.sv` | Experiments, self-checking comparison of `mystery` vs `solution`, and the password test |
| `README.md` | This file |

## How to run

1. Open the EDA Playground link above (or paste `design.sv` and `testbench.sv` into a new playground).
2. Select **Icarus Verilog 12.0** and run.
3. The log ends with:

```
correct_count =       31595
error_count =           0
PASS
```

## Test plan

`testbench.sv` drives `mystery` and `solution` with the same `clk`, `rst_n`, `en` and `din`. Each test step applies `en`/`din` at the falling edge. The `check` task then compares `dout` and `flag` of both designs 1 ns after the rising edge. Every checked cycle counts as correct or as an error, and each error prints `FAIL` with its cycle number, time and both outputs.

### Phase 1 — Directed experiments (469 cycles)

| ID | Stimulus | What it checks |
|----|----------|----------------|
| T1 | Reset, then `en = 0` with `din = 5`, `9` | Reset value of `dout`/`flag`; `din` is ignored while `en` is low |
| T2 | `din = 5` ×20 | Counter in `dout[7:4]` and its wrap-around F → 0; key sequence 6, 7, 4, 5 |
| T3 | `din = 9` ×20 | Counter and key continue across a new input; mod-16 wrap of `din + key` (9 + 7 = 0) |
| T4 | `din = 2` ×20 | Same cipher with another value |
| T5 | Every `din` 0–F, 20 times each (400 cycles) | `ciphertext = din + key` for all 16 inputs at every key position |
| T6 | `rst_n = 0` with `en = 1` | Reset overrides `en` (synchronous clear) |
| T7 | After reset: `en = 1`, `en = 0` ×2, then `en = 1` ×3 | Counter and key restart at position 1; `en` low freezes counter, key and `dout` |

### Phase 2 — Random test (31,105 cycles)

| ID | Stimulus | What it checks |
|----|----------|----------------|
| R1 | 30,000 iterations with `din = $random` | Encryption for arbitrary input sequences |
| R2 | One extra `en = 0` cycle every 30th iteration (1,000 cycles) | Holding state in the middle of a message, at every key position |
| R3 | One-cycle reset every 190th iteration that is not a multiple of 30 (105 resets) | Reset from arbitrary counter, key and history states |

### Phase 3 — Password and edge cases (21 cycles)

| ID | Sequence | Expected `flag` | What it checks |
|----|----------|-----------------|----------------|
| P1 | reset, `6 3 B 9` | Rises on the 4th nibble | The password produces `CAFE` and raises `flag` |
| P2 | reset, `6 3 B`, reset, `9` | Stays 0 | Reset clears the ciphertext history |
| P3 | reset, `6 3`, `en` low, `B 9` | Rises on the last nibble | An `en`-low cycle pauses the history without breaking the word |
| P4 | reset, `6 3 B 9`, `en` low ×3, `0` | Rises, holds while `en` is low, falls on the next nibble | `flag` is registered and updates only on enabled edges |

### Optional — Exhaustive password search (commented out)

The testbench also contains a loop, commented out, that tries all 65,536 four-nibble inputs after reset. It prints every input that raises `flag`. Only `6 3 B 9` does.

### Pass criterion

The run passes when `error_count = 0` over all 31,595 checked cycles (469 + 31,105 + 21), and the log then prints `PASS`.

## Summary

- **Task 1 — Re-implementation:** `solution` is written as readable RTL. It uses a 4-state FSM that picks the key, a 4-bit encryption counter, a 16-bit ciphertext history and registered `dout`/`flag`. It was derived from simulation experiments, not from the netlist.
- **Task 2 — Self-checking testbench:** `mystery` and `solution` run side by side on the same inputs. The testbench replays the directed experiments and then runs 30,000 random iterations with `en`-low cycles and resets inserted. It compares `dout` and `flag` on every cycle: **31,595 cycles, 0 mismatches, PASS.**
- **Task 3 — Password:** the target word `CAFE` was decrypted with the known key sequence (6, 7, 4, 5). A commented-out exhaustive search over all 65,536 four-nibble inputs is included in the testbench as a check.