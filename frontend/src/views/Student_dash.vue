<template>
  <div class="container mt-4 mb-5">
    <!-- Header with Profile Icon -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Student Dashboard</h2>
      <button class="btn btn-outline-primary rounded-circle" @click="openProfileModal" title="Profile">
        👤
      </button>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <div class="alert alert-info border-0 shadow-sm mb-4">
        Welcome{{ stats.email ? ', ' + stats.email : '' }}! Discover and apply for your dream jobs below. Click the profile icon to keep your resume updated!
      </div>

      <!-- Navigation Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'jobs' }" href="#" @click.prevent="activeTab = 'jobs'">Job Postings</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'applications' }" href="#" @click.prevent="activeTab = 'applications'">My Applications</a>
        </li>
      </ul>

      <!-- Jobs Posting Tab -->
      <div v-if="activeTab === 'jobs'">
        
        <!-- Search bar -->
        <div class="input-group mb-4 shadow-sm">
          <span class="input-group-text bg-white border-end-0">🔍</span>
          <input type="text" class="form-control border-start-0" v-model="searchQuery" placeholder="Search by company, position, or skills...">
        </div>

        <div v-if="filteredJobs.length === 0" class="text-center text-muted my-5">
          <p>No jobs found matching your search.</p>
        </div>

        <div class="row">
          <div class="col-md-6 mb-4" v-for="job in filteredJobs" :key="job.id">
            <div class="card h-100 shadow-sm border-0 job-card">
              <div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h5 class="card-title text-primary fw-bold mb-0">{{ job.title }}</h5>
                  <span class="badge bg-light text-dark border">{{ job.company_name }}</span>
                </div>
                
                <p class="text-muted small mb-3">
                  <span class="me-3" v-if="job.location">📍 {{ job.location }}</span>
                  <span class="me-3" v-if="job.salary">💰 {{ job.salary }}</span>
                  <span class="text-danger" v-if="job.deadline">⏰ {{ new Date(job.deadline).toLocaleDateString() }}</span>
                </p>

                <p class="card-text mb-3 flex-grow-1">{{ job.description }}</p>

                <div class="mb-3">
                  <div v-if="job.skills" class="mb-1"><small><strong>Skills:</strong> {{ job.skills }}</small></div>
                  <div v-if="job.experience" class="mb-1"><small><strong>Experience:</strong> {{ job.experience }}</small></div>
                  <div v-if="job.benefits" class="mb-1"><small><strong>Benefits:</strong> {{ job.benefits }}</small></div>
                </div>

                <button class="btn btn-outline-success mt-auto" @click="applyForJob(job.id)">
                  Apply Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My Applications Tab -->
      <div v-if="activeTab === 'applications'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4 class="mb-0">My Applications</h4>
          <button class="btn btn-sm btn-outline-secondary" @click="requestCSVExport" :disabled="exporting">
            <span v-if="exporting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            {{ exporting ? 'Exporting...' : '📄 Export CSV' }}
          </button>
        </div>

        <div v-if="applications.length === 0" class="text-center text-muted my-5">
           <p>You haven't applied for any jobs yet.</p>
        </div>

        <div class="card mb-3 shadow-sm border-0" v-for="app in applications" :key="app.id">
          <div class="card-body">
            <div class="row align-items-center">
              <div class="col-md-4 border-end">
                <h5 class="text-primary mb-1">{{ app.job_title }}</h5>
                <p class="text-muted mb-0 small"><i class="bi bi-building"></i> {{ app.company_name }}</p>
                <small class="text-muted">Applied: {{ new Date(app.applied_at).toLocaleDateString() }}</small>
              </div>
              
              <div class="col-md-4 border-end px-4">
                <strong>Status:</strong> 
                <span class="badge ms-2" :class="{
                  'bg-secondary': app.status === 'Applied',
                  'bg-primary': app.status === 'Shortlisted',
                  'bg-success': app.status === 'Selected' || app.status === 'Placed',
                  'bg-danger': app.status === 'Rejected',
                  'bg-info': app.status === 'Interview Scheduled' || app.status === 'Offer'
                }">{{ app.status }}</span>

                <div v-if="app.interview_date" class="mt-2 text-info small">
                   <strong>Interview:</strong> {{ new Date(app.interview_date).toLocaleString() }}
                </div>
              </div>

              <div class="col-md-4 px-4 text-center">
                <div v-if="app.feedback" class="small fst-italic text-muted mb-2">
                  "{{ app.feedback }}"
                </div>
                
                <button v-if="app.status === 'Selected' || app.status === 'Offer' || app.status === 'Placed'" class="btn btn-sm btn-success w-100 mt-2 text-white" @click="downloadOfferLetter(app)">
                  📥 Download Offer Letter
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>


    <!-- Profile Modal Form -->
    <div class="modal" tabindex="-1" :class="{ 'd-block': showModal }" :style="{ backgroundColor: showModal ? 'rgba(0,0,0,0.5)' : '' }">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Complete Profile</h5>
            <button type="button" class="btn-close" @click="closeProfileModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitProfile">
              <div class="mb-3">
                <label for="fullName" class="form-label">Full Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control" id="fullName" v-model="profile.full_name" required placeholder="John Doe" />
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="education" class="form-label">Education</label>
                  <input type="text" class="form-control" id="education" v-model="profile.education" placeholder="E.g., B.Tech in CS" />
                </div>

                <div class="col-md-6 mb-3">
                  <label for="cgpa" class="form-label">CGPA</label>
                  <input type="number" step="0.01" max="10" min="0" class="form-control" id="cgpa" v-model="profile.cgpa" placeholder="E.g., 8.5" />
                </div>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="skills" class="form-label">Skills</label>
                  <input type="text" class="form-control" id="skills" v-model="profile.skills" placeholder="E.g., Python, Vue" />
                </div>

                <div class="col-md-6 mb-3">
                  <label for="experience" class="form-label">Experience</label>
                  <input type="text" class="form-control" id="experience" v-model="profile.experience" placeholder="E.g., 1 Year Internship" />
                </div>
              </div>

              <div class="mb-3">
                <label for="resume" class="form-label">Resume Link</label>
                <input type="text" class="form-control" id="resume" v-model="profile.resume_filename" placeholder="Link to your resume (e.g. Google Drive link)" />
              </div>

              <div class="d-grid gap-2 mt-4">
                <button type="submit" class="btn btn-success" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  Save Profile
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const stats = ref({})
const loading = ref(true)

