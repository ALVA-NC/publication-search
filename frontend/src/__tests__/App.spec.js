import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'

import App from '../App.vue'

describe('App', () => {
  it('renders the skip link', () => {
    const wrapper = mount(App, {
      global: {
        stubs: { RouterView: true }
      }
    })

    const skipLink = wrapper.find('.skip-link')
    expect(skipLink.exists()).toBe(true)
    expect(skipLink.text()).toBe('Skip to main content')
    expect(skipLink.attributes('href')).toBe('#main-content')
  })
})
