// ===============================
// CONFIG
// ===============================

const BASE_API_URL = "http://127.0.0.1:8000";

// ===============================
// THEME MANAGEMENT
// ===============================

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';

  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  updateThemeIcon(newTheme);

  if (typeof updateChartColors === "function") {
    updateChartColors();
  }
}

function updateThemeIcon(theme) {
  const btn = document.getElementById('themeToggle');
  if (btn) {
    btn.textContent = theme === 'light' ? '🌙' : '☀️';
  }
}

// ===============================
// AUTHENTICATION
// ===============================

document.addEventListener("DOMContentLoaded", () => {
  const savedTheme = localStorage.getItem('theme') || 'light';
  updateThemeIcon(savedTheme);
  checkAuth();
});

function checkAuth() {
  const token = localStorage.getItem("token");
  const isAuthPage = window.location.pathname.includes("login.html") || window.location.pathname.includes("signup.html");

  // Also consider empty path as root which should be protected 
  // depending on server, but typically it resolves to index.html
  const isRootOrIndex = window.location.pathname === "/" || window.location.pathname.includes("index.html");

  if (token) {
    if (isAuthPage) {
      window.location.href = "index.html";
    } else {
      const logoutBtn = document.getElementById("logoutBtn");
      if (logoutBtn) logoutBtn.style.display = "block";
    }
  } else {
    // If not authenticated and not on an auth page, send to login
    if (!isAuthPage && isRootOrIndex) {
      window.location.href = "login.html";
    }
  }
}

async function handleLoginSubmit(event) {
  event.preventDefault();

  const email = document.getElementById("authEmail").value;
  const password = document.getElementById("authPassword").value;
  const errorEl = document.getElementById("authError");

  errorEl.style.display = "none";

  try {
    const response = await fetch(`${BASE_API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Authentication failed");
    }

    localStorage.setItem("token", data.access_token);
    if (data.full_name) localStorage.setItem("full_name", data.full_name);

    window.location.href = "index.html";

  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.style.display = "block";
  }
}

async function handleSignupSubmit(event) {
  event.preventDefault();

  const full_name = document.getElementById("authName").value;
  const email = document.getElementById("authEmail").value;
  const password = document.getElementById("authPassword").value;
  const confirmPassword = document.getElementById("authConfirmPassword").value;
  const errorEl = document.getElementById("authError");

  errorEl.style.display = "none";

  if (password !== confirmPassword) {
    errorEl.textContent = "Passwords do not match";
    errorEl.style.display = "block";
    return;
  }

  try {
    const response = await fetch(`${BASE_API_URL}/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ full_name, email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Registration failed");
    }

    alert("Registration successful! Please log in.");
    window.location.href = "login.html";

  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.style.display = "block";
  }
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("full_name");
  window.location.href = "login.html";
}

const JOB_ROLES = [
  "Data Analyst",
  "Data Engineer",
  "Business Analyst",
  "Machine Learning Engineer",
  "AI Engineer",
  "Backend Developer",
  "Frontend Developer",
  "Full Stack Developer",
  "DevOps Engineer",
  "Cloud Engineer",
  "Cyber Security Analyst",
  "UI/UX Designer",
  "Product Manager",
  "QA Engineer",
  "Mobile App Developer"
];

// ===============================
// STEP NAVIGATION
// ===============================

