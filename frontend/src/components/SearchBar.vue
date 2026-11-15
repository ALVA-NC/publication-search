
<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search'])

const searchQuery = ref('')

function submitSearch() {
  emit('search', searchQuery.value.trim())
}
</script>

<template>
  <form class="search-bar" @submit.prevent="submitSearch">
    <input
      v-model="searchQuery"
      type="search"
      placeholder="Search publications, authors or countries..."
      aria-label="Search publications"
    />

    <button type="submit">
      Search
    </button>
  </form>
</template>
