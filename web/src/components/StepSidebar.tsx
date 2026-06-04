import type { IntakePhase, IntakeSection } from '../types/intake'

interface Props {
  sections: IntakeSection[]
  currentSectionIndex: number
  phase: IntakePhase
}

export function StepSidebar({ sections, currentSectionIndex, phase }: Props) {
  return (
    <aside className="step-sidebar" aria-label="Intake progress">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="3" fill="#FCBA19"/>
            <text x="16" y="22" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#013366" fontFamily="sans-serif">BC</text>
          </svg>
        </div>
        <div className="sidebar-title">
          <span className="sidebar-title-sub">Small Claims Court</span>
          <span className="sidebar-title-main">Notice of Claim</span>
          <span className="sidebar-title-version">Form 1</span>
        </div>
      </div>

      <nav>
        <ol className="step-list" aria-label="Form sections">
          {sections.map((section, i) => {
            const isDone = phase === 'complete' || i < currentSectionIndex
            const isCurrent = phase !== 'complete' && i === currentSectionIndex
            const isUpcoming = !isDone && !isCurrent

            return (
              <li
                key={section.id}
                className={`step-item ${isDone ? 'done' : ''} ${isCurrent ? 'current' : ''} ${isUpcoming ? 'upcoming' : ''}`}
                aria-current={isCurrent ? 'step' : undefined}
              >
                <span className="step-number" aria-hidden="true">
                  {isDone ? (
                    <svg width="11" height="11" viewBox="0 0 12 12" fill="none">
                      <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  ) : (
                    i + 1
                  )}
                </span>
                <span className="step-label">{section.label}</span>
              </li>
            )
          })}
        </ol>
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-item">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
            <path d="M12 8v4m0 4h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
          Maximum claim: <strong>$35,000</strong>
        </div>
        <div className="sidebar-footer-item">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          BC Small Claims Court
        </div>
      </div>
    </aside>
  )
}
