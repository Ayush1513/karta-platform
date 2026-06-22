import { FaBell } from "react-icons/fa";
import "./Navbar.css";

export default function Navbar() {
  return (
    <div className="navbar">

      <input
        type="text"
        placeholder="Search anything..."
        className="search-bar"
      />

      <div className="navbar-right">
        <button className="notification-btn">
          <FaBell />
          <span className="badge">3</span>
        </button>

        <div className="user-profile">
          Ayush
        </div>
      </div>

    </div>
  );
}