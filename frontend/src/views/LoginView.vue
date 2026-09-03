<template>
    <div class="container-fluid d-flex justify-content-center align-items-center vh-100">
        <div class="col-md-4 bg-light p-4 rounded-3 shadow">
            <h2 class="text-center">Login</h2>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="email" class="form-label">Email address</label>
                    <input 
                    type="email" 
                    class="form-control" 
                    id="email" 
                    aria-describedby="emailHelp" 
                    v-model="email"
                    placeholder="Enter your email address">
                    <div id="emailHelp" class="form-text">
                        We will never share your email with anyone else.
                    </div>
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input 
                    type="password" 
                    class="form-control" 
                    id="password" 
                    v-model="password" 
                    @input="validate_password"
                    placeholder="Enter your password">
                    <div id="passwordHelp" class="form-text">
                        {{ password_error }}
                    </div>
                </div>

                <button type="submit" class="btn btn-primary w-100">
                    Login
                </button>
            </form>
        </div>
    </div>
</template>


<script setup>
import router from '@/router'
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const password_error = ref('')

const validate_password = () => {
    if (password.value.length < 4) {
        password_error.value = 'Password must be at least 4 characters long'
        return false
    } else {
        password_error.value = ''
        return true
    }
}

async function login() {

    if (!validate_password()) {
        alert("Invalid password. Please try again.")
        return
    }

    if (email.value === '' || password.value === '') {
        alert("Please fill in all fields.")
        return
    }

    const user = {
        email: email.value,
        password: password.value
    }

    const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    })

    console.log(response)

    if (!response.ok) {
        const errorData = await response.json()
        alert(`Login failed: ${errorData.message}`)
        return
    }
    else {
        const data = await response.json()
        console.log(data)
        localStorage.setItem('token', data.token)
        localStorage.setItem('user_id', data.user_details.id)
        // save roles array for later guards
        localStorage.setItem('roles', JSON.stringify(data.user_details.roles || []))
        alert("Login successful!")
        const roles = data.user_details.roles || []
        if (roles.includes('admin')) {
           router.push('/admin_dash')
        } else if (roles.includes('company')) {
           router.push('/company_dash')
        } else {
           router.push('/student_dash')
        }
    }
}
</script>