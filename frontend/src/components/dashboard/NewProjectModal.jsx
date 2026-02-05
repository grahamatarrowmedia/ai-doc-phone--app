import { useState } from 'react'

export default function NewProjectModal({ isOpen, onClose, onCreate }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [type, setType] = useState('DOCUMENTARY')
  const [loading, setLoading] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim()) return

    setLoading(true)
    try {
      await onCreate({
        name: name.trim(),
        description: description.trim(),
        type
      })
      setName('')
      setDescription('')
      onClose()
    } catch (err) {
      console.error('Failed to create project:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-bg-secondary rounded-xl p-6 w-full max-w-md">
        <h2 className="text-xl font-heading font-bold text-text-primary mb-4">
          New Project
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-mono uppercase text-text-tertiary mb-1">
              Project Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 bg-bg-input border border-border-subtle rounded-lg text-text-primary focus:outline-none focus:border-accent-red"
              placeholder="e.g., Declassified"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-mono uppercase text-text-tertiary mb-1">
              Type
            </label>
            <select
              value={type}
              onChange={(e) => setType(e.target.value)}
              className="w-full px-3 py-2 bg-bg-input border border-border-subtle rounded-lg text-text-primary focus:outline-none focus:border-accent-red"
            >
              <option value="DOCUMENTARY">Documentary</option>
              <option value="SERIES">Series</option>
              <option value="FEATURE">Feature</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-mono uppercase text-text-tertiary mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 bg-bg-input border border-border-subtle rounded-lg text-text-primary focus:outline-none focus:border-accent-red resize-none"
              rows={3}
              placeholder="Brief description of the project..."
            />
          </div>

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 bg-bg-input text-text-secondary rounded-lg hover:bg-border-medium transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !name.trim()}
              className="flex-1 px-4 py-2 bg-accent-red text-white rounded-lg hover:bg-accent-red-dark transition-colors disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
