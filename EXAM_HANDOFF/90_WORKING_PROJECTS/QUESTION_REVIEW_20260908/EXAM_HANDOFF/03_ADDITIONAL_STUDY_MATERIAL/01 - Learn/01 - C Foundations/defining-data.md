# Defining data in C and ARM assembly

Use this guide when a question asks you to define constants, arrays, matrices,
tables, state shared with an interrupt, or objects shared between C and assembly.
The companion buildable example is `Code Recipes/01 - C and Assembly
Integration/Sharing data`.

## 1. C declarations and definitions

A declaration tells the compiler a name and type. A definition also allocates
storage (or supplies a function body). An external object must have exactly one
definition in the whole program.

```c
/* shared.h: declarations; safe to include from many C files */
extern volatile uint32_t sample_ready;
extern int16_t samples[64];

/* shared.c: the one definition of each object */
volatile uint32_t sample_ready;
int16_t samples[64];
```

Putting a non-`static` definition in a header creates one definition per C file
and usually causes a multiply-defined-symbol linker error. `extern` without an
initializer is a declaration. `extern uint32_t x = 1;` is still a definition and
should normally live in a `.c` file.

## 2. Choose the width and signedness deliberately

Use `<stdint.h>` types where the question specifies a width:

| C type | Width | Typical ARM access |
|---|---:|---|
| `uint8_t` / `int8_t` | 8 bits | `LDRB` / `LDRSB` |
| `uint16_t` / `int16_t` | 16 bits | `LDRH` / `LDRSH` |
| `uint32_t` / `int32_t` | 32 bits | `LDR` / `STR` |
| `uint64_t` / `int64_t` | 64 bits | two words, normally low then high |

Unsigned arithmetic wraps modulo 2^N. Signed overflow is undefined in C. Use
unsigned intermediate arithmetic, explicit range checks, or a wider type when
overflow is possible. In assembly, choose signed conditions (`LT`, `GE`, `GT`,
`LE`) or unsigned conditions (`LO/CC`, `HS/CS`, `HI`, `LS`) to match the data.

## 3. Initialization and storage duration

```c
uint32_t ticks;                     /* static storage, zero-initialized */
uint32_t limit = 1000u;             /* initialized writable object */
static uint8_t private_state;       /* visible only inside this C file */
const uint16_t sine[4] = {0, 512, 1023, 512};

void f(void) {
  uint32_t temporary;               /* automatic local; indeterminate */
  uint32_t cleared = 0u;
  static uint32_t calls;             /* static lifetime; retains value */
}
```

Globals and `static` objects live for the entire program. Uninitialized ones are
zero-filled before `main`. Ordinary locals normally use the stack and do not
start at zero. Do not make a large exam buffer an ordinary local: it can exhaust
the small embedded stack. Prefer a file-local `static` array unless recursion or
reentrancy requires separate instances.

## 4. `const`, `volatile`, and interrupt-shared state

- `const` means the program must not modify the object through that name. It is
  suitable for lookup tables and may be placed in flash.
- `volatile` tells the compiler that every read and write is observable. Use it
  for memory-mapped registers and state changed by an ISR, hardware, or another
  execution context.
- `static volatile` is a common choice for interrupt-shared state that should be
  private to one C file.
- `volatile` does not make `counter++` atomic. It is a load, add, and store. For
  a multi-step shared update, use `critical_enter()` and `critical_exit()` or
  design a single-writer event handoff.

```c
static volatile uint32_t event_bits;

void timer_callback(uint8_t timer, uint32_t flags) {
  (void)timer;
  (void)flags;
  event_bits |= 1u;
}

uint32_t take_events(void) {
  uint32_t key = critical_enter();
  uint32_t result = event_bits;
  event_bits = 0u;
  critical_exit(key);
  return result;
}
```

## 5. Scalars, arrays, matrices, strings, structures, enums, and pointers

```c
uint32_t count = 4u;
int16_t vector[5] = {3, -1, 8};           /* remaining two are zero */
uint8_t grid[3][4] = {{1, 2}, {3}, {4}};  /* row-major */
char message[] = "READY";                 /* includes trailing '\0' */
const char *message_ptr = "READY";        /* pointer to a literal */

typedef enum { IDLE, RUNNING, DONE } state_t;
typedef struct {
  int16_t x;
  int16_t y;
  uint32_t flags;
} point_t;

point_t point = {.y = 7, .x = -2, .flags = 1u};
uint16_t values[8] = {[0] = 10u, [7] = 20u};

typedef void (*work_callback_t)(uint32_t event);
work_callback_t callback;
```

