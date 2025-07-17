import { createRouter, createWebHistory } from 'vue-router'

// Import komponen halaman
import Home from '@/views/Home.vue'
import HomePage from '@/components/HomePage.vue'
import Dashboard from '@/components/Dashboard.vue'
import VisualisasiPage from '@/components/Visualisasi.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/homepage',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
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
