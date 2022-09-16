import Vue from 'vue'
import VueRouter from 'vue-router'

import Index from '@/views/Index'
import VoteGood from '@/views/VoteGood'
import VoteBad from '@/views/VoteBad'
import VoteSend from '@/views/VoteSend'


Vue.use(VueRouter)

const routes = [
  {
    path: '',
    component: Index,
    name: 'index'
  },
  {
    path: '/vote-good',
    component: VoteGood,
    name: 'vote_good'
  },
  {
    path: '/vote-bad',
    component: VoteBad,
    name: 'vote_bad'
  },
  {
    path: '/vote-send',
    component: VoteSend,
    name: 'vote_send'
  },
]

const router = new VueRouter({
  base: window.location.pathname,
  mode: 'hash',
  routes
})


export default router
