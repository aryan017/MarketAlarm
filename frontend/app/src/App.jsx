import React from "react";
import StockAlerts from "./pages/StockAlerts";
import AlertForm from "./pages/AlertForm";

function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-5">
      <h1 className="text-3xl font-bold mb-6">📈 Real-Time Stock Alert System</h1>
      <AlertForm />
      <StockAlerts />
    </div>
  );
}

export default App;
