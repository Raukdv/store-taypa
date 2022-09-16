<template>
  <div>
    <p>{{ company.widget_positive_text }}</p>

    <a class="align-items-center border d-flex justify-content-between mb-2 p-3 rounded" :href="link.url" :key="index" target="_blank" v-for="(link, index) in sortedLinkSet">
      <img class="img-fluid w-25" v-if="link.icon" :src="link.icon" />
      <span class="flex-fill text-center">{{ link.name }}</span>
    </a>
  </div>
</template>

<script>
export default {
  computed: {
    company() {
      return this.$store.getters.company
    },
    sortedLinkSet() {
      const company = this.$store.getters.company
      if (!company) return []
      return company.link_set.sort((a, b) => a.order - b.order)
    }
  }
}
</script>
