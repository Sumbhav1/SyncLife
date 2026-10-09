import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import SignUp from './pages/SignUp';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import AddAMeal from './pages/AddAMeal';
import AddSleep from './pages/AddSleep';
import SettingsLoggedIn from './pages/SettingsLoggedIn';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/" element={<Navigate to="/login" />} />  {/* Redirect to login if visiting root */}

        {/* Accessible only if logged in AND settings not finished */}
        <Route element={<ProtectedRoute requireSettingsComplete={false} />}>
          <Route path="/settings" element={<Settings />} />
        </Route>

        {/* Accessible only if logged in AND settings are finished */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/add-a-meal" element={<AddAMeal />} />
          <Route path="/add-sleep" element={<AddSleep />} />
          <Route path="/settings-logged-in"element={<SettingsLoggedIn />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;



