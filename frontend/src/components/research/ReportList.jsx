import ReportCard from './ReportCard'

export default function ReportList({ reports, selectedReport, onSelectReport, onNewResearch, loading }) {
  return (
    <div className="flex-1 overflow-auto p-4">
      {/* New Research Button */}
      <button
        onClick={onNewResearch}
        className="w-full mb-4 px-4 py-3 bg-accent-red text-white rounded-lg hover:bg-accent-red-dark transition-colors flex items-center justify-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        New Research
      </button>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="w-6 h-6 border-2 border-accent-red border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Reports */}
      {!loading && (
        <div className="space-y-3">
          {reports.map((report) => (
            <ReportCard
              key={report.id}
              report={report}
              isSelected={selectedReport?.id === report.id}
              onClick={() => onSelectReport(report)}
            />
          ))}

          {reports.length === 0 && (
            <div className="text-center py-8">
              <p className="text-sm text-text-tertiary">
                No research reports yet.
              </p>
              <p className="text-xs text-text-tertiary mt-1">
                Click "New Research" to begin.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
