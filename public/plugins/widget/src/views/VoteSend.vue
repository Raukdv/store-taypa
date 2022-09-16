<template>
  <div class="py-5">
    <h3>{{ company.widget_submitted_title }}</h3>
    <p>{{ company.widget_submitted_text }}</p>
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
