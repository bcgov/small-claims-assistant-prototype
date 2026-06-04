import {
  Header,
  Footer,
  FooterLinks,
  Callout,
  TagGroup,
  TagList,
  Tag,
  Heading,
} from '@bcgov/design-system-react-components'
import { sampleCase } from './data/sampleCase'

function App() {
  const canonicalJson = JSON.stringify(sampleCase, null, 2)

  return (
    <>
      <Header title="BC Small Claims Assistant" />

      <main className="page-content">

        <Callout>
          <strong>Notice of Claim — guided intake demo</strong>
          <p>
            This web host shares the same canonical Notice of Claim JSON used by the
            plugin path. Intake, PDF generation, and the filing adapter remain separate
            deterministic services.
          </p>
        </Callout>

        <section style={{ marginTop: '2rem' }}>
          <Heading level={2}>Case status</Heading>
          <TagGroup label="Case status milestones" selectionMode="none" style={{ marginTop: '0.75rem' }}>
            <TagList>
              <Tag id="intake">Guided intake</Tag>
              <Tag id="review">Ready for review</Tag>
              <Tag id="pdf">Ready for PDF</Tag>
              <Tag id="filing">Mock filing</Tag>
            </TagList>
          </TagGroup>
        </section>

        <div className="branch-grid" style={{ marginTop: '2rem' }}>
          <div className="branch-card">
            <p className="branch-kicker">Upstream</p>
            <h3>Guided intake</h3>
            <p>Conversational intake owns user guidance and canonical JSON updates.</p>
          </div>
          <div className="branch-card">
            <p className="branch-kicker">Deterministic output</p>
            <h3>PDF generation</h3>
            <p>The web host hands the same canonical case to the renderer — no duplicate form logic.</p>
          </div>
          <div className="branch-card">
            <p className="branch-kicker">Downstream adapter</p>
            <h3>Mock filing adapter</h3>
            <p>Filing payload transformation remains a separate seam for future API-backed submission.</p>
          </div>
        </div>

        <section style={{ marginTop: '2rem' }}>
          <Heading level={2}>Canonical case JSON</Heading>
          <p style={{ color: '#606060', fontSize: '0.9rem', marginBottom: '0.75rem' }}>
            Read-only — first web slice shows the shared contract before editing workflows are added.
          </p>
          <label
            htmlFor="canonical-case-json"
            style={{ display: 'block', fontWeight: 700, marginBottom: '0.5rem', fontSize: '0.875rem' }}
          >
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

      <Footer>
        <FooterLinks>
          <a href="/privacy">Privacy</a>
          <a href="/disclaimer">Disclaimer</a>
          <a href="/accessibility">Accessibility</a>
          <a href="/copyright">Copyright</a>
        </FooterLinks>
      </Footer>
    </>
  )
}

export default App
