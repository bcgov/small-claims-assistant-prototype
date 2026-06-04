export type MessageRole = 'assistant' | 'user'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  type?: 'text' | 'choice' | 'summary' | 'hint'
  choices?: string[]
  hint?: string
}

export interface IntakeStep {
  id: string
  label: string
  shortLabel: string
  question: string
  placeholder: string
  hint?: string
  fieldKey: keyof PartialCase
  choices?: string[]
  optional?: boolean
}

export interface PartialCase {
  claimantName?: string
  claimantAddress?: string
  defendantName?: string
  defendantAddress?: string
  claimCategory?: string
  narrative?: string
  location?: string
  dateRange?: string
  remedyTotal?: string
}

export type IntakePhase = 'intake' | 'confirming' | 'complete'
