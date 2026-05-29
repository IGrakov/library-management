<script setup lang="ts">
import Button from "primevue/button";
import Dialog from "primevue/dialog";

withDefaults(
  defineProps<{
    visible: boolean;
    title: string;

    loading?: boolean;

    submitLabel?: string;
    submitSeverity?: "primary" | "secondary" | "success" | "info" | "warn" | "help" | "danger" | "contrast";

    cancelLabel?: string;
  }>(),
  {
    submitLabel: "Save",
    submitSeverity: "primary",
    cancelLabel: "Cancel",
  },
);

const emit = defineEmits<{
  "update:visible": [boolean];
  submit: [];
}>();
</script>

<template>
  <Dialog :visible="visible" modal :header="title" class="w-sm" @update:visible="emit('update:visible', $event)">
    <div class="flex flex-col gap-4">
      <slot />

      <div class="flex justify-end gap-2">
        <Button :label="cancelLabel" severity="secondary" @click="emit('update:visible', false)" />

        <Button :label="submitLabel" :severity="submitSeverity" :loading="loading" @click="emit('submit')" />
      </div>
    </div>
  </Dialog>
</template>
