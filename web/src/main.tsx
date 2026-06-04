import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import '@bcgov/design-tokens/css/variables.css'
import '@bcgov/bc-sans/css/BCSans.css'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
