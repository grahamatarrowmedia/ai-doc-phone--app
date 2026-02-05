import { useState, useEffect } from 'react'
import * as api from '../../api/client'

export default function EpisodeSelector({ projectId, seriesId, selectedEpisode, onSelect }) {
  const [episodes, setEpisodes] = useState([])
  const [loading, setLoading] = useState(false)
  const [showAdd, setShowAdd] = useState(false)
  const [newTitle, setNewTitle] = useState('')
  const [newCode, setNewCode] = useState('')

  useEffect(() => {
    if (projectId && seriesId) {
      fetchEpisodes()
    } else {
      setEpisodes([])
    }
  }, [projectId, seriesId])

  const fetchEpisodes = async () => {
    try {
      setLoading(true)
      const data = await api.getEpisodes(projectId, seriesId)
      setEpisodes(data.episodes || [])
    } catch (err) {
      console.error('Failed to fetch episodes:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddEpisode = async (e) => {
    e.preventDefault()
    if (!newTitle.trim()) return

    try {
      const episodeNum = episodes.length + 1
      await api.createEpisode(projectId, seriesId, {
        title: newTitle.trim(),
        code: newCode.trim() || `EP${String(episodeNum).padStart(2, '0')}`
      })
      setNewTitle('')
      setNewCode('')
      setShowAdd(false)
      fetchEpisodes()
    } catch (err) {
      console.error('Failed to create episode:', err)
    }
  }

  if (!seriesId) {
    return (
      <div className="mb-6">
        <h3 className="text-[10px] font-mono uppercase tracking-wider text-text-tertiary mb-2 px-1">
          2. Select Episode
        </h3>
        <p className="px-3 py-2 text-sm text-text-tertiary italic">
          Select a series first
        </p>
      </div>
    )
  }

  return (
    <div className="mb-6">
      <h3 className="text-[10px] font-mono uppercase tracking-wider text-text-tertiary mb-2 px-1">
        2. Select Episode
      </h3>

      {loading ? (
        <div className="px-3 py-2 text-sm text-text-tertiary">Loading...</div>
      ) : (
        <div className="space-y-1">
          {episodes.map((ep) => (
            <button
              key={ep.id}
              onClick={() => onSelect(ep)}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-left transition-colors ${
                selectedEpisode?.id === ep.id
                  ? 'bg-bg-elevated text-text-primary'
                  : 'text-text-secondary hover:bg-bg-elevated hover:text-text-primary'
              }`}
            >
              <span className="font-mono text-accent-blue text-xs">{ep.code}</span>
              <span className="truncate">{ep.title}</span>
            </button>
          ))}

          {showAdd ? (
            <form onSubmit={handleAddEpisode} className="px-1 pt-2 space-y-2">
              <input
                type="text"
                value={newCode}
                onChange={(e) => setNewCode(e.target.value)}
                placeholder="EP01"
                className="w-20 px-2 py-1 bg-bg-input border border-border-subtle rounded text-xs font-mono text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-red"
              />
              <input
                type="text"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="Episode title..."
                className="w-full px-3 py-2 bg-bg-input border border-border-subtle rounded text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-red"
                autoFocus
              />
              <div className="flex gap-2">
                <button
                  type="submit"
                  className="flex-1 px-3 py-1 bg-accent-red text-white text-xs rounded hover:bg-accent-red-dark"
                >
                  Add
                </button>
                <button
                  type="button"
                  onClick={() => setShowAdd(false)}
                  className="flex-1 px-3 py-1 bg-bg-input text-text-secondary text-xs rounded hover:bg-border-medium"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <button
              onClick={() => setShowAdd(true)}
              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-text-tertiary hover:bg-bg-elevated hover:text-text-primary transition-colors"
            >
              <span className="w-4 h-4 flex items-center justify-center">+</span>
              Add Episode...
            </button>
          )}
        </div>
      )}
    </div>
  )
}
