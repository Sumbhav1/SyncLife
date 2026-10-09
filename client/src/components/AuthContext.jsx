import { createContext, useCallback, useContext, useMemo, useState } from "react";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

// Read synchronously so the first render already knows whether someone is logged in
function readStoredUser() {
  try {
    const token = localStorage.getItem("token");
    const user = JSON.parse(localStorage.getItem("user"));
    if (token && user && jwtDecode(token).exp * 1000 > Date.now()) {
      return user;
    }
  } catch {
    // Malformed token or user JSON: treat as logged out
  }
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  return null;
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(readStoredUser);

  const login = useCallback((token, newUser) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(newUser));
    setUser(newUser);
  }, []);

  const updateUser = useCallback((newUser) => {
    localStorage.setItem("user", JSON.stringify(newUser));
    setUser(newUser);
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, login, updateUser, logout }),
    [user, login, updateUser, logout]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
