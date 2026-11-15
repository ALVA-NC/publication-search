import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'

import PublicationCard from '../components/PublicationCard.vue'

const basePublication = {
  id: 'https://openalex.org/W123',
  title: 'A Study of Things',
  author_names: ['Alice', 'Bob'],
  institution_names: ['MIT'],
  publication_date: '2025-01-01',
  cited_by_count: 42,
  concept_names: ['Physics', 'Math', 'Chem', 'Bio'],
  abstract: 'This is a long abstract. '.repeat(20)
}

function mountCard(overrides = {}) {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/:pathMatch(.*)*', component: { render: () => null } }
    ]
  })

  return mount(PublicationCard, {
    props: { publication: { ...basePublication, ...overrides } },
    global: {
      plugins: [router]
    }
  })
}

describe('PublicationCard', () => {
  it('renders the title, authors, date and citation count', () => {
    const wrapper = mountCard()

    expect(wrapper.text()).toContain('A Study of Things')
    expect(wrapper.text()).toContain('Alice, Bob')
    expect(wrapper.text()).toContain('2025-01-01')
    expect(wrapper.text()).toContain('42 citations')
  })

  it('falls back to placeholder text when fields are missing', () => {
    const wrapper = mountCard({
      title: '',
      author_names: [],
      cited_by_count: undefined
    })

    expect(wrapper.text()).toContain('Untitled publication')
    expect(wrapper.text()).toContain('Authors unavailable')
    expect(wrapper.text()).not.toContain('citations')
  })

  it('limits the displayed concepts to three', () => {
    const wrapper = mountCard()

    const tags = wrapper.findAll('.tag')
    expect(tags.length).toBe(3)
    expect(wrapper.text()).toContain('Physics')
    expect(wrapper.text()).not.toContain('Bio')
  })

  it('truncates the abstract', () => {
    const wrapper = mountCard()
    const abstract = wrapper.find('.abstract')

    expect(abstract.exists()).toBe(true)
    expect(abstract.text()).toContain(basePublication.abstract.slice(0, 100))
    expect(abstract.text().length).toBeLessThan(basePublication.abstract.length)
  })

  it('does not render an abstract block when there is no abstract', () => {
    const wrapper = mountCard({ abstract: null })

    expect(wrapper.find('.abstract').exists()).toBe(false)
  })
})
