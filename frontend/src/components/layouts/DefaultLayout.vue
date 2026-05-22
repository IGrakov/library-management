<script setup lang="ts">
import { VueQueryDevtools } from "@tanstack/vue-query-devtools";
import TheHeader from "@/components/layouts/TheHeader.vue";
import TheFooter from "@/components/layouts/TheFooter.vue";
</script>

<template>
  <div class="flex flex-col min-h-screen">
    <TheHeader />

    <main class="flex min-h-[calc(100vh-200px)] items-center justify-center">
      <slot />
    </main>

    <TheFooter />
    <VueQueryDevtools />
  </div>
</template>
