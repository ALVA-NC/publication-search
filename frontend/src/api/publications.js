
const API_BASE_URL = '/api'

export async function searchPublications({
  q = '',
  author = '',
  institution = '',
  country = '',
  concept = '',
  page = 1,
  perPage = 20
} = {}) {
  const params = new URLSearchParams()

  if (q) params.append('q', q)
  if (author) params.append('author', author)
  if (institution) params.append('institution', institution)
  if (country) params.append('country', country)
  if (concept) params.append('concept', concept)

  params.append('page', page)
  params.append('per_page', perPage)

  const response = await fetch(
    `${API_BASE_URL}/publications?${params.toString()}`
  )

  if (!response.ok) {
    throw new Error('Failed to retrieve publications')
  }

  return response.json()
}

export async function getPublication(id) {
  const response = await fetch(
    `${API_BASE_URL}/publications/${encodeURIComponent(id)}`
  )

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Publication not found')
    }

    throw new Error('Failed to retrieve publication')
  }

  return response.json()
}
