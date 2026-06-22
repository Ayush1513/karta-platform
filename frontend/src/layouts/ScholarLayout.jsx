import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import "./ScholarLayout.css";

export default function ScholarLayout({
  children,
}) {
  return (
    <div className="layout">

      <Sidebar />

      <div className="main-content">
        <Navbar />

        <div className="page-content">
          {children}
        </div>
      </div>

    </div>
  );
}