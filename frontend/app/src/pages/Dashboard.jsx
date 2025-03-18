import React, { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/authContext";
import AlertForm from "./AlertForm";
import StockAlerts from "./StockAlerts";

const Dashboard = () => {
  const { logout } = useContext(AuthContext); 
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); 
    navigate("/login"); 
  };

  return (
    <div>
      <h2>Dashboard</h2>
      <button onClick={handleLogout}>Logout</button>
      <AlertForm />
      <StockAlerts />
    </div>
  );
};

export default Dashboard;
