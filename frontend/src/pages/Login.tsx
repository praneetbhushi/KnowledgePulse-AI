import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { loginUser } from "../api/authApi";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loginLoading, setLoginLoading] = useState(false);

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (
    e: React.FormEvent
  ) => {
    e.preventDefault();

    try {
      setLoginLoading(true);

      const data = await loginUser(
        username,
        password
      );

      await login(data.access_token);

      navigate("/dashboard");
    } catch (err) {
      console.error("Login failed:", err);
      alert("Login failed. Please check your email and password.");
    } finally {
      setLoginLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">

      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-lg rounded-xl p-8 w-96"
      >

        <h1 className="text-3xl font-bold mb-6">
          KnowledgePulse AI
        </h1>

        <input
          type="text"
          placeholder="Username / Email"
          className="w-full border rounded-lg p-3 mb-4"
          value={username}
          onChange={(e) =>
            setUsername(e.target.value)
          }
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border rounded-lg p-3 mb-6"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          required
        />

        <button
          type="submit"
          disabled={loginLoading}
          className="w-full bg-blue-600 text-white rounded-lg py-3 disabled:opacity-50"
        >
          {loginLoading ? "Logging in..." : "Login"}
        </button>

      </form>

    </div>
  );
}