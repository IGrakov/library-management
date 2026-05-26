<script setup lang="ts">
import Button from "primevue/button";
import Card from "primevue/card";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import { useToast } from "primevue/usetoast";
import { ref } from "vue";
import { useRouter } from "vue-router";

import DefaultLayout from "@/components/layouts/DefaultLayout.vue";
import { useAuthStore } from "@/stores/auth.store";

const router = useRouter();

const authStore = useAuthStore();

const toast = useToast();

const email = ref("");
const password = ref("");

async function onSubmit() {
  await authStore.login(email.value, password.value);

  await router.push("/");
}
</script>

<template>
  <DefaultLayout>
    <Card class="max-w-xl mx-auto p-6">
      <template #content>
        <form class="flex justify-center flex-col gap-4" @submit.prevent="onSubmit">
          <div class="flex flex-col gap-1">
            <InputText v-model="email" name="email" type="text" placeholder="Email" class="border p-2 rounded" />
          </div>
          <div class="flex flex-col gap-1">
            <Password v-model="password" name="password" placeholder="Password" :feedback="false" fluid />
          </div>
          <Button type="submit" variant="outlined" severity="info" label="Submit" class="mt-6" />
        </form>
      </template>
    </Card>
  </DefaultLayout>
</template>
