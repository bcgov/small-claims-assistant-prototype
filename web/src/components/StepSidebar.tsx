import type { IntakePhase } from '../types/intake'
import type { IntakeStep } from '../types/intake'

interface Props {
  steps: IntakeStep[]
  currentIndex: number
  phase: IntakePhase
}

export function StepSidebar({ steps, currentIndex, phase }: Props) {
  return (
    <aside className="step-sidebar" aria-label="Intake progress">
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
            <rect width="32" height="32" rx="4" fill="#FCBA19"/>
            <text x="16" y="22" textAnchor="middle" fontSize="16" fontWeight="bold" fill="#013366">BC</text>
          </svg>
        </div>
        <div className="sidebar-title">
          <span className="sidebar-title-sub">Small Claims</span>
          <span className="sidebar-title-main">Notice of Claim</span>
        </div>
      </div>

      <nav>
        <ol className="step-list" aria-label="Form sections">
          {steps.map((step, i) => {
            const isDone = phase === 'complete' || i < currentIndex || (phase === 'confirming' && i < steps.length)
            const isCurrent = phase === 'intake' && i === currentIndex
            const isUpcoming = !isDone && !isCurrent

            return (
              <li
                key={step.id}
                className={`step-item ${isDone ? 'done' : ''} ${isCurrent ? 'current' : ''} ${isUpcoming ? 'upcoming' : ''}`}
                aria-current={isCurrent ? 'step' : undefined}
              >
                <span className="step-number" aria-hidden="true">
                  {isDone ? (
                    <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                      <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  ) : (
                    i + 1
                  )}
                </span>
                <span className="step-label">{step.shortLabel}</span>
              </li>
            )
          })}

          <li className={`step-item ${phase === 'confirming' || phase === 'complete' ? 'current' : 'upcoming'}`}>
            <span className="step-number" aria-hidden="true">
              {phase === 'complete' ? (
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M2 6l3 3 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              ) : (
                steps.length + 1
              )}
            </span>
            <span className="step-label">Review</span>
          </li>
        </ol>
      </nav>

      <div className="sidebar-footer">
        <p>BC Small Claims Court handles disputes up to <strong>$35,000</strong>.</p>
      </div>
    </aside>
  )
}
