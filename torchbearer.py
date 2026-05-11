"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Jingyi Chen
Student ID:   828510638

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return (
        "- A single shortest-path run from S only gives the cheapest cost from the entrance to each node once; it cannot decide which relic should be visited first, second, or last.\n"
        "- After all inter-location costs are known, the remaining structural decision is the visitation order of the relic chambers before finishing at T.\n"
        "- This problem is a search over orders because different valid relic orders can produce different total route costs even when every pairwise travel cost is already known."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    """
    sources = []
    seen = set()

    for node in [spawn] + list(relics):
        if node not in seen:
            seen.add(node)
            sources.append(node)

    return sources

    pass


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    dist = {node: float('inf') for node in graph}
    if source not in dist:
        return dist

    dist[source] = 0
    heap = [(0, source)]

    while heap:
        current_dist, u = heapq.heappop(heap)
        if current_dist != dist[u]:
            continue

        for v, weight in graph.get(u, []):
            new_dist = current_dist + weight
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))

    return dist

    pass


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    dist_table = {}
    for source in select_sources(spawn, relics, exit_node):
        dist_table[source] = run_dijkstra(graph, source)
    return dist_table

    pass


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return (
        "### Part 3a: Invariant Explanation\n"
        "- **For nodes already finalized (in S):** Once a node is finalized, its distance is no longer just a candidate; it is the true shortest-path cost from the source.\n"
        "- **For nodes not yet finalized (not in S):** Each non finalized node store the best path found so far whose internal node are already finalized, so the value is the best discovered frontier estimate.\n\n"
        "### Part 3b: Why Each Phase Holds\n"
        "- **Initialization : why the invariant holds before iteration 1:** The source start at distance 0, every other node start at infinity, and no finalized node has an incorrect value, so the invariant is true before the first extraction.\n"
        "- **Maintenance : why finalizing the min-dist node is always correct:** The smallest tentative distance is safe to finalize because edge weight are nonnegative, so any alternate path that goes through an unfinalized node cannot come back and make that distance smaller.\n"
        "- **Termination : what the invariant guarantees when the algorithm ends:** When the algorithm stop, every reachable node has its true shortest path distance recorded, and every unreachable node correctly remain at infinity.\n\n"
        "### Part 3c: Why This Matters for the Route Planner\n"
        "- The route planner treat these distance as exact leg cost between important location, so if the shortest path value was wrong the final relic order search could optimize the wrong route."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    
    """
    return (
        "### Why Greedy Fails\n"
        "- **The failure mode:** Picking the cheapest next relic can force a much more expensive remaining route later.\n"
        "- **Counter-example setup:** Suppose the precomput cost are S->B = 1, S->C = 2, B->C = 100, C->B = 1, B->T = 1, and C->T = 1, and both B and C must be collected.\n"
        "- **What greedy picks:** A greedy next step rule pick B first because 1 is cheaper than 2.\n"
        "- **What optimal picks:** The optimal order is C then B, with total cost 2 + 1 + 1 = 4.\n"
        "- **Why greedy loses:** Greedy get stuck with S->B->C->T costing 1 + 100 + 1 = 102, so the locally cheapest first move is not globally cheapest.\n\n"
        "### What the Algorithm Must Explore\n"
        "- The algorithm must explore the order of visiting relics, because different valid order can produce different total fuel costs even after shortest path precomputation is finished."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    unique_relics = []
    seen = set()
    for relic in relics:
        if relic not in seen:
            seen.add(relic)
            unique_relics.append(relic)

    if not unique_relics:
        exit_cost = dist_table.get(spawn, {}).get(exit_node, float('inf'))
        if exit_cost == float('inf'):
            return (float('inf'), [])
        return (exit_cost, [])

    best = [float('inf'), []]
    relics_remaining = set(unique_relics)
    relics_visited_order = []
    cost_so_far = 0

    _explore(
        dist_table,
        spawn,
        relics_remaining,
        relics_visited_order,
        cost_so_far,
        exit_node,
        best,
    )

    return (best[0], best[1]) if best[0] != float('inf') else (float('inf'), [])


def _lower_bound(dist_table, current_loc, relics_remaining, exit_node):

    if not relics_remaining:
        return dist_table.get(current_loc, {}).get(exit_node, float('inf'))

    first_step = min(
        dist_table.get(current_loc, {}).get(relic, float('inf'))
        for relic in relics_remaining
    )

    total = first_step
    for relic in relics_remaining:
        next_options = set(relics_remaining)
        next_options.discard(relic)
        next_options.add(exit_node)

        best_out = min(
            dist_table.get(relic, {}).get(target, float('inf'))
            for target in next_options
        )
        total += best_out

    return total


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    if not relics_remaining:
        exit_cost = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        if exit_cost == float('inf'):
            return

        total_cost = cost_so_far + exit_cost
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return

    lower_bound = _lower_bound(dist_table, current_loc, relics_remaining, exit_node)

    # This prune is safe because lower_bound is an optimistic estimate of the
    # cheapest possible completion from this state. If cost_so_far + lower_bound
    # already cannot beat best[0], then no full route below this branch can beat it either.
    if lower_bound == float('inf') or cost_so_far + lower_bound >= best[0]:
        return

    for next_relic in sorted(relics_remaining):
        step_cost = dist_table.get(current_loc, {}).get(next_relic, float('inf'))
        if step_cost == float('inf'):
            continue

        relics_remaining.remove(next_relic)
        relics_visited_order.append(next_relic)

        _explore(
            dist_table,
            next_relic,
            relics_remaining,
            relics_visited_order,
            cost_so_far + step_cost,
            exit_node,
            best,
        )

        relics_visited_order.pop()
        relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
