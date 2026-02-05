export default function ActiveContext({ episode }) {
  if (!episode) {
    return (
      <div className="px-4 py-3 border-b border-border-subtle">
        <p className="text-[10px] font-mono uppercase tracking-wider text-text-tertiary">
          Active Context
        </p>
        <p className="text-sm text-text-secondary italic mt-1">
          Select an episode to begin research
        </p>
      </div>
    )
  }

  return (
    <div className="px-4 py-3 border-b border-border-subtle">
      <p className="text-[10px] font-mono uppercase tracking-wider text-text-tertiary">
        Active Context
      </p>
      <p className="text-sm text-text-primary font-medium mt-1">
        <span className="text-accent-blue font-mono mr-2">{episode.code}</span>
        {episode.title}
      </p>
    </div>
  )
}
