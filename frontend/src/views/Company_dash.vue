<template>
  <div class="container mt-4 mb-5">
    <!-- Header with Profile Icon -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Company Dashboard</h2>
      <button class="btn btn-outline-primary rounded-circle" @click="openProfileModal" title="Profile">
        🏢
      </button>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else>
      <div class="alert alert-info border-0 shadow-sm">
        Welcome{{ stats.email ? ', ' + stats.email : '' }}! Manage your job postings and applicants below.
      </div>
      
      <!-- Approval Status Banner -->
      <div v-if="stats.is_approved === false" class="alert alert-warning border-warning shadow-sm mt-3 d-flex align-items-center">
        <div class="me-3 fs-3">⏳</div>
        <div>
          <h5 class="alert-heading mb-1">Pending Approval</h5>
          <p class="mb-0">Your company account is currently waiting for admin approval. You will be able to post jobs once approved.</p>
        </div>
      </div>
      
      <!-- Approved Content -->
      <div v-else-if="stats.is_approved === true">
        <div class="d-flex justify-content-between align-items-center mt-5 mb-3">
          <h4>Your Job Postings</h4>
          <div>
            <button class="btn btn-outline-secondary me-2" @click="requestCSVExport" :disabled="exporting">
              <span v-if="exporting" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ exporting ? 'Exporting...' : '📄 Export CSV' }}
            </button>
            <button class="btn btn-success" @click="openPostJobModal">
              + Post New Job
            </button>
          </div>
        </div>

        <div v-if="jobs.length === 0" class="text-center text-muted my-4">
          <p>No jobs posted yet.</p>
        </div>

        <div class="card mb-4 shadow-sm" v-for="job in jobs" :key="job.id">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <h5 class="card-title text-primary">{{ job.title }}</h5>
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" :id="'jobStatus' + job.id" :checked="job.is_active" @change="toggleJobStatus(job)">
                <label class="form-check-label" :for="'jobStatus' + job.id">{{ job.is_active ? 'Active' : 'Closed' }}</label>
              </div>
            </div>
            
            <p class="card-text text-muted mb-2">
              <strong>Location:</strong> {{ job.location || 'N/A' }} | 
              <strong>Salary:</strong> {{ job.salary || 'N/A' }} | 
              <strong>Deadline:</strong> {{ job.deadline ? new Date(job.deadline).toLocaleDateString() : 'N/A' }}
            </p>
            <button class="btn btn-sm btn-outline-primary mt-2" @click="viewApplications(job)">
              View Applicants
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Post Job Modal -->
    <div class="modal" tabindex="-1" :class="{ 'd-block': showPostJobModal }" :style="{ backgroundColor: showPostJobModal ? 'rgba(0,0,0,0.5)' : '' }">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-light">
            <h5 class="modal-title">Post a New Job</h5>
            <button type="button" class="btn-close" @click="closePostJobModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitJob">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Job Title <span class="text-danger">*</span></label>
                  <input type="text" class="form-control" v-model="newJob.title" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Location</label>
                  <input type="text" class="form-control" v-model="newJob.location">
                </div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Description <span class="text-danger">*</span></label>
                <textarea class="form-control" rows="3" v-model="newJob.description" required></textarea>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Skills Required</label>
                  <input type="text" class="form-control" v-model="newJob.skills" placeholder="e.g. Python, SQL">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Experience</label>
                  <input type="text" class="form-control" v-model="newJob.experience" placeholder="e.g. 2+ years">
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Salary</label>
                  <input type="text" class="form-control" v-model="newJob.salary" placeholder="e.g. $80k - $100k">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Deadline <span class="text-danger">*</span></label>
                  <input type="datetime-local" class="form-control" v-model="newJob.deadline" required>
                </div>
              </div>

              <div class="mb-3">
                <label class="form-label">Benefits</label>
                <textarea class="form-control" rows="2" v-model="newJob.benefits"></textarea>
              </div>
              
              <div class="d-grid mt-4">
                <button type="submit" class="btn btn-success" :disabled="saving">
                   <span v-if="saving" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                   Post Job
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Applicants Modal -->
    <div class="modal" tabindex="-1" :class="{ 'd-block': showApplicantsModal }" :style="{ backgroundColor: showApplicantsModal ? 'rgba(0,0,0,0.5)' : '' }">
      <div class="modal-dialog modal-xl modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header bg-light">
            <h5 class="modal-title">Applicants for: <span class="text-primary">{{ selectedJob?.title }}</span></h5>
            <button type="button" class="btn-close" @click="closeApplicantsModal"></button>
          </div>
          <div class="modal-body bg-light">
            
            <div v-if="applications.length === 0" class="text-center py-4">
              <p class="text-muted mb-0">No applications received yet for this position.</p>
            </div>
            
            <div class="card mb-3 border-0 shadow-sm" v-for="app in applications" :key="app.id">
              <div class="card-body">
                <div class="row">
                  <div class="col-md-3 border-end">
                    <h6 class="mb-1 text-primary">{{ app.student_name }}</h6>
                    <small class="text-muted d-block mb-2">{{ app.student_email }}</small>
                    <p class="mb-1" style="font-size: 0.9em;"><strong>CGPA:</strong> {{ app.student_cgpa || 'N/A' }}</p>
                    <p class="mb-2" style="font-size: 0.9em;"><strong>Skills:</strong> {{ app.student_skills || 'None' }}</p>
                    <a v-if="app.student_resume" :href="app.student_resume" target="_blank" class="btn btn-outline-info btn-sm">View Resume</a>
                  </div>
                  
                  <div class="col-md-9">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                      <div>
                        Status: 
                        <span class="badge" :class="{
                          'bg-secondary': app.status === 'Applied',
                          'bg-primary': app.status === 'Shortlisted',
                          'bg-success': app.status === 'Selected' || app.status === 'Placed',
                          'bg-danger': app.status === 'Rejected',
                          'bg-info': app.status === 'Interview Scheduled' || app.status === 'Offer'
                        }">{{ app.status }}</span>
                      </div>
                      <small class="text-muted">Applied: {{ new Date(app.applied_at).toLocaleDateString() }}</small>
                    </div>

                    <form @submit.prevent="updateApplication(app)">
                      <div class="row align-items-end">
                        <div class="col-md-4 mb-2">
                          <label class="form-label" style="font-size: 0.85em;">Action / Status</label>
                          <select class="form-select form-select-sm" v-model="app.status">
                            <option value="Applied">Applied</option>
                            <option value="Shortlisted">Shortlisted</option>
                            <option value="Interview Scheduled">Interview</option>
                            <option value="Selected">Selected</option>
                            <option value="Offer">Offer Sent</option>
                            <option value="Placed">Placed</option>
                            <option value="Rejected">Rejected</option>
                          </select>
                        </div>
                        <div class="col-md-4 mb-2" v-if="app.status === 'Interview Scheduled'">
                          <label class="form-label" style="font-size: 0.85em;">Interview Date & Time</label>
                          <input type="datetime-local" class="form-control form-control-sm" v-model="app.interview_date">
                        </div>
                        <div class="col-md-12 mb-2">
                          <label class="form-label" style="font-size: 0.85em;">Feedback / Remarks (Sent to Applicant)</label>
                          <input type="text" class="form-control form-control-sm" v-model="app.feedback" placeholder="e.g. Great technical skills!">
                        </div>
                        <div class="col-md-12 mt-2 text-end">
                           <button type="submit" class="btn btn-sm btn-primary px-4">Save Update</button>
                        </div>
                      </div>
                    </form>

                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Edit Profile Modal Form (Existing logic) -->
    <div class="modal" tabindex="-1" :class="{ 'd-block': showModal }" :style="{ backgroundColor: showModal ? 'rgba(0,0,0,0.5)' : '' }">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Complete Company Profile</h5>
            <button type="button" class="btn-close" @click="closeProfileModal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitProfile">
              <div class="mb-3">
                <label for="companyName" class="form-label">Company Name <span class="text-danger">*</span></label>
                <input type="text" class="form-control" id="companyName" v-model="profile.company_name" required placeholder="E.g., Tech Corp" />
              </div>

              <div class="mb-3">
                <label for="industry" class="form-label">Industry</label>
                <input type="text" class="form-control" id="industry" v-model="profile.industry" placeholder="E.g., Software, Finance, Healthcare" />
              </div>

              <div class="mb-3">
                <label for="location" class="form-label">Location</label>
                <input type="text" class="form-control" id="location" v-model="profile.location" placeholder="E.g., New York, NY" />
              </div>

              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" rows="4" v-model="profile.description" placeholder="Short description of your company..."></textarea>
              </div>

              <div class="d-grid gap-2">
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const stats = ref({})
const loading = ref(true)

