# paper-lcd-maze

Generate the maze with the supplied ARM depthFirstSearch interface, draw walls at 16-pixel cell size, and move a white square only through open passages.

## Run and inspect

Start at row 1, column 2. A blocked direction leaves the square still. A legal edge moves one cell. A hold does not repeat. All four outer boundaries remain inaccessible.

## Resource ownership

- LCD: supplied GLCD parallel driver; P0.0–P0.7 data, P0.19–P0.25 control; see driver pin masks
- RIT:50 ms joystick sampling; IRQ queues edges; foreground performs drawing
- ARM depthFirstSearch: original four-argument maze generation contract
- Queue:seven usable direction snapshots; dropped_moves reports overflow

## Files to replace

Open sample.uvprojx. All files below are already installed in this project. To adapt another template copy, replace these exact files; do not add a second handler.
- Source/sample.c
- Source/ASM_funct.s
- Source/button_EXINT/IRQ_button.c
- Source/timer/IRQ_timer.c
- Source/RIT/IRQ_RIT.c
- Source/systick/IRQ_systick.c
- Source/adc/IRQ_adc.c
- Source/GLCD/AsciiLib.c
- Source/GLCD/AsciiLib.h
- Source/GLCD/GLCD.c
- Source/GLCD/GLCD.h
- Source/GLCD/HzLib.c
- Source/GLCD/HzLib.h
