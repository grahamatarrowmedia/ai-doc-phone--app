import { Link } from 'react-router-dom'

const PHASE_LABELS = {
  research: 'Research',
  archive: 'Archive',
  scripting: 'Script',
  interviews: 'Interviews',
  voiceover: 'Voice Over',
  assembly: 'Assembly',
  review: 'Review'
}

export default function ProjectCard({ project }) {
  const phase = project.current_phase || 'research'
  const progress = project.phase_progress || 0

  return (
    <Link
      to={`/project/${project.id}/research`}
      className="block bg-bg-secondary rounded-xl p-5 hover:bg-bg-elevated transition-colors group"
    >
      {/* Type badge */}
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-mono uppercase tracking-wider text-text-tertiary">
          {project.type || 'Documentary'}
        </span>
        {project.editing && (
          <span className="text-[10px] font-mono uppercase px-2 py-0.5 bg-accent-orange/20 text-accent-orange rounded">
            Editing
          </span>
        )}
      </div>

      {/* Title */}
      <h3 className="text-lg font-heading font-bold text-accent-red group-hover:text-accent-red-dark transition-colors mb-2">
        {project.name}
      </h3>

      {/* Description */}
      <p className="text-sm text-text-secondary line-clamp-2 mb-4">
        {project.description || 'No description'}
      </p>

      {/* Progress */}
      <div className="flex items-center gap-3">
        <span className="text-xs font-mono text-text-tertiary uppercase">
          {PHASE_LABELS[phase] || phase}
        </span>
        <div className="flex-1 progress-bar">
          <div
            className="progress-bar-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-xs font-mono text-text-tertiary">
          {progress}%
        </span>
      </div>
    </Link>
  )
}
