<script setup>
// No imports needed for ref in Nuxt (auto-imported)

const mode = ref('link') // 'link' or 'wifi'
const linkUrl = ref('')
const wifiSSID = ref('')
const wifiPassword = ref('')
const qrImage = ref(null)
const format = ref('png') // Let's add the option for SVG or PNG

const generateCode = async () => {
  const formData = new FormData()
  
  // 1. Prepare Data
  formData.append('mode', mode.value)
  formData.append('format', format.value) // We will send this to backend
  
  if (mode.value === 'link') {
    formData.append('data', linkUrl.value)
  } else {
    formData.append('ssid', wifiSSID.value)
    formData.append('password', wifiPassword.value)
  }

  try {
    // 2. Send Request using Nuxt's native $fetch
    const response = await $fetch('http://127.0.0.1:8000/api/generate/', {
      method: 'POST',
      body: formData,
      responseType: 'blob' // Crucial: tells Nuxt to treat response as a file
    })

    // 3. Convert Blob to Displayable URL
    if (qrImage.value) URL.revokeObjectURL(qrImage.value) // Cleanup old image
    qrImage.value = URL.createObjectURL(response)
    
  } catch (error) {
    console.error("Error generating QR:", error)
    alert("Failed to connect to Django server.")
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
  <div class="container">
    <h1>QR Generator (Nuxt)</h1>

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
      <input v-model="wifiSSID" placeholder="MyHomeWifi" />
      
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
</template>

<style scoped>
/* Simple CSS for a clean look */
.container { max-width: 450px; margin: 4rem auto; font-family: 'Segoe UI', sans-serif; text-align: center; color: #333; }
.tabs { margin-bottom: 20px; display: flex; justify-content: center; gap: 10px; }
.tabs button { padding: 10px 20px; border: none; background: #eee; cursor: pointer; border-radius: 8px; font-weight: 600; }
.tabs button.active { background: #00dc82; color: white; } /* Nuxt Green */

.card { background: #f9f9f9; padding: 20px; border-radius: 12px; text-align: left; margin-bottom: 15px; }
.card label { display: block; font-size: 0.9rem; margin-bottom: 5px; color: #666; }
input, select { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }

.generate-btn { width: 100%; padding: 12px; background: #333; color: white; border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; transition: 0.2s; }
.generate-btn:hover { background: #000; }

.result-area { margin-top: 30px; animation: fadeIn 0.5s; }
.qr-preview { max-width: 200px; border: 1px solid #ddd; border-radius: 8px; }
.download-btn { margin-top: 15px; padding: 8px 16px; background: #00dc82; color: white; border: none; border-radius: 6px; cursor: pointer; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
