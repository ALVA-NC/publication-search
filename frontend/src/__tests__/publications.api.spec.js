import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'

import { searchPublications, getPublication } from '../api/publications'

describe('api/publications', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  describe('searchPublications', () => {
    it('builds the query string and returns the parsed results', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          results: [{ id: 'W1' }],
          pagination: { page: 2, per_page: 10, total: 1, total_pages: 1 }
        })
      })

      const data = await searchPublications({ q: 'climate', page: 2, perPage: 10 })

      expect(fetch).toHaveBeenCalledWith(
        '/api/publications?q=climate&page=2&per_page=10'
      )
      expect(data.results).toHaveLength(1)
    })

    it('omits empty filters and uses defaults', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ results: [], pagination: {} })
      })

      await searchPublications({})

      expect(fetch).toHaveBeenCalledWith('/api/publications?page=1&per_page=20')
    })

    it('throws when the response is not ok', async () => {
      fetch.mockResolvedValueOnce({ ok: false, status: 500, json: async () => ({}) })

      await expect(searchPublications({ q: 'x' })).rejects.toThrow(
        'Failed to retrieve publications'
      )
    })
  })

  describe('getPublication', () => {
    it('fetches and returns the publication', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'W1', title: 'Hello' })
      })

      const publication = await getPublication('W1')

      expect(fetch).toHaveBeenCalledWith('/api/publications/W1')
      expect(publication.title).toBe('Hello')
    })

    it('encodes the id in the request', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'a/b', title: 'X' })
      })

      await getPublication('a/b')

      expect(fetch).toHaveBeenCalledWith('/api/publications/a%2Fb')
    })

    it('throws a specific error on 404', async () => {
      fetch.mockResolvedValueOnce({ ok: false, status: 404, json: async () => ({}) })

      await expect(getPublication('missing')).rejects.toThrow('Publication not found')
    })

    it('throws a generic error on other failures', async () => {
      fetch.mockResolvedValueOnce({ ok: false, status: 500, json: async () => ({}) })

      await expect(getPublication('W1')).rejects.toThrow('Failed to retrieve publication')
    })
  })
})
