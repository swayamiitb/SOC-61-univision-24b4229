"""Week 5: validate a block-based pipeline as a Directed Acyclic Graph.

A topological sort (via DFS) computes a safe execution order so no block runs
before the blocks it depends on.
"""

pipeline_graph = {
    "LoadImage":     ["Grayscale", "Resize"],
    "Grayscale":     ["DetectObjects"],
    "Resize":        ["DetectObjects"],
    "DetectObjects": ["SaveResult"],
    "SaveResult":    [],
}


def topological_sort(graph):
    visited, stack = set(), []

    def dfs(node):
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            stack.append(node)

    for key in graph:
        dfs(key)
    return stack[::-1]


if __name__ == "__main__":
    print("Safe execution order:", topological_sort(pipeline_graph))