function goToStep(stepNumber) {
  // 1. VALIDATION (Only when moving FORWARD)
  const activeStepEl = document.querySelector(".step-content.active");
  const currentStep = activeStepEl ? parseInt(activeStepEl.id.replace("step", "")) : 1;

  if (stepNumber > currentStep) {
    if (currentStep === 1) {
      const fileInput = document.getElementById("resumeFile");
      const file = fileInput.files[0];
      if (!file) {
        fileInput.classList.add("input-error");
        alert("Please upload your CV/Resume to proceed.");
        return;
      }
      fileInput.classList.remove("input-error");
    }
    if (currentStep === 2) {
      const roleInput = document.getElementById("targetRole");
      const expInput = document.getElementById("experienceYears");
      const projInput = document.getElementById("projectsCount");

      const role = roleInput.value.trim();
      const exp = expInput.value.trim();
      const projects = projInput.value.trim();

      let hasError = false;
      if (!role) { roleInput.classList.add("input-error"); hasError = true; }
      else roleInput.classList.remove("input-error");

      if (!exp) { expInput.classList.add("input-error"); hasError = true; }
      else expInput.classList.remove("input-error");

      if (!projects) { projInput.classList.add("input-error"); hasError = true; }
      else projInput.classList.remove("input-error");

      if (hasError) {
        alert("Job Title, Experience Years, and Project Count are all mandatory.");
        return;
      }
    }
  }

  // 2. NAVIGATION LOGIC
  // Ensure the workflow is visible and results are hidden when moving between steps
  document.getElementById("wizardWorkflow").style.display = "block";
  document.getElementById("resultsPage").style.display = "none";

  document.querySelectorAll(".step-content").forEach(el => {
    el.classList.remove("active");
  });

  document.querySelectorAll(".step").forEach((el, index) => {
    el.classList.remove("active", "completed");
    if (index < stepNumber - 1) {
      el.classList.add("completed");
    }
    if (index === stepNumber - 1) {
      el.classList.add("active");
    }
  });

  document.getElementById(`step${stepNumber}`).classList.add("active");

  // Ensure Mock Interview is hidden during wizard steps
  const mockPanel = document.getElementById("mockInterviewPanel");
  if (mockPanel) mockPanel.style.display = "none";


  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Add listeners to clear errors on input
document.addEventListener("DOMContentLoaded", () => {
  const fields = ["resumeFile", "targetRole", "experienceYears", "projectsCount"];
  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener("input", () => el.classList.remove("input-error"));
      el.addEventListener("change", () => el.classList.remove("input-error"));
    }
  });
});

function resetWizard() {
  // Clear all inputs
  document.getElementById("resumeFile").value = "";
  document.getElementById("targetRole").value = "";
  document.getElementById("jdText").value = "";
  document.getElementById("experienceYears").value = "";
  document.getElementById("projectsCount").value = "";

  // Back to step 1
  goToStep(1);

  // Explicitly hide mock interview on reset
  const mockPanel = document.getElementById("mockInterviewPanel");
  if (mockPanel) {
    mockPanel.style.display = "none";
    mockPanel.classList.remove("expanded");
  }
}

// ===============================
// AUTOCOMPLETE
// ===============================

const roleInput = document.getElementById("targetRole");
const suggestionsBox = document.getElementById("roleSuggestions");

if (roleInput) {
  roleInput.addEventListener("input", () => {
    const query = roleInput.value.toLowerCase().trim();
    suggestionsBox.innerHTML = "";

    if (!query) {
      suggestionsBox.style.display = "none";
      return;
    }

    const matches = JOB_ROLES.filter(role =>
      role.toLowerCase().includes(query)
    );

    if (matches.length === 0) {
      suggestionsBox.style.display = "none";
      return;
    }

    matches.forEach(role => {
      const div = document.createElement("div");
      div.className = "suggestion-item";
      div.textContent = role;

      div.onclick = () => {
        roleInput.value = role;
        suggestionsBox.style.display = "none";
      };

      suggestionsBox.appendChild(div);
    });

    suggestionsBox.style.display = "block";
  });
}

if (suggestionsBox) {
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".autocomplete-container")) {
      suggestionsBox.style.display = "none";
    }
  });
}

// ===============================
// ANALYZE
// ===============================

