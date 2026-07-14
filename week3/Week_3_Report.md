# Week 3: Web Basics And React Thinking

## What I Studied & Researched:
This week I dove into frontend web architecture to figure out how a real-time AI dashboard actually handles data. I learned how to separate the visual layout from the behavioral logic, and I went down a bit of a rabbit hole learning React state management so my dashboard could respond instantly to pipeline events.

## My Code Experiment:

```jsx
import React, { useState, useEffect } from 'react';

function PipelineDashboard() {
    const [pipelineState, setPipelineState] = useState("Idle");
    const [detections, setDetections] = useState(0);

    useEffect(() => {
        const handleEvent = (eventData) => {
            setPipelineState(eventData.status);
            setDetections(eventData.count);
        };

        const mockStream = setInterval(() => {
            handleEvent({ status: "Processing", count: Math.floor(Math.random() * 5) });
        }, 2000);

        return () => clearInterval(mockStream);
    }, []);

    return (
        <div className="dashboard">
            <h1>System Status: {pipelineState}</h1>
            <h2>Objects Detected: {detections}</h2>
        </div>
    );
}
```

## How It Works Under the Hood:
* **HTML / CSS / JavaScript**: The `return` block structures the layout using JSX (which looks like HTML), while the JavaScript logic inside `useEffect` quietly controls the data flow in the background.
* **Components**: `PipelineDashboard` is built as a self-contained module, meaning I could reuse it anywhere in the app without rewriting code.
* **State Management**: `useState` is super cool, it tracks data that changes over time. When my fake event stream calls `setPipelineState`, React automatically repaints the UI to show the new status without me having to manually mess with the DOM.

## My Progress This Week

### Work Completed So Far:
I sketched out the conceptual and functional state management for a real-time React dashboard. I successfully separated the visual UI elements from the asynchronous data streams running behind the scenes.

### Key Milestones Achieved:
* Built a fully stateful, working mock React component.
* Simulated a real-time pipeline event stream that drives the UI updates with no page reloads required.

### Challenges Faced:
Wrapping my head around React's component lifecycle and the asynchronous nature of `useEffect` was definitely tricky. I also ran into an issue where my mock event stream caused memory leaks, which forced me to research how to properly unmount components and clear intervals.

## Resources & References
_Resources I studied this week (paste your links):_

- React fundamentals — <add link>
- The Virtual DOM & reconciliation — <add link>
- `useState` / `useEffect` hooks — <add link>
- Memory leaks & cleanup functions in React — <add link>
