import { useNavigate } from "react-router-dom";
import SettingsForm from "../components/SettingsForm";

// Editing settings from the dashboard; stays on the page after saving
const SettingsLoggedIn = () => {
  const navigate = useNavigate();
  return <SettingsForm onBack={() => navigate("/dashboard")} />;
};

export default SettingsLoggedIn;
