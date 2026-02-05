import ProducerNotes from './ProducerNotes'
import LinkedAssets from './LinkedAssets'
import Bibliography from './Bibliography'

const CONFIDENCE_COLORS = {
  high: 'text-accent-green',
  medium: 'text-accent-orange',
  low: 'text-accent-red'
}

export default function ReportDetail({ report, episode, onMarkComplete, onUpdateNotes, onLinkAsset }) {
  if (!report) {
    return (
      <div className="flex-1 bg-bg-detail flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-200 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8 text-gray-400">
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
          </div>
          <p className="text-text-detail-muted">
            Select a research report to view details
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 bg-bg-detail overflow-auto detail-panel">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <h2 className="text-xl font-heading font-bold text-text-detail flex-1 pr-4">
            {report.title}
          </h2>
          <div className="flex items-center gap-2">
            <button className="px-3 py-1.5 bg-text-detail text-white text-sm rounded hover:bg-text-detail-muted transition-colors flex items-center gap-1">
              Deep Research
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
            <button
              onClick={onMarkComplete}
              className={`px-3 py-1.5 text-sm rounded flex items-center gap-1 transition-colors ${
                report.status === 'complete'
                  ? 'bg-accent-green text-white'
                  : 'bg-gray-200 text-text-detail hover:bg-gray-300'
              }`}
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
              {report.status === 'complete' ? 'Completed' : 'Mark Complete'}
            </button>
          </div>
        </div>

        {/* Linked Episode */}
        <p className="text-sm text-text-detail-muted mb-6">
          Linked to: <span className="font-medium">{episode?.title || 'Unknown'}</span>
        </p>

        {/* Executive Summary */}
        <div className="mb-6">
          <h3 className="text-xs font-heading font-bold uppercase text-accent-red tracking-wider mb-3">
            Executive Summary
          </h3>
          <p className="text-text-detail font-body leading-relaxed">
            {report.executive_summary || 'No summary available.'}
          </p>
        </div>

        {/* Key Findings */}
        {report.key_findings && report.key_findings.length > 0 && (
          <div className="mb-6">
            <h3 className="text-xs font-heading font-bold uppercase text-accent-red tracking-wider mb-3">
              Key Findings
            </h3>
            <ul className="space-y-3">
              {report.key_findings.map((finding, index) => (
                <li key={index} className="flex items-start gap-2">
                  <span className="text-accent-red mt-1">•</span>
                  <div className="flex-1">
                    <span className="font-bold text-text-detail">"{finding.name}"</span>
                    <span className="text-text-detail"> — {finding.description}</span>
                    {finding.source_indices && finding.source_indices.length > 0 && (
                      <span className="text-accent-blue font-mono text-sm ml-1">
                        [{finding.source_indices.join(', ')}]
                      </span>
                    )}
                    {finding.confidence && (
                      <span className={`ml-2 text-xs font-mono uppercase ${CONFIDENCE_COLORS[finding.confidence]}`}>
                        [{finding.confidence}]
                      </span>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Producer Notes */}
        <ProducerNotes
          notes={report.producer_notes}
          onSave={(notes) => onUpdateNotes(report.id, notes)}
        />

        {/* Linked Assets */}
        <LinkedAssets
          assets={report.linked_assets}
          onLinkAsset={() => onLinkAsset(report.id)}
        />

        {/* Bibliography */}
        <Bibliography bibliography={report.bibliography} />
      </div>
    </div>
  )
}
