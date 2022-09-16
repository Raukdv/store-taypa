import Vue from 'vue'
import axios from 'axios'

import App from '@/App.vue'
import router from '@/router'
import store from '@/store'


Vue.config.productionTip = false
Vue.prototype.$http = axios


new Vue({
  beforeMount() {
    this.companySlug = this.$el.dataset.slug
  },
  data() {
    return {
      companySlug: null,
      messageId: null,
    }
  },
  render: function (h) {
    return h(App, {
      props: {
        slug: this.companySlug
      }
    })
  },
  router,
  store
}).$mount('#taypa-widget')
