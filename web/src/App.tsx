import { Footer, FooterLinks, Header } from '@bcgov/design-system-react-components'
import { IntakeChat } from './components/IntakeChat'

function App() {
  return (
    <div className="app">
      <Header title="BC Small Claims Assistant" />

      <main className="main-content">
        <IntakeChat />
      </main>

      <Footer>
        <FooterLinks>
          <a href="/privacy">Privacy</a>
          <a href="/disclaimer">Disclaimer</a>
          <a href="/accessibility">Accessibility</a>
          <a href="/copyright">Copyright</a>
        </FooterLinks>
      </Footer>
    </div>
  )
}

export default App
