<template>
  <div class="container-fluid d-flex justify-content-center align-items-center vh-100">
    <div class="col-md-4 bg-light p-4 rounded-3 shadow">
      <h2 class="text-center">Register</h2>

      <form @submit.prevent="register">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input
            type="email"
            class="form-control"
            id="email"
            aria-describedby="emailHelp"
            v-model="email"
            @input="checkEmailAvailability"
            placeholder="Enter your email address"
          />
          
          <p class="form-text" v-if="emailHelp">{{ emailHelp }}</p>
            
        </div>

        <div class="mb-3">
          <label for="role" class="form-label">Role</label>
          <select class="form-select" id="role" v-model="role">
            <option value="student">Student</option>
            <option value="company">Company</option>
          </select>
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            @input="validatePassword"
            placeholder="Enter your password"
          />
          <div id="passwordHelp" class="form-text">
            {{ passwordError }}
          </div>
        </div>

        <div class="d-grid gap-2 col-6 mx-auto">
  <button class="btn btn-success" type="submit">Register</button>
</div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const email = ref('')
const password = ref('')
const passwordError = ref('')
const emailHelp = ref('')
const role = ref('student')

const validatePassword = () => {
  if (password.value.length < 4) {
    passwordError.value = 'Password must be at least 4 characters long'
    return false
  }
  passwordError.value = ''
  return true
}

const checkEmailAvailability = async () => {
  if (!email.value.includes('@')) {
    emailHelp.value = 'Please enter a valid email address'
    return false
  }

  try {
    const res = await fetch('http://localhost:5000/api/check_email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value }),
    })
    if (!res.ok) {
      console.error('Failed to check email availability')
      return false
    }
    const data = await res.json()
    emailHelp.value = data.available
      ? 'Email is available'
      : 'Email is already taken'
  } catch (e) {
    console.error(e)
  }
}

const register = async () => {
  if (!validatePassword()) {
    alert('Invalid password. Please try again.')
    return
  }

  if (email.value === '' || password.value === '') {
    alert('Please fill in all fields.')
    return
  }

  if (emailHelp.value !== 'Email is available') {
    alert('Please use valid email address.')
    return
  }

  const user = {
    email: email.value,
    password: password.value,
    role: role.value,
  }

  const response = await fetch('http://127.0.0.1:5000/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  })

  if (!response.ok) {
    const errorData = await response.json()
    alert(`Registration failed: ${errorData.message}`)
    return
  } else {
    const data = await response.json()
    console.log(data)
    alert('Registration successful! You can now log in.')
    router.push('/login')
  }
}
</script>

