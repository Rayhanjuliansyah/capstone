<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-100 to-white py-10 px-4">
    <div class="max-w-4xl mx-auto mt-12">
      <!-- Judul -->
      <h1 class="text-3xl font-bold text-center text-black mb-6">🌤️ Informasi Cuaca</h1>
      <p class="text-center text-gray-700 mb-6">
        Data real-time cuaca kota <strong>Padang</strong> 
      </p>

      <!-- Isi 2 kartu -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Card Cuaca -->
        <div class="bg-white rounded-2xl shadow-lg p-6 text-gray-800 hover:shadow-2xl transition-shadow">
          <h2 class="text-xl font-semibold text-pink-700 mb-4">📍 Cuaca Saat Ini</h2>

          <div v-if="weather">
            <p class="text-lg mb-1">🌡️ Suhu: <span class="text-blue-600 font-bold">{{ weather.suhu_sekarang }}°C</span></p>
            <p class="mb-1">💧 Kelembapan: <span class="text-blue-500">{{ weather.kelembapan }}%</span></p>
            <p class="mb-3">🔍 Kondisi: <span class="capitalize text-purple-700 font-medium">{{ weather.cuaca }}</span></p>
            <p class="text-xs text-gray-500 mt-4">🕒 Terakhir diperbarui: {{ lastUpdated }}</p>
          </div>
          <p v-else class="text-gray-500 italic">Memuat data cuaca...</p>
        </div>

        <!-- Card Info Penyakit -->
        <div class="bg-white rounded-2xl shadow-lg p-6 text-gray-800 hover:shadow-2xl transition-shadow">
          <h2 class="text-xl font-semibold text-green-700 mb-4">💡 Penting Diketahui</h2>
          <ul class="list-disc pl-5 space-y-2 text-sm">
            <li>Perubahan cuaca dapat memengaruhi pola penyakit musiman.</li>
            <li>Data digunakan untuk memprediksi risiko DBD, ISPA, dan Influenza.</li>
            <li>Gunakan informasi ini sebagai langkah preventif dan edukatif.</li>
          </ul>
        </div>
      </div>

      <!-- Tombol ke Prediksi -->
      <div class="text-center mt-10">
        <router-link
          to="/homepage"
          class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition"
        >
          🔍 Prediksi
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const weather = ref(null)
const lastUpdated = ref('')

const fetchCuaca = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/cuaca/today?kota=Padang')
    console.log('Respons cuaca:', res.data) // 🔍 Tambahkan log ini

    weather.value = res.data
    lastUpdated.value = new Date().toLocaleString('id-ID')
  } catch (err) {
    console.error('Gagal mengambil data cuaca:', err)
  }
}



onMounted(() => {
  fetchCuaca()
})
</script>
