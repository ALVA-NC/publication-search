import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import PublicationFilters from '../components/PublicationFilters.vue'

describe('PublicationFilters', () => {
  it('renders the four filter inputs', () => {
    const wrapper = mount(PublicationFilters)

    expect(wrapper.findAll('input').length).toBe(4)
    expect(wrapper.find('.apply-button').exists()).toBe(true)
    expect(wrapper.find('.clear-button').exists()).toBe(true)
  })

  it('emits "filter" with the current values on apply', async () => {
    const wrapper = mount(PublicationFilters)
    const inputs = wrapper.findAll('input')

    await inputs[0].setValue('Ada Lovelace') // author
    await inputs[2].setValue('DK') // country

    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('filter')).toBeTruthy()
    expect(wrapper.emitted('filter')[0]).toEqual([
      { author: 'Ada Lovelace', institution: '', country: 'DK', concept: '' }
    ])
  })

  it('emits empty filters when cleared', async () => {
    const wrapper = mount(PublicationFilters)
    const inputs = wrapper.findAll('input')

    await inputs[0].setValue('Someone')
    await wrapper.find('.clear-button').trigger('click')

    expect(wrapper.emitted('filter')).toBeTruthy()
    expect(wrapper.emitted('filter').at(-1)).toEqual([
      { author: '', institution: '', country: '', concept: '' }
    ])
  })
})
