import { useContext, useState } from "react";
import { AuthContext } from "../context/authContext";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { UserPlus, Mail, BriefcaseBusiness, User, Lock } from 'lucide-react';
import '../styles/signup.css'

const Signup = () => {
  const { signup } = useContext(AuthContext);
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", email: "", password: "", profession: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await signup(formData.username, formData.email, formData.password, formData.profession);
    navigate("/dashboard");
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <div className="signup-header">
          <div className="signup-icon-container">
            <UserPlus className="signup-icon" />
          </div>
          <h2 className="signup-title">Create an account</h2>
          <p className="signup-subtext">Join us today and get started</p>
        </div>

        <form onSubmit={handleSubmit} className="signup-form">
          <div className="signup-input-container">
            <label>Full Name</label>
            <div className="signup-input-wrapper">
              <div className="signup-input-icon">
                <User />
              </div>
              <input
                type="text"
                name="username"
                value={formData.name}
                onChange={handleChange}
                className="signup-input"
                placeholder="Enter your full name"
                required
              />
            </div>
          </div>

          <div className="signup-input-container">
            <label>Email address</label>
            <div className="signup-input-wrapper">
              <div className="signup-input-icon">
                <Mail />
              </div>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="signup-input"
                placeholder="Enter your email"
                required
              />
            </div>
          </div>

          <div className="signup-input-container">
            <label>Password</label>
            <div className="signup-input-wrapper">
              <div className="signup-input-icon">
                <Lock />
              </div>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="signup-input"
                placeholder="Create a password"
                required
              />
            </div>
          </div>

          <div className="signup-input-container">
            <label>Profession</label>
            <div className="signup-input-wrapper">
              <div className="signup-input-icon">
              <BriefcaseBusiness />
              </div>
              <input
                type="text"
                name="profession"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="signup-input"
                placeholder="Profession"
                required
              />
            </div>
          </div>

          <button type="submit" className="signup-button">
            Create Account
          </button>
        </form>

        <div className="signup-footer">
          <p>
            Already have an account?{' '}
            <Link to="/login">Sign in instead</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;
