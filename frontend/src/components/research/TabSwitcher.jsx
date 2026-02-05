export default function TabSwitcher({ activeTab, onTabChange, briefsCount, kbCount }) {
  return (
    <div className="flex border-b border-border-subtle">
      <button
        onClick={() => onTabChange('briefs')}
        className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
          activeTab === 'briefs'
            ? 'text-accent-red border-b-2 border-accent-red'
            : 'text-text-secondary hover:text-text-primary'
        }`}
      >
        AI Briefs
        {briefsCount > 0 && (
          <span className="ml-2 px-1.5 py-0.5 bg-bg-input rounded text-xs font-mono">
            {briefsCount}
          </span>
        )}
      </button>
      <button
        onClick={() => onTabChange('knowledge')}
        className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${
          activeTab === 'knowledge'
            ? 'text-accent-red border-b-2 border-accent-red'
            : 'text-text-secondary hover:text-text-primary'
        }`}
      >
        Knowledge Base
        {kbCount > 0 && (
          <span className="ml-2 px-1.5 py-0.5 bg-bg-input rounded text-xs font-mono">
            {kbCount}
          </span>
        )}
      </button>
    </div>
  )
}
