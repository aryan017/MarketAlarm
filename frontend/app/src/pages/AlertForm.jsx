import React, { useState } from "react";
import { Bell, IndianRupee, Mail, Loader2 } from "lucide-react";
import axios from "axios";
import '../styles/alertForm.css'

const AlertForm = () => {
  const [symbol, setSymbol] = useState("");
  const [targetPrice, setTargetPrice] = useState("");
  const [contact, setContact] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symbol || !targetPrice || !contact) {
      setError("All fields are required!");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const token = localStorage.getItem("token");
      await axios.post(
        "http://localhost:8000/alert",
        {
          symbol: symbol.toUpperCase(),
          target_price: parseFloat(targetPrice),
          user_contact: contact,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setSuccess(`Alert successfully set for ${symbol.toUpperCase()} at $${targetPrice}`);
      setSymbol("");
      setTargetPrice("");
      setContact("");
    } catch (error) {
      setError(error.response?.data?.message || "Failed to set alert. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="alert-form-container">
      <div className="alert-form-header">
        <Bell className="icon" />
        <h2>Stock Price Alert</h2>
      </div>

      {error && <div className="alert-message error-message">{error}</div>}
      {success && <div className="alert-message success-message">{success}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="input-group">
          <IndianRupee className="icon" />
          <input
            type="text"
            placeholder="Stock Symbol (e.g., AAPL)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
            className="input-field"
            disabled={loading}
          />
        </div>

        <div className="input-group">
          <IndianRupee className="icon" />
          <input
            type="number"
            step="0.01"
            placeholder="Target Price"
            value={targetPrice}
            onChange={(e) => setTargetPrice(e.target.value)}
            className="input-field"
            disabled={loading}
          />
        </div>

        <div className="input-group">
          <Mail className="icon" />
          <input
            type="text"
            placeholder="Email or Phone Number"
            value={contact}
            onChange={(e) => setContact(e.target.value)}
            className="input-field"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="submit-button"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin icon" /> Setting Alert...
            </>
          ) : (
            <>
              <Bell className="icon" /> Set Price Alert
            </>
          )}
        </button>
      </form>

      <p className="footer-text">
        We'll notify you when the stock reaches your target price
      </p>
    </div>
  );
};

export default AlertForm;
