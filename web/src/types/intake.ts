export type MessageRole = 'assistant' | 'user'

export interface ChatMessage {
  id: string
  role: MessageRole
  content: string
  type?: 'text' | 'choice' | 'info' | 'summary'
  choices?: string[]
  hint?: string
}

export interface IntakeStep {
  id: string
  sectionId: string
  question: string
  placeholder: string
  hint?: string
  fieldKey: keyof PartialCase | '_info'
  choices?: string[]
  optional?: boolean
  isInfo?: boolean                              // no capture — just show, then continue
  skipIf?: (data: PartialCase) => boolean
}

export interface IntakeSection {
  id: string
  label: string
  shortLabel: string
  stepIds: string[]
}

export interface PartialCase {
  // Claimant
  claimantType?: string           // 'Individual' | 'Organization'
  claimantSurname?: string
  claimantFirstName?: string
  claimantOrgName?: string
  claimantStreet?: string
  claimantCity?: string
  claimantPostal?: string
  claimantPhone?: string

  // Defendant
  defendantType?: string          // 'Individual' | 'Organization'
  defendantSurname?: string
  defendantFirstName?: string
  defendantOrgName?: string
  defendantStreet?: string
  defendantCity?: string
  defendantPostal?: string

  // What Happened
  claimCategory?: string
  narrative?: string
  agreementWritten?: string       // 'Yes' | 'No'
  amountAgreed?: string
  wrongDescription?: string
  defendantCorrected?: string     // 'Yes' | 'No'

  // Where & When
  locationCity?: string
  dateRange?: string

  // Remedy
  remedyItems?: string            // formatted list user enters
  remedyInterest?: string

  // Filing
  registryLocation?: string
}

export type IntakePhase = 'intake' | 'confirming' | 'complete'
