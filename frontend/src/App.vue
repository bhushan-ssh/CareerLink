<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { ref, onMounted, watch } from 'vue'
import router from './router'

const token = ref(localStorage.getItem("token"))
const role = ref(localStorage.getItem("role"))
const route = useRoute()

onMounted(() => {
  token.value = localStorage.getItem("token")
  role.value = localStorage.getItem("role")
})

function logout(){
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  token.value = null
  role.value = null
  router.push("/")
}

// Watch for changes in localStorage if needed, or rely on manual updates
// For now, simple polling or just trust initial state + local changes
router.afterEach(() => {
  token.value = localStorage.getItem("token")
  role.value = localStorage.getItem("role")
})

const getDashLink = () => {
    if (role.value === 'admin') return '/admin_dash'
    if (role.value === 'student') return '/student_dash'
    if (role.value === 'company') return '/company_dash'
    return '/'
}
</script>

<template>
  <nav class="navbar navbar-expand-lg border-bottom" style="background-color: #f8f9fa;">
    <div class="container">
      <span class="navbar-brand fw-bold text-primary" style="cursor: default;">CareerLink</span>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item" v-if="!token && route.path !== '/login'">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>
          <li class="nav-item" v-if="!token && route.path !== '/register'">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>
          

          <li class="nav-item" v-if="token">
            <button class="btn btn-link nav-link text-danger" @click="logout" style="text-decoration: none;">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <RouterView />
</template>