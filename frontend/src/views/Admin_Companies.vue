<template>
<div class="container mt-4">

  <h2>Company Approvals</h2>

  <ul class="list-group mt-3">
    <li
      v-for="user in users.filter(u => u.role === 'company')"
      :key="user.id"
      class="list-group-item d-flex justify-content-between align-items-center"
    >

      <span>{{ user.name }}</span>

      <button
        v-if="!user.company_profile.approved"
        class="btn btn-primary"
        @click="approveCompany(user.company_profile.id)"
      >
        Approve
      </button>

      <span v-else class="text-success">✔ Approved</span>

    </li>
  </ul>

</div>
</template>

<script>

export default {

data() {
  return {
    companies: []
  }
},

mounted() {
  this.getCompanies()
},

methods: {

  getCompanies() {
    fetch("http://127.0.0.1:5000/api/admin/companies")
    .then(res => res.json())
    .then(data => {
      this.companies = data
    })
  },

  approveCompany(id) {

    fetch(`http://127.0.0.1:5000/api/admin/approve_company/${id}`, {
      method: "POST"
    })
    .then(res => res.json())
    .then(() => {
      this.getCompanies()
    })

  }

}

}

</script>