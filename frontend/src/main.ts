import "primeicons/primeicons.css"; // icons
import "./assets/main.css"; // Tailwind CSS

import Aura from "@primeuix/themes/aura";
import { QueryClient, VueQueryPlugin, VueQueryPluginOptions } from "@tanstack/vue-query";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import ConfirmationService from "primevue/confirmationservice";
import ToastService from "primevue/toastservice";
import { createApp } from "vue";

import router from "@/router";

import App from "./App.vue";

const app = createApp(App);

const queryClient = new QueryClient();
const vueQueryOptions: VueQueryPluginOptions = { queryClient };
const pinia = createPinia();

app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
  ripple: false,
});
app.use(VueQueryPlugin, vueQueryOptions);
app.use(pinia);
app.use(router);
app.use(ToastService);
app.use(ConfirmationService);
app.mount("#app");
