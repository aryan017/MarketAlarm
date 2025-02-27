import React, { useEffect, useState } from "react";

const StockAlerts = () => {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="w-full max-w-lg bg-gray-800 p-4 rounded-lg shadow-lg mt-5">
      <h2 className="text-xl font-semibold mb-3">📢 Real-Time Stock Alerts</h2>
      <ul className="space-y-2">
        {messages.length === 0 ? (
          <p className="text-gray-400">No alerts yet...</p>
        ) : (
          messages.map((msg, index) => (
            <li key={index} className="bg-gray-700 p-2 rounded-lg">
              {msg}
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default StockAlerts;