async function analyze(event) {
  if (event) event.preventDefault();

  const resumeFile = document.getElementById("resumeFile").files[0];
  const targetRole = document.getElementById("targetRole").value.trim();
  const jdText = document.getElementById("jdText").value.trim();
  const experienceYears = document.getElementById("experienceYears")?.value.trim() || "";
  const projects = document.getElementById("projectsCount")?.value.trim() || "";

  if (!resumeFile || !targetRole || !experienceYears || !projects) {
    alert("Please ensure all mandatory fields (Resume, Role, Experience, Projects) are filled.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("target_role", targetRole);
  formData.append("experience_years", experienceYears);
  formData.append("projects", projects);

  if (jdText) {
    formData.append("job_description_text", jdText);
  }

  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please login first.");
      logout();
      return;
    }

    const response = await fetch(`${BASE_API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    });

    if (response.status === 401) {
      alert("Session expired. Please login again.");
      logout();
      return;
    }

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Analysis failed. Please try again.");
      return;
    }

    renderResults(data);

  } catch (err) {
    console.error("Analyze error:", err);
    alert("Backend error");
  }
}

// ===============================
// RENDER RESULTS
// ===============================

function renderResults(data) {
  // 1. Switch views: Hide inputs, Show results
  document.getElementById("wizardWorkflow").style.display = "none";
  const resultsPage = document.getElementById("resultsPage");
  resultsPage.style.display = "block";

  // Show the Mock Interview tab only on results page
  const mockPanel = document.getElementById("mockInterviewPanel");
  if (mockPanel) mockPanel.style.display = "flex";


  // Scroll to results top
  setTimeout(() => window.scrollTo({ top: 0, behavior: 'smooth' }), 100);

  // Clear the 'already learned' tracking for the new results session
  sessionLearnedSkills.clear();

  document.getElementById("resTargetRole").textContent = data.target_role || "-";
  const roleMatchCard = document.getElementById("resRoleMatch").parentElement;
  const jdMatchCard = document.getElementById("resJdMatch").parentElement;

  if (data.jd_match_percentage !== null) {
    // === SPECIFIC MODE (JD) ===
    jdMatchCard.style.display = "block";
    roleMatchCard.style.display = "none";
    document.getElementById("resJdMatch").textContent = data.jd_match_percentage + "%";
  } else {
    // === GENERAL MODE (ROLE) ===
    jdMatchCard.style.display = "none";
    roleMatchCard.style.display = "block";
    document.getElementById("resRoleMatch").textContent = data.role_match_percentage + "%";
  }

  // 2. TOGGLE VIEWS (Specific JD vs. General Career)
  const specificBox = document.getElementById("specificJobReadiness");
  const generalBox = document.getElementById("generalReadinessBox");
  const recommendedTitle = document.getElementById("recommendedJobsTitle");
  const recommendedJobs = document.getElementById("recommendedJobs");

  const roleSkillsSection = document.getElementById("roleMissingSkills");
  const jdSkillsSection = document.getElementById("jdSpecificSkills");

  if (data.jd_match_percentage !== null) {
    // === SPECIFIC MODE (JD) ===
    specificBox.style.display = "block";
    if (generalBox) generalBox.style.display = "none";
    if (recommendedTitle) recommendedTitle.style.display = "none";
    if (recommendedJobs) recommendedJobs.style.display = "none";

    // Hide original role-based skills, show JD-based
    if (roleSkillsSection) roleSkillsSection.style.display = "none";
    if (jdSkillsSection) jdSkillsSection.style.display = "block";

    document.getElementById("resSpecificReadyScore").textContent = data.specific_job_readiness + "%";
    document.getElementById("resSpecificReadyLevel").textContent = data.specific_job_level;
    document.getElementById("resSpecificReadyRoleName").textContent = data.target_role;

    getSpecificJobLinks(data.target_role, data.specific_job_level);

    // Render list for JD only
    renderList("jdMissingSkillsList", data.role_missing_skills); // role_missing_skills contains JD gaps in this mode
  } else {
    // === GENERAL MODE (ROLE) ===
    if (specificBox) specificBox.style.display = "none";
    if (generalBox) generalBox.style.display = "block";
    if (recommendedTitle) recommendedTitle.style.display = "block";
    if (recommendedJobs) recommendedJobs.style.display = "grid";

    // Show role-based skills, hide JD-based
    if (roleSkillsSection) roleSkillsSection.style.display = "block";
    if (jdSkillsSection) jdSkillsSection.style.display = "none";

    if (data.career_profile && data.career_profile[data.target_role]) {
      const profile = data.career_profile[data.target_role];
      const scoreEl = document.getElementById("resReadyScore");
      const levelEl = document.getElementById("resReadyLevel");
      const roleNameEl = document.getElementById("resReadyRoleName");
      if (scoreEl) scoreEl.textContent = profile.score + "%";
      if (levelEl) levelEl.textContent = profile.level;
      if (roleNameEl) roleNameEl.textContent = data.target_role;

      // Handle Career Pivot Suggestion
      const pivotContainer = document.getElementById("pivotInsightContainer");
      const pivotText = document.getElementById("pivotTooltipText");
      if (pivotContainer && pivotText) {
        const higherRoles = Object.entries(data.career_profile)
          .filter(([role, p]) => p.score > profile.score && role !== data.target_role)
          .sort((a, b) => b[1].score - a[1].score)
          .slice(0, 2);

        if (higherRoles.length > 0) {
          pivotContainer.style.display = "block";
          const rolesList = higherRoles.map(r => `<strong>${r[0]} (${r[1].score}%)</strong>`).join(" and ");
          pivotText.innerHTML = `Based on your skillset, you show stronger compatibility for ${rolesList}. Consider exploring these career paths.`;
        } else {
          pivotContainer.style.display = "none";
        }
      }
    }

    renderRecommendedJobs(data);

    // Render list for Role only
    renderList("roleMissingSkillsList", data.role_missing_skills);
  }

  // Common Breakdown (Always Show)
  renderList("roleExtraSkillsList", data.role_extra_skills);
  renderChart(data.role_matches || {});
}

async function getSpecificJobLinks(role, level) {
  const container = document.getElementById("specificApplyLinks");
  if (!container) return;

  container.innerHTML = "<em>Finding best job matches...</em>";

  const formData = new FormData();
  formData.append("role", role);
  formData.append("level", level);

  try {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BASE_API_URL}/job-recommendations`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    });

    if (!response.ok) throw new Error("Failed to fetch links");

    const result = await response.json();
    container.innerHTML = `
      <a class="job-btn linkedin" href="${result.external_links.linkedin}" target="_blank">
        Apply on LinkedIn →
      </a>
      <a class="job-btn indeed" href="${result.external_links.indeed}" target="_blank">
        Apply on Indeed →
      </a>
    `;
  } catch (err) {
    console.error("Link fetch error:", err);
    container.innerHTML = "<em>Could not load apply links.</em>";
  }
}

