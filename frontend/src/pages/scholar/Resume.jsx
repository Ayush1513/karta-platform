import ScholarLayout from "../../layouts/ScholarLayout";
import "./resume.css";

export default function Resume() {
  return (
    <ScholarLayout>
      <div className="resume-page">

        {/* Header */}
        <div className="resume-header">
          <h1>📄 Resume</h1>
          <p>Upload and manage your latest resume.</p>
        </div>

        {/* Resume Status */}
        <div className="resume-status-card">

          <h2>Resume Status</h2>

             <div className="resume-info-grid">

             <div className="resume-info-box">
            <h4>Status</h4>
            <p>Uploaded ✅</p>
             </div>

               <div className="resume-info-box">
                 <h4>File Name</h4>
                <p>Ayush_Resume.pdf</p>
                </div>

                <div className="resume-info-box">
               <h4>Last Updated</h4>
              <p>18 June 2026</p>
             </div>

             </div>

           <div className="resume-actions">
            <button>View Resume</button>
            <button>Replace Resume</button>

            <button className="danger-btn">
              Delete Resume
            </button>
          </div>
        </div>

        {/* Upload Area */}
        <div className="upload-card">
          <h2>Upload Resume</h2>

          <div className="upload-box">
            <div className="upload-icon">📄</div>

             <h3>Drag & Drop Resume</h3>

              <p>
               Upload your latest resume for AI analysis
              </p>

            <p>or browse from your computer</p>

             <label className="custom-file-upload">
               📄 Select Resume
                <input type="file" />
             </label>

            <small>
              PDF Only • Max Size 5 MB
            </small>
          </div>

          <button className="upload-btn">
            Upload Resume
          </button>
        </div>

      {/* AI Resume Insights */}
     <div className="analysis-card">

     <h2>🤖 AI Resume Insights</h2>

     <div className="analysis-grid">

       {/* Skills Card */}
       <div className="insight-card">

      <h3>Detected Skills</h3>

      <div className="skills-grid">
        <span>Python</span>
        <span>FastAPI</span>
        <span>SQL</span>
        <span>React</span>
        <span>Machine Learning</span>
      </div>

       </div>

      {/* Score Card */}
      <div className="insight-card score-card">

      <h3>AI Profile Score</h3>

      <div className="score-circle">
        87%
      </div>

      <p>Strong Profile</p>

    </div>

    {/* Recommendation Card */}
    <div>
        <h3>Recommended Skills</h3>

       <div className="recommended-skills">

         <span>Docker</span>
         <span>Kubernetes</span>
         <span>CI/CD</span>

     </div>
    </div>
    </div>

   </div>

      </div>
    </ScholarLayout>
  );
}