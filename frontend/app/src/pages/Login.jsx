import { useContext, useState } from "react";
import { AuthContext } from "../context/authContext";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { Lock, Mail, LogIn } from 'lucide-react';
import '../styles/login.css';

const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(formData.email, formData.password);
    navigate("/dashboard");
  };

  return (
    <div className="login-container">
    <div className="login-header">
      <div className="icon-container">
        <LogIn className="icon" />
      </div>
      <h2 className="login-title">Welcome back</h2>
      <p className="login-subtitle">Please sign in to your account</p>
    </div>

    <form onSubmit={handleSubmit} className="login-form">
      <div className="form-group">
        <label className="label">Email address</label>
        <div className="input-container">
          <div className="input-icon">
            <Mail className="icon" />
          </div>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="input-field"
            placeholder="Enter your email"
            required
          />
        </div>
      </div>

      <div className="form-group">
        <label className="label">Password</label>
        <div className="input-container">
          <div className="input-icon">
            <Lock className="icon" />
          </div>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="input-field"
            placeholder="Enter your password"
            required
          />
        </div>
      </div>

      <div className="options">
        <div className="remember-me">
          <input type="checkbox" id="remember-me" />
          <label htmlFor="remember-me">Remember me</label>
        </div>
        <button type="button" className="forgot-password">
          Forgot password?
        </button>
      </div>

      <button type="submit" className="submit-btn">Sign in</button>
    </form>

    <div className="sign-up">
      <p>
        Don't have an account?{' '}
        <Link to="/signup" className="sign-up-link">
          Sign up now
        </Link>
      </p>
    </div>
  </div>
  );
};

export default Login;


