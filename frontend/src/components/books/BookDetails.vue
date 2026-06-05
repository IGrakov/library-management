<script setup lang="ts">
import type { DetailedBook } from "@/types/books";

defineProps<{
  book: DetailedBook;
}>();
</script>

<template>
  <div class="flex flex-col gap-4">
    <div><strong>Title:</strong> {{ book.title }}</div>
    <div>
      <strong>Authors:</strong>
      {{ book.author.map((a) => [a.last_name, a.first_name, a.middle_name].filter(Boolean).join(" ")).join(", ") }}
    </div>
    <div>
      <strong>Languages:</strong>
      {{ book.language.map((l) => l.name).join(", ") }}
    </div>
    <div>
      <strong>Genres:</strong>
      {{ book.genre.map((g) => g.name).join(", ") }}
    </div>
    <div><strong>Published:</strong> {{ book.published_date }}</div>
    <div><strong>Pages:</strong> {{ book.pages }}</div>
    <div><strong>ISBN:</strong> {{ book.isbn }}</div>
    <div v-if="book.cover">
      <img :src="book.cover" alt="Book cover" class="max-w-xs" />
    </div>
  </div>
</template>
