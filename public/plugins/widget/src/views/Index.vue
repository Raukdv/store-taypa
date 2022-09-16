<template>
  <div class="row">
    <div class="col-12 mb-3">
      <p class="lead">{{ company.widget_welcome_text }}</p>
    </div>

    <div class="col-6">
      <router-link class="btn btn-success btn-lg" :to="{name: 'vote_good'}" title="Good" type="button">
        <i class="fas fa-thumbs-up"></i>
        <span class="sr-only">Good</span>
      </router-link>
    </div>

    <div class="col-6">
      <router-link class="btn btn-danger btn-lg" :to="{name: 'vote_bad'}" title="Bad" type="button">
        <i class="fas fa-thumbs-down"></i>
        <span class="sr-only">Bad</span>
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
  }
}
</script>
