# The Torchbearer

**Student Name:** Jingyi Chen
**Student ID:** 828510638
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
A single shortest path run from S only gives the cheapest cost from the entrance to each node once; it cannot decide which relic should be visited first, second, or last.

- **What decision remains after all inter-location costs are known:**
After all inter location cost are known, the remaining structural decision is the visitation order of the relic chamber before finishing at T.

- **Why this requires a search over orders (one sentence):**
This problem is a search over orders because different valid relic order can produce different total route cost even when every pairwise travel cost is already known.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Entrance `S` | The planner starts here, so it needs shortest distances from the entrance to every relic and possibly to the exit. |
| Each relic chamber in `M` | After collecting one relic, the next decision starts from that relic, so the planner needs shortest distances from every relic to every other relevant destination. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary `dist_table` |
| What the keys represent | Outer key = source node, inner key = destination node |
| What the values represent | The shortest-path fuel cost from the source node to the destination node |
| Lookup time complexity | `O(1)` average-case dictionary lookup |
| Why O(1) lookup is possible | Python dictionaries are hash tables, so a precomputed `dist_table[u][v]` lookup is constant time on average |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** `k + 1` runs, one from `S` and one from each relic in `M`
- **Cost per run:** `O(m log n)`
- **Total complexity:** `O((k + 1) * m log n)` which is `O(km log n)`
- **Justification (one line):** The same single-source shortest-path algorithm is run once per relevant source node, and each run costs `O(m log n)`.


---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
Once a node is finalized, its distance is no longer just a candidate; it is the true shortest path cost from the source.

- **For nodes not yet finalized (not in S):**
Each non finalized node store the best path found so far whose internal node are already finalized, so the value is the best discovered frontier estimate.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
The source start at distance 0, every other node start at infinity, and no finalized node has an incorrect value, so the invariant is true before the first extraction.

- **Maintenance : why finalizing the min-dist node is always correct:**
The smallest tentative distance is safe to finalize because edge weight are nonnegative, so any alternate path that goes through an unfinalized node cannot come back and make that distance smaller.

- **Termination : what the invariant guarantees when the algorithm ends:**
When the algorithm stop, every reachable node has its true shortest path distance record, and every unreachable node correctly remain at infinity.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

The route planner treat these distances as exact leg cost between important location, so if the shortest path value was wrong the final relic order search could optimize the wrong route.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Your answer here._
- **Counter-example setup:** _Your answer here._
- **What greedy picks:** _Your answer here._
- **What optimal picks:** _Your answer here._
- **Why greedy loses:** _Your answer here._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _Your answer here._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
