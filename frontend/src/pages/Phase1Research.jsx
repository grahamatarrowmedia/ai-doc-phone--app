import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useProject } from '../context/ProjectContext'
import * as api from '../api/client'

import SeriesSelector from '../components/research/SeriesSelector'
import EpisodeSelector from '../components/research/EpisodeSelector'
import ActiveContext from '../components/research/ActiveContext'
import TabSwitcher from '../components/research/TabSwitcher'
import ReportList from '../components/research/ReportList'
import ReportDetail from '../components/research/ReportDetail'
import DeepResearchModal from '../components/research/DeepResearchModal'
import KnowledgeBaseView from '../components/research/KnowledgeBaseView'

export default function Phase1Research() {
  const { projectId } = useParams()
  const { selectProject, currentProject } = useProject()

  // Selection state
  const [selectedSeries, setSelectedSeries] = useState(null)
  const [selectedEpisode, setSelectedEpisode] = useState(null)

  // Data state
  const [reports, setReports] = useState([])
  const [knowledgeBase, setKnowledgeBase] = useState([])
  const [selectedReport, setSelectedReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [kbLoading, setKbLoading] = useState(false)

  // UI state
  const [activeTab, setActiveTab] = useState('briefs')
  const [showResearchModal, setShowResearchModal] = useState(false)

  // Load project on mount
  useEffect(() => {
    if (projectId) {
      selectProject(projectId)
    }
  }, [projectId, selectProject])

  // Fetch reports when episode changes
  useEffect(() => {
    if (selectedEpisode && selectedSeries) {
      fetchReports()
      fetchKnowledgeBase()
    } else {
      setReports([])
      setKnowledgeBase([])
      setSelectedReport(null)
    }
  }, [selectedEpisode, selectedSeries])

  const fetchReports = async () => {
    if (!projectId || !selectedSeries?.id || !selectedEpisode?.id) return
    try {
      setLoading(true)
      const data = await api.getResearchReports(projectId, selectedSeries.id, selectedEpisode.id)
      setReports(data.reports || [])
    } catch (err) {
      console.error('Failed to fetch reports:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchKnowledgeBase = async () => {
    if (!projectId || !selectedSeries?.id || !selectedEpisode?.id) return
    try {
      setKbLoading(true)
      const data = await api.getKnowledgeBase(projectId, selectedSeries.id, selectedEpisode.id)
      setKnowledgeBase(data.entries || [])
    } catch (err) {
      console.error('Failed to fetch knowledge base:', err)
    } finally {
      setKbLoading(false)
    }
  }

  const handleNewResearch = async ({ query, files }) => {
    if (!projectId || !selectedSeries?.id || !selectedEpisode?.id) return

    // For now, just pass the query. File upload will be handled separately.
    const data = await api.createResearch(projectId, selectedSeries.id, selectedEpisode.id, {
      query,
      attached_files: files.map(f => ({ name: f.name, type: f.type }))
    })

    // Refresh reports
    await fetchReports()

    // Select the new report
    setSelectedReport(data)
  }

  const handleMarkComplete = async () => {
    if (!selectedReport) return
    try {
      await api.markResearchComplete(projectId, selectedSeries.id, selectedEpisode.id, selectedReport.id)
      await fetchReports()
      // Update selected report status
      setSelectedReport(prev => ({ ...prev, status: 'complete' }))
    } catch (err) {
      console.error('Failed to mark complete:', err)
    }
  }

  const handleUpdateNotes = async (reportId, notes) => {
    try {
      await api.updateResearch(projectId, selectedSeries.id, selectedEpisode.id, reportId, {
        producer_notes: notes
      })
      await fetchReports()
    } catch (err) {
      console.error('Failed to update notes:', err)
    }
  }

  const handleLinkAsset = (reportId) => {
    // TODO: Open asset linking modal
    console.log('Link asset to report:', reportId)
  }

  return (
    <div className="flex flex-col h-full">
      {/* Phase Header */}
      <div className="bg-bg-secondary border-b border-border-subtle px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-xl font-heading font-bold text-text-primary">
                Phase 01: Intelligent Discovery
              </h1>
            </div>
            <p className="text-sm text-text-secondary mt-1">
              Deep Research & Brief Generation | Project: {currentProject?.name || 'Loading...'}
            </p>
          </div>
          <Link
            to={`/project/${projectId}/archive`}
            className="px-4 py-2 bg-bg-input text-text-secondary rounded-lg hover:bg-border-medium hover:text-text-primary transition-colors flex items-center gap-2"
          >
            Next Phase
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </Link>
        </div>
      </div>

      {/* Three-Column Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Column - Series & Episode Selection */}
        <div className="w-60 bg-bg-primary border-r border-border-subtle p-4 overflow-auto">
          <SeriesSelector
            projectId={projectId}
            selectedSeries={selectedSeries}
            onSelect={setSelectedSeries}
          />
          <EpisodeSelector
            projectId={projectId}
            seriesId={selectedSeries?.id}
            selectedEpisode={selectedEpisode}
            onSelect={setSelectedEpisode}
          />
        </div>

        {/* Center Column - Reports List */}
        <div className="w-80 bg-bg-primary border-r border-border-subtle flex flex-col">
          <ActiveContext episode={selectedEpisode} />
          <TabSwitcher
            activeTab={activeTab}
            onTabChange={setActiveTab}
            briefsCount={reports.length}
            kbCount={knowledgeBase.length}
          />
          {activeTab === 'briefs' ? (
            <ReportList
              reports={reports}
              selectedReport={selectedReport}
              onSelectReport={setSelectedReport}
              onNewResearch={() => setShowResearchModal(true)}
              loading={loading}
            />
          ) : (
            <KnowledgeBaseView
              entries={knowledgeBase}
              loading={kbLoading}
            />
          )}
        </div>

        {/* Right Column - Report Detail */}
        <ReportDetail
          report={selectedReport}
          episode={selectedEpisode}
          onMarkComplete={handleMarkComplete}
          onUpdateNotes={handleUpdateNotes}
          onLinkAsset={handleLinkAsset}
        />
      </div>

      {/* Deep Research Modal */}
      <DeepResearchModal
        isOpen={showResearchModal}
        onClose={() => setShowResearchModal(false)}
        onSubmit={handleNewResearch}
        series={selectedSeries}
        episode={selectedEpisode}
      />
    </div>
  )
}
