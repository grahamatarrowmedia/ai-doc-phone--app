import { useState, useRef } from 'react'

export default function DeepResearchModal({ isOpen, onClose, onSubmit, series, episode }) {
  const [query, setQuery] = useState('')
  const [files, setFiles] = useState([])
  const [currentFileIndex, setCurrentFileIndex] = useState(0)
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef(null)

  if (!isOpen) return null

  const handleFileChange = (e) => {
    const newFiles = Array.from(e.target.files)
    setFiles([...files, ...newFiles])
  }

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index))
    if (currentFileIndex >= files.length - 1) {
      setCurrentFileIndex(Math.max(0, files.length - 2))
    }
  }

  const handleSubmit = async () => {
    if (!query.trim()) return

    setLoading(true)
    try {
      await onSubmit({
        query: query.trim(),
        files
      })
      setQuery('')
      setFiles([])
      onClose()
    } catch (err) {
      console.error('Research failed:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-bg-secondary rounded-xl w-full max-w-2xl mx-4">
        {/* Header */}
        <div className="p-4 border-b border-border-subtle">
          <h2 className="text-lg font-heading font-bold text-text-primary">
            Deep Research
          </h2>
          <p className="text-sm text-text-secondary mt-1">
            Targeting: <span className="text-accent-red">{series?.title}</span>
            {episode && (
              <> | <span className="text-accent-blue">{episode.code} {episode.title}</span></>
            )}
          </p>
        </div>

        {/* Body */}
        <div className="p-6">
          {/* File Upload Area */}
          <div className="mb-6">
            <div
              onClick={() => fileInputRef.current?.click()}
              className="w-32 h-32 mx-auto rounded-full bg-bg-input border-2 border-dashed border-border-medium flex items-center justify-center cursor-pointer hover:border-accent-red transition-colors"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-10 h-10 text-text-tertiary">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              className="hidden"
              multiple
              accept="image/*,.pdf,.doc,.docx,.txt"
            />
            <p className="text-center text-xs text-text-tertiary mt-2">
              Click to attach files (optional)
            </p>
          </div>

          {/* Attached Files */}
          {files.length > 0 && (
            <div className="mb-4">
              <div className="flex items-center justify-center gap-2 mb-2">
                {files.length > 1 && (
                  <button
                    onClick={() => setCurrentFileIndex(Math.max(0, currentFileIndex - 1))}
                    className="p-1 text-text-tertiary hover:text-text-primary"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
                    </svg>
                  </button>
                )}

                <div className="flex items-center gap-2 px-3 py-1.5 bg-bg-input rounded-full">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 text-accent-blue">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M18.375 12.739l-7.693 7.693a4.5 4.5 0 01-6.364-6.364l10.94-10.94A3 3 0 1119.5 7.372L8.552 18.32m.009-.01l-.01.01m5.699-9.941l-7.81 7.81a1.5 1.5 0 002.112 2.13" />
                  </svg>
                  <span className="text-sm text-text-primary truncate max-w-[200px]">
                    {files[currentFileIndex]?.name}
                  </span>
                  <button
                    onClick={() => removeFile(currentFileIndex)}
                    className="text-text-tertiary hover:text-accent-red"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                {files.length > 1 && (
                  <button
                    onClick={() => setCurrentFileIndex(Math.min(files.length - 1, currentFileIndex + 1))}
                    className="p-1 text-text-tertiary hover:text-text-primary"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                    </svg>
                  </button>
                )}
              </div>
              {files.length > 1 && (
                <p className="text-center text-xs text-text-tertiary">
                  {currentFileIndex + 1} of {files.length} files
                </p>
              )}
            </div>
          )}

          {/* Query Input */}
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={`Research topic for ${episode?.code || 'episode'}...`}
              className="flex-1 px-4 py-3 bg-bg-input border border-border-subtle rounded-lg text-text-primary placeholder-text-tertiary focus:outline-none focus:border-accent-red"
              onKeyDown={(e) => e.key === 'Enter' && !loading && handleSubmit()}
              autoFocus
            />
            <button
              onClick={handleSubmit}
              disabled={loading || !query.trim()}
              className="w-12 h-12 bg-accent-red text-white rounded-full flex items-center justify-center hover:bg-accent-red-dark transition-colors disabled:opacity-50"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-border-subtle flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-text-secondary hover:text-text-primary transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}
