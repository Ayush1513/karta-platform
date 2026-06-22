import ScholarLayout from "../../layouts/ScholarLayout";
import "./profile.css";

export default function Profile() {
  return (
    <ScholarLayout>
      <div className="profile-container">

        {/* Header */}
        <div className="page-header">
          <div className="profile-header">

            <div>
              <h1>👤 My Profile</h1>

              <p>
                Manage your personal and academic details.
              </p>

              <div className="profile-stats-grid">

                <div className="profile-stat-card">
                  <h4>Projects</h4>
                  <h2>5</h2>
                </div>

                <div className="profile-stat-card">
                  <h4>Achievements</h4>
                  <h2>8</h2>
                </div>

                <div className="profile-stat-card">
                  <h4>AI Score</h4>
                  <h2>87%</h2>
                </div>

              </div>
            </div>

            <div className="profile-completion-card">
              <h4>Profile Completion</h4>

              <div className="completion-score">
                82%
              </div>

              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: "82%" }}
                ></div>
              </div>

              <p>Strong Profile</p>
            </div>

          </div>
        </div>

        {/* Profile Summary */}
        <div className="profile-avatar-card">

          <div className="avatar-circle">
            AK
          </div>

          <div className="avatar-info">
            <h3>Ayush Kumar</h3>
            <p>
              AI & Data Science • Shoolini University
            </p>
          </div>

        </div>

        {/* Personal Information */}
        <div className="profile-card">

          <h2>Personal Information</h2>

          <div className="form-grid">

            <div className="form-group">
              <label>Full Name</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>Phone Number</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>Country</label>
              <input type="text" />
            </div>

          </div>

        </div>

        {/* Academic Information */}
        <div className="profile-card">

          <h2>Academic Information</h2>

          <div className="form-grid">

            <div className="form-group">
              <label>University</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>Course</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>Academic Year</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>CGPA</label>
              <input type="text" />
            </div>

          </div>

        </div>

        {/* Resume + Professional Links */}
        <div className="profile-card">

          <div className="resume-card">

            <h3>📄 Resume Status</h3>

            <div className="resume-info-grid">

              <div className="resume-info-box">
                <small>Status</small>
                <h4>Uploaded ✅</h4>
              </div>

              <div className="resume-info-box">
                <small>File Name</small>
                <h4>Ayush_Resume.pdf</h4>
              </div>

              <div className="resume-info-box">
                <small>Last Updated</small>
                <h4>18 June 2026</h4>
              </div>

            </div>

          </div>

          <h2>Professional Links</h2>

          <div className="form-grid">

            <div className="form-group">
              <label>Github</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>LinkedIn</label>
              <input type="text" />
            </div>

            <div className="form-group">
              <label>Portfolio</label>
              <input type="text" />
            </div>

          </div>

        </div>

        {/* About Me */}
        <div className="profile-card">

          <h2>About Me</h2>

          <div className="form-group">
            <textarea
              className="about-textarea"
              placeholder="Tell us about yourself..."
            />
          </div>

        </div>

        <button className="save-btn">
          Save Profile
        </button>

      </div>
    </ScholarLayout>
  );
}