
import { createRouter, createWebHistory } from 'vue-router'

import SearchView from '../views/SearchView.vue'
import PublicationDetailView from '../views/PublicationDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'search',
      component: SearchView
    },
    {
      path: '/publications/:id',
      name: 'publication-detail',
      component: PublicationDetailView
    }
  ]
})

export default router
