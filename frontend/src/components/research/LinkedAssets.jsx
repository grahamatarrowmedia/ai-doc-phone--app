export default function LinkedAssets({ assets, onLinkAsset }) {
  return (
    <div className="mb-6">
      <h3 className="text-xs font-heading font-bold uppercase text-accent-red tracking-wider mb-3">
        Linked Archive Assets
      </h3>

      {assets && assets.length > 0 ? (
        <div className="space-y-2 mb-3">
          {assets.map((asset, index) => (
            <div
              key={index}
              className="flex items-center gap-3 px-3 py-2 bg-white border border-gray-200 rounded-lg"
            >
              <div className="w-8 h-8 bg-gray-100 rounded flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 text-gray-500">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5a2.25 2.25 0 002.25-2.25V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z" />
                </svg>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-text-detail">{asset.name}</p>
                <p className="text-xs text-text-detail-muted">{asset.type}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-text-detail-muted italic mb-3">
          No assets linked yet.
        </p>
      )}

      <button
        onClick={onLinkAsset}
        className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-sm text-text-detail hover:bg-gray-50 transition-colors"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Link Clip
      </button>
    </div>
  )
}
