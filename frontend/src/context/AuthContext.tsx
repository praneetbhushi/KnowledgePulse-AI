import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import type { ReactNode } from "react";

import api from "../api/axios";

interface User {
  id: number;
  name: string;
  email: string;
  department_id: number | null;
  role_id: number;
}

interface AuthContextType {
  token: string | null;
  user: User | null;
  login: (token: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<
  AuthContextType | undefined
>(undefined);

export function AuthProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("token")
  );

  const [user, setUser] = useState<User | null>(null);

  const [loading, setLoading] = useState(true);

  const fetchCurrentUser = async (
    authToken: string
  ) => {
    try {
      const response = await api.get(
        "/api/v1/users/me",
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );

      console.log(
        "CURRENT USER:",
        response.data
      );

      setUser(response.data);

      return response.data;
    } catch (error) {
      console.error(
        "Failed to fetch current user:",
        error
      );

      setUser(null);

      throw error;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const storedToken =
      localStorage.getItem("token");

    if (storedToken) {
      setToken(storedToken);

      fetchCurrentUser(storedToken).catch(() => {
        localStorage.removeItem("token");
        setToken(null);
      });
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (
    newToken: string
  ) => {
    localStorage.setItem(
      "token",
      newToken
    );

    setToken(newToken);
    setLoading(true);

    await fetchCurrentUser(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");

    setToken(null);
    setUser(null);
    setLoading(false);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        login,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(
    AuthContext
  );

  if (!context) {
    throw new Error(
      "useAuth must be used within AuthProvider"
    );
  }

  return context;
}