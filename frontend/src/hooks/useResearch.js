import { useState, useCallback } from 'react'
import * as api from '../api/client'

export function useResearch(projectId, seriesId, episodeId) {
  const [reports, setReports] = useState([])
  const [knowledgeBase, setKnowledgeBase] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchReports = useCallback(async () => {
    if (!projectId || !seriesId || !episodeId) return
    try {
      setLoading(true)
      setError(null)
      const data = await api.getResearchReports(projectId, seriesId, episodeId)
      setReports(data.reports || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [projectId, seriesId, episodeId])

  const fetchKnowledgeBase = useCallback(async () => {
    if (!projectId || !seriesId || !episodeId) return
    try {
      const data = await api.getKnowledgeBase(projectId, seriesId, episodeId)
      setKnowledgeBase(data.entries || [])
    } catch (err) {
      console.error('Failed to fetch KB:', err)
    }
  }, [projectId, seriesId, episodeId])

  const createResearch = useCallback(async (query, attachedFiles = []) => {
    if (!projectId || !seriesId || !episodeId) {
      throw new Error('Missing required IDs')
    }
    const result = await api.createResearch(projectId, seriesId, episodeId, {
      query,
      attached_files: attachedFiles
    })
    await fetchReports()
    return result
  }, [projectId, seriesId, episodeId, fetchReports])

  const markComplete = useCallback(async (reportId) => {
    await api.markResearchComplete(projectId, seriesId, episodeId, reportId)
    await fetchReports()
  }, [projectId, seriesId, episodeId, fetchReports])

  const updateNotes = useCallback(async (reportId, notes) => {
    await api.updateResearch(projectId, seriesId, episodeId, reportId, {
      producer_notes: notes
    })
    await fetchReports()
  }, [projectId, seriesId, episodeId, fetchReports])

  const linkAsset = useCallback(async (reportId, assetData) => {
    await api.linkAssetToResearch(projectId, seriesId, episodeId, reportId, assetData)
    await fetchReports()
  }, [projectId, seriesId, episodeId, fetchReports])

  const addToKB = useCallback(async (factData) => {
    await api.addToKnowledgeBase(projectId, seriesId, episodeId, factData)
    await fetchKnowledgeBase()
  }, [projectId, seriesId, episodeId, fetchKnowledgeBase])

  return {
    reports,
    knowledgeBase,
    loading,
    error,
    fetchReports,
    fetchKnowledgeBase,
    createResearch,
    markComplete,
    updateNotes,
    linkAsset,
    addToKB
  }
}
