# Wlad ElHalal — speaker detour

Separate practice copy of the exam starting project. The original template is
not edited. This is an audio playback experiment, separate from exam lessons.

## What plays

A six-second excerpt, 00:45–00:51, from
[Tamer Ashour — Wlad ElHalal](https://www.youtube.com/watch?v=tcZgr2oM6kg).
The recording is converted to mono, 8 kHz, IMA ADPCM with half gain
and short fades at the ends. It includes vocals and instruments rather than a
note-only melody approximation. Sound quality is limited by the conversion
and board speaker.

The initial 20-second PCM version exceeded the installed evaluation linker's
image-size allowance. This shorter compressed version uses 24,576 bytes of
audio data so the complete firmware can fit the installed tools' limit.

[Listen to the converted clip](Audio/preview.wav).

## Open and run

1. Open [sample.uvprojx](sample.uvprojx) in Keil.
2. For the physical board, select `LandTiger_LPC1768 (release)` and build.
   The `SW_Debug` target is intended for the simulator.
3. Connect/configure the debugger and load this practice program when ready.
   This project has not been flashed or tested on the physical board here.
4. Enable the board's DAC-to-speaker connection as required by its jumper or
   switch arrangement. The program uses DAC output P0.26.
5. Reset and run. LD4 indicates playback; LD5 indicates completion. LD6
   indicates timer configuration failure. Reset and run again to replay.

The clip plays once; it does not loop. The potentiometer and buttons are not
used. Stopping at breakpoints interrupts the audio, so run continuously to
listen. Simulator build success does not imply that Keil produces PC sound.

## How it works

- [Source/sample.c](Source/sample.c) initializes the DAC and Timer0 at 8,000
  interrupts per second.
- [Source/timer/IRQ_timer.c](Source/timer/IRQ_timer.c) writes one stored sample
  to the DAC per interval. It maps a decoded signed 16-bit sample to the
  10-bit DAC scale. After the clip, it stops Timer0 and returns to midscale.
- [Source/song_samples.h](Source/song_samples.h) contains compressed constant
  audio stored in flash, not a large writable RAM buffer.
- [Source/song_decoder.h](Source/song_decoder.h) decodes one sample at a time,
  producing 48,000 samples over six seconds.
- [Audio/source.json](Audio/source.json) records the excerpt and conversion.

Unlike a two-level square wave, this recording has many samples per waveform
cycle. Here 8 kHz is the audio sampling rate, not the song's pitch.

## Verification

See [BUILD_REPORT.json](BUILD_REPORT.json) and the build logs in `Listings`.
The decoder algorithm was checked against FFmpeg: all 48,000 samples match.
Native compiler/linker validation covers both target variants. It does not
prove physical speaker wiring, volume, or real-time interrupt performance.
Command-line build outputs are under `Objects/board` and `Objects/simulator`;
the Keil project can build its own normal output separately.

The local preparation and build helpers are in
[SONG_DETOUR_TOOLS](../SONG_DETOUR_TOOLS/). No network access is needed by the
board: the excerpt is compiled into the firmware.
For reproduction, `prepare_player.py` creates a fresh copy, then
`compress_player.py` converts it to this size-limited version, and
`build_player.py` compiles both target variants. Preparation refuses to
overwrite an existing project.

After this detour, return to the
[peripheral lessons](../../01_EXAM_READY/FRESH_SOLVED_ARM_EXAMS/01_GUIDES_AND_INDEXES/PERIPHERALS_CANONICAL.md).
