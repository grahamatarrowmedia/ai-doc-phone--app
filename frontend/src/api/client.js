const API_BASE = '/api'

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
    config.body = JSON.stringify(config.body)
  }

  if (config.body instanceof FormData) {
    delete config.headers['Content-Type']
  }

  const response = await fetch(url, config)

  if (!response.ok) {
    const error = await response.json().catch(() => ({ message: 'Request failed' }))
    throw new Error(error.message || error.error || 'Request failed')
  }

  return response.json()
}

// Projects
export const getProjects = () => request('/projects')
export const getProject = (id) => request(`/projects/${id}`)
export const createProject = (data) => request('/projects', { method: 'POST', body: data })
export const updateProject = (id, data) => request(`/projects/${id}`, { method: 'PUT', body: data })
export const deleteProject = (id) => request(`/projects/${id}`, { method: 'DELETE' })

// Series
export const getSeries = (projectId) => request(`/projects/${projectId}/series`)
export const createSeries = (projectId, data) => request(`/projects/${projectId}/series`, { method: 'POST', body: data })
export const updateSeries = (projectId, seriesId, data) => request(`/projects/${projectId}/series/${seriesId}`, { method: 'PUT', body: data })
export const deleteSeries = (projectId, seriesId) => request(`/projects/${projectId}/series/${seriesId}`, { method: 'DELETE' })

// Episodes
export const getEpisodes = (projectId, seriesId) => request(`/projects/${projectId}/series/${seriesId}/episodes`)
export const createEpisode = (projectId, seriesId, data) => request(`/projects/${projectId}/series/${seriesId}/episodes`, { method: 'POST', body: data })
export const updateEpisode = (projectId, seriesId, episodeId, data) => request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}`, { method: 'PUT', body: data })
export const deleteEpisode = (projectId, seriesId, episodeId) => request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}`, { method: 'DELETE' })

// Research
export const getResearchReports = (projectId, seriesId, episodeId) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/research`)
export const getResearchReport = (projectId, seriesId, episodeId, reportId) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/research/${reportId}`)
export const createResearch = (projectId, seriesId, episodeId, data) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/research`, { method: 'POST', body: data })
export const updateResearch = (projectId, seriesId, episodeId, reportId, data) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/research/${reportId}`, { method: 'PUT', body: data })
export const markResearchComplete = (projectId, seriesId, episodeId, reportId) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/research/${reportId}/complete`, { method: 'POST' })
export const linkAssetToResearch = (projectId, seriesId, episodeId, reportId, assetData) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/research/${reportId}/link-asset`, { method: 'POST', body: assetData })

// Knowledge Base
export const getKnowledgeBase = (projectId, seriesId, episodeId) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/knowledge-base`)
export const addToKnowledgeBase = (projectId, seriesId, episodeId, data) =>
  request(`/projects/${projectId}/series/${seriesId}/episodes/${episodeId}/knowledge-base`, { method: 'POST', body: data })

// File Upload
export const uploadFile = (formData) => request('/upload', { method: 'POST', body: formData })
