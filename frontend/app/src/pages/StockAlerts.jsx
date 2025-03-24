import React, { useEffect, useState } from "react";
import { Bell, TrendingUp, AlertCircle } from "lucide-react";
import '../styles/stockAlerts.css'

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
    <div className="container">
      <div className="card">
        <div className="header">
          <Bell className="header-icon" />
          <h2 className="title">Real-Time Stock Alerts</h2>
        </div>

        <div className="alert-container">
          {messages.length === 0 ? (
            <div className="empty-state">
              <TrendingUp className="empty-icon" />
              <p className="empty-text">Waiting for stock alerts...</p>
              <p className="empty-subtext">New alerts will appear here in real-time</p>
            </div>
          ) : (
            <ul className="alert-list">
              {messages.map((msg, index) => (
                <li key={index} className="alert-item">
                  <AlertCircle className="alert-icon" />
                  <div>
                    <p className="alert-text">{msg}</p>
                    <p className="alert-time">{new Date().toLocaleTimeString()}</p>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default StockAlerts;
