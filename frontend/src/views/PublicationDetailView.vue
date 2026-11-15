
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

import { getPublication } from '../api/publications'

const route = useRoute()

const publication = ref(null)
const loading = ref(true)
const error = ref('')

async function loadPublication() {
  loading.value = true
  error.value = ''

  try {
    publication.value = await getPublication(route.params.id)
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(loadPublication)
</script>

<template>
  <main id="main-content" class="detail-page">
    <RouterLink to="/" class="back-link">
      ← Back to search
    </RouterLink>

    <p v-if="loading" role="status" aria-live="polite">
      Loading publication...
    </p>

    <div v-else-if="error" role="alert">
      <h1>Unable to load publication</h1>
      <p>{{ error }}</p>
      <RouterLink to="/">Return to search</RouterLink>
    </div>

    <article v-else-if="publication" class="publication-detail">

      <header class="detail-header">
        <h1>{{ publication.title || 'Untitled publication' }}</h1>

        <p class="publication-date">
          Published: {{ publication.publication_date || 'Unknown' }}
        </p>
      </header>

      <!-- Page navigation -->
      <nav class="detail-navigation" aria-label="On this page">
        <h2>On this page</h2>

        <ul>
          <li><a href="#abstract">Abstract</a></li>
          <li><a href="#authors">Authors and affiliations</a></li>
          <li><a href="#publication-info">Publication information</a></li>
          <li><a href="#concepts">Concepts</a></li>
          <li><a href="#topics">Topics</a></li>
          <li v-if="publication.primary_location">
            <a href="#publication-source">Publication source</a>
          </li>
        </ul>
      </nav>

      <!-- Abstract -->
      <section
        id="abstract"
        class="detail-section"
        aria-labelledby="abstract-heading"
        tabindex="-1"
      >
        <h2 id="abstract-heading">Abstract</h2>

        <p v-if="publication.abstract">
          {{ publication.abstract }}
        </p>

        <p v-else>No abstract available.</p>
      </section>

      <!-- Authors -->
      <section
        id="authors"
        class="detail-section"
        aria-labelledby="authors-heading"
        tabindex="-1"
      >
        <h2 id="authors-heading">Authors and affiliations</h2>

        <p v-if="!publication.authorships?.length">
          No author information available.
        </p>

        <ul v-else class="author-list">
          <li
            v-for="(authorship, index) in publication.authorships"
            :key="authorship.author?.id || index"
            class="author"
          >
            <strong>
              {{ authorship.author?.display_name || 'Unknown author' }}
            </strong>

            <ul v-if="authorship.institutions?.length">
              <li
                v-for="institution in authorship.institutions"
                :key="institution.id"
              >
                {{ institution.display_name }}
                <span v-if="institution.country_code">
                  ({{ institution.country_code }})
                </span>
              </li>
            </ul>

            <p v-else>No affiliation available.</p>
          </li>
        </ul>
      </section>

      <!-- Publication information -->
      <section
        id="publication-info"
        class="detail-section"
        aria-labelledby="publication-info-heading"
        tabindex="-1"
      >
        <h2 id="publication-info-heading">Publication information</h2>

        <dl class="publication-metadata">
          <div>
            <dt>Citations</dt>
            <dd>{{ publication.cited_by_count ?? 0 }}</dd>
          </div>

          <div>
            <dt>Countries</dt>
            <dd>
              {{ publication.country_codes?.join(', ') || 'Unknown' }}
            </dd>
          </div>

          <div>
            <dt>DOI</dt>
            <dd>
              <a
                v-if="publication.doi"
                :href="publication.doi"
                target="_blank"
                rel="noopener noreferrer"
              >
                {{ publication.doi }}
                <span class="visually-hidden">(opens in a new tab)</span>
              </a>
              <span v-else>Not available</span>
            </dd>
          </div>

          <div>
            <dt>Open access</dt>
            <dd>
              {{ publication.open_access?.is_oa ? 'Yes' : 'No' }}
            </dd>
          </div>

          <div v-if="publication.open_access?.oa_status">
            <dt>Open access status</dt>
            <dd>{{ publication.open_access.oa_status }}</dd>
          </div>

          <div v-if="publication.open_access?.oa_url">
            <dt>Open access URL</dt>
            <dd>
              <a
                :href="publication.open_access.oa_url"
                target="_blank"
                rel="noopener noreferrer"
              >
                Read publication
                <span class="visually-hidden">(opens in a new tab)</span>
              </a>
            </dd>
          </div>
        </dl>
      </section>

      <!-- Concepts -->
      <section
        id="concepts"
        class="detail-section"
        aria-labelledby="concepts-heading"
        tabindex="-1"
      >
        <h2 id="concepts-heading">Concepts</h2>

        <ul v-if="publication.concepts?.length" class="tags">
          <li
            v-for="concept in publication.concepts"
            :key="concept.id"
            class="tag"
          >
            {{ concept.display_name }}
          </li>
        </ul>

        <p v-else>No concepts available.</p>
      </section>

      <!-- Topics -->
      <section
        id="topics"
        class="detail-section"
        aria-labelledby="topics-heading"
        tabindex="-1"
      >
        <h2 id="topics-heading">Topics</h2>

        <ul v-if="publication.topics?.length" class="tags">
          <li
            v-for="topic in publication.topics"
            :key="topic.id"
            class="tag"
          >
            {{ topic.display_name }}
          </li>
        </ul>

        <p v-else>No topics available.</p>
      </section>

      <!-- Publication source -->
      <section
        v-if="publication.primary_location"
        id="publication-source"
        class="detail-section"
        aria-labelledby="source-heading"
        tabindex="-1"
      >
        <h2 id="source-heading">Publication source</h2>

        <p>
          {{
            publication.primary_location.source?.display_name
            || 'Unknown source'
          }}
        </p>

        <a
          v-if="publication.primary_location.landing_page_url"
          :href="publication.primary_location.landing_page_url"
          target="_blank"
          rel="noopener noreferrer"
        >
          Visit publication page
          <span class="visually-hidden">(opens in a new tab)</span>
        </a>
      </section>

    </article>
  </main>
</template>
