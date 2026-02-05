export default function TopBar({ title, subtitle, children }) {
  return (
    <div className="bg-bg-secondary border-b border-border-subtle px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-heading font-bold text-text-primary">
            {title}
          </h1>
          {subtitle && (
            <p className="text-sm text-text-secondary mt-0.5">
              {subtitle}
            </p>
          )}
        </div>
        {children}
      </div>
    </div>
  )
}
