<template>
  <div
    class="w-screen h-screen bg-cover bg-center bg-no-repeat relative overflow-hidden"
    style="background-image: url('https://source.unsplash.com/featured/?weather');"
  >
    <!-- Overlay gelap -->
    <div class="absolute inset-0 bg-black bg-opacity-50"></div>

    <!-- Konten di tengah layar -->
    <div class="absolute inset-0 z-10 flex justify-center items-center px-4">
      <div
        class="form-container text-black bg-white bg-opacity-90 p-8 rounded-2xl shadow-2xl w-full max-w-lg"
      >
        <h1 class="text-3xl font-extrabold mb-6 text-center text-hitam">
          Prediksi Pola Penyakit Musiman
        </h1>

        <div class="space-y-4">
          <!-- Input Form -->
          <input
            v-model="kelembaban"
            type="number"
            placeholder="Kelembaban (%)"
            class="input-field text-putih"
          />
          <input
            v-model="suhu"
            type="number"
            placeholder="Suhu (°C)"
            class="input-field text-putih"
          />
          <select v-model="cuaca" class="input-field text-putih">
            <option value="" disabled>Pilih cuaca</option>
            <option>Berawan</option>
            <option>Cerah</option>
            <option>Hujan Lokal</option>
            <option>Hujan Petir</option>
            <option>Hujan Ringan</option>
            <option>Hujan Sedang</option>
          </select>

          <button
            @click="kirim"
            class="submit-btn w-full"
            :disabled="loading"
          >
            {{ loading ? 'Memproses...' : 'Prediksi' }}
          </button>

          <div
            v-if="hasil"
            class="mt-4 font-semibold text-hitam p-4 bg-green-50 border border-green-300 rounded-lg space-y-2"
          >
            <p>✅ Prediksi jumlah kasus:</p>
            <p>• DBD: {{ hasil.dbd }}</p>
            <p>• ISPA: {{ hasil.ispa }}</p>
            <p>• Influenza: {{ hasil.influenza }}</p>
          </div>

          <div
            v-if="error"
            class="mt-4 font-semibold text-red-800 p-4 bg-red-100 border border-red-300 rounded-lg"
          >
            {{ error }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const kelembaban = ref('')
const suhu = ref('')
const cuaca = ref('')
const hasil = ref(null)
const error = ref('')
const loading = ref(false)

const kirim = async () => {
  hasil.value = null
  error.value = ''
  loading.value = true

  if (!kelembaban.value || !suhu.value || !cuaca.value.trim()) {
    error.value = '❌ Harap isi semua input terlebih dahulu.'
    loading.value = false
    return
  }

  try {
    const res = await axios.post('http://localhost:5000/api/predict', {
  kelembaban: parseFloat(kelembaban.value),
  suhu: parseFloat(suhu.value),
  cuaca: cuaca.value
})


    if (res.data.status === 'success') {
      hasil.value = res.data.predictions
    } else {
      error.value = '❌ Gagal memproses prediksi.'
    }
  } catch (err) {
    console.error('Error:', err)
    error.value = '❌ Terjadi kesalahan saat menghubungi server.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form-container {
  backdrop-filter: blur(10px);
}
.text-hitam {
  color: #111827;
}
.text-putih {
  color: #ffffff;
}
.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 10px;
  outline: none;
  font-size: 1rem;
  transition: border 0.2s;
}
.input-field:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
}
.submit-btn {
  padding: 12px;
  background-color: #3b82f6;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.submit-btn:hover {
  background-color: #2563eb;
}
.submit-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}
</style>
