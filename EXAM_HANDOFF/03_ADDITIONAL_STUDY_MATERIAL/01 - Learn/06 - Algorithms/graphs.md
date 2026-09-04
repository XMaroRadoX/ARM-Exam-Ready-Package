# Graph patterns

## DFS shape

1. mark the current vertex visited;
2. scan all possible neighbors;
3. skip absent edges and already-visited vertices;
4. recursively visit or push the neighbor;
5. preserve loop state across the recursive `BL`.

Recursive DFS is non-leaf. Keep base pointers and vertex count in R4-R11 or on the stack, and maintain eight-byte alignment before recursion.

## Shortest path relaxation

For each candidate edge `(u,v,w)`, if `distance[u]` is finite and `distance[u] + w < distance[v]`, update `distance[v]`. Check overflow/sentinel semantics before addition.

## Kruskal

Sort edges by weight, then accept an edge only if its endpoints belong to different sets. The exam may provide or expect a simple component-label array rather than a sophisticated disjoint-set implementation; match the specified representation.

Historical graph papers: 2024-02-12 maze, 2024-02-28 shortest path, 2024-07-09 DFS, and 2024-09-16 Kruskal.

