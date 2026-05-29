<script setup lang="ts">
defineProps<{
  label?: string;
  error?: string;
}>();
</script>

<template>
  <div class="flex flex-col gap-1">
    <label class="font-medium text-sm">
      {{ label }}
    </label>

    <slot />

    <small v-if="error" class="text-red-500">
      {{ error }}
    </small>
  </div>
</template>
