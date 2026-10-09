import { useNavigate } from "react-router-dom";
import SettingsForm from "../components/SettingsForm";

// First-time setup, shown until the user has saved settings once
const Settings = () => {
  const navigate = useNavigate();
  return <SettingsForm onSaved={() => navigate("/dashboard")} />;
};

export default Settings;
