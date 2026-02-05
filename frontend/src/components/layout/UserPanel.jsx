import { useProject } from '../../context/ProjectContext'

export default function UserPanel() {
  const { user } = useProject()

  return (
    <div className="flex items-center gap-3 px-4 py-3 bg-bg-secondary rounded-lg">
      <div className="w-8 h-8 rounded-full bg-accent-red flex items-center justify-center text-white font-bold text-sm">
        {user?.name?.charAt(0) || 'U'}
      </div>
      <div>
        <p className="text-sm font-medium text-text-primary">{user?.name || 'User'}</p>
        <p className="text-[10px] text-text-tertiary font-mono uppercase">{user?.role || 'Producer'}</p>
      </div>
    </div>
  )
}
