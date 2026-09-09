<template>
  <div class="career-page">

    <!-- ================= NAVBAR ================= -->
    <nav class="navbar">
      <div class="nav-container">
        <a href="/" class="brand">
          <span class="brand-icon">C</span>
          Career<span>Link</span>
        </a>

        <div class="nav-links">
          <a href="/" class="nav-link active">Home</a>
          <a href="/jobs" class="nav-link">Jobs</a>
          <a href="/companies" class="nav-link">Companies</a>
          <a href="#features" class="nav-link">Features</a>
        </div>

        <div class="nav-actions">
          <a href="/login" class="login-btn">Login</a>
          <a href="/register" class="register-btn">Get Started</a>
        </div>
      </div>
    </nav>


    <!-- ================= HERO ================= -->
    <section class="hero">
      <div class="hero-container">

        <div class="hero-content">

          <div class="hero-badge">
            <span>✦</span>
            Your career journey starts here
          </div>

          <h1>
            Build Your Career.
            <span>Find Your Future.</span>
          </h1>

          <p class="hero-description">
            Discover the right opportunities, connect with leading companies,
            and take the next step toward your dream career with CareerLink.
          </p>

          <!-- SEARCH -->
          <div class="search-box">

            <div class="search-field">
              <span class="search-icon">⌕</span>

              <div>
                <small>What are you looking for?</small>
                <input
                  type="text"
                  placeholder="Job title, skills or keywords"
                />
              </div>
            </div>

            <div class="search-divider"></div>

            <div class="search-field location-field">
              <span class="location-icon">⌖</span>

              <div>
                <small>Location</small>
                <input
                  type="text"
                  placeholder="City or remote"
                />
              </div>
            </div>

            <button class="search-btn" @click="searchJobs">
              Search Jobs
            </button>

          </div>

          <div class="popular-searches">
            <span>Popular:</span>
            <a href="/jobs?search=software">Software Developer</a>
            <a href="/jobs?search=data">Data Science</a>
            <a href="/jobs?search=internship">Internships</a>
          </div>

        </div>


        <!-- HERO VISUAL -->
        <div class="hero-visual">

          <div class="floating-card card-one">
            <div class="mini-icon">✓</div>
            <div>
              <strong>New Opportunity</strong>
              <small>Software Developer</small>
            </div>
          </div>

          <div class="profile-card">

            <div class="profile-top">
              <div class="profile-avatar">
                BS
              </div>

              <div>
                <strong>Career Profile</strong>
                <span>Ready for opportunities</span>
              </div>

              <div class="verified">✓</div>
            </div>

            <div class="profile-line"></div>

            <div class="profile-info">
              <div>
                <span>Skills</span>
                <strong>Java · Python · SQL</strong>
              </div>

              <div>
                <span>Experience</span>
                <strong>Fresher</strong>
              </div>
            </div>

            <div class="progress-section">
              <div class="progress-heading">
                <span>Profile completion</span>
                <strong>85%</strong>
              </div>

              <div class="progress-bar">
                <div class="progress-value"></div>
              </div>
            </div>

            <button class="profile-btn" @click="goToProfile">
              Complete Profile →
            </button>

          </div>

          <div class="floating-card card-two">
            <div class="company-icon">★</div>

            <div>
              <strong>Top Companies</strong>
              <small>Find your next opportunity</small>
            </div>
          </div>

        </div>

      </div>
    </section>


    <!-- ================= STATS ================= -->
    <section class="stats-section">
      <div class="stats-container">

        <div class="stat">
          <strong>100+</strong>
          <span>Job Opportunities</span>
        </div>

        <div class="stat">
          <strong>50+</strong>
          <span>Companies</span>
        </div>

        <div class="stat">
          <strong>500+</strong>
          <span>Registered Users</span>
        </div>

        <div class="stat">
          <strong>24/7</strong>
          <span>Career Access</span>
        </div>

      </div>
    </section>


    <!-- ================= FEATURES ================= -->
    <section id="features" class="features-section">

      <div class="section-heading">

        <div class="section-badge">
          WHY CAREERLINK?
        </div>

        <h2>
          Everything you need to
          <span>grow your career</span>
        </h2>

        <p>
          CareerLink brings students, job seekers and companies together
          on one simple platform.
        </p>

      </div>


      <div class="feature-grid">

        <div class="feature-card">

          <div class="feature-icon blue">
            🔎
          </div>

          <h3>Discover Opportunities</h3>

          <p>
            Search and explore jobs and internships based on your
            skills, interests and career goals.
          </p>

          <a href="/jobs">Explore Jobs →</a>

        </div>


        <div class="feature-card">

          <div class="feature-icon purple">
            👤
          </div>

          <h3>Build Your Profile</h3>

          <p>
            Create a professional career profile and showcase your
            skills, education and experience.
          </p>

          <a href="/register">Create Profile →</a>

        </div>


        <div class="feature-card">

          <div class="feature-icon green">
            🏢
          </div>

          <h3>Connect With Companies</h3>

          <p>
            Find companies looking for talented candidates and
            discover opportunities that match your profile.
          </p>

          <a href="/companies">View Companies →</a>

        </div>


        <div class="feature-card">

          <div class="feature-icon orange">
            📈
          </div>

          <h3>Grow Your Career</h3>

          <p>
            Track your applications and stay organized throughout
            your career journey.
          </p>

          <a href="/login">Track Applications →</a>

        </div>

      </div>

    </section>


    <!-- ================= HOW IT WORKS ================= -->
    <section class="how-section">

      <div class="section-heading">

        <div class="section-badge">
          SIMPLE PROCESS
        </div>

        <h2>
          Your career journey in
          <span>3 simple steps</span>
        </h2>

      </div>


      <div class="steps">

        <div class="step">

          <div class="step-number">01</div>

          <div>
            <h3>Create Your Profile</h3>
            <p>
              Register on CareerLink and build your professional profile.
            </p>
          </div>

        </div>


        <div class="step-line"></div>


        <div class="step">

          <div class="step-number">02</div>

          <div>
            <h3>Discover Opportunities</h3>
            <p>
              Browse jobs and internships that match your skills.
            </p>
          </div>

        </div>


        <div class="step-line"></div>


        <div class="step">

          <div class="step-number">03</div>

          <div>
            <h3>Apply & Grow</h3>
            <p>
              Apply for opportunities and take the next step in your career.
            </p>
          </div>

        </div>

      </div>

    </section>


    <!-- ================= CTA ================= -->
    <section class="cta-section">

      <div class="cta-content">

        <div class="cta-icon">
          🚀
        </div>

        <h2>
          Ready to take the next step?
        </h2>

        <p>
          Start building your career with CareerLink today.
        </p>

        <div class="cta-buttons">

          <a href="/register" class="cta-primary">
            Create Your Profile →
          </a>

          <a href="/jobs" class="cta-secondary">
            Explore Jobs
          </a>

        </div>

      </div>

    </section>


    <!-- ================= FOOTER ================= -->
    <footer>

      <div class="footer-container">

        <div class="footer-brand">
          <a href="/" class="brand">
            <span class="brand-icon">C</span>
            Career<span>Link</span>
          </a>

          <p>
            Connecting talent with opportunity.
          </p>
        </div>

        <div class="footer-links">
          <a href="/">Home</a>
          <a href="/jobs">Jobs</a>
          <a href="/companies">Companies</a>
          <a href="/login">Login</a>
          <a href="/register">Register</a>
        </div>

        <div class="copyright">
          © 2026 CareerLink. All rights reserved.
        </div>

      </div>

    </footer>

  </div>
