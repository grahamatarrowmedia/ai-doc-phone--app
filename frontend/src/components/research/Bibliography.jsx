import { useState } from 'react'

export default function Bibliography({ bibliography }) {
  const [expanded, setExpanded] = useState(false)

  const aiSources = bibliography?.ai_generated || []
  const externalSources = bibliography?.external || []
  const totalSources = aiSources.length + externalSources.length

  if (totalSources === 0) {
    return null
  }

  return (
    <div className="mb-6">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 text-xs font-heading font-bold uppercase text-accent-red tracking-wider mb-3"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={2}
          stroke="currentColor"
          className={`w-4 h-4 transition-transform ${expanded ? 'rotate-90' : ''}`}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
        </svg>
        Bibliography & Sources ({totalSources})
      </button>

      {expanded && (
        <div className="space-y-4 pl-6">
          {aiSources.length > 0 && (
            <div>
              <span className="inline-block px-2 py-0.5 bg-accent-red text-white text-[10px] font-mono uppercase rounded mb-2">
                AI Generated
              </span>
              <ul className="list-decimal list-inside space-y-1">
                {aiSources.map((source, index) => (
                  <li key={index} className="text-sm text-text-detail">
                    {source}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {externalSources.length > 0 && (
            <div>
              <span className="inline-block px-2 py-0.5 bg-accent-blue text-white text-[10px] font-mono uppercase rounded mb-2">
                External References
              </span>
              <ul className="list-decimal list-inside space-y-1">
                {externalSources.map((source, index) => (
                  <li key={index} className="text-sm text-text-detail">
                    {source.startsWith('http') ? (
                      <a
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-accent-blue hover:underline"
                      >
                        {source}
                      </a>
                    ) : (
                      source
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
