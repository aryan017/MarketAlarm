import { useState } from "react";
import axios from "axios";

const StockAlertForm = () => {
  const [symbol, setSymbol] = useState("");
  const [price, setPrice] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/set_alert/", {
        symbol,
        target_price: parseFloat(price),
      });
      alert(`Alert set for ${symbol} at ${price}`);
    } catch (error) {
      console.error("Error setting alert", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="alert-form">
      <h2>Set Stock Alert</h2>
      <input
        type="text"
        placeholder="Stock Symbol (e.g., RELIANCE)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Target Price"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        required
      />
      <button type="submit">Set Alert</button>
    </form>
  );
};

export default StockAlertForm;
