export function TypingIndicator() {
  return (
    <div className="typing-indicator" aria-label="Assistant is typing">
      <div className="typing-avatar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 18a8 8 0 100-16 8 8 0 000 16zm-1-9h2v6h-2V11zm0-4h2v2h-2V7z" fill="currentColor"/>
        </svg>
      </div>
      <div className="typing-dots">
        <span className="dot" />
        <span className="dot" />
        <span className="dot" />
      </div>
    </div>
  )
}
