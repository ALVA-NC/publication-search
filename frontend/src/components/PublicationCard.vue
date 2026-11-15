
<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  publication: {
    type: Object,
    required: true
  }
})

const concepts = computed(() =>
  (props.publication.concept_names || []).slice(0, 3)
)

const authors = computed(() => {
  return (props.publication.author_names || []).join(', ')
})

const institutions = computed(() => {
  return (props.publication.institution_names || []).join(', ')
})

const publicationId = computed(() => {
  return props.publication.id?.split('/').pop()
})
</script>

<template>
  <article class="publication-card">
    <h3>
      <RouterLink :to="`/publications/${publicationId}`">
        {{ publication.title || 'Untitled publication' }}
      </RouterLink>
    </h3>

    <p class="authors">
      {{ authors || 'Authors unavailable' }}
    </p>

    <div class="metadata">
      <span v-if="publication.publication_date">
        {{ publication.publication_date }}
      </span>

      <span v-if="institutions">
        {{ institutions }}
      </span>

      <span v-if="publication.cited_by_count !== undefined">
        {{ publication.cited_by_count }} citations
      </span>
    </div>

    <ul v-if="concepts.length" class="tags" aria-label="Concepts">
        <li v-for="concept in concepts" :key="concept" class="tag">
            {{ concept }}
        </li>
    </ul>

    <p v-if="publication.abstract" class="abstract">
      {{ publication.abstract.slice(0, 300) }}...
    </p>
  </article>
</template>
