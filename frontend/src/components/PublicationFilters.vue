
<script setup>
import { reactive } from 'vue'

const emit = defineEmits(['filter'])

const filters = reactive({
  author: '',
  institution: '',
  country: '',
  concept: ''
})

function applyFilters() {
  emit('filter', { ...filters })
}

function clearFilters() {
  filters.author = ''
  filters.institution = ''
  filters.country = ''
  filters.concept = ''

  applyFilters()
}
</script>

<template>
  <aside class="filters">
    <h2>Filters</h2>

    <form @submit.prevent="applyFilters">
      <label>
        Author
        <input
          v-model="filters.author"
          placeholder="Author name"
        />
      </label>

      <label>
        Institution
        <input
          v-model="filters.institution"
          placeholder="Institution name"
        />
      </label>

      <label>
        Country
        <input
          v-model="filters.country"
          placeholder="Country code (e.g. DK)"
          maxlength="2"
        />
      </label>

      <label>
        Concept
        <input
          v-model="filters.concept"
          placeholder="e.g. Climate change"
        />
      </label>

      <button type="submit" class="apply-button">
        Apply filters
      </button>

      <button
        type="button"
        class="clear-button"
        @click="clearFilters"
      >
        Clear filters
      </button>
    </form>
  </aside>
</template>
