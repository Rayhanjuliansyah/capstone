<template>
  <div class="page-container">
    <div class="content-container">
      <!-- Tombol Kembali -->
      <div class="back-button-container">
        <button @click="goToDashboard" class="back-btn">← Dashboard    </button>
      </div>

      <h1 class="page-title">📊 Visualisasi Statistik Penyakit</h1>

      <div class="form-grid">
        <div>
          <label class="label">Tanggal Awal</label>
          <input type="date" v-model="tanggalAwal" class="input-field" />
        </div>
        <div>
          <label class="label">Tanggal Akhir</label>
          <input type="date" v-model="tanggalAkhir" class="input-field" />
        </div>
        <div class="button-container">
          <button @click="fetchData" :disabled="isLoading" class="submit-btn">
            {{ isLoading ? 'Memuat...' : 'Tampilkan Data' }}
          </button>
        </div>
      </div>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <div class="chart-container">
        <div class="chart-inner">
          <line-chart
            v-if="chartData"
            :chart-data="chartData"
            :chart-options="chartOptions"
          />
          <p v-else-if="!isLoading && !errorMessage" class="placeholder-text">
            Silakan pilih rentang tanggal dan klik "Tampilkan Data".
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import LineChart from './LineChart.vue' // Karena file ada di folder yang sama

const router = useRouter()
const goToDashboard = () => {
  router.push('/dashboard')
}

const tanggalAwal = ref('')
const tanggalAkhir = ref('')
const chartData = ref(null)
const errorMessage = ref('')
const isLoading = ref(false)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Tren Penyakit Berdasarkan Tanggal',
      font: {
        size: 18,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
    },
  },
}

const fetchData = async () => {
  errorMessage.value = ''
  chartData.value = null

  if (!tanggalAwal.value || !tanggalAkhir.value) {
    errorMessage.value = 'Silakan isi kedua tanggal terlebih dahulu.'
    return
  }

  isLoading.value = true

  try {
    const res = await axios.get('http://localhost:8000/riwayat', {
      params: {
        start: tanggalAwal.value,
        end: tanggalAkhir.value,
      },
    })

    console.log('Hasil respon:', res.data) // 🔍 debugging

    const records = res.data.data // 👈 ubah ini sesuai struktur respons

    if (!Array.isArray(records) || records.length === 0) {
      errorMessage.value = 'Tidak ada data ditemukan untuk rentang tanggal tersebut.'
    } else {
      const labels = records.map(d => d.tanggal)
      chartData.value = {
        labels,
        datasets: [
          {
            label: 'DBD',
            data: records.map(d => d.dbd),
            borderColor: '#ef4444',
            backgroundColor: '#fecaca',
            fill: false,
            tension: 0.3,
          },
          {
            label: 'Influenza',
            data: records.map(d => d.influenza),
            borderColor: '#3b82f6',
            backgroundColor: '#bfdbfe',
            fill: false,
            tension: 0.3,
          },
          {
            label: 'ISPA',
            data: records.map(d => d.ispa),
            borderColor: '#10b981',
            backgroundColor: '#d1fae5',
            fill: false,
            tension: 0.3,
          },
        ],
      }
    }
  } catch (err) {
    console.error('Gagal fetch data statistik:', err)
    errorMessage.value = 'Terjadi kesalahan saat mengambil data.'
  } finally {
    isLoading.value = false
  }
}

</script>

<style scoped>
/* Container */
.page-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9fafb;
  padding: 20px;
}
.content-container {
  width: 100%;
  max-width: 1000px;
  padding: 40px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Back Button */
.back-button-container {
  margin-bottom: 16px;
}
.back-btn {
  background: none;
  color: #2563eb;
  border: none;
  font-weight: 600;
  cursor: pointer;
  font-size: 14px;
  padding: 6px 0;
}
.back-btn:hover {
  text-decoration: underline;
}

/* Title */
.page-title {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 40px;
  color: #1f2937;
}

/* Form */
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 20px;
  margin-bottom: 24px;
  align-items: end;
}
.label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #374151;
}
.input-field {
  width: 100%;
  padding: 10px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
}
.input-field:focus {
  border-color: #3b82f6;
}

/* Button */
.button-container {
  display: flex;
  justify-content: flex-start;
}
.submit-btn {
  background-color: #3b82f6;
  color: white;
  padding: 10px 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.submit-btn:hover {
  background-color: #2563eb;
}
.submit-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

/* Chart Container */
.chart-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.chart-inner {
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Texts */
.error-text {
  color: #dc2626;
  text-align: center;
  margin-bottom: 16px;
}
.placeholder-text {
  color: #6b7280;
  font-size: 14px;
}
</style>
