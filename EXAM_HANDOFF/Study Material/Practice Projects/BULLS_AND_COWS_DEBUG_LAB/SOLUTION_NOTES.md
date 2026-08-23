# Bulls and Cows solution notes

- Q1 uses four pointer arguments, so no stacked argument is required.
- The assembly routine saves R4-R11 and keeps the ten-register frame eight-byte aligned.
- Exact matches are excluded from both frequency arrays.
- C clears the work arrays before every attempt.
- Timer1 runs freely and is sampled only for the first game start.
- Guess digits occupy LED fields `[1:0]`, `[3:2]`, `[5:4]` and `[7:6]`; this maps guess 0 to LEDs 10/11 and guess 3 to LEDs 4/5.
- Joystick callbacks retain only new press edges. The foreground state machine performs the assembly call.
- The formula is `((2^bulls - 1) << 4) + (2^cows - 1)`; the PDF's superscript can disappear during text extraction.
- The high result nibble equals fifteen when bulls equals four, which turns on LEDs 4-7 and ends the game.

Build the only `CA Exam` target. Physical acceptance requires the LandTiger board and confirmed joystick operation.
