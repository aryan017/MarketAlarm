import { useState, useEffect } from "react";

const StockAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws"); // Connect to FastAPI WebSocket

    socket.onmessage = (event) => {
      setAlerts((prev) => [...prev, event.data]); // Append new alerts
    };

    socket.onclose = () => {
      console.log("WebSocket Disconnected");
    };

    setWs(socket);

    return () => socket.close();
  }, []);

  return (
    <div className="alerts-container">
      <h2>📢 Stock Alerts</h2>
      <ul>
        {alerts.map((alert, index) => (
          <li key={index}>{alert}</li>
        ))}
      </ul>
    </div>
  );
};

export default StockAlerts;