For a real array in its defining scope, the element count is
`sizeof array / sizeof array[0]`. `sizeof array` alone is the number of bytes.
An array name usually converts to a pointer to its first element, and that
pointer does not contain the array length, so calculate the count before the
conversion and pass it separately. A two-dimensional array is contiguous and
row-major: `grid[r][c]` is at
`base + (r * column_count + c) * element_size`.

An array object and a pointer object are different. `sizeof vector` in its
defining scope is the full array size; `sizeof pointer` is only the address size.
Inside `void f(int a[])`, `a` is a pointer parameter, not an array object.

## 6. Size, alignment, padding, and structure layout

Use `sizeof(type)` for total size and `offsetof(type, member)` from `<stddef.h>`
for field offsets. The compiler may insert padding to align members. Never guess
structure offsets in assembly.

For the `point_t` above on this target:

| Member | Expected offset | Access |
|---|---:|---|
| `x` | 0 | `LDRSH`/`STRH` |
| `y` | 2 | `LDRSH`/`STRH` |
| `flags` | 4 | `LDR`/`STR` |
| total size | 8 | — |

Document and verify this contract:

```c
_Static_assert(offsetof(point_t, x) == 0u, "point_t.x layout");
_Static_assert(offsetof(point_t, y) == 2u, "point_t.y layout");
_Static_assert(offsetof(point_t, flags) == 4u, "point_t.flags layout");
_Static_assert(sizeof(point_t) == 8u, "point_t size");
```

If the course compiler does not enable `_Static_assert`, inspect the values in
the debugger or encode them as enum constants during development.

## 7. Passing data between C and assembly

AAPCS passes the first four 32-bit words in `R0`–`R3`; further arguments begin
on the caller's stack. A function result normally returns in `R0`. A 64-bit
result uses `R0:R1` (low word, high word).

### Array pointer and length

```c
extern int32_t asm_sum(const int32_t *values, uint32_t count);
int32_t total = asm_sum(values, 8u); /* R0=address, R1=8 */
```

```asm
asm_sum PROC
        MOVS    R2, #0
loop    CBZ     R1, done
        LDR     R3, [R0], #4
        ADD     R2, R2, R3
        SUBS    R1, R1, #1
        B       loop
done    MOV     R0, R2
        BX      LR
        ENDP
```

### Writable output buffer

```c
extern uint32_t asm_filter(const int16_t *source, uint32_t count,
                           int16_t *destination, uint32_t capacity);
```

Here `R0` is the input address, `R1` the input count, `R2` the output address,
and `R3` the output capacity. Return the number of elements written in `R0`.
The capacity prevents assembly from writing past the destination.

### Matrix

```c
extern int32_t asm_matrix_sum(const int32_t *base,
                              uint32_t rows, uint32_t columns);
int32_t total = asm_matrix_sum(&matrix[0][0], ROWS, COLUMNS);
```

Assembly may multiply `rows * columns` for a flat traversal, or calculate
`((row * columns) + column) << 2` for indexed access.

### Structure pointer

```c
extern uint32_t asm_point_score(const point_t *point);
```

`R0` contains an address, not the structure bytes. Use `LDRSH [R0,#0]`, `LDRSH
[R0,#2]`, and `LDR [R0,#4]` for the verified layout above.

### Constant table

```c
const uint16_t scale_table[4] = {1u, 10u, 100u, 1000u};
```

Assembly imports the symbol, obtains its address with `LDR R0, =scale_table`,
and reads an element with `LDRH R1, [R0, R2, LSL #1]`. Do not store through the
address.

## 8. ARMASM data definitions

### Areas and constants

```asm
BUFFER_COUNT    EQU     16
FLAG_READY      EQU     (1 :SHL: 3)

        AREA    |.constdata|, DATA, READONLY
table   DCB     1, 2, 3, 4       ; bytes
halves  DCW     100, 200         ; 16-bit halfwords
words   DCD     &11223344, 99    ; 32-bit words

        AREA    |.data|, DATA, READWRITE
        ALIGN   2                ; 2^2 = 4-byte alignment in ARMASM
counter DCD     0
buffer  SPACE   BUFFER_COUNT
```

`EQU` creates an assembly-time constant and allocates no storage. `DCB`, `DCW`,
and `DCD` allocate initialized bytes, halfwords, and words. `SPACE` reserves the
given number of bytes. Place writable objects in `DATA, READWRITE` and constants
in `DATA, READONLY`.

### Address versus contents

```asm
        LDR     R0, =counter  ; R0 = address of counter
        LDR     R1, [R0]      ; R1 = 32-bit contents
        ADDS    R1, R1, #1
        STR     R1, [R0]      ; write the new contents
```

