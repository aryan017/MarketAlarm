import React, { useState } from "react";
import axios from "axios";

const AlertForm = () => {
  const [symbol, setSymbol] = useState("");
  const [targetPrice, setTargetPrice] = useState("");
  const [contact, setContact] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symbol || !targetPrice || !contact) return alert("All fields required!");

    try {
      await axios.post("http://localhost:8000/alert", {
        symbol,
        target_price: parseFloat(targetPrice),
        user_contact: contact,
      });

      alert(`Alert set for ${symbol} at ${targetPrice}`);
      setSymbol("");
      setTargetPrice("");
      setContact("");
    } catch (error) {
      console.error("Error setting alert:", error);
    }
  };

  return (
    <div className="w-full max-w-lg bg-gray-800 p-4 rounded-lg shadow-lg">
      <h2 className="text-xl font-semibold mb-3">📌 Set a Stock Alert</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="text"
          placeholder="Stock Symbol (e.g., AAPL)"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
        />
        <input
          type="number"
          placeholder="Target Price"
          value={targetPrice}
          onChange={(e) => setTargetPrice(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
        />
        <input
          type="text"
          placeholder="Email or Phone"
          value={contact}
          onChange={(e) => setContact(e.target.value)}
          className="w-full p-2 rounded bg-gray-700 text-white"
        />
        <button type="submit" className="w-full p-2 bg-blue-500 rounded-lg">
          Set Alert 🚀
        </button>
      </form>
    </div>
  );
};

export default AlertForm;
