import { useState, useEffect } from 'react'
import * as api from '../../api/client'

export default function SeriesSelector({ projectId, selectedSeries, onSelect }) {
  const [series, setSeries] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [newTitle, setNewTitle] = useState('')

  useEffect(() => {
    if (projectId) {
      fetchSeries()
    }
  }, [projectId])

  const fetchSeries = async () => {
    try {
      setLoading(true)
      const data = await api.getSeries(projectId)
      setSeries(data.series || [])
    } catch (err) {
      console.error('Failed to fetch series:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddSeries = async (e) => {
    e.preventDefault()
    if (!newTitle.trim()) return

    try {
      await api.createSeries(projectId, { title: newTitle.trim() })
      setNewTitle('')
      setShowAdd(false)
      fetchSeries()
    } catch (err) {
      console.error('Failed to create series:', err)
    }
  }

  return (
    <div className="mb-6">
      <h3 className="text-[10px] font-mono uppercase tracking-wider text-text-tertiary mb-2 px-1">
        1. Select Series
      </h3>

      {loading ? (
        <div className="px-3 py-2 text-sm text-text-tertiary">Loading...</div>
      ) : (
        <div className="space-y-1">
          {series.map((s) => (
            <button
              key={s.id}
              onClick={() => onSelect(s)}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-left transition-colors ${
                selectedSeries?.id === s.id
                  ? 'bg-bg-elevated text-accent-red'
                  : 'text-text-secondary hover:bg-bg-elevated hover:text-text-primary'
              }`}
            >
              <span className={`w-2 h-2 rounded-full ${selectedSeries?.id === s.id ? 'bg-accent-red' : 'bg-text-tertiary'}`} />
              {s.title}
            </button>
          ))}

          {showAdd ? (
            <form onSubmit={handleAddSeries} className="px-1 pt-2">
              <input
                type="text"
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                placeholder="Series title..."
                className="w-full px-3 py-2 bg-bg-input border border-border-subtle rounded text-sm text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-red"
                autoFocus
              />
              <div className="flex gap-2 mt-2">
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
              Add Series...
            </button>
          )}
        </div>
      )}
    </div>
  )
}
