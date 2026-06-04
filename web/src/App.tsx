import './App.css'
import { sampleCase } from './data/sampleCase'

function App() {
  const canonicalJson = JSON.stringify(sampleCase, null, 2)

  return (
    <main className="app-shell">
      <section className="hero-panel">
        <p className="eyebrow">BC Gov web path</p>
        <h1>BC Small Claims Assistant</h1>
        <p className="hero-copy">
          Web host over the canonical Notice of Claim JSON core.
        </p>
        <div className="status-row" aria-label="case status milestones">
          <span className="status-pill status-pill-active">guided intake</span>
          <span className="status-pill">ready for review</span>
          <span className="status-pill">ready for pdf</span>
          <span className="status-pill">mock filing</span>
        </div>
      </section>

      <section className="branch-grid" aria-label="downstream branches">
        <article className="branch-card">
          <p className="branch-kicker">Upstream</p>
          <h2>Guided intake</h2>
          <p>
            Conversational intake still owns user guidance and canonical JSON updates.
          </p>
        </article>
        <article className="branch-card">
          <p className="branch-kicker">Deterministic output</p>
          <h2>PDF generation</h2>
          <p>
            The web host hands the same canonical case to the renderer instead of duplicating form logic.
          </p>
        </article>
        <article className="branch-card">
          <p className="branch-kicker">Downstream adapter</p>
          <h2>Mock filing adapter</h2>
          <p>
            Filing payload transformation remains a separate seam for future API-backed submission.
          </p>
        </article>
      </section>

      <section className="json-panel">
        <div className="json-panel-header">
          <div>
            <p className="branch-kicker">Shared contract</p>
            <h2>Canonical case JSON</h2>
          </div>
          <p className="json-note">First web slice is read-only: show the shared core before editing workflows are added.</p>
        </div>
        <label className="json-label" htmlFor="canonical-case-json">
          Canonical case JSON
        </label>
        <textarea
          id="canonical-case-json"
          className="json-textarea"
          value={canonicalJson}
          readOnly
          aria-label="Canonical case JSON"
        />
      </section>
    </main>
  )
}

export default App
