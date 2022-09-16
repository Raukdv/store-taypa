<template>
  <div class="card text-center" v-if="company">
    <div class="card-body">
      <img :alt="company.name" class="img-fluid" v-if="company.logo" :src="company.logo" :title="company.name" />
      <h2 v-if="!company.logo">{{ company.name }}</h2>

      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  beforeMount() {
    this.getCompany()
  },
  computed: {
    company() {
      return this.$store.getters.company
    }
  },
  methods: {
    getCompany() {
      if (!this.slug) return

      this.$http.get(`/api/company/${this.slug}/`)
        .then(response => {
          this.$store.dispatch('setCompany', response.data)
        })
    }
  },
  props: {
    slug: {
      required: true,
      type: String
    }
  }
}
</script>
