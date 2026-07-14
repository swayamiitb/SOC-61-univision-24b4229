// Week 3: a React dashboard that renders a fast, simulated pipeline stream
// without leaking memory. The useEffect cleanup is what stops the leak.
import React, { useState, useEffect } from 'react';

function RealTimeAIDashboard() {
    // state changes trigger a re-render only when the reference changes
    const [systemMetrics, setSystemMetrics] = useState({ state: "Idle", fps: 0 });

    useEffect(() => {
        let isComponentMounted = true;

        const connectToPipeline = setInterval(() => {
            if (isComponentMounted) {
                // stand-in for a data fetch from the AI core
                setSystemMetrics({
                    state: "Processing Frame",
                    fps: Math.floor(Math.random() * 15) + 30
                });
            }
        }, 100); // 10Hz refresh

        // cleanup: stop the stream when the component unmounts
        return () => {
            isComponentMounted = false;
            clearInterval(connectToPipeline);
        };
    }, []);

    return (
        <div className="dashboard-container" style={{ fontFamily: 'monospace' }}>
            <header>
                <h2>System Status: {systemMetrics.state}</h2>
                <h3 style={{ color: systemMetrics.fps < 35 ? 'red' : 'green' }}>
                    Pipeline Speed: {systemMetrics.fps} FPS
                </h3>
            </header>
        </div>
    );
}

export default RealTimeAIDashboard;
