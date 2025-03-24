import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useContext } from "react";
import Login from "./pages/Login";
import Signup from "./pages/SignUp";
import Dashboard from "./pages/Dashboard";
import { AuthContext } from "./context/authContext";
import AlertForm from "./pages/AlertForm";
import StockAlerts from "./pages/StockAlerts";

function CheckAuthentication({ element }) {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? element : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/create-alert" element={<CheckAuthentication element={<AlertForm />} />}/>
        <Route path="/my-alerts" element={<CheckAuthentication element={<StockAlerts />} />}/>
        <Route path="/dashboard" element={<CheckAuthentication element={<Dashboard />} />} />
      </Routes>
    </Router>
  );
}

export default App;
