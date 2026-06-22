import ScholarLayout from "../../layouts/ScholarLayout";
import "./scholarships.css";

export default function Scholarships() {

const scholarships = [
{
id: 1,
title: "Tata Capital Pankh Scholarship",
amount: "₹12,000",
deadline: "30 July 2026",
category: "Merit Based",
match: "92%"
},
{
id: 2,
title: "Buddy4Study Merit Scholarship",
amount: "₹50,000",
deadline: "15 August 2026",
category: "Need Based",
match: "95%"
},
{
id: 3,
title: "HDFC Scholarship",
amount: "₹75,000",
deadline: "20 August 2026",
category: "Private",
match: "88%"
}
];

return ( <ScholarLayout> <div className="scholarships-page">

```
    <div className="scholarships-header">
      <h1>🎓 Scholarships</h1>
      <p>
        Find scholarships matching your profile.
      </p>
    </div>

    {/* Statistics */}

    <div className="scholarship-stats">

      <div className="stat-box">
        <h2>24</h2>
        <p>Active Scholarships</p>
      </div>

      <div className="stat-box">
        <h2>₹12L+</h2>
        <p>Total Funding</p>
      </div>

      <div className="stat-box">
        <h2>5</h2>
        <p>Applied</p>
      </div>

    </div>

    {/* Search */}

    <input
      className="search-box"
      placeholder="Search scholarships..."
    />

    {/* Filters */}

    <div className="filter-row">

      <button>All</button>
      <button>Merit</button>
      <button>Need Based</button>
      <button>Government</button>
      <button>Private</button>

    </div>

    {/* Scholarship Cards */}

    <div className="scholarship-grid">

      {scholarships.map((item) => (
        <div
          key={item.id}
          className="scholarship-card"
        >

          <h3>{item.title}</h3>

          <div className="amount-badge">
            {item.amount}
          </div>

          <p className="deadline">
            ⏳ Deadline: {item.deadline}
          </p>

          <div className="scholarship-tags">

            <span className="category-tag">
              {item.category}
            </span>

            <span className="match-tag">
              🎯 {item.match} Match
            </span>

          </div>

          <div className="card-actions">

            <button>
              View Details
            </button>

            <button className="apply-btn">
              Apply
            </button>

          </div>

        </div>
      ))}

    </div>

  </div>
</ScholarLayout>


);
}
