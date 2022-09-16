<template>
  <div>
    <form class="form" @submit.prevent="sendFeedback">
      <div class="form-group">
        <label for="id_details">{{ company.widget_negative_text }}</label>

        <textarea class="form-control" id="id_details" name="details" v-bind:class="{'is-invalid': errors.detail}" v-model="detail" rows="5"></textarea>

        <div class="invalid-feedback" v-if="errors.detail">
          <span class="d-block" :key="index" v-for="(error, index) in errors.detail">{{ error }}</span>
        </div>
      </div>

      <div class="form-group">
        <button class="btn btn-primary" type="submit">Send feedback</button>
      </div>
    </form>

    <div class="d-block">
      <router-link class="btn btn-link btn-sm" :to="{name: 'index'}" title="Cancel" type="button">
        Cancel
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    company() {
      return this.$store.getters.company
    }
  },
  data() {
    return {
      detail: '',
      errors: {},
      loading: false
    }
  },
  methods: {
    sendFeedback() {
      this.errors = {}
      this.loading = true
      const data = {detail: this.detail}

      this.$http.post(`/api/company/${this.company.slug}/feedback/`, data)
        .then(() => {
          this.detail = ''
          this.loading = false
          this.$router.push({name: 'vote_send'})
        })
        .catch(error => {
          this.errors = error.response.data
          this.loading = false
        })
    }
  }
}
</script>
