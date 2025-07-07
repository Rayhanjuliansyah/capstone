import { createRouter, createWebHistory } from 'vue-router'

// Import komponen halaman
import HomePage from '@/components/HomePage.vue'
import VisualisasiPage from '@/components/visualisasi.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    alias: '/dashboard' // Alias untuk akses lewat '/dashboard'
  },
  {
    path: '/visualisasi',
    name: 'Visualisasi',
    component: VisualisasiPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
