<script setup>
import QRCode from 'qrcode'

const mode = ref('link') // 'link' or 'wifi'
const linkUrl = ref('')
const wifiSSID = ref('')
const wifiPassword = ref('')
const qrImage = ref(null)
const format = ref('png') // Let's add the option for SVG or PNG

const generateCode = async () => {
  if (mode.value === 'wifi') {
    alert("Wi-Fi mode isn't supported yet.")
    return
  }

  try {
    if (format.value === 'svg') {
      const svgString = await QRCode.toString(linkUrl.value, { type: 'svg' })
      qrImage.value = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svgString)}`
    } else {
      qrImage.value = await QRCode.toDataURL(linkUrl.value, { type: 'image/png' })
    }
  } catch (error) {
    console.error("Error generating QR:", error)
    alert("Failed to generate QR code.")
  }
}

const downloadCode = () => {
  const link = document.createElement('a')
  link.href = qrImage.value
  // Dynamically name the file based on format
  link.download = `qrcode_${mode.value}.${format.value}` 
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div class="main-wrapper">
    <div class="container">
      <h1>QRcodism</h1>
      <div class="tabs">
      <button :class="{ active: mode === 'link' }" @click="mode = 'link'">🔗 Link</button>
      <button :class="{ active: mode === 'wifi' }" @click="mode = 'wifi'">📶 Wi-Fi</button>
    </div>

    <div v-if="mode === 'link'" class="card">
      <label>Enter Website URL</label>
      <input v-model="linkUrl" placeholder="https://example.com" />
    </div>

    <div v-if="mode === 'wifi'" class="card">
      <label>Network Name (SSID)</label>
      <input v-model="wifiSSID" placeholder="Wifi Name" />
      
      <label>Password</label>
      <input v-model="wifiPassword" type="text" placeholder="SecretPassword123" />
    </div>

    <div class="options">
      <label>Format: </label>
      <select v-model="format">
        <option value="png">PNG (Image)</option>
        <option value="svg">SVG (Vector)</option>
      </select>
    </div>

    <button class="generate-btn" @click="generateCode">Generate QR Code</button>

    <div v-if="qrImage" class="result-area">
      <p>Here is your code:</p>
      <img :src="qrImage" alt="QR Code" class="qr-preview" />
      <br>
      <button class="download-btn" @click="downloadCode">
        Download {{ format.toUpperCase() }}
      </button>
    </div>
  </div>
  </div>
</template>

<style scoped>
/* Simple CSS for a clean, centered card */
.main-wrapper { background: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 2rem 1rem; }
.container { max-width: 720px; width: 100%; background: white; border-radius: 14px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); padding: 3rem; font-family: 'Segoe UI', sans-serif; text-align: center; color: #333; display: flex; flex-direction: column; gap: 1rem; box-sizing: border-box; }
.tabs { margin-bottom: 24px; display: flex; justify-content: center; gap: 14px; }
.tabs button { padding: 12px 22px; border: none; background: #eee; cursor: pointer; border-radius: 8px; font-weight: 600; }
.tabs button.active { background: #00dc82; color: white; } /* Nuxt Green */

.card { background: #f9f9f9; padding: 24px; border-radius: 12px; text-align: left; margin-bottom: 18px; }
.card label { display: block; font-size: 0.95rem; margin-bottom: 8px; color: #666; }
input, select { width: 100%; padding: 12px; margin-bottom: 16px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }

.generate-btn { width: 100%; padding: 14px; background: #333; color: white; border: none; border-radius: 10px; font-size: 1.05rem; cursor: pointer; transition: 0.18s; }
.generate-btn:hover { background: #000; }

.result-area { margin-top: 30px; animation: fadeIn 0.5s; }
.qr-preview { max-width: 260px; border: 1px solid #ddd; border-radius: 10px; }
.download-btn { margin-top: 15px; padding: 10px 18px; background: #00dc82; color: white; border: none; border-radius: 8px; cursor: pointer; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Mobile responsiveness */
@media (max-width: 640px) {
  .main-wrapper { padding: 1.25rem; }
  .container { max-width: 95%; padding: 1.25rem; border-radius: 12px; }
  .tabs { gap: 8px; margin-bottom: 18px; }
  .tabs button { padding: 8px 12px; font-size: 0.95rem; }
  .card { padding: 16px; }
  .card label { font-size: 0.9rem; }
  input, select { padding: 10px; margin-bottom: 12px; }
  .generate-btn { padding: 12px; font-size: 1rem; border-radius: 8px; }
  .qr-preview { max-width: 180px; }
}

@media (max-width: 380px) {
  .container { padding: 1rem; }
  h1 { font-size: 1.1rem; margin-bottom: 0.5rem; }
  .tabs { flex-wrap: wrap; gap: 6px; }
  .qr-preview { max-width: 160px; }
}

</style>
