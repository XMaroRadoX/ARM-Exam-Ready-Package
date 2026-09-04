#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

/*
 * Exam-study reference: Bounded DFS with an explicit stack.
 * Recognition cue: visit graph without recursion using bounded stack.
 *
 * Contract rules:
 * - Fixed-width types make width and signedness part of the interface.
 * - A pointer never carries its length; count/capacity arguments are explicit.
 * - const input objects are not mutated. Non-const outputs may be changed only
 *   within their documented bounds.
 * - Invalid, empty, duplicate and arithmetic-limit behavior is executable in
 *   pattern_edge_vectors() and described in the adjacent README.
 *
 * Trace the validation step first, then the main loop/recurrence invariant,
 * then the final result or capacity check. Public suffix functions are named
 * variants of the same advertised pattern, not unrelated shortcuts.
 */

/* Primary algorithm and its named variants. */
uint32_t pat_alg_dfs_stack_001(const uint8_t *adj, uint32_t n, uint32_t start,
                               uint8_t *seen, uint32_t *stack) {
  uint32_t top=0,visited=0;
  if(!adj||!seen||!stack||start>=n||n>65535u||seen[start])return 0;
  seen[start]=1;stack[top++]=start;
  while(top){
    uint32_t v=stack[--top]; ++visited;
    for(uint32_t w=n;w>0;--w)if(adj[v*n+w-1]&&!seen[w-1]){
      seen[w-1]=1; stack[top++]=w-1;
    }
  }
  return visited;
}

