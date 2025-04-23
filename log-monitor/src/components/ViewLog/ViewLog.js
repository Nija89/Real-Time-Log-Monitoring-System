import React, { useEffect, useState, useRef } from 'react';
import '../../App.css';

export const ViewLog = () => {
    const [logs, setLogs] = useState([]);
    const logsContainerRef = useRef(null);

    useEffect(() => {
        const socket = new WebSocket("ws://localhost:8081/ws");

        socket.onopen = () => {
            console.log("WebSocket Connected successfully!");
        };

        socket.onmessage = (event) => {
            try {
                const newLog = JSON.parse(event.data);
                setLogs((prevLogs) => [...prevLogs, newLog]);
            } catch (error) {
                console.error("Error receiving WebSocket message:", error);
            }
        };

        socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
        };

        socket.onclose = () => {
            console.log("WebSocket Disconnected");
        };

        return () => {
            socket.close();
        };
    }, []);

    useEffect(() => {
        if (logsContainerRef.current) {
            logsContainerRef.current.scrollTop = logsContainerRef.current.scrollHeight;
        }
    }, [logs]);

    const startGenerate = async () => {
        try {
            const url = "http://localhost:8080/startLogGeneration";
            const response = await fetch(url, {
                method: "POST",
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.log("Failed to fetch data: " + error.message);
        }
    };

    const generateButton = () => {
        startGenerate();
    };

    const stopGenerate = async () => {
        try {
            const url = "http://localhost:8080/stopLogGeneration";
            const response = await fetch(url, {
                method: "POST",
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        } catch (error) {
            console.log("Failed to fetch data: " + error.message);
        }
    };

    const stopButton = () => {
        stopGenerate();
    };

    return (
        <div className="container mt-4">
            <h1 className="log-heading text-center">Real-time Error and Critical Log Monitoring</h1>
    
            <div className="button-container text-center mb-4">
                <button className="btn btn-primary mx-2" onClick={generateButton}>Generate</button>
                <button className="btn btn-danger mx-2" onClick={stopButton}>Stop</button>
            </div>
    
            <div ref={logsContainerRef} className="log-container mb-4">
                <ul className="log-list">
                    {
                        logs.length === 0 ? <p className="no-logs-message text-center">No Logs to Show</p> :
                            logs.map((log, index) => (
                                <li key={index} className="log-item">
                                    {`{
                                        "level": "${log.level}", 
                                        "message": "${log.message}", 
                                        "timestamp": "${log.timestamp}"
                                    }`}
                                </li>
                            ))
                    }
                </ul>
            </div>
        </div>
    );
    
    
};
