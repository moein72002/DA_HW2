def solve():
    import sys
    data = input().strip().split()
    n = int(data[0])
    m = int(data[1])

    # Read the original grid
    grid = []
    idx = 2
    for _ in range(n):
        row = list(map(int, input().strip().split()))
        idx += m
        grid.append(row)

    # freq[c][t] = how many chocolates of type t are in column c
    # t ranges 1..m, so make freq[c] size (m+1)
    freq = [[0]*(m+1) for _ in range(m)]
    for r in range(n):
        for c in range(m):
            t = grid[r][c]
            freq[c][t] += 1

    # We'll construct a flow network with the following node naming:
    # "S" = source, "T" = sink
    # "slot_{i}_{c}" for each row i, col c
    # "type_{i}_{t}" for each row i, type t
    # "CT_{c}_{t}" for each col c, type t

    # Pseudocode for building the graph (using a dict-of-dicts for capacities):
    from collections import defaultdict
    capacity = defaultdict(lambda: defaultdict(int))

    S = "S"
    T = "T"
    capacity[S]  # ensure S is in the dictionary
    capacity[T]  # ensure T is in the dictionary

    # 1) Source -> slot_{i}_{c} edges, capacity = 1
    for i in range(n):
        for c in range(m):
            slot_node = f"slot_{i}_{c}"
            capacity[S][slot_node] = 1

    # 2) slot_{i}_{c} -> type_{i}_{t}, capacity = 1 for all t = 1..m
    #    Because cell (i,c) might be assigned type t
    for i in range(n):
        for c in range(m):
            slot_node = f"slot_{i}_{c}"
            for t in range(1, m+1):
                type_node = f"type_{i}_{t}"
                capacity[slot_node][type_node] = 1

    # 3) type_{i}_{t} -> CT_{c}_{t}, capacity = 1
    #    Because if row i uses type t, it can come from one column c.
    #    We'll allow connecting to all columns c (the usage limit is enforced later).
    for i in range(n):
        for t in range(1, m+1):
            type_node = f"type_{i}_{t}"
            for c in range(m):
                ct_node = f"CT_{c}_{t}"
                # We'll allow capacity 1 here
                capacity[type_node][ct_node] = 1

    # 4) CT_{c}_{t} -> sink T, capacity = freq[c][t]
    for c in range(m):
        for t in range(1, m+1):
            ct_node = f"CT_{c}_{t}"
            capacity[ct_node][T] = freq[c][t]

    # Now we have a big flow network. Let's implement or use any MaxFlow (e.g. Dinic).

    # We'll write a small Dinic or Edmond–Karp for demonstration.
    # (In practice, you could use a library.)

    def bfs_level_graph():
        level = {node: -1 for node in capacity}
        level[S] = 0
        queue = [S]
        for u in queue:
            for v in capacity[u]:
                if capacity[u][v] > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        return level

    def send_flow(u, flow_in, T, level, it):
        if u == T:
            return flow_in
        while it[u] < len(capacity[u]):
            v = list(capacity[u].keys())[it[u]]
            if capacity[u][v] > 0 and level[v] == level[u] + 1:
                # Try sending flow
                curr_flow = min(flow_in, capacity[u][v])
                temp_flow = send_flow(v, curr_flow, T, level, it)
                if temp_flow > 0:
                    # Adjust
                    capacity[u][v] -= temp_flow
                    capacity[v][u] += temp_flow
                    return temp_flow
            it[u] += 1
        return 0

    def dinic_maxflow(S, T):
        total_flow = 0
        while True:
            level = bfs_level_graph()
            if level[T] < 0:  # no path
                return total_flow
            it = {u: 0 for u in capacity}
            while True:
                flow_sent = send_flow(S, float('inf'), T, level, it)
                if flow_sent <= 0:
                    break
                total_flow += flow_sent

    max_flow = dinic_maxflow(S, T)

    # If the max flow is n*m, we have a valid arrangement
    if max_flow < n*m:
        print("No valid rearrangement possible.")
        return

    # Otherwise, extract the arrangement
    # We know each slot_{i}_{c} -> type_{i}_{t} might have used 1 unit of flow,
    # but we need to see which column c the type_{i}_{t} eventually used to get
    # to CT_{c}_{t} -> T.  However, a simpler way:
    #  - For each slot_{i}_{c}, see which type_{i}_{t} has residual capacity < 1
    #    on the edge slot_{i}_{c} -> type_{i}_{t}. If capacity < 1, that edge
    #    carried flow. That means (i,c) = type t.

    final_arr = [[0]*m for _ in range(n)]

    for i in range(n):
        for c in range(m):
            slot_node = f"slot_{i}_{c}"
            chosen_type = None
            for t in range(1, m+1):
                type_node = f"type_{i}_{t}"
                # If the original capacity was 1, and now it's 0,
                # that edge was used by 1 unit of flow.
                # But we have to be careful: we overwrote capacity in place.
                # We can check capacity[type_node][slot_node] instead,
                # which is the "reverse edge" capacity after the flow push.
                if capacity[type_node][slot_node] == 1:
                    # Means we used that direction forward.
                    chosen_type = t
                    break
            final_arr[i][c] = chosen_type

    # Print the final arrangement
    for r in range(n):
        print(" ".join(map(str, final_arr[r])))

solve()