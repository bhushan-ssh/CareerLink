<template>
  <div class="container mt-4 mb-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-0">Admin Dashboard</h2>
      <div v-if="!loading" class="text-muted small">Welcome, Admin</div>
    </div>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="row mb-5">
        <div class="col-md-3 mb-3">
          <div class="card text-center bg-primary text-white shadow-sm border-0 h-100">
            <div class="card-body py-4">
              <h6 class="card-subtitle mb-2 small opacity-75">Students</h6>
              <h2 class="card-title fw-bold">{{ stats.total_students || 0 }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card text-center bg-success text-white shadow-sm border-0 h-100">
            <div class="card-body py-4">
              <h6 class="card-subtitle mb-2 small opacity-75">Companies</h6>
              <h2 class="card-title fw-bold">{{ stats.total_companies || 0 }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card text-center bg-info text-white shadow-sm border-0 h-100">
            <div class="card-body py-4">
              <h6 class="card-subtitle mb-2 small opacity-75">Job Postings</h6>
              <h2 class="card-title fw-bold">{{ stats.total_jobs || 0 }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card text-center bg-warning text-white shadow-sm border-0 h-100">
            <div class="card-body py-4">
              <h6 class="card-subtitle mb-2 small opacity-75">Applications</h6>
              <h2 class="card-title fw-bold">{{ stats.total_applications || 0 }}</h2>
            </div>
          </div>
        </div>
      </div>

      <!-- Tab Navigation -->
      <ul class="nav nav-pills nav-fill mb-4 bg-light p-2 rounded shadow-sm">
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'companies' }" @click="setTab('companies')">🏢 Companies</button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'students' }" @click="setTab('students')">🎓 Students</button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'jobs' }" @click="setTab('jobs')">💼 Jobs</button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'applications' }" @click="setTab('applications')">📄 Apps</button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'placements' }" @click="setTab('placements')">🏆 Placed</button>
        </li>
      </ul>

      <!-- Companies Tab -->
      <div v-show="activeTab === 'companies'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4>Manage Companies</h4>
          <div class="d-flex gap-2">
            <input type="text" v-model="filters.companySearch" class="form-control form-control-sm" placeholder="Search name..." @input="debouncedFetchCompanies">
            <input type="text" v-model="filters.industrySearch" class="form-control form-control-sm" placeholder="Industry..." @input="debouncedFetchCompanies">
          </div>
        </div>
        <div class="table-responsive bg-white shadow-sm rounded">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Company</th>
                <th>Industry</th>
                <th>Status</th>
                <th>Account</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in companies" :key="c.id">
                <td>
                  <div class="fw-bold">{{ c.company_name }}</div>
                  <small class="text-muted">{{ c.email }}</small>
                </td>
                <td>{{ c.industry || 'N/A' }}</td>
                <td>
                  <span v-if="c.is_approved" class="badge bg-success">Approved</span>
                  <span v-else class="badge bg-warning text-dark">Pending</span>
                </td>
                <td>
                  <span v-if="c.is_active" class="badge bg-primary">Active</span>
                  <span v-else class="badge bg-danger">Deactivated</span>
                </td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button v-if="!c.is_approved" class="btn btn-outline-success" @click="updateCompany(c.id, 'approve')">Approve</button>
                    <button v-else class="btn btn-outline-warning" @click="updateCompany(c.id, 'revoke')">Revoke</button>
                    
                    <button v-if="c.is_active" class="btn btn-outline-danger" @click="updateCompany(c.id, 'deactivate')">Deactivate</button>
                    <button v-else class="btn btn-outline-primary" @click="updateCompany(c.id, 'activate')">Activate</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Students Tab -->
      <div v-show="activeTab === 'students'">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h4>Manage Students</h4>
          <input type="text" v-model="filters.studentSearch" class="form-control form-control-sm w-25" placeholder="Search name/email..." @input="debouncedFetchStudents">
        </div>
        <div class="table-responsive bg-white shadow-sm rounded">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Student</th>
                <th>Education</th>
                <th>CGPA</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in students" :key="s.id">
                <td>
                  <div class="fw-bold">{{ s.full_name }}</div>
                  <small class="text-muted">{{ s.email }}</small>
                </td>
                <td>{{ s.education }}</td>
                <td>{{ s.cgpa || 'N/A' }}</td>
                <td>
                  <span v-if="s.is_active" class="badge bg-primary">Active</span>
                  <span v-else class="badge bg-danger">Deactivated</span>
                </td>
                <td>
                  <button v-if="s.is_active" class="btn btn-sm btn-outline-danger" @click="updateStudent(s.id, 'deactivate')">Deactivate</button>
                  <button v-else class="btn btn-sm btn-outline-primary" @click="updateStudent(s.id, 'activate')">Activate</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Jobs Tab -->
      <div v-show="activeTab === 'jobs'">
        <h4>Job Postings</h4>
        <div class="table-responsive bg-white shadow-sm rounded mt-3">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Job Title</th>
                <th>Company</th>
                <th>Status</th>
                <th>Deadline</th>
                <th>Apps</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="j in jobs" :key="j.id">
                <td class="fw-bold">{{ j.title }}</td>
                <td>{{ j.company_name }}</td>
                <td>
                  <span v-if="j.is_active" class="badge bg-success">Active</span>
                  <span v-else class="badge bg-secondary">Closed</span>
                </td>
                <td>{{ new Date(j.deadline).toLocaleDateString() }}</td>
                <td><span class="badge bg-light text-dark border">{{ j.app_count }}</span></td>
                <td>
                  <div class="btn-group btn-group-sm">
                    <button v-if="j.is_active" class="btn btn-outline-warning" @click="updateJob(j.id, 'deactivate')">Close</button>
                    <button v-else class="btn btn-outline-success" @click="updateJob(j.id, 'activate')">Open</button>
                    <button class="btn btn-outline-danger" @click="updateJob(j.id, 'delete')">Remove</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Applications Tab -->
      <div v-show="activeTab === 'applications'">
        <h4>Job Applications History</h4>
        <div class="table-responsive bg-white shadow-sm rounded mt-3">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Student</th>
                <th>Job & Company</th>
                <th>Date Applied</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in applications" :key="a.id">
                <td><div class="fw-bold">{{ a.student_name }}</div></td>
                <td>
                  <div class="fw-bold">{{ a.job_title }}</div>
                  <small class="text-muted">{{ a.company_name }}</small>
                </td>
                <td>{{ new Date(a.applied_at).toLocaleDateString() }}</td>
                <td>
                  <span class="badge" 
                    :class="{
                      'bg-secondary': a.status === 'Applied',
                      'bg-primary': a.status === 'Shortlisted',
                      'bg-success': a.status === 'Selected' || a.status === 'Placed',
                      'bg-danger': a.status === 'Rejected',
                      'bg-info': a.status === 'Interview Scheduled' || a.status === 'Offer'
                    }">{{ a.status }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Placements Tab -->
      <div v-show="activeTab === 'placements'">
        <h4>Successful Placements History</h4>
        <div class="table-responsive bg-white shadow-sm rounded mt-3">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th>Student</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>Salary</th>
                <th>Joining Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in placements" :key="p.id">
                <td><div class="fw-bold text-success">{{ p.student_name }}</div></td>
                <td>{{ p.company_name }}</td>
                <td>{{ p.job_title }}</td>
                <td>{{ p.salary || 'N/A' }}</td>
                <td>{{ p.joining_date ? new Date(p.joining_date).toLocaleDateString() : 'TBD' }}</td>
              </tr>
              <tr v-if="placements.length === 0">
                <td colspan="5" class="text-center text-muted py-4">No placements recorded yet.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(true)
const activeTab = ref('companies')
const stats = ref({})

const companies = ref([])
const students = ref([])
const jobs = ref([])
const applications = ref([])
const placements = ref([])

const filters = reactive({
  companySearch: '',
  industrySearch: '',
  studentSearch: ''
})

const fetchStats = async () => {
  try {
    const res = await callApi('/admin/stats')
    if (res) stats.value = res
  } catch (e) {
    console.error(e)
  }
}

const fetchCompanies = async () => {
  try {
    const query = `?search=${filters.companySearch}&industry=${filters.industrySearch}`
    const res = await callApi('/admin/companies' + query)
    if (res) companies.value = res
  } catch (e) {
    console.error(e)
  }
}

const fetchStudents = async () => {
  try {
    const query = `?search=${filters.studentSearch}`
    const res = await callApi('/admin/students' + query)
    if (res) students.value = res
  } catch (e) {
    console.error(e)
  }
}

const fetchJobs = async () => {
  try {
    const res = await callApi('/admin/jobs')
    if (res) jobs.value = res
  } catch (e) {
    console.error(e)
  }
}

const fetchApplications = async () => {
  try {
    const res = await callApi('/admin/applications')
    if (res) applications.value = res
  } catch (e) {
    console.error(e)
  }
}

const fetchPlacements = async () => {
  try {
    const res = await callApi('/admin/placements')
    if (res) placements.value = res
  } catch (e) {
    console.error(e)
  }
}

const updateCompany = async (id, action) => {
  const res = await callApi('/admin/companies', 'POST', { company_id: id, action })
  if (res) fetchCompanies()
}

const updateStudent = async (id, action) => {
  const res = await callApi('/admin/students', 'POST', { student_id: id, action })
  if (res) fetchStudents()
}

const updateJob = async (id, action) => {
  if (action === 'delete') {
    if (!confirm("Are you sure you want to remove this job posting?")) return
  }
  const res = await callApi('/admin/jobs', 'POST', { job_id: id, action })
  if (res) fetchJobs()
}

const setTab = (tab) => {
  activeTab.value = tab
  if (tab === 'companies') fetchCompanies()
  if (tab === 'students') fetchStudents()
  if (tab === 'jobs') fetchJobs()
  if (tab === 'applications') fetchApplications()
  if (tab === 'placements') fetchPlacements()
}

// Global API Caller with Token handling
const callApi = async (path, method = 'GET', body = null) => {
  const token = localStorage.getItem("token")
  if (!token) {
    router.push("/login")
    return null
  }

  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authentication-Token": token
    }
  }
  if (body) options.body = JSON.stringify(body)

  try {
    const res = await fetch(`http://127.0.0.1:5000/api${path}`, options)
    if (res.status === 401) {
      localStorage.removeItem("token")
      router.push("/login")
      return null
    }

    const newToken = res.headers.get("Authentication-Token")
    if (newToken) localStorage.setItem("token", newToken)

    return await res.json()
  } catch (err) {
    console.error("API Error at " + path, err)
    return null
  }
}

let timeout = null
const debouncedFetchCompanies = () => {
  clearTimeout(timeout)
  timeout = setTimeout(fetchCompanies, 300)
}
const debouncedFetchStudents = () => {
  clearTimeout(timeout)
  timeout = setTimeout(fetchStudents, 300)
}

onMounted(async () => {
  loading.value = true
  await fetchStats()
  await fetchCompanies()
  loading.value = false
})
</script>

<style scoped>
.nav-pills .nav-link {
  color: #495057;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
}
.nav-pills .nav-link.active {
  background-color: #0d6efd;
  color: white;
}
.nav-pills .nav-link:hover:not(.active) {
  background-color: #e9ecef;
}
</style>