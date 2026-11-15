import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import SearchBar from '../components/SearchBar.vue'

describe('SearchBar', () => {
  it('renders a search input and a submit button', () => {
    const wrapper = mount(SearchBar)

    expect(wrapper.find('input[type="search"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('emits "search" with the trimmed query on submit', async () => {
    const wrapper = mount(SearchBar)

    await wrapper.find('input').setValue('   climate change   ')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('search')).toBeTruthy()
    expect(wrapper.emitted('search')[0]).toEqual(['climate change'])
  })

  it('emits an empty string when the query is blank', async () => {
    const wrapper = mount(SearchBar)

    await wrapper.find('input').setValue('   ')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('search')[0]).toEqual([''])
  })
})
