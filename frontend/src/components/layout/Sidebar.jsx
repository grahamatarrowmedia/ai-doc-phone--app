import { NavLink, useLocation } from 'react-router-dom'
import { useProject } from '../../context/ProjectContext'

const WORKFLOW_PHASES = [
  { id: 'research', label: '1. Research', num: 1 },
  { id: 'archive', label: '2. Archive', num: 2 },
  { id: 'scripting', label: '3. Script', num: 3 },
  { id: 'interviews', label: '3b. Interviews', num: 3.5 },
  { id: 'voiceover', label: '4. Voice Over', num: 4 },
  { id: 'assembly', label: '5. Assembly', num: 5 },
  { id: 'review', label: '6. Review', num: 6 },
]

export default function Sidebar() {
  const { user, currentProject } = useProject()
  const location = useLocation()
  const isInProject = location.pathname.includes('/project/')

  return (
    <aside className="w-60 bg-bg-sidebar border-r border-border-subtle flex flex-col h-full">
      {/* Logo */}
      <div className="p-4 border-b border-border-subtle">
        <div className="flex items-center gap-2">
          <span className="text-accent-red font-heading font-bold text-2xl">AiM</span>
        </div>
        <p className="text-[10px] text-text-tertiary font-mono uppercase tracking-wider mt-1">
          Intelligent Media v2.0
        </p>
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
              isActive && !isInProject
                ? 'bg-bg-elevated text-text-primary'
                : 'text-text-secondary hover:bg-bg-elevated hover:text-text-primary'
            }`
          }
        >
          <span className="w-5 h-5 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" />
            </svg>
          </span>
          Dashboard
        </NavLink>

        <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-text-secondary hover:bg-bg-elevated hover:text-text-primary transition-colors">
          <span className="w-5 h-5 flex items-center justify-center relative">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
            </svg>
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-accent-red rounded-full text-[10px] flex items-center justify-center font-mono">
              3
            </span>
          </span>
          Notifications
        </button>

        <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-text-secondary hover:bg-bg-elevated hover:text-text-primary transition-colors">
          <span className="w-5 h-5 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15a4.5 4.5 0 004.5 4.5H18a3.75 3.75 0 001.332-7.257 3 3 0 00-3.758-3.848 5.25 5.25 0 00-10.233 2.33A4.502 4.502 0 002.25 15z" />
            </svg>
          </span>
          Cloud Management
        </button>

        {/* Project Workflow - Only show when in a project */}
        {isInProject && currentProject && (
          <div className="mt-6">
            <p className="px-3 text-[10px] text-text-tertiary font-mono uppercase tracking-wider mb-2">
              Project Workflow
            </p>
            {WORKFLOW_PHASES.map((phase) => {
              const isActive = location.pathname.includes(`/${phase.id}`)
              return (
                <NavLink
                  key={phase.id}
                  to={`/project/${currentProject.id}/${phase.id}`}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                    isActive
                      ? 'text-accent-red border-l-2 border-accent-red bg-bg-elevated'
                      : 'text-text-secondary hover:bg-bg-elevated hover:text-text-primary'
                  }`}
                >
                  {phase.label}
                </NavLink>
              )
            })}
          </div>
        )}
      </nav>

      {/* User Panel */}
      <div className="p-4 border-t border-border-subtle">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-accent-red flex items-center justify-center text-white font-bold">
            {user?.name?.charAt(0) || 'U'}
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-text-primary">{user?.name || 'User'}</p>
            <p className="text-xs text-text-tertiary font-mono uppercase">{user?.role || 'Producer'}</p>
          </div>
        </div>
        <div className="flex gap-2 mt-3">
          <button className="flex-1 px-3 py-1.5 text-xs text-text-secondary bg-bg-input rounded hover:bg-border-medium transition-colors">
            Settings
          </button>
          <button className="flex-1 px-3 py-1.5 text-xs text-text-secondary bg-bg-input rounded hover:bg-border-medium transition-colors">
            Log Out
          </button>
        </div>
      </div>
    </aside>
  )
}
