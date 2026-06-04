import { Header } from '@bcgov/design-system-react-components'
import { IntakeChat } from './components/IntakeChat'

function App() {
  return (
    <div className="app">
      <Header title="BC Small Claims Assistant" />

      <main className="main-content">
        <IntakeChat />
      </main>
    </div>
  )
}

export default App
