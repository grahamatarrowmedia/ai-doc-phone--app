import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import * as api from '../api/client'

const ProjectContext = createContext(null)

export function ProjectProvider({ children }) {
  const [projects, setProjects] = useState([])
  const [currentProject, setCurrentProject] = useState(null)
  const [currentSeries, setCurrentSeries] = useState(null)
  const [currentEpisode, setCurrentEpisode] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // User info (could come from auth later)
  const [user] = useState({ name: 'Felix', role: 'PRODUCER' })

  const fetchProjects = useCallback(async () => {
    try {
      setLoading(true)
      const data = await api.getProjects()
      setProjects(data.projects || [])
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  const selectProject = useCallback(async (projectId) => {
    if (!projectId) {
      setCurrentProject(null)
      setCurrentSeries(null)
      setCurrentEpisode(null)
      return
    }
    try {
      const data = await api.getProject(projectId)
      setCurrentProject(data)
      setCurrentSeries(null)
      setCurrentEpisode(null)
    } catch (err) {
      setError(err.message)
    }
  }, [])

  const selectSeries = useCallback((series) => {
    setCurrentSeries(series)
    setCurrentEpisode(null)
  }, [])

  const selectEpisode = useCallback((episode) => {
    setCurrentEpisode(episode)
  }, [])

  const createProject = useCallback(async (data) => {
    const result = await api.createProject(data)
    await fetchProjects()
    return result
  }, [fetchProjects])

  useEffect(() => {
    fetchProjects()
  }, [fetchProjects])

  const value = {
    projects,
    currentProject,
    currentSeries,
    currentEpisode,
    user,
    loading,
    error,
    fetchProjects,
    selectProject,
    selectSeries,
    selectEpisode,
    createProject,
  }

  return (
    <ProjectContext.Provider value={value}>
      {children}
    </ProjectContext.Provider>
  )
}

export function useProject() {
  const context = useContext(ProjectContext)
  if (!context) {
    throw new Error('useProject must be used within a ProjectProvider')
  }
  return context
}