const showModal = ref(false)
const saving = ref(false)
const profile = ref({
  company_name: '',
  industry: '',
  location: '',
  description: ''
})

const jobs = ref([])
const showPostJobModal = ref(false)
const newJob = ref({
  title: '',
  description: '',
  skills: '',
  experience: '',
  salary: '',
  benefits: '',
  location: '',
  deadline: ''
})

const applications = ref([])
const exporting = ref(false)
const showApplicantsModal = ref(false)
const selectedJob = ref(null)

const fetchStats = async () => {
  loading.value = true

  try {
    const token = localStorage.getItem("token")
    if (!token) {
      router.push("/login")
      return
    }

    const res = await fetch("http://127.0.0.1:5000/api/company_dash", {
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

    if (data.is_approved) {
      await fetchJobs()
    }

  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const fetchJobs = async () => {
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/company/jobs", {
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
  } catch (err) {
    console.error("Failed to load jobs", err)
  }
}

const toggleJobStatus = async (job) => {
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const newStatus = !job.is_active
    const res = await fetch(`http://127.0.0.1:5000/api/company/jobs/${job.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      },
      body: JSON.stringify({ is_active: newStatus })
    })

    if (res.ok) {
      const newToken = res.headers.get("Authentication-Token")
      if (newToken) localStorage.setItem("token", newToken)
      job.is_active = newStatus
    } else {
      alert("Failed to update status")
    }
  } catch (e) {
    console.error(e)
  }
}

const openPostJobModal = () => {
  newJob.value = {
    title: '', description: '', skills: '', experience: '', salary: '', benefits: '', location: '', deadline: ''
  }
  showPostJobModal.value = true
}

const closePostJobModal = () => showPostJobModal.value = false

const submitJob = async () => {
  saving.value = true
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    // Convert local datetime to ISO
    const localDate = new Date(newJob.value.deadline)
    const payload = { ...newJob.value, deadline: localDate.toISOString() }

    const res = await callApi("/company/jobs", "POST", payload)
    if (res) {
      closePostJobModal()
      await fetchJobs()
    }
  } catch (err) {
    console.error(err)
    alert("Failed to post job: " + (err.message || 'Unknown error'))
  } finally {
    saving.value = false
  }
}

const viewApplications = async (job) => {
  selectedJob.value = job
  showApplicantsModal.value = true
  applications.value = []
  
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch(`http://127.0.0.1:5000/api/company/jobs/${job.id}/applications`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      }
    })

    if (res.ok) {
      const newToken = res.headers.get("Authentication-Token")
      if (newToken) localStorage.setItem("token", newToken)
      
      const rawApps = await res.json()
      // ensure interview_date maps back to input type=datetime-local format
      applications.value = rawApps.map(app => {
        if (app.interview_date) {
           const d = new Date(app.interview_date)
           // quick format hack for datetime-local
           d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
           app.interview_date = d.toISOString().slice(0,16)
        }
        return app
      })
    }
  } catch (err) {
    console.error(err)
  }
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

const closeApplicantsModal = () => showApplicantsModal.value = false

const updateApplication = async (app) => {
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const payload = {
      status: app.status,
      feedback: app.feedback,
    }
    if (app.status === 'Interview Scheduled' && app.interview_date) {
       payload.interview_date = new Date(app.interview_date).toISOString()
    } else {
       payload.interview_date = '' // empty clears it or handles parsing logic
    }

    const res = await fetch(`http://127.0.0.1:5000/api/company/applications/${app.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": token
      },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      const newToken = res.headers.get("Authentication-Token")
      if (newToken) localStorage.setItem("token", newToken)
      alert("Application updated!")
    } else {
      const err = await res.json()
      alert("Failed to update application: " + (err.message || 'Unknown error'))
    }
  } catch (err) {
    console.error(err)
  }
}

// Profile Logic
const openProfileModal = async () => {
  showModal.value = true
  try {
    const token = localStorage.getItem("token")
    if (!token) return

    const res = await fetch("http://127.0.0.1:5000/api/company_profile", {
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
        profile.value.company_name = data.company_name || ''
        profile.value.industry = data.industry || ''
        profile.value.location = data.location || ''
        profile.value.description = data.description || ''
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

    const res = await fetch("http://127.0.0.1:5000/api/company_profile", {
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

    fetchStats()

  } catch (err) {
    console.error(err)
    alert("Error saving profile")
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
