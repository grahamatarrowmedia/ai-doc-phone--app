import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/layout/Sidebar'
import Dashboard from './pages/Dashboard'
import Phase1Research from './pages/Phase1Research'

function App() {
  return (
    <div className="flex h-screen bg-bg-primary">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/project/:projectId/research" element={<Phase1Research />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
