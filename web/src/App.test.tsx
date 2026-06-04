import { render, screen } from '@testing-library/react'

import App from './App'


describe('App', () => {
  it('shows the canonical JSON core and downstream branches', () => {
    render(<App />)

    expect(
      screen.getByRole('heading', { name: /bc small claims assistant/i }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(/web host over the canonical notice of claim json core/i),
    ).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /guided intake/i })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /pdf generation/i })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: /mock filing adapter/i })).toBeInTheDocument()
    const jsonField = screen.getByLabelText(/canonical case json/i) as HTMLTextAreaElement

    expect(jsonField.value).toContain('"formType": "bc-small-claims-notice-of-claim"')
  })
})