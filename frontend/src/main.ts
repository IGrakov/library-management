import { createApp } from "vue";
import { VueQueryPlugin, QueryClient, VueQueryPluginOptions } from "@tanstack/vue-query";
import { createPinia } from "pinia";
import App from "./App.vue";
import PrimeVue from "primevue/config";
import Aura from "@primeuix/themes/aura";
import "primeicons/primeicons.css"; // icons
import "./assets/main.css"; // Tailwind CSS
import router from "@/router";
import ToastService from "primevue/toastservice";

const app = createApp(App);

const queryClient = new QueryClient();
const vueQueryOptions: VueQueryPluginOptions = { queryClient };
const pinia = createPinia();

app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
});
app.use(VueQueryPlugin, vueQueryOptions);
app.use(pinia);
app.use(router);
app.use(ToastService);
app.mount("#app");