</template>


<script setup>

const searchJobs = () => {
  const inputs = document.querySelectorAll(".search-field input")

  const keyword = inputs[0]?.value || ""
  const location = inputs[1]?.value || ""

  const params = new URLSearchParams()

  if (keyword) {
    params.append("search", keyword)
  }

  if (location) {
    params.append("location", location)
  }

  window.location.href = `/jobs?${params.toString()}`
}


const goToProfile = () => {
  window.location.href = "/profile"
}

</script>


<style scoped>

/* ================= GLOBAL ================= */

* {
  box-sizing: border-box;
}

.career-page {
  min-height: 100vh;
  background: #ffffff;
  color: #172033;
  font-family:
    Inter,
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    sans-serif;
}


/* ================= NAVBAR ================= */

.navbar {
  height: 74px;
  border-bottom: 1px solid #e8edf5;
  background: rgba(255, 255, 255, 0.96);
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.nav-container {
  width: min(1180px, 92%);
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  text-decoration: none;
  color: #172033;
  font-size: 24px;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand > span:not(.brand-icon) {
  color: #1769ff;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: #1769ff;
  color: white;
  border-radius: 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.nav-links {
  display: flex;
  gap: 34px;
  margin-left: 80px;
}

.nav-link {
  color: #687386;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
  transition: 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: #1769ff;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 18px;
}

.login-btn {
  text-decoration: none;
  color: #344054;
  font-weight: 600;
}

.register-btn {
  text-decoration: none;
  color: white;
  background: #1769ff;
  padding: 11px 21px;
  border-radius: 9px;
  font-weight: 600;
  box-shadow: 0 5px 15px rgba(23, 105, 255, 0.2);
}


/* ================= HERO ================= */

.hero {
  background:
    radial-gradient(circle at 80% 20%, #e8f1ff 0, transparent 32%),
    linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
  padding: 90px 0 70px;
  overflow: hidden;
}

.hero-container {
  width: min(1180px, 92%);
  margin: auto;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  align-items: center;
  gap: 60px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #eaf2ff;
  color: #1769ff;
  padding: 8px 14px;
  border-radius: 30px;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 20px;
}

.hero-content h1 {
  font-size: clamp(44px, 5vw, 68px);
  line-height: 1.06;
  letter-spacing: -2.5px;
  margin: 0;
  font-weight: 800;
}

.hero-content h1 span {
  display: block;
  color: #1769ff;
}

.hero-description {
  color: #687386;
  font-size: 18px;
  line-height: 1.7;
  max-width: 610px;
  margin: 25px 0 30px;
}


/* ================= SEARCH ================= */

.search-box {
  background: white;
  border: 1px solid #e0e6ef;
  border-radius: 15px;
  padding: 9px;
  display: flex;
  align-items: center;
  box-shadow: 0 15px 40px rgba(32, 66, 120, 0.1);
  max-width: 720px;
}

.search-field {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 14px;
  flex: 1;
}

.search-field small {
  display: block;
  color: #98a2b3;
  font-size: 11px;
  font-weight: 600;
  margin-bottom: 3px;
}

.search-field input {
  border: 0;
  outline: none;
  width: 100%;
  font-size: 14px;
  color: #344054;
  background: transparent;
}

.search-icon,
.location-icon {
  font-size: 25px;
  color: #1769ff;
}

.search-divider {
  height: 40px;
  width: 1px;
  background: #e6eaf0;
}

.search-btn {
  border: none;
  background: #1769ff;
  color: white;
  padding: 15px 22px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
}

.search-btn:hover {
  transform: translateY(-1px);
  background: #0756df;
}

.popular-searches {
  margin-top: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  font-size: 12px;
}

.popular-searches span {
  color: #98a2b3;
}

.popular-searches a {
  color: #536174;
  text-decoration: none;
}

.popular-searches a:hover {
  color: #1769ff;
}


/* ================= HERO VISUAL ================= */

.hero-visual {
  min-height: 430px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.profile-card {
  width: 380px;
  background: white;
  border: 1px solid #e3e8f0;
  border-radius: 22px;
  padding: 28px;
  box-shadow: 0 25px 60px rgba(37, 72, 130, 0.13);
  transform: rotate(2deg);
}

.profile-top {
  display: flex;
  align-items: center;
  gap: 13px;
}

.profile-avatar {
  width: 54px;
  height: 54px;
  border-radius: 50%;
  background: #eaf2ff;
  color: #1769ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}

.profile-top strong {
  display: block;
  font-size: 16px;
}

.profile-top span {
  display: block;
  color: #98a2b3;
  font-size: 12px;
  margin-top: 4px;
}

.verified {
  margin-left: auto;
  background: #e8f8ef;
  color: #16a05d;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.profile-line {
  height: 1px;
  background: #edf0f5;
  margin: 25px 0;
}

.profile-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.profile-info span {
  color: #98a2b3;
  font-size: 11px;
  display: block;
  margin-bottom: 5px;
}

.profile-info strong {
  font-size: 12px;
  color: #344054;
}

.progress-section {
  margin-top: 25px;
}

.progress-heading {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-bottom: 8px;
}

.progress-heading span {
  color: #667085;
}

.progress-heading strong {
  color: #1769ff;
}

.progress-bar {
  height: 7px;
  background: #edf1f6;
  border-radius: 20px;
  overflow: hidden;
}

.progress-value {
  width: 85%;
  height: 100%;
  background: #1769ff;
  border-radius: 20px;
}

.profile-btn {
  margin-top: 22px;
  width: 100%;
  padding: 11px;
  border: 1px solid #dce4ef;
  background: white;
  border-radius: 9px;
  cursor: pointer;
  color: #1769ff;
  font-weight: 700;
}

.floating-card {
  position: absolute;
  background: white;
  border: 1px solid #e4e9f1;
  border-radius: 13px;
  padding: 14px 17px;
  display: flex;
  gap: 11px;
  align-items: center;
  box-shadow: 0 15px 35px rgba(30, 60, 110, 0.1);
}

.floating-card strong {
  display: block;
  font-size: 12px;
}

.floating-card small {
  display: block;
  color: #98a2b3;
  font-size: 10px;
  margin-top: 4px;
}

.card-one {
  left: 0;
  top: 50px;
}

.card-two {
  right: 0;
  bottom: 50px;
}

.mini-icon,
.company-icon {
  width: 35px;
  height: 35px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eaf2ff;
  color: #1769ff;
}


/* ================= STATS ================= */

.stats-section {
  border-top: 1px solid #edf0f5;
  border-bottom: 1px solid #edf0f5;
  background: white;
}

.stats-container {
  width: min(1000px, 90%);
  margin: auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  padding: 35px 0;
}

.stat {
  text-align: center;
  border-right: 1px solid #edf0f5;
}

.stat:last-child {
  border: none;
}

.stat strong {
  display: block;
  color: #1769ff;
  font-size: 28px;
  font-weight: 800;
}

.stat span {
  color: #7b8798;
  font-size: 13px;
}


/* ================= SECTION ================= */

.features-section,
.how-section {
  padding: 100px 0;
  width: min(1180px, 92%);
  margin: auto;
}

.section-heading {
  text-align: center;
  max-width: 680px;
  margin: 0 auto 55px;
}

.section-badge {
  color: #1769ff;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1.5px;
  margin-bottom: 12px;
}

.section-heading h2 {
  font-size: 40px;
  line-height: 1.15;
  margin: 0;
  letter-spacing: -1px;
}

.section-heading h2 span {
  color: #1769ff;
}

.section-heading p {
  color: #7b8798;
  line-height: 1.7;
}


/* ================= FEATURES ================= */

.feature-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.feature-card {
  padding: 27px;
  border: 1px solid #e8edf4;
  border-radius: 16px;
  background: white;
  transition: 0.25s;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 45px rgba(35, 70, 120, 0.09);
  border-color: #d9e5fb;
}

.feature-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  margin-bottom: 22px;
}

.feature-icon.blue {
  background: #eaf2ff;
}

.feature-icon.purple {
  background: #f1eaff;
}

.feature-icon.green {
  background: #e8f8ef;
}

.feature-icon.orange {
  background: #fff2df;
}

.feature-card h3 {
  font-size: 17px;
  margin: 0 0 10px;
}

.feature-card p {
  color: #7b8798;
  font-size: 13px;
  line-height: 1.7;
  min-height: 88px;
}

.feature-card a {
  color: #1769ff;
  text-decoration: none;
  font-size: 13px;
  font-weight: 700;
}


/* ================= HOW IT WORKS ================= */

.how-section {
  background: #f8fbff;
  max-width: none;
  width: 100%;
  padding-left: max(4%, calc((100% - 1180px) / 2));
  padding-right: max(4%, calc((100% - 1180px) / 2));
}

.steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.step {
  display: flex;
  gap: 18px;
  max-width: 290px;
}

.step-number {
  color: #1769ff;
  font-size: 28px;
  font-weight: 800;
}

.step h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.step p {
  margin: 0;
  color: #7b8798;
  font-size: 13px;
  line-height: 1.6;
}

.step-line {
  height: 1px;
  width: 90px;
  background: #dce5f1;
}


/* ================= CTA ================= */

.cta-section {
  width: min(1100px, 90%);
  margin: 90px auto;
  background: linear-gradient(120deg, #1769ff, #4c8dff);
  border-radius: 25px;
  padding: 65px 30px;
  text-align: center;
  color: white;
  box-shadow: 0 25px 50px rgba(23, 105, 255, 0.2);
}

.cta-icon {
  font-size: 35px;
  margin-bottom: 12px;
}

.cta-section h2 {
  font-size: 38px;
  margin: 0 0 12px;
}

.cta-section p {
  opacity: 0.9;
  margin-bottom: 28px;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.cta-primary,
.cta-secondary {
  padding: 13px 23px;
  border-radius: 9px;
  text-decoration: none;
  font-weight: 700;
  font-size: 14px;
}

.cta-primary {
  background: white;
  color: #1769ff;
}

.cta-secondary {
  border: 1px solid rgba(255,255,255,0.5);
  color: white;
}


/* ================= FOOTER ================= */

footer {
  border-top: 1px solid #e8edf4;
  padding: 35px 0;
}

.footer-container {
  width: min(1180px, 92%);
  margin: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-brand p {
  color: #98a2b3;
  font-size: 12px;
}

.footer-links {
  display: flex;
  gap: 25px;
}

.footer-links a {
  color: #667085;
  text-decoration: none;
  font-size: 12px;
}

.copyright {
  color: #98a2b3;
  font-size: 11px;
}


/* ================= RESPONSIVE ================= */

@media (max-width: 950px) {

  .nav-links {
    display: none;
  }

  .hero-container {
    grid-template-columns: 1fr;
  }

  .hero-content {
    text-align: center;
  }

  .hero-description {
    margin-left: auto;
    margin-right: auto;
  }

  .search-box {
    margin: auto;
  }

  .popular-searches {
    justify-content: center;
  }

  .hero-visual {
    max-width: 550px;
    width: 100%;
    margin: auto;
  }

  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .steps {
    flex-direction: column;
    gap: 30px;
    align-items: flex-start;
  }

  .step-line {
    display: none;
  }

  .footer-container {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
}


@media (max-width: 650px) {

  .hero {
    padding: 60px 0;
  }

  .hero-content h1 {
    font-size: 42px;
  }

  .search-box {
    flex-direction: column;
    align-items: stretch;
  }

  .search-divider {
    width: 100%;
    height: 1px;
  }

  .search-btn {
    width: 100%;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 25px;
  }

  .stat {
    border: none;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .profile-card {
    width: 90%;
  }

  .card-one {
    left: -5px;
  }

  .card-two {
    right: -5px;
  }

  .cta-section h2 {
    font-size: 30px;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .cta-primary,
  .cta-secondary {
    display: block;
  }

  .footer-links {
    flex-wrap: wrap;
    justify-content: center;
  }
}

</style>