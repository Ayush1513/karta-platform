import { Routes, Route } from "react-router-dom";

import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";

import Home from "../pages/scholar/Home";
import Profile from "../pages/scholar/Profile";
import Resume from "../pages/scholar/Resume";
import Scholarships from "../pages/scholar/Scholarships";
import Opportunities from "../pages/scholar/Opportunities";
import Applications from "../pages/scholar/Applications";
import Projects from "../pages/scholar/Projects";
import Achievements from "../pages/scholar/Achievements";
import AIInsights from "../pages/scholar/AIInsights";
import Settings from "../pages/scholar/Settings";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route path="/scholar/home" element={<Home />} />
      <Route path="/scholar/profile" element={<Profile />} />
      <Route path="/scholar/resume" element={<Resume />} />
      <Route path="/scholar/scholarships" element={<Scholarships />} />
      <Route path="/scholar/opportunities" element={<Opportunities />} />
      <Route path="/scholar/applications" element={<Applications />} />
      <Route path="/scholar/projects" element={<Projects />} />
      <Route path="/scholar/achievements" element={<Achievements />} />
      <Route path="/scholar/ai" element={<AIInsights />} />
      <Route path="/scholar/settings" element={<Settings />} />
    </Routes>
  );
}