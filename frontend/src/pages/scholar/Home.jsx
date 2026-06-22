import ScholarLayout from "../../layouts/ScholarLayout";
import "./home.css";

export default function Home() {
  return (
    <ScholarLayout>
      {/* Welcome Section */}
      <div className="welcome-section">
        <div>
          <h1>Welcome Back, Ayush 👋</h1>
          <p>
            AI & Data Science • Shoolini University
          </p>
        </div>

        <div className="profile-progress">
          <span>Profile Completion</span>
          <h2>82%</h2>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>📋 Applications</h3>
          <h1>12</h1>
          <p>+2 this month</p>
        </div>

        <div className="stat-card">
          <h3>🤖 AI Score</h3>
          <h1>87%</h1>
          <p>Strong Profile</p>
        </div>

        <div className="stat-card">
          <h3>🚀 Projects</h3>
          <h1>5</h1>
          <p>2 featured</p>
        </div>

        <div className="stat-card">
          <h3>🏆 Achievements</h3>
          <h1>8</h1>
          <p>Growing portfolio</p>
        </div>
      </div>

      {/* Main Grid */}
      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>🎓 Recommended Scholarships</h2>

          <div className="scholarship-item">
            <h4>Buddy4Study Merit Scholarship</h4>
            <span>₹50,000 Support</span>
          </div>

          <div className="scholarship-item">
            <h4>Tata Capital Pankh Scholarship</h4>
            <span>₹12,000 Support</span>
          </div>

          <div className="scholarship-item">
            <h4>HDFC Scholarship</h4>
            <span>Merit Based</span>
          </div>
        </div>

        <div className="dashboard-card">
          <h2>🔔 Recent Notifications</h2>

          <div className="notification-item">
            New Scholarship Added
          </div>

          <div className="notification-item">
            Application Approved
          </div>

          <div className="notification-item">
            Resume Analysis Completed
          </div>

          <div className="notification-item">
            Profile Score Increased
          </div>
        </div>

      </div>
    </ScholarLayout>
  );
}