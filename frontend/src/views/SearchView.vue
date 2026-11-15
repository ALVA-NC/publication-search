
<script setup>
import { ref, onMounted } from 'vue'

import SearchBar from '../components/SearchBar.vue'
import PublicationFilters from '../components/PublicationFilters.vue'
import PublicationCard from '../components/PublicationCard.vue'

import { searchPublications } from '../api/publications'

const publications = ref([])
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')

const filters = ref({
  author: '',
  institution: '',
  country: '',
  concept: ''
})

const pagination = ref({
  page: 1,
  per_page: 20,
  total: 0,
  total_pages: 0
})

async function loadPublications(page = 1) {
  loading.value = true
  error.value = ''

  try {
    const response = await searchPublications({
      q: searchQuery.value,
      ...filters.value,
      page,
      perPage: pagination.value.per_page
    })

    publications.value = response.results
    pagination.value = response.pagination
  } catch (err) {
    error.value = err.message
    publications.value = []
  } finally {
    loading.value = false
  }
}

function handleSearch(query) {
  searchQuery.value = query
  loadPublications(1)
}

function handleFilter(newFilters) {
  filters.value = newFilters
  loadPublications(1)
}

function changePage(page) {
  if (page < 1 || page > pagination.value.total_pages) {
    return
  }

  loadPublications(page)
}

onMounted(() => {
  loadPublications()
})
</script>

<template>
  <main id="main-content" class="search-page">
    <header>
      <h1>Publication Search</h1>
      <p>Discover academic research from OpenAlex.</p>
    </header>

    <SearchBar @search="handleSearch" />

    <div class="content">
      <PublicationFilters @filter="handleFilter" />

      <section class="results">
        <p v-if="loading" role="status">
          Loading publications...
        </p>

        <p v-else-if="error" role="alert">
          {{ error }}
        </p>

        <template v-else>
          <p class="result-count">
            {{ pagination.total }} publications found
          </p>

          <p v-if="publications.length === 0">
            No publications found. Try changing your search.
          </p>

          <PublicationCard
            v-for="publication in publications"
            :key="publication.id"
            :publication="publication"
          />

          <nav
            v-if="pagination.total_pages > 1"
            class="pagination"
            aria-label="Publication result pages"
          >
            <button
              :disabled="pagination.page === 1"
              @click="changePage(pagination.page - 1)"
            >
              Previous
            </button>

            <span>
              Page {{ pagination.page }} of {{ pagination.total_pages }}
            </span>

            <button
              :disabled="pagination.page === pagination.total_pages"
              @click="changePage(pagination.page + 1)"
            >
              Next
            </button>
          </nav>
        </template>
      </section>
    </div>
  </main>
</template>

