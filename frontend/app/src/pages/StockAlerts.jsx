import React, { useEffect, useState } from "react";

const StockAlerts = () => {
  const token = localStorage.getItem("token");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

  }, []);

  return (
    <div>
      <h2>📢 Real-Time Stock Alerts</h2>
      <ul>
        {messages.length === 0 ? (
          <p>No alerts yet...</p>
        ) : (
          messages.map((msg, index) => (
            <li key={index}>
              {msg}
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default StockAlerts;
