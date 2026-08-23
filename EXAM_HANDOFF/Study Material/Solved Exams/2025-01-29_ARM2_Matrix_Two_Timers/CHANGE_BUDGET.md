# Change budget

The code is organized so the usual correction is localized. The expected budget is a measured target, not permission to skip rebuilding and rerunning tests.

| Variation | Target source lines changed |
|---|---:|
| Constant, array size, timer period, or seed | 1-3 |
| Pin or peripheral instance | 1-4 |
| Result encoding | 3-8 |
| Recurrence or stopping rule | 4-12 |
| Replace the main algorithm family | use another canonical pattern; no honest small-line promise |
