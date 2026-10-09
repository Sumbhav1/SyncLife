import React from "react";
import SyncLife from "../assets/images/SyncLife.png";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api";
import { useAuth } from "../components/AuthContext";

const SignUp = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const isValidPassword = (password) => {
    return (
      password.length >= 8 &&
      /[A-Z]/.test(password) && // at least one uppercase letter
      /[a-z]/.test(password) && // at least one lowercase letter
      /[0-9]/.test(password) // at least one number
    );
  };
  const handleSignUp = async (e) => {
    e.preventDefault();
    setError("");

    if (!name || !email || !password || !confirmPassword) {
      setError("All fields must be filled");
      return; 
    }

    if (!isValidPassword(password)) {
      setError(
        "Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, and one number."
      );
      return;
    }
    if (password !== confirmPassword) {
      setError("passwords do not match");
      return;
    }
    try {
      const response = await api.post("/auth/signup", { name, email, password });
      login(response.data.token, response.data.user);
      navigate("/settings");
    } catch (err) {
      setError(
        err.response?.status === 409
          ? "That email is already in use."
          : "Sign up failed. Please try again."
      );
    }
  };
  return (
    <div className="flex items-center justify-center h-screen bg-blue-300">
      <div className="bg-blue-200 p-10 rounded-lg shadow-lg w-96 text-center">
        <div className="flex justify-center mb-5">
          <img
            src={SyncLife}
            alt="SyncLife Logo"
            className="w-24 h-24 rounded-lg"
          />
        </div>
        <p className="mt-2 text-lg font-medium">Sign up</p>
        {error && <p className="text-red-600">{error}</p>}

        <form className="mt-4 space-y-4" onSubmit={handleSignUp}>
          <div className="text-left">
            <label className="block font-medium">Name:</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500"
            />
          </div>
          <div className="text-left">
            <label className="block font-medium">Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500"
            />
          </div>
          <div className="text-left">
            <label className="block font-medium">Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500"
            />
          </div>
          <div className="text-left">
            <label className="block font-medium">Confirm password:</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2 rounded-lg border border-gray-400 focus:ring focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition"
          >
            Register
          </button>
        </form>

        <p className="mt-4 text-sm">
          Back to login?{" "}
          <Link to="/login" className="text-blue-600 font-semibold underline">
            Go Back
          </Link>
        </p>
      </div>
    </div>
  );
};

export default SignUp;