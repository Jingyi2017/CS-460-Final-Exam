# Development Log – The Torchbearer

**Student Name:** Jingyi Chen
**Student ID:** 828510638

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – 2026-05-10: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

My plan was to implement Dijkstra first, then the distance precomputation table, and finally the recursive relic-order search with pruning. I expected the pruning part to be the trickiest because it had to be strong enough to help but still be obviously safe.

---

## Entry 2 – 2026-05-10: Source Selection and Search-State Decision


> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

At first I considered running Dijkstra from the exit as well, but after tracing how the planner uses distances, I realized the exit is only a destination and never a new starting state in the recursive search. I kept the source set as `spawn + relics`.

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
