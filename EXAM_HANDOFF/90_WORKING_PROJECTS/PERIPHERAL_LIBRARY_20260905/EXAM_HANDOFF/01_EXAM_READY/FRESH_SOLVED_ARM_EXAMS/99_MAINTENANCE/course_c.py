"""C curriculum: explanations, traces, attempt-first exercises, and answers."""
def lesson(key, title, explanation, code, trace, task, hints, answer, mistakes, checkpoint, tags, reading=None, tier="Exam core"):
    return dict(id=key, title=title, explanation=explanation, code=code, trace=trace,
                task=task, hints=hints, answer=answer, mistakes=mistakes,
                checkpoint=checkpoint, tags=tags.split("|"), reading=reading, tier=tier)

C = [
lesson("c-program", "1. Your first program and the build process",
"""A program is a sequence of instructions operating on data. C is the language you write; the processor executes machine instructions produced from it. A source file ends in .c. The compiler checks and translates it into an object file. The linker combines object files and finds definitions for names used across files. A debugger lets you pause the program and inspect its state.

Copy the whole Official Combined Exam API project into 90_WORKING_PROJECTS, open sample.uvprojx, and build the unchanged copy. The C entry point is main in Source/sample.c. Braces group statements; a semicolon ends a statement. Comments explain intent but do not execute.

The include lines make declarations available. exam_init initializes shared board support; it does not start every peripheral. The infinite loop keeps the embedded program alive. __WFI means wait for an interrupt: it is not a time delay and is inappropriate while immediate work remains.""",
'''#include "LPC17xx.h"
#include "exam_api.h"
int main(void)
{
    exam_init();
    for (;;) {
        __WFI();
    }
}''',
"Reset/startup initializes the C runtime → main begins → exam_init runs once → the loop waits → an interrupt may wake it → the loop repeats.",
"Build this in a copy. Put a breakpoint on exam_init and step into the loop. Explain why moving exam_init inside the loop changes behavior.",
["Count how often each statement runs.", "Initialization resets software state; it is not repeated foreground work."],
"exam_init belongs before the loop because it runs once. Repeating it can erase events and reinitialize outputs. A baseline build separates environment failures from later logic errors.",
"Compiler errors concern syntax/types; undefined-symbol linker errors mean a referenced definition is missing. Fix the first meaningful error, not every follow-on message.",
"Point to main, initialization, and repeated work; describe compile versus link.", "Core|Toolchain|Build", 1),

lesson("c-values", "2. Variables, assignment, types, and expressions",
"""A variable is named storage with a type. A definition creates it; initialization gives its starting value. Assignment later replaces that value. In x = x + 1, read old x, calculate the result, then store it back.

uint32_t describes a 32-bit unsigned integer and comes from stdint.h. A literal such as 3u is unsigned. Signed values use int32_t when negatives are meaningful. These types affect both the representable range and how expressions are calculated.

Multiplication and division bind more tightly than addition; parentheses make intent explicit. Integer division discards the fractional part. % gives the remainder, not a percentage. A local automatic variable without an initializer has no promised usable starting value. Initialize before reading, and put units such as milliseconds in names or comments.""",
'''#include <stdint.h>
uint32_t boxes = 3u;
uint32_t per_box = 4u;
uint32_t total = boxes * per_box;
total = total + 2u;
uint32_t groups = total / 5u;
uint32_t left = total % 5u;''',
"total=12 → total=14 → groups=2, left=4. Integer division does not produce 2.8.",
"Trace a=7u; b=3u; a=a+b; b=a/4u; a=a%4u. Then define a variable representing -3.",
["Assignments use the most recent values.", "Use a signed type for negative data."],
"a becomes 10, b becomes 2, and a finally becomes 2. Use int32_t temperature = -3; for the negative quantity.",
"Uninitialized values are unreliable. 7/2 is 3 in integer arithmetic. Prevent division by zero.",
"Predict intermediate values and distinguish initialization from later assignment.", "C|Types|Arithmetic", 3),

lesson("c-decisions", "3. Conditions, Boolean logic, and switch",
"""A comparison such as count == 0u produces true or false. Assignment uses =; equality uses ==. C treats zero as false and nonzero as true. if executes a body when its condition is true; else supplies the alternative.

Logical && means both conditions; || means at least one. They short-circuit: the right side might not execute. This permits a pointer check before a dereference. ! reverses truth. Bitwise & and | operate on bits and do not give the same short-circuit protection.

switch selects among integer or enum values. A case is a label, not an automatically isolated branch: execution continues until break, return, or the end. Use default to handle unexpected values deliberately. Braces keep multi-statement branches unambiguous.""",
'''uint32_t count = 2u, ready = 1u, action = 0u;
if ((ready != 0u) && (count > 0u)) {
    action = 1u;
} else {
    action = 2u;
}
switch (action) {
case 1u: count--; break;
case 2u: count = 0u; break;
default: break;
}''',
"Both conditions are true → action=1 → count becomes 1 → break prevents case 2 from clearing it.",
"Accept values 10 through 20 inclusive. Explain the effect of removing break after case 1.",
["Inclusive bounds use >= and <=.", "Switch cases fall through without an exit."],
"if ((value >= 10u) && (value <= 20u)) accepts the range. Without break, count becomes zero in case 2. Test 9, 10, 20, 21.",
"if (x=0) changes x and evaluates false. A stray semicolon after if ends the controlled statement.",
"Explain =, ==, &, and && with concrete values.", "C|Conditions|State", 3),

lesson("c-loops", "4. Loops, tracing, and termination",
"""A for loop groups initialization, condition, and update. Initialization runs once; the condition is checked before each body; the update follows the body. while also checks before its body. do/while runs its body at least once.

For n elements, indexes range from zero through n-1. Use i<n: it naturally permits n=0 without computing n-1 in unsigned arithmetic. break exits the nearest loop; continue advances to the next iteration's update or condition.

An invariant is a fact true at the same point in each iteration. For a sum, 'sum contains the first i elements' explains whether the update order is correct. A termination argument states what moves toward the exit. Write an iteration table before adding nested loops.""",
'''uint32_t sum = 0u;
for (uint32_t i = 0u; i < 4u; ++i) {
    sum += i;
}''',
"Before bodies: (i,sum)=(0,0),(1,0),(2,1),(3,3). After the last body sum=6. i becomes 4 and the condition fails.",
"Sum integers 1 through n for n<=1000. Trace n=0, n=1, n=4.",
["Start the term at 1.", "The stated bound matters: a UINT32_MAX bound requires another termination design."],
"sum=0u; for(i=1u;i<=n;++i) sum+=i; gives 0, 1, 10. The n<=1000 contract prevents loop-counter wrap and sum overflow in this illustration.",
"Omitting an update can create an infinite loop. <=n accesses one element too far in zero-based arrays. Unsigned decrement below zero wraps.",
"State the invariant, stopping rule, and number of iterations.", "C|Loops|Bounds", 5),

lesson("c-functions", "5. Functions, parameters, scope, and lifetime",
"""A prototype states a function's return type, name, and parameter types. Calling it evaluates arguments and transfers control. return supplies the result and returns to the caller. A void return means no result; void in the empty parameter list means no parameters.

C passes ordinary arguments by value. A parameter gets a copy, so modifying it does not modify the caller's variable. Later, output pointers provide explicit access to caller-owned objects.

Scope means where a name is usable. Lifetime means how long its object exists. An automatic local belongs to one invocation; a static local survives later calls and introduces persistent state. Prefer explicit inputs and outputs for algorithms so you can test them without peripherals.""",
'''static uint32_t add_one(uint32_t value)
{
    value = value + 1u;
    return value;
}
/* Inside a function: */
uint32_t a = 4u;
uint32_t b = add_one(a);''',
"a=4 → parameter value=4 → local value=5 → return assigns b=5. a remains 4.",
"Write maximum(a,b) for signed 32-bit values. Test equality and two negatives.",
["Keep the prototype and body signed.", "Equal inputs permit either one to be returned."],
"static int32_t maximum(int32_t a,int32_t b) { return (a>b)?a:b; } changes neither caller argument. maximum(-4,-2)=-2; maximum(7,7)=7.",
"A declaration without a definition can fail at linking. Returning an automatic local's address creates a dangling pointer.",
"Write a prototype and explain exactly what crosses the function boundary.", "C|Functions|ABI", 4),

lesson("c-bits", "6. Binary, hexadecimal, widths, and safe arithmetic",
"""A bit is 0 or 1; eight bits form a byte. One hexadecimal digit represents four bits: 0xA is decimal 10, 0xFF is 255. uint8_t ranges 0..255; int8_t ranges -128..127. A word on this ARM target is 32 bits. Width and signedness are contractual, not cosmetic.

OR sets selected bits; AND keeps selected bits; XOR toggles them; complement inverts them. A mask selects positions. Use unsigned operands and a shift count smaller than the operand width: shifting a 32-bit value by 32 is invalid.

Unsigned arithmetic wraps modulo its width. Signed overflow is undefined C behavior, not a reliable wraparound technique. Cast before multiplying for a wide intermediate; casting afterwards cannot recover high bits already lost. Validate a result's range before narrowing it.""",
'''uint32_t value = 0x05u;          /* 00000101 */
value |= (1u << 1);             /* 00000111 */
value &= ~(1u << 2);            /* 00000011 */
value ^= (1u << 0);             /* 00000010 */
uint64_t product = (uint64_t)100000u * 100000u;''',
"value becomes 7, 3, then 2. product=10000000000 cannot fit in uint32_t.",
"Extract bits 4..7 of 0xAB. Replace that field with 3, preserving bits 0..3.",
["Shift right, then mask with 0xF.", "Clear the old field before inserting the replacement."],
"field=(word>>4)&0xFu gives 10. word=(word&~0xF0u)|((3u&0xFu)<<4) gives 0x3B. Validate the range 0..15 if truncation is not allowed.",
"Do not detect C signed overflow by performing it. Signed/unsigned comparisons may convert negative values unexpectedly.",
"Convert 0xA5 to binary and explain widening before multiplication.", "C|Bits|Overflow|Fixed-point", 6),

lesson("c-pointers", "7. Memory, pointers, and output parameters",
"""Memory stores bytes at addresses. A pointer contains an address, not the object itself. &x obtains x's address; *p accesses the object at p. A pointer's type determines the object's size and interpretation. For uint32_t*, p+1 advances one word, or four bytes on this target.

A null pointer denotes no object. Check before dereferencing, but remember non-null is insufficient: lifetime, alignment, accessible range, and type must also be correct. A function cannot infer buffer capacity from a pointer; pass counts explicitly.

An output parameter is a pointer through which a function changes caller-owned storage. const uint32_t *p prevents modifying the pointed-to value through p; it does not make the pointer variable itself constant.""",
'''static int divide_by_two(uint32_t value, uint32_t *out)
{
    if (out == 0) return 0;
    *out = value / 2u;
    return 1;
}
/* Inside a function: */
uint32_t result = 99u;
int ok = divide_by_two(9u, &result);''',
"&result supplies the address → out receives it → *out=4 changes result → ok=1 reports success.",
"Write swap for two int32_t pointers. State a null policy and test swapping an object with itself.",
["Save the first value before overwriting it.", "Check both pointers before either dereference."],
"static void swap(int32_t *a,int32_t *b) { if(!a||!b)return; int32_t t=*a; *a=*b; *b=t; } treats null as no operation. The same valid pointer twice leaves its value unchanged.",
"An uninitialized pointer allocates no object. Passing result instead of &result confuses a value and an address. sizeof(pointer) is not capacity.",
"Draw pointer storage and pointed-to storage separately.", "C|Pointers|Memory", 4),

lesson("c-collections", "8. Arrays, strings, matrices, and bounds",
"""An array stores consecutive same-type elements. uint32_t a[3] has indexes 0,1,2. In most expressions an array becomes a pointer to its first element; when passing it to a function, carry the length separately. The caller must provide a valid region.

A C string ends in a zero byte. Capacity includes that terminator; an arbitrary byte buffer is not necessarily a string. Find a terminator within the available capacity before calling a function that assumes one exists.

Rectangular C arrays use row-major order. For cols words per row, element (r,c) is at byte offset (r*cols+c)*4. A pointer-to-pointer is not a flat matrix. Keep coordinates, element indexes, and byte offsets separate.""",
'''static uint32_t sum(const uint32_t *a, uint32_t n)
{
    uint32_t total = 0u;
    for (uint32_t i=0u; i<n; ++i) total += a[i];
    return total;
}
/* Contract: a addresses n words; unsigned wrap is intentional. */
uint32_t grid[2][3] = {{1u,2u,3u},{4u,5u,6u}};
char word[3] = {'O','K','\0'};''',
"grid[1][2] is element 5 at byte offset 20, containing 6. word needs three bytes for two visible letters.",
"Trace sum for [] and [2,4,6]. Find the flat index of row 2 column 1 in a 4-by-3 matrix. How much storage holds HELLO?",
["An empty sum must not load element zero.", "Stride is the column count, not the row count."],
"Sums are 0 and 12. Matrix index=2*3+1=7; word-byte offset=28. HELLO needs six bytes including zero. A null array pointer is usable in this sum only when n=0 and no access occurs.",
"<=n reads past the end. A wrong stride can appear correct for square matrices; test non-square dimensions.",
"Explain length versus capacity and map coordinates into memory.", "C|Arrays|Strings|Matrix|Bounds", 5),

lesson("c-state", "9. Structures, enums, and explicit state machines",
"""A structure groups named fields. Use a dot for an object field and -> for a pointed-to object's field. The compiler may insert padding for alignment. When assembly shares a structure, determine the actual target offsets rather than summing field widths.

An enum names states. A state machine defines current state, event, next state, and action. An event records something that happened; a state records what remains true afterwards. Write a transition table before code.

Separate persistent data from per-round data. A secret, calibration, or accumulated score may need to survive restart. Explicit state prevents one event from accidentally meaning both submit and restart in the same pass.""",
'''enum phase { EDITING, SHOWING };
struct game { enum phase phase; uint32_t guess; uint32_t secret; };
static void select_pressed(struct game *g)
{
    if (g->phase == EDITING) {
        g->phase = SHOWING; /* compute/display result here */
    } else {
        g->guess = 0u;
        g->phase = EDITING;
    }
}''',
"EDITING, guess=3, secret=7 → first press enters SHOWING → second press clears guess and returns to EDITING; secret stays 7.",
"Add FINISHED, which ignores select. Write transition rows before editing.",
["Handle FINISHED before the existing branches.", "Winning is a deliberate transition, not a reset."],
"Return immediately in FINISHED. In EDITING compute the result: winning enters FINISHED, otherwise SHOWING. SHOWING+select clears only guess and enters EDITING. Distinguish distinct presses from a held level.",
"Several independent flags may form impossible states. Clearing the whole structure also destroys persistent fields.",
"List every transition and every field that survives restart.", "C|State|Joystick|Buttons", 8),

lesson("c-files", "10. Headers, declarations, and ownership",
"""A translation unit is a C file after includes are processed. #include supplies declarations, not necessarily an implementation. Headers normally declare shared functions and extern objects rather than defining mutable global storage repeatedly.

File-scope static keeps a name private to that file. extern declares storage defined elsewhere. const prevents writes through that declaration. Header guards prevent repeated inclusion in one translation unit. Macros substitute text: parenthesize arguments and avoid side effects such as i++ in a macro that evaluates an argument twice.

Edit Source/sample.c and Source/ASM_funct.s for answers. Existing IRQ files may already define a required vector. Find and edit that owner in the working copy; adding a second handler in sample.c causes duplicate symbols. Do not remove whole driver groups simply to silence errors.""",
'''/* counter.h */
#ifndef COUNTER_H
#define COUNTER_H
#include <stdint.h>
extern uint32_t counter;
void increment(void);
#endif
/* counter.c: the single definition */
uint32_t counter = 0u;
void increment(void) { ++counter; }''',
"Multiple files can include the declaration. Only counter.c allocates counter. The linker connects references to that definition.",
"Explain undefined symbol versus multiply defined symbol. Should a helper used only in sample.c be static?",
["One case has zero definitions; the other has multiple.", "Limit visibility when sharing is unnecessary."],
"Undefined means an implementation is absent, excluded, or differently named. Multiply defined means several included files own the same symbol. A private helper should normally be static. Check project membership first.",
"An initialized global in a header creates multiple definitions. Renaming an IRQ handler prevents the vector from reaching it.",
"Identify the one owner of each shared object and interrupt vector.", "C|Headers|Linker|IRQ", 2),

lesson("c-events", "11. Interrupts, volatile, and shared events",
"""An interrupt temporarily diverts execution into a handler. Foreground is ordinary main-loop work. A peripheral flag identifies the interrupt's cause. Clearing that hardware flag and consuming a software event are different operations.

volatile says a value can change outside ordinary control flow. It does not make compound operations atomic. Read a flag, process, then clear it: an interrupt between the read and clear can be lost.

The API's atomic event helpers transfer bit flags. A bit means 'at least one occurrence'; repeated sets coalesce. If every occurrence matters, use a bounded counter or queue with a stated overflow policy and brief protection. Long calculations belong in foreground. Do not wait for interrupts with interrupts disabled.""",
'''/* In the single existing Timer0 handler: */
if (exam_timer_ack(EXAM_TIMER0) & 1u) {
    exam_events_set(1u);
}
/* In the foreground loop: */
uint32_t events = exam_events_take(1u);
if (events & 1u) {
    /* bounded foreground work */
}''',
"Two IRQs set bit 0 before main consumes it → main receives 1, not 2. The flag is a pending condition, not a count.",
"A sensor must retain every sample in order. Design the storage and full-buffer policy.",
["Notification and sample storage are separate.", "Decide what happens when producer overtakes consumer."],
"Use a fixed-capacity sample queue with protected indexes. A bit can announce nonempty storage but cannot replace it. For example reject newest on full and increment an overflow count; do not silently discard required data.",
"volatile alone cannot protect read-modify-write. A wrong acknowledgement can cause endless IRQ entries. An empty-check followed by sleep has a race; use a documented wait strategy or bounded foreground polling.",
"Explain why two events coalesce and when a queue is required.", "C|IRQ|Events|Atomic", 9),

lesson("c-integration", "12. C calls assembly and incremental debugging",
"""The C prototype and exported assembly symbol describe the same interface. Match name, argument order, width, signedness, and return type. Ordinary first-four 32-bit words use R0-R3. Later words use stack handling. Study the AAPCS unit before applying this simplified rule to 64-bit arguments.

First use a temporary correctly named stub to prove linking and project membership. A stub proves connection, not correctness. Record it visibly and remove it before submission. Replace it with the smallest real operation and inspect the returned value.

Keep pure computation separate from LED output and handlers. A wrong display can be an encoding or physical-index problem even when the function is correct. Check the returned value in the debugger before blaming the display.""",
'''extern uint32_t add_three(uint32_t value);
static volatile uint32_t observed;
/* Inside main, after initialization: */
observed = add_three(7u);
/* Expected debugger value: 10 */''',
"C passes 7 in R0 → assembly returns 10 in R0 → C stores observed=10. The deliberate volatile object keeps a debugger-visible result.",
"Write add_three in ARMASM. List checks before wiring its return to LEDs. Use unsigned-wrap semantics.",
["This is a leaf function, so no nested BL is needed.", "Only R0 changes; no callee-saved register needs saving."],
"Export add_three. Body: ADD R0,R0,#3; BX LR. Keep the file's AREA/THUMB/END structure. Test 0→3, 7→10, UINT32_MAX→2, then separately test LED encoding.",
"Mismatched prototypes can yield plausible wrong values. A successful stub call is not a finished solution. Compilation does not prove board behavior.",
"Demonstrate a real known-result C-to-ARM call with no temporary placeholder left.", "C|Assembly|ABI|Debug", 11),
]
