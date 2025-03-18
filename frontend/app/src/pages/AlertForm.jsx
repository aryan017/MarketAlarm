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
      const token = localStorage.getItem("token");
      const response = await axios.post("http://localhost:8000/alert", {
        symbol,
        target_price: parseFloat(targetPrice),
        user_contact: contact,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

      alert(`Alert set for ${symbol} at ${targetPrice}`);
      console.log("Server Response:", response.data); 
      setSymbol("");
      setTargetPrice("");
      setContact("");
    } catch (error) {
      console.error("Error setting alert:", error);
      if (error.response) {
        console.log("Error Response:", error.response.data);
      }
    }
  };

  return (
    <div>
      <h2> Set a Stock Alert</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Stock Symbol"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
        />
        <input
          type="number"
          placeholder="Target Price"
          value={targetPrice}
          onChange={(e) => setTargetPrice(e.target.value)}
        />
        <input
          type="text"
          placeholder="Email or Phone"
          value={contact}
          onChange={(e) => setContact(e.target.value)}
        />
        <button type="submit">
          Set Alert
        </button>
      </form>
    </div>
  );
};

export default AlertForm;
