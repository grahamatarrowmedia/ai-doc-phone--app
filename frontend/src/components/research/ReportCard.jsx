const STATUS_COLORS = {
  deep_research: 'bg-accent-red',
  in_progress: 'bg-accent-orange',
  complete: 'bg-accent-green'
}

const STATUS_LABELS = {
  deep_research: 'Deep Research',
  in_progress: 'In Progress',
  complete: 'Complete'
}

export default function ReportCard({ report, isSelected, onClick }) {
  const statusColor = STATUS_COLORS[report.status] || STATUS_COLORS.in_progress

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-lg transition-colors ${
        isSelected
          ? 'bg-bg-elevated ring-1 ring-accent-red'
          : 'bg-bg-secondary hover:bg-bg-elevated'
      }`}
    >
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-medium text-text-primary text-sm line-clamp-2 pr-2">
          {report.title}
        </h4>
        <button className="text-text-tertiary hover:text-text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
          </svg>
        </button>
      </div>

      {report.executive_summary && (
        <p className="text-xs text-text-secondary line-clamp-2 mb-3">
          {report.executive_summary}
        </p>
      )}

      {/* Status bar */}
      <div className="flex items-center gap-2">
        <div className={`h-1 flex-1 rounded-full ${statusColor}`} />
        <span className="text-[10px] font-mono uppercase text-text-tertiary">
          {STATUS_LABELS[report.status] || report.status}
        </span>
      </div>
    </button>
  )
}
