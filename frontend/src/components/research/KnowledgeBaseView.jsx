const CONFIDENCE_COLORS = {
  high: 'bg-accent-green/20 text-accent-green',
  medium: 'bg-accent-orange/20 text-accent-orange',
  low: 'bg-accent-red/20 text-accent-red'
}

const CATEGORY_LABELS = {
  person: 'Person',
  event: 'Event',
  location: 'Location',
  general: 'General'
}

export default function KnowledgeBaseView({ entries, loading }) {
  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="w-6 h-6 border-2 border-accent-red border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!entries || entries.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-bg-elevated flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-text-tertiary">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
            </svg>
          </div>
          <h3 className="text-lg font-heading font-semibold text-text-primary mb-2">
            Knowledge Base Empty
          </h3>
          <p className="text-sm text-text-tertiary">
            Complete research reports to build up verified facts.
          </p>
        </div>
      </div>
    )
  }

  // Group by category
  const grouped = entries.reduce((acc, entry) => {
    const cat = entry.category || 'general'
    if (!acc[cat]) acc[cat] = []
    acc[cat].push(entry)
    return acc
  }, {})

  return (
    <div className="flex-1 overflow-auto p-4">
      <div className="mb-4">
        <p className="text-sm text-text-secondary">
          <span className="font-mono text-accent-green">{entries.length}</span> verified facts
        </p>
      </div>

      {Object.entries(grouped).map(([category, items]) => (
        <div key={category} className="mb-6">
          <h3 className="text-xs font-mono uppercase tracking-wider text-text-tertiary mb-2">
            {CATEGORY_LABELS[category] || category} ({items.length})
          </h3>
          <div className="space-y-2">
            {items.map((entry) => (
              <div
                key={entry.id}
                className="p-3 bg-bg-secondary rounded-lg"
              >
                <p className="text-sm text-text-primary mb-2">
                  {entry.fact}
                </p>
                <div className="flex items-center gap-2">
                  {entry.confidence && (
                    <span className={`px-1.5 py-0.5 text-[10px] font-mono uppercase rounded ${CONFIDENCE_COLORS[entry.confidence]}`}>
                      {entry.confidence}
                    </span>
                  )}
                  {entry.source_indices && entry.source_indices.length > 0 && (
                    <span className="text-xs font-mono text-accent-blue">
                      [{entry.source_indices.join(', ')}]
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
