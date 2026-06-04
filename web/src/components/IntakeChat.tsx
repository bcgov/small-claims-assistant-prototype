import { useEffect, useRef } from 'react'
import { INTAKE_STEPS } from '../data/intakeFlow'
import { useIntakeChat } from '../hooks/useIntakeChat'
import { StepSidebar } from './StepSidebar'
import { TypingIndicator } from './TypingIndicator'

function formatContent(text: string) {
  // Render **bold** and newlines
  return text.split('\n').map((line, lineIdx) => {
    if (line === '') return <span key={lineIdx} className="bubble-break" />
    const parts = line.split(/(\*\*[^*]+\*\*)/g)
    return (
      <p key={lineIdx}>
        {parts.map((part, i) =>
          part.startsWith('**') && part.endsWith('**')
            ? <strong key={i}>{part.slice(2, -2)}</strong>
            : part,
        )}
      </p>
    )
  })
}

export function IntakeChat() {
  const {
    messages, stepIndex, currentSectionIndex, phase,
    isTyping, input, setInput, send, sections,
  } = useIntakeChat()

  const scrollRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  useEffect(() => {
    if (!isTyping) inputRef.current?.focus()
  }, [isTyping, messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) send(input)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (input.trim()) send(input)
    }
  }

  const isComplete = phase === 'complete'
  const isConfirming = phase === 'confirming'
  const currentStep = INTAKE_STEPS[stepIndex]
  const currentSection = sections[currentSectionIndex]

  // Progress: count unique sections visited
  const progressPct = isComplete ? 100
    : isConfirming ? 95
    : Math.round((currentSectionIndex / sections.length) * 100)

  return (
    <div className="chat-layout">
      <StepSidebar
        sections={sections}
        currentSectionIndex={currentSectionIndex}
        phase={phase}
      />

      <div className="chat-main">
        {/* Step bar */}
        <div className="chat-step-bar">
          <span className="chat-step-bar-text">
            {isComplete
              ? 'Intake complete — ready to generate PDF'
              : isConfirming
              ? 'Review your answers'
              : `${currentSection?.label ?? ''}`}
          </span>
          <div
            className="chat-progress-track"
            role="progressbar"
            aria-valuenow={progressPct}
            aria-valuemax={100}
            aria-label="Intake progress"
          >
            <div className="chat-progress-fill" style={{ width: `${progressPct}%` }} />
          </div>
        </div>

        {/* Messages */}
        <div className="messages-area" role="log" aria-live="polite" aria-label="Conversation">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-row ${msg.role}`}>
              {msg.role === 'assistant' && (
                <div className="avatar assistant-avatar" aria-hidden="true">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1 14v-4H8l4-8v4h3l-4 8z" fill="currentColor"/>
                  </svg>
                </div>
              )}

              <div className={`bubble bubble-${msg.role}${msg.type === 'summary' ? ' bubble-summary' : ''}`}>
                <div className="bubble-content">
                  {formatContent(msg.content)}
                </div>

                {msg.hint && (
                  <div className="bubble-hint">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2"/>
                      <path d="M12 8v4m0 4h.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                    </svg>
                    {msg.hint}
                  </div>
                )}

                {msg.choices && msg.choices.length > 0 && (
                  <div className="choice-chips" role="group" aria-label="Choose an option">
                    {msg.choices.map((choice) => (
                      <button
                        key={choice}
                        className="choice-chip"
                        onClick={() => send(choice)}
                        type="button"
                      >
                        {choice}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {msg.role === 'user' && (
                <div className="avatar user-avatar" aria-hidden="true">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              )}
            </div>
          ))}

          {isTyping && (
            <div className="message-row assistant">
              <div className="avatar assistant-avatar" aria-hidden="true">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1 14v-4H8l4-8v4h3l-4 8z" fill="currentColor"/>
                </svg>
              </div>
              <TypingIndicator />
            </div>
          )}

          <div ref={scrollRef} />
        </div>

        {/* Input */}
        <form className="input-area" onSubmit={handleSubmit}>
          {isComplete ? (
            <div className="complete-banner">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Intake complete — proceed to generate your Notice of Claim PDF.
            </div>
          ) : (
            <>
              <textarea
                ref={inputRef}
                className="chat-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={
                  isConfirming
                    ? 'Type "confirm" to proceed, or describe what to change…'
                    : currentStep?.isInfo
                    ? 'Press Enter to continue…'
                    : (currentStep?.placeholder ?? 'Type your reply…')
                }
                rows={currentStep?.id === 'narrative' || currentStep?.id === 'remedy_items' ? 3 : 2}
                disabled={isTyping}
                aria-label="Your message"
              />
              <button
                type="submit"
                className="send-button"
                disabled={!input.trim() || isTyping}
                aria-label="Send"
              >
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                <span>Send</span>
              </button>
            </>
          )}
        </form>
      </div>
    </div>
  )
}
