import {
  FaHome,
  FaUser,
  FaFileAlt,
  FaTrophy,
  FaBriefcase,
  FaClipboardList,
  FaRocket,
  FaRobot,
  FaCog,
  FaGraduationCap
} from "react-icons/fa";

import { NavLink } from "react-router-dom";
import "./Sidebar.css";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="logo">
        <div className="brand">
         <span className="brand-star">✦</span>
        <div>
       <h2>Karta</h2>
       <small>Connect</small>
     </div>
    </div>
      </div>

    <nav>
  <NavLink to="/scholar/home">
  <FaHome /> Home
  </NavLink>

  <NavLink to="/scholar/profile">
    <FaUser /> Profile
  </NavLink>

  <NavLink to="/scholar/resume">
    <FaFileAlt /> Resume
  </NavLink>

  <NavLink to="/scholar/scholarships">
    <FaGraduationCap /> Scholarships
  </NavLink>

  <NavLink to="/scholar/opportunities">
    <FaBriefcase /> Opportunities
  </NavLink>

  <NavLink to="/scholar/applications">
    <FaClipboardList /> Applications
  </NavLink>

  <NavLink to="/scholar/projects">
    <FaRocket /> Projects
  </NavLink>

  <NavLink to="/scholar/achievements">
    <FaTrophy /> Achievements
  </NavLink>

  <NavLink to="/scholar/ai">
    <FaRobot /> AI Insights
  </NavLink>

  <NavLink to="/scholar/settings">
    <FaCog /> Settings
  </NavLink>
 </nav>
    </div>
  );
}