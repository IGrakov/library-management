import { createApp } from 'vue'
import { VueQueryPlugin } from '@tanstack/vue-query'
import App from './App.vue'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'
import "primeicons/primeicons.css"; // icons

import './assets/main.css'  // <-- Tailwind CSS

const app = createApp(App)

app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(VueQueryPlugin)

app.mount("#app")