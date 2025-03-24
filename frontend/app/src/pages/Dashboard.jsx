import React, { useContext } from "react";
import { useNavigate } from 'react-router-dom';
import { AuthContext } from "../context/authContext";
import { Bell, List, LogOut } from 'lucide-react';
import '../styles/dashboard.css'

const Dashboard=() => {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext); 

  const handleLogout = () => {
    logout(); 
    navigate("/login"); 
  };
  return (
    <div className="dashboard">
      <div className="container">
        <h1 className="dashboard-title">Stock Alert Dashboard</h1>

        <div className="button-grid">
          {/* Create Alert Button */}
          <button onClick={() => navigate('/create-alert')} className="card-button">
            <div className="icon-wrapper bg-blue">
              <Bell className="icon icon-blue" />
            </div>
            <h2 className="card-title">Create Alert</h2>
            <p className="card-description">Set up new stock price alerts</p>
          </button>

          {/* My Alerts Button */}
          <button onClick={() => navigate('/my-alerts')} className="card-button">
            <div className="icon-wrapper bg-green">
              <List className="icon icon-green" />
            </div>
            <h2 className="card-title">My Alerts</h2>
            <p className="card-description">View and manage your alerts</p>
          </button>

          {/* Logout Button */}
          <button onClick={handleLogout} className="card-button">
            <div className="icon-wrapper bg-red">
              <LogOut className="icon icon-red" />
            </div>
            <h2 className="card-title">Logout</h2>
            <p className="card-description">Sign out of your account</p>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