`LDR Rn, =constant` is a pseudo-instruction that materializes a value or address.
`LDR Rn, [Rm]` dereferences the address held in `Rm`.

### Arrays, strings, structures, and pointer tables

```asm
        AREA    |.constdata|, DATA, READONLY
bytes   DCB     4, 8, 15, 16, 23, 42
text    DCB     "READY", 0

        ALIGN   2
matrix  DCD     1, 2, 3       ; row 0
        DCD     4, 5, 6       ; row 1

POINT_X     EQU 0
POINT_Y     EQU 2
POINT_FLAGS EQU 4
point0  DCW     -2, 7
        DCD     1

        ALIGN   2
pointers DCD    bytes, text, matrix, point0
```

On the LPC1768, memory is little-endian: the least-significant byte of a word is
at the lowest address. Element address scaling is `index`, `index << 1`, or
`index << 2` for byte, halfword, or word arrays.

### Local stack storage

```asm
worker  PROC
        PUSH    {R4-R7,LR}    ; 20 bytes: SP is now misaligned by 4
        SUB     SP, SP, #20   ; total change 40 bytes, preserves 8-byte alignment
        ; [SP,#0]..[SP,#19] is private temporary storage
        ADD     SP, SP, #20
        POP     {R4-R7,PC}
        ENDP
```

Calculate the complete frame, including saved registers, stacked arguments, and
locals. SP must be 8-byte aligned at a public call boundary. After changing SP,
the offsets of arguments originally passed on the stack also change.

## 9. Exporting and importing objects

### C defines, assembly uses

```c
/* one C definition */
volatile uint32_t c_counter;
uint32_t c_values[8];
const uint16_t c_table[4] = {1, 10, 100, 1000};
```

```asm
        IMPORT  c_counter
        IMPORT  c_values
        IMPORT  c_table
```

### Assembly defines, C uses

```asm
        AREA    |.data|, DATA, READWRITE
        ALIGN   2
        EXPORT  asm_counter
asm_counter DCD 0

        EXPORT  asm_buffer
asm_buffer  SPACE 32
```

```c
extern uint32_t asm_counter;
extern uint8_t asm_buffer[32];
```

The C declaration must match the element width, signedness where comparisons or
extension matter, array extent when known, and mutability. Do not declare a
read-only assembly table as writable C data.

## 10. Common failures and fast diagnosis

| Symptom | Likely cause | Check |
|---|---|---|
| Undefined symbol | missing definition, spelling/case mismatch, missing `EXPORT` | linker symbol name and project file list |
| Multiply defined | object definition placed in a header | keep one definition; use `extern` elsewhere |
| Values look truncated | wrong element width | C type versus `LDRB/H`, `LDRSB/SH`, `LDR` |
| Negative values become large positive | unsigned load/comparison | use signed type, `LDRSB/SH`, signed branch |
| First elements work, later ones fail | wrong address scale or missing count check | element size and loop bound |
| Structure fields are nonsense | guessed padding/offset | `offsetof` and `sizeof` |
| Works without optimization only | missing `volatile`, lifetime bug, or undefined behavior | ISR sharing, dangling pointer, overflow, bounds |
| Stack corruption | large local, wrong fifth-argument offset, unbalanced frame | SP delta and stack view |
| Flash fault | attempted store to `const`/read-only area | section attributes and `STR` target |

## 11. Debugger checklist

1. Open the map/symbol view and confirm each shared symbol has one address.
2. Inspect the memory at the symbol address before and after the call.
3. At assembly entry, confirm `R0`–`R3` contain the documented addresses/counts.
4. Check array end addresses: `base + count * element_size` is one past the end.
5. Compare structure field addresses with `offsetof`.
6. Confirm constants are in a read-only section and buffers in read-write/zero
   initialized storage.
7. Single-step one iteration and watch the base pointer advance by exactly the
   element width.
8. Check SP alignment before every `BL` and verify the restore path on every exit.

## 12. Exam adaptation checklist

- Write the element type, signedness, count, mutation permission, and invalid
  input behavior before coding.
- Decide whether data belongs on the stack, in static writable storage, or in a
  read-only table.
- For C/assembly calls, write the register contract beside the prototype.
- For a structure, record verified offsets and total size.
- For arrays/matrices, pass every dimension not fixed by the function contract.
- For ISR-shared state, choose a single-writer design or protect compound access.
- Test empty, one-element, maximum-size, negative/signed, duplicate, and boundary
  cases, then inspect the exact bytes in memory.
