import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    { path: '/', name: 'home', component: () => import('../views/HomeView.vue') },
    { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
    { path: '/register', name: 'register', component: () => import('../views/RegisterView.vue') },
    { path: '/admin_dash', name: 'admin_dash', component: () => import('../views/Admin_dash.vue') },
    { path: '/student_dash', name: 'student_dash', component: () => import('../views/Student_dash.vue') },
    { path: '/company_dash', name: 'company_dash', component: () => import('../views/Company_dash.vue') },






  ],
})

/* Navigation Guard */
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("token")

  if (!token && to.path !== "/" && to.path !== "/login" && to.path !== "/register") {
    next("/login")
  } else {
    next()
  }

})

export default router