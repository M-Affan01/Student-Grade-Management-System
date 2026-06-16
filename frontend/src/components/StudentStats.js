import React from "react";

function StudentStats({ stats }) {
  if (!stats || stats.total_students === 0) {
    return (
      <div className="card stats-card">
        <h2>Class Statistics</h2>
        <p className="no-data">No data available</p>
      </div>
    );
  }

  return (
    <div className="card stats-card">
      <h2>Class Statistics</h2>
      <div className="stats-grid">
        <div className="stat-item">
          <span className="stat-label">Total Students</span>
          <span className="stat-value">{stats.total_students}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Average Grade</span>
          <span className="stat-value avg">
            {Number(stats.average_grade).toFixed(1)}
          </span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Highest Grade</span>
          <span className="stat-value high">{stats.highest_grade}</span>
        </div>
        <div className="stat-item">
          <span className="stat-label">Lowest Grade</span>
          <span className="stat-value low">{stats.lowest_grade}</span>
        </div>
      </div>

      <div className="grade-distribution">
        <h3>Grade Distribution</h3>
        <div className="bar-chart">
          {["A", "B", "C", "D", "F"].map((letter) => {
            const count =
              letter === "A"
                ? stats.grade_a || 0
                : letter === "B"
                ? stats.grade_b || 0
                : letter === "C"
                ? stats.grade_c || 0
                : letter === "D"
                ? stats.grade_d || 0
                : stats.grade_f || 0;
            const percentage =
              stats.total_students > 0
                ? (count / stats.total_students) * 100
                : 0;
            return (
              <div key={letter} className="bar-item">
                <span className="bar-label">{letter}</span>
                <div className="bar-container">
                  <div
                    className={`bar bar-${letter.toLowerCase()}`}
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
                <span className="bar-count">{count}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

export default StudentStats;
