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

At first I consider running Dijkstra from the exit as well, but after tracing how the planner uses distances, I realized the exit is only a destination and never a new starting state in the recursive search. I kept the source set as `spawn + relics`.

---

## Entry 3 – 2026-05-10: Bug Fix in the Route Search

My first version of the search was correct but the lower bound idea was too vague, the code was not clear tied to the README explanation. I rewrote the bound so it explicitly use the current location, the remaining relic set, and one optimistic outgoing leg per remaining relic. That made the prune easy to justify and also improved readability.

---

## Entry 4 – 2026-05-10: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

After the provid test passed, I checked a few extra edge case such as no relics, duplicate relic name. If I had more time, I would probably add memoization by `(current_loc, frozenset(relics_remaining))` to avoid re exploring equivalent state and make the search scale better for larger `k`.

---

## Final Entry – 2026-05-10: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 0.5 |
| Part 2: Precomputation Design | 0.75 |
| Part 3: Algorithm Correctness | 0.75 |
| Part 4: Search Design | 0.5 |
| Part 5: State and Search Space | 0.75 |
| Part 6: Pruning | 1.0 |
| Part 7: Implementation | 1.5 |
| README and DEVLOG writing | 0.75 |
| **Total** | 6.5 |