// ===============================
// LIST RENDER
// ===============================

function renderList(id, items = []) {
  const container = document.getElementById(id);
  if (!container) return;

  container.innerHTML = "";

  // 1. Update the Count Badge in the parent section header
  const sectionId = container.parentElement.id; // e.g. "roleMissingSkills"
  const countIdMapping = {
    "roleMissingSkillsList": "roleMissingCount",
    "roleExtraSkillsList": "roleExtraCount",
    "jdMissingSkillsList": "jdMissingCount"
  };

  const countBadge = document.getElementById(countIdMapping[id]);
  if (countBadge) {
    countBadge.textContent = items.length;
  }

  // 2. Clear view if empty
  if (items.length === 0) {
    container.innerHTML = "<div class='no-skills-msg'>None identified 😇</div>";
    return;
  }

  // 3. Determine Layout Type
  const isBadgeLayout = id === "roleExtraSkillsList"; // Extracted extra skills use badges
  const isAccordionLayout = id.toLowerCase().includes("missing"); // Gaps use accordions for info

  items.forEach(item => {
    if (isAccordionLayout) {
      // PREMIUM ACCORDION
      const detail = document.createElement("details");
      detail.className = "skill-item-container";

      const summary = document.createElement("summary");
      summary.className = "skill-summary";
      summary.textContent = item;

      const content = document.createElement("div");
      content.className = "skill-detailed-content";
      content.innerHTML = "<em>Loading insights...</em>";

      detail.appendChild(summary);
      detail.appendChild(content);

      detail.addEventListener('toggle', () => {
        if (detail.open && content.dataset.loaded !== "true") {
          fetchSkillInfo(item, content);
        }
      });

      container.appendChild(detail);
    }
    else if (isBadgeLayout) {
      // MODERN CHIP/TAG
      const tag = document.createElement("div");
      tag.className = "skill-tag extra";
      tag.textContent = item;
      container.appendChild(tag);
    }
    else {
      // DEFAULT LIST FALLBACK
      const li = document.createElement("div");
      li.className = "skill-tag";
      li.textContent = item;
      container.appendChild(li);
    }
  });
}

