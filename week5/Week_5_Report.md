# Week 5: Block-Based Workflow Design

## What I Studied & Researched:
This week, I looked into how we can abstract complex AI logic into connectable, modular blocks. I dove deep into Graph Theory, specifically Directed Acyclic Graphs (DAGs). I wanted to understand how to validate a pipeline and figure out the exact order nodes should execute in without getting stuck in a loop.

## My Code Experiment:

```python
pipeline_graph = {
    "LoadImage": ["Grayscale", "Resize"],
    "Grayscale": ["DetectObjects"],
    "Resize": ["DetectObjects"],
    "DetectObjects": ["SaveResult"],
    "SaveResult": []
}

def topological_sort(graph):
    visited = set()
    stack = []

    def dfs(node):
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                dfs(neighbor)
            stack.append(node)

    for key in graph:
        dfs(key)
        
    return stack[::-1]

execution_order = topological_sort(pipeline_graph)
```

## How It Works Under the Hood:
* **Blocks & Ports**: The keys in my dictionary represent the physical blocks, and the arrays represent the data flowing from output ports into the next block's input ports.
* **DAG (Directed Acyclic Graph)**: The dictionary maps out a strict, forward-flowing timeline. There are absolutely no loops (like "SaveResult" trying to feed backwards into "LoadImage"), which means it's "acyclic" and safe to run.
* **Topological Sorting**: I wrote a custom Depth-First Search (DFS) algorithm to crawl through the graph. It ensures that a downstream node like `DetectObjects` will absolutely never trigger until both `Resize` and `Grayscale` have finished their jobs.

## My Progress This Week

### Work Completed So Far:
I researched Directed Acyclic Graphs (DAGs) and how they power visual node-based editors. I then translated that abstract graph theory into a working Python topological sorting algorithm.

### Key Milestones Achieved:
* Successfully represented a complex visual pipeline as a mathematical dictionary in Python.
* Coded a Depth-First Search algorithm that strictly validates the graph and prints out the exact, safe execution order of the connected blocks.

### Challenges Faced:
Honestly, wrapping my head around recursion and graph traversal took a lot of mental effort. Trying to ensure my algorithm could correctly detect the difference between independent nodes and deep dependencies (and avoid endless loops) was a major hurdle this week.

## Resources & References
_Resources I studied this week (paste your links):_

- Graph theory basics — <add link>
- Directed Acyclic Graphs (DAGs) — <add link>
- Topological sorting — <add link>
- Depth-First Search (DFS) — <add link>