const activeTab = ref('jobs')

// Profile State
const showModal = ref(false)
const saving = ref(false)
const profile = ref({
  full_name: '',
  education: '',
  cgpa: '',
  skills: '',
  experience: '',
  resume_filename: ''
})

// Feature states
const jobs = ref([])
const applications = ref([])
const searchQuery = ref('')
const exporting = ref(false)

// Filter jobs based on search query
const filteredJobs = computed(() => {
  const query = searchQuery.value.toLowerCase()
  if (!query) return jobs.value
  
  return jobs.value.filter(job => {
    return (job.title && job.title.toLowerCase().includes(query)) ||
           (job.company_name && job.company_name.toLowerCase().includes(query)) ||
           (job.skills && job.skills.toLowerCase().includes(query))
  })
})

const fetchStats = async () => {
  try {
    const token = localStorage.getItem("token")

    if (!token) {
      router.push("/login")
      return
    }

    const res = await fetch("http://127.0.0.1:5000/api/student_dash", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    if (res.status === 401) {
      localStorage.removeItem("token")
      router.push("/login")
      return
    }

    const newToken = res.headers.get("Authentication-Token")
    if (newToken) {
      localStorage.setItem("token", newToken)
    }

    const data = await res.json()
    stats.value = data

  } catch (err) {
    console.error(err)
  }
}

const fetchJobs = async () => {
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/student/jobs", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    if (res.ok) {
        const newToken = res.headers.get("Authentication-Token")
        if (newToken) localStorage.setItem("token", newToken)
        jobs.value = await res.json()
    }
  } catch (e) {
    console.error(e)
  }
}

const fetchApplications = async () => {
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/student/applications", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    if (res.ok) {
        const newToken = res.headers.get("Authentication-Token")
        if (newToken) localStorage.setItem("token", newToken)
        applications.value = await res.json()
    } else {
        // Not completed profile perhaps
    }
  } catch (e) {
    console.error(e)
  }
}

