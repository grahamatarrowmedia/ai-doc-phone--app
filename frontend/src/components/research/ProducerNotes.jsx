import { useState, useEffect } from 'react'

export default function ProducerNotes({ notes, onSave }) {
  const [value, setValue] = useState(notes || '')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    setValue(notes || '')
  }, [notes])

  const handleSave = async () => {
    setSaving(true)
    try {
      await onSave(value)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="mb-6">
      <h3 className="text-xs font-heading font-bold uppercase text-accent-red tracking-wider mb-3">
        Producer Notes & Annotations
      </h3>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Add your notes and annotations here..."
        className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-text-detail font-body resize-none focus:outline-none focus:ring-2 focus:ring-accent-red/20"
        rows={4}
      />
      {value !== notes && (
        <button
          onClick={handleSave}
          disabled={saving}
          className="mt-2 px-4 py-1.5 bg-text-detail text-white text-sm rounded hover:bg-text-detail-muted transition-colors disabled:opacity-50"
        >
          {saving ? 'Saving...' : 'Save Notes'}
        </button>
      )}
    </div>
  )
}
