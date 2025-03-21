import { createContext, useState, useEffect } from "react";
import axios from "axios";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  useEffect(() => {
    const Token = localStorage.getItem("token");
    if (Token) {
      setIsAuthenticated(true);
    }
  }, []);

  const saveToken = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const login = async (email, password) => {
    try {
      const response = await axios.post("http://localhost:8000/login", {
        email,
        password,
      },
      {
        headers: { "Content-Type": "application/json" }
      }
    );
      setIsAuthenticated(true);
      saveToken(response.data.access_token);
      await fetchUser();
    } catch (error) {
      console.error("Login failed:", error.response?.data?.detail || error);
    }
  };

  const signup = async (username, email, password, profession) => {
    try {
      console.log(username)
      console.log(email)
      console.log(password)
      console.log(profession)
      await axios.post("http://localhost:8000/signup", {
        username,
        email,
        password,
        profession,
      });
      await login(email, password);
    } catch (error) {
      console.error("Signup failed:", error.response?.data?.detail || error);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setIsAuthenticated(false);
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated,user, token, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