const applyForJob = async (jobId) => {
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch(`http://127.0.0.1:5000/api/student/jobs/${jobId}/apply`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    const data = await res.json()
    
    if (res.ok) {
      const newToken = res.headers.get("Authentication-Token")
      if (newToken) localStorage.setItem("token", newToken)
      
      alert(data.message)
      await fetchApplications()
      activeTab.value = 'applications'
    } else {
      alert("Error: " + data.message)
      if (data.message.includes("complete your profile")) {
          openProfileModal()
      }
    }
  } catch (e) {
    console.error(e)
  }
}

const downloadOfferLetter = (app) => {
  // A mock download feature mapping the placement context
  const content = `OFFER LETTER / PLACEMENT CONFIRMATION\n\nCongratulations!\nYou have been Selected for the position of ${app.job_title} at ${app.company_name}.\n\nFeedback: ${app.feedback || 'None'}\n\nWe look forward to welcoming you to the team.`
  const blob = new Blob([content], { type: "text/plain" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = `Offer_Letter_${app.company_name.replace(/\s+/g, '_')}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const requestCSVExport = async () => {
  exporting.value = true
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/export", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    if (!res.ok) {
      const err = await res.json()
      alert("Export failed: " + (err.error || err.message))
      exporting.value = false
      return
    }

    const data = await res.json()
    const taskId = data.task_id
    
    // Poll for status
    const pollInterval = setInterval(async () => {
      const statusRes = await fetch(`http://127.0.0.1:5000/api/export/status/${taskId}`, {
        headers: { "Authentication-Token": token }
      })
      const statusData = await statusRes.json()
      
      if (statusData.state === 'SUCCESS') {
        clearInterval(pollInterval)
        exporting.value = false
        alert("Batch job is complete! Your export is ready.")
        
        // Trigger download via fetch with auth header
        try {
          const dlRes = await fetch(`http://127.0.0.1:5000/api/export/download/${statusData.result.file_name}`, {
            headers: { "Authentication-Token": token }
          })
          if (!dlRes.ok) throw new Error("File not found")
          const blob = await dlRes.blob()
          const url = URL.createObjectURL(blob)
          const a = document.createElement("a")
          a.style.display = "none"
          a.href = url
          a.download = statusData.result.file_name
          document.body.appendChild(a)
          a.click()
          URL.revokeObjectURL(url)
          document.body.removeChild(a)
        } catch (e) {
             alert('Download failed: ' + e.message)
        }
        
      } else if (statusData.state === 'FAILURE') {
        clearInterval(pollInterval)
        exporting.value = false
        alert("Export failed: " + statusData.status)
      }
    }, 2000)

  } catch (err) {
    console.error(err)
    alert("Error requesting export")
    exporting.value = false
  }
}

// Profile Modal API
const openProfileModal = async () => {
  showModal.value = true
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/student_profile", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    if (res.ok) {
      const newToken = res.headers.get("Authentication-Token")
      if (newToken) localStorage.setItem("token", newToken)
      
      const data = await res.json()
      if (data && Object.keys(data).length > 0) {
        profile.value.full_name = data.full_name || ''
        profile.value.education = data.education || ''
        profile.value.cgpa = data.cgpa || ''
        profile.value.skills = data.skills || ''
        profile.value.experience = data.experience || ''
        profile.value.resume_filename = data.resume_filename || ''
      }
    }
  } catch (err) {
    console.error("Failed to load profile", err)
  }
}

const closeProfileModal = () => {
  showModal.value = false
}

const submitProfile = async () => {
  saving.value = true
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/student_profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      },
      body: JSON.stringify(profile.value)
    })

    if (!res.ok) {
      const errorData = await res.json()
      alert("Failed to save profile: " + (errorData.message || 'Unknown error'))
      return
    }

    const newToken = res.headers.get("Authentication-Token")
    if (newToken) localStorage.setItem("token", newToken)

    alert("Profile saved successfully!")
    showModal.value = false
    
    // Refresh apps as they might have been blocked
    fetchApplications()

  } catch (err) {
    console.error(err)
    alert("Error saving profile")
  } finally {
    saving.value = false
  }
}

const loadAllData = async () => {
  loading.value = true
  await fetchStats()
  await fetchJobs()
  await fetchApplications()
  loading.value = false
}

onMounted(() => {
  loadAllData()
})
</script>

<style scoped>
.job-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.job-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 .25rem .75rem rgba(0,0,0,.1) !important;
}
.nav-tabs .nav-link {
  color: #495057;
  font-weight: 500;
}
.nav-tabs .nav-link.active {
  color: #0d6efd;
  font-weight: bold;
}
</style>