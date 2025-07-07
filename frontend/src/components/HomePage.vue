<template>
  <div class="flex flex-col md:flex-row min-h-screen">
    <!-- Panel Kiri -->
    <div class="md:w-1/2 w-full bg-white p-6 overflow-y-auto shadow-md">
      <button
        class="mb-4 px-4 py-2 bg-blue-600 text-white font-semibold rounded hover:bg-blue-700 transition"
        @click="goToVisualisasi"
      >
        Visualisasi
      </button>

      <div class="overflow-x-auto">
        <table class="w-full table-auto border border-gray-300 text-sm text-gray-800">
          <thead class="bg-gray-100 text-gray-900">
            <tr>
              <th class="px-4 py-2 border">Tanggal</th>
              <th class="px-4 py-2 border">DBD</th>
              <th class="px-4 py-2 border">ISPA</th>
              <th class="px-4 py-2 border">Influenza</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in tableData"
              :key="item.tanggal"
              class="hover:bg-gray-50"
            >
              <td class="px-4 py-2 border">{{ item.tanggal }}</td>
              <td class="px-4 py-2 border">{{ item.dbd }}</td>
              <td class="px-4 py-2 border">{{ item.ispa }}</td>
              <td class="px-4 py-2 border">{{ item.influenza }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Panel Kanan -->
    <div class="md:w-1/2 w-full bg-gray-50 flex items-center justify-center p-6">
      <!-- 👇 Tambahkan listener event dari Dashboard -->
      <Dashboard @prediksi-berhasil="getRiwayat" />
    </div>
  </div>
</template>

<script setup>
import Dashboard from './Dashboard.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const tableData = ref([])
const router = useRouter()

const goToVisualisasi = () => {
  router.push('/visualisasi')
}

// ✅ Fungsi yang bisa dipanggil dari Dashboard setelah prediksi berhasil
const getRiwayat = async () => {
  try {
    const res = await fetch('http://localhost:8000/riwayat')
    const json = await res.json()

    if (json.status === 'success') {
      tableData.value = json.data
    } else {
      console.error('Gagal mengambil data:', json)
    }
  } catch (error) {
    console.error('Gagal mengambil data:', error)
  }
}

// 👇 Pertama kali halaman diload
onMounted(() => {
  getRiwayat()
})
</script>