// ===============================
// SKILL INFO TRACKING
// ===============================
let sessionLearnedSkills = new Set();

async function fetchSkillInfo(skill, container) {
  const skillKey = skill.toLowerCase().trim();

  // If already learned in this session, show the blessing message
  if (sessionLearnedSkills.has(skillKey)) {
    container.dataset.loaded = "true";
    container.innerHTML = `
      <div class="skill-details-block" style="text-align: center; padding: 10px 0;">
        <strong style="color: #059669; font-size: 1.1rem;">You are already aware of this!</strong>
        <p style="margin-top: 8px; font-weight: 600;">Thanks to CV Sir 😇</p>
      </div>
    `;
    return;
  }

  try {
    const token = localStorage.getItem("token");
    const response = await fetch(`${BASE_API_URL}/skill-info/${encodeURIComponent(skill)}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    if (!response.ok) throw new Error("Failed to fetch");

    const data = await response.json();
    container.dataset.loaded = "true";

    // 1. Build Roadmap Steps HTML
    let roadmapHtml = "";
    if (data.path && data.path.length > 0) {
      const steps = data.path.map((step, index) => `
        <div class="roadmap-step ${index === 0 ? 'active' : ''}">
          ${step}
          ${index === 0 ? '<span class="roadmap-step-desc">Master this first 🚀</span>' : ''}
        </div>
      `).join("");

      roadmapHtml = `
        <div class="roadmap-container">
          <div class="roadmap-title">🗺️ Learning Success Roadmap</div>
          <div class="roadmap-steps">
            ${steps}
          </div>
        </div>
      `;
    }

    // 2. Prepare Priority Badge
    const priority = data.priority || "Standard";
    const priorityClass = `priority-${priority.toLowerCase()}`;
    const priorityText = priority.toLowerCase() === "highest" ? "🚨 Highest" : priority;

    container.innerHTML = `
      <div class="skill-details-header">
        <strong style="color: var(--primary);">Skill Intelligence</strong>
        <span class="priority-badge ${priorityClass}">${priorityText} Priority</span>
      </div>
      <div class="skill-details-block"><strong>🔍 Overview:</strong> ${data.description}</div>
      <div class="skill-details-block"><strong>⭐ Importance:</strong> ${data.importance}</div>
      <div class="skill-details-block"><strong>📚 Recommended:</strong> ${data.learning}</div>
      <div class="skill-details-block"><strong>💡 CV Strategy:</strong> ${data.tip}</div>
      ${roadmapHtml}
    `;

    // Mark as learned for this session
    sessionLearnedSkills.add(skillKey);

  } catch (err) {
    console.error("Skill detail fetch error:", err);
    container.innerHTML = "<em>Could not load details.</em>";
  }
}

// ===============================
// CHART
// ===============================

let roleChart = null;

function updateChartColors() {
  if (!roleChart) return;
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  const textColor = isDark ? "#ffffff" : "#587483";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.05)";

  roleChart.options.scales.x.ticks.color = textColor;
  roleChart.options.scales.x.grid.color = gridColor;
  roleChart.options.scales.y.ticks.color = textColor;
  roleChart.options.scales.y.grid.color = gridColor;
  roleChart.update();
}

function renderChart(roleMatches) {
  const labels = Object.keys(roleMatches);
  const values = Object.values(roleMatches);

  const canvas = document.getElementById("roleChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  if (roleChart) roleChart.destroy();

  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  const textColor = isDark ? "#ffffff" : "#587483";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.1)" : "rgba(0, 0, 0, 0.05)";

  roleChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Role Match %",
        data: values,
        backgroundColor: "#587483",
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          ticks: { color: textColor },
          grid: { color: gridColor, drawBorder: false }
        },
        y: {
          beginAtZero: true,
          max: 100,
          ticks: { color: textColor },
          grid: { color: gridColor, drawBorder: false }
        }
      }
    }
  });
}

// ===============================
// JOB RECOMMENDATIONS
// ===============================

async function renderRecommendedJobs(data) {

  const container = document.getElementById("recommendedJobs");
  container.innerHTML = "";

  const rankedRoles = Object.entries(data.career_profile || {})
    .sort((a, b) => b[1].score - a[1].score)
    .slice(0, 3);

  for (const [role, profile] of rankedRoles) {

    const formData = new FormData();
    formData.append("role", role);
    formData.append("level", profile.level);

    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${BASE_API_URL}/job-recommendations`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`
        },
        body: formData
      });

      if (response.status === 401) {
        alert("Session expired.");
        logout();
        return;
      }

      const result = await response.json();

      const card = document.createElement("div");
      card.className = "job-card";

      // 🔥 ONLY UI CHANGE HERE
      card.innerHTML = `
        <h4>${role}</h4>

        <div class="job-meta">
          <span><strong>Level:</strong> ${profile.level}</span>
          <span><strong>Readiness:</strong> ${profile.score}%</span>
        </div>

        <div class="job-links">
          <a class="job-btn linkedin" href="${result.external_links.linkedin}" target="_blank">
            LinkedIn Jobs →
          </a>
          <a class="job-btn indeed" href="${result.external_links.indeed}" target="_blank">
            Indeed Jobs →
          </a>
        </div>
      `;

      container.appendChild(card);

    } catch (err) {
      console.error("Recommendation error:", err);
    }
  }
}

// AI MOCK INTERVIEW LOGIC
// ===============================

const MOCK_QUESTIONS = [
  "Can you tell me about yourself and your background?",
  "What are your greatest strengths and how do they apply to this role?",
  "Why do you want to work at this company specifically?",
  "Tell me about a challenging situation at work and how you handled it.",
  "Where do you see yourself in five years?"
];

const MOCK_REACTIONS = [
  {
    positive: "That's a very solid background! Your experience seems well-aligned with what we're looking for.",
    constructive: "Thank you for sharing. In a real interview, try to highlight your most relevant achievements first."
  },
  {
    positive: "Great strengths! Those specific skills are highly valuable for this role.",
    constructive: "I see. Try to connect those strengths more directly to the specific problems this role solves."
  },
  {
    positive: "It's clear you've done your research! We value candidates who understand our mission.",
    constructive: "That's a fair point. For even better impact, mention a specific project of ours that excites you."
  },
  {
    positive: "Excellent problem-solving approach. Your ability to handle pressure is impressive.",
    constructive: "A good start. Using the STAR method (Situation, Task, Action, Result) would make this story even stronger."
  },
  {
    positive: "I love that ambition! It's great to see a candidate with a clear long-term vision.",
    constructive: "Interesting goals. Make sure to emphasize how growing with *this* company fits into that 5-year plan."
  }
];

let mockCurrentStep = 0;
let mockScore = 0;
let mockStarted = false;

function toggleMockInterview() {
  const panel = document.getElementById("mockInterviewPanel");
  const icon = document.getElementById("mockToggleIcon");

  if (!panel) return;

  const isExpanded = panel.classList.toggle("expanded");
  if (icon) icon.textContent = isExpanded ? "▼" : "▲";

  // Start the interview if it's the first time expanding
  if (isExpanded && !mockStarted) {
    startMockInterviewSession();
  }
}

function startMockInterviewSession() {
  const chatMessages = document.getElementById("chatMessages");
  const overlay = document.getElementById("mockResultOverlay");

  if (!chatMessages || !overlay) return;

  overlay.style.display = "none";
  chatMessages.innerHTML = "";
  mockCurrentStep = 0;
  mockScore = 0;
  mockStarted = true;

  setTimeout(() => {
    appendChatMessage("ai", "Hello! I am your AI Interviewer. Let's start with the first question:");
    setTimeout(() => {
      askNextMockQuestion();
    }, 800);
  }, 500);
}

function closeMockInterview() {
  const panel = document.getElementById("mockInterviewPanel");
  const icon = document.getElementById("mockToggleIcon");
  if (panel) {
    panel.classList.remove("expanded");
    if (icon) icon.textContent = "▲";
  }
}

function handleChatKey(e) {
  if (e.key === "Enter") sendChatMessage();
}

const MOCK_FEEDBACK_POSITIVE = [
  "✅ Perfect answer! You demonstrated great clarity.",
  "🌟 Excellent response. Your experience really shines through.",
  "🚀 Brilliant! That's a very professional way to frame it.",
  "🎯 Spot on. You addressed the core of the question perfectly."
];

const MOCK_FEEDBACK_CONSTRUCTIVE = [
  "💡 Good start, but try to provide a more specific example.",
  "🧐 Nice effort, but focus more on the result of your actions.",
  "🔨 Solid logic, but try to keep it a bit more concise.",
  "🤝 Interesting point, but relate it back to the company's goals."
];

function sendChatMessage() {
  const input = document.getElementById("chatInput");
  const text = input.value.trim();
  if (!text) return;

  appendChatMessage("user", text);
  input.value = "";

  // Simulation logic
  setTimeout(() => {
    const isGood = text.length > 30;
    const reaction = MOCK_REACTIONS[mockCurrentStep];
    const feedback = isGood ? reaction.positive : reaction.constructive;

    appendChatMessage("ai", feedback);
    mockScore += isGood ? 2 : 1;

    mockCurrentStep++;

    setTimeout(() => {
      if (mockCurrentStep < MOCK_QUESTIONS.length) {
        askNextMockQuestion();
      } else {
        showMockResults();
      }
    }, 1000);
  }, 800);
}

function askNextMockQuestion() {
  if (mockCurrentStep < MOCK_QUESTIONS.length) {
    appendChatMessage("ai", MOCK_QUESTIONS[mockCurrentStep]);
  }
}

function appendChatMessage(sender, text) {
  const chatMessages = document.getElementById("chatMessages");
  if (!chatMessages) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}-bubble`;
  bubble.textContent = text;
  chatMessages.appendChild(bubble);

  // Clean scroll to bottom
  chatMessages.scrollTo({
    top: chatMessages.scrollHeight,
    behavior: "smooth"
  });
}

function showMockResults() {
  const overlay = document.getElementById("mockResultOverlay");
  const scoreDisplay = document.getElementById("mockScoreDisplay");
  const improvementMsg = document.getElementById("mockImprovementMsg");

  if (!overlay || !scoreDisplay || !improvementMsg) return;

  const finalScore = Math.min(mockScore, 10);
  scoreDisplay.textContent = `${finalScore}/10`;

  if (finalScore >= 8) {
    improvementMsg.textContent = "Outstanding! You are highly prepared for this role.";
  } else if (finalScore >= 5) {
    improvementMsg.textContent = "Good progress! A bit more detail in your answers will make you stand out.";
  } else {
    improvementMsg.textContent = "Practice makes perfect. Focus on structured answering techniques like STAR.";
  }

  overlay.style.display = "flex";
}
