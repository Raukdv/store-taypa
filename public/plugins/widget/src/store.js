import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    company: null
  },
  mutations: {
    setCompany(state, company) {
      state.company = company
    }
  },
  actions: {
    setCompany({commit}, company) {
      commit('setCompany', company)
    },
  },
  getters: {
    company: state => state.company
  }
})

export default store
