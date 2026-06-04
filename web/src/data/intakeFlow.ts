import type { IntakeSection, IntakeStep, PartialCase } from '../types/intake'

// ─── Sections (sidebar display) ──────────────────────────────────────────────

export const INTAKE_SECTIONS: IntakeSection[] = [
  {
    id: 'claimant',
    label: 'Who You Are',
    shortLabel: 'Who You Are',
    stepIds: ['claimant_type', 'claimant_surname', 'claimant_firstname', 'claimant_orgname',
               'claimant_street', 'claimant_city', 'claimant_postal', 'claimant_phone'],
  },
  {
    id: 'defendant',
    label: 'Who You Are Suing',
    shortLabel: 'Defendant',
    stepIds: ['defendant_intro', 'defendant_type', 'defendant_surname', 'defendant_firstname',
               'defendant_orgname', 'defendant_street', 'defendant_city', 'defendant_postal'],
  },
  {
    id: 'what_happened',
    label: 'What Happened',
    shortLabel: 'What Happened',
    stepIds: ['claim_category', 'narrative', 'agreement_written', 'amount_agreed',
               'wrong_description', 'defendant_corrected'],
  },
  {
    id: 'where_when',
    label: 'Where & When',
    shortLabel: 'Where & When',
    stepIds: ['location_city', 'date_range'],
  },
  {
    id: 'remedy',
    label: 'What You Are Asking For',
    shortLabel: 'Amount Claimed',
    stepIds: ['remedy_items', 'remedy_interest'],
  },
  {
    id: 'filing',
    label: 'Filing Details',
    shortLabel: 'Filing',
    stepIds: ['registry_location'],
  },
  {
    id: 'settle',
    label: 'Options to Settle',
    shortLabel: 'Settle Options',
    stepIds: ['settle_info'],
  },
  {
    id: 'review',
    label: 'Review & Finish',
    shortLabel: 'Review',
    stepIds: ['_review'],
  },
]

// ─── Steps ────────────────────────────────────────────────────────────────────

const isOrg  = (d: PartialCase) => d.claimantType === 'Organization'
const isIndiv = (d: PartialCase) => d.claimantType === 'Individual'
const defIsOrg  = (d: PartialCase) => d.defendantType === 'Organization'
const defIsIndiv = (d: PartialCase) => d.defendantType === 'Individual'

export const INTAKE_STEPS: IntakeStep[] = [
  // ── CLAIMANT ───────────────────────────────────────────────────────────────
  {
    id: 'claimant_type',
    sectionId: 'claimant',
    question: "Welcome to the BC Small Claims Notice of Claim assistant. I'll guide you through Form 1 step by step.\n\nLet's start with you. Are you filing as an **individual** (yourself), or on behalf of an **organization**?",
    placeholder: 'Choose below or type Individual or Organization',
    fieldKey: 'claimantType',
    choices: ['Individual', 'Organization'],
  },
  {
    id: 'claimant_surname',
    sectionId: 'claimant',
    question: 'What is your surname (last name)?\n\nUse your full legal name — do not use initials (e.g. JANE SMITH, not J. SMITH) and do not include titles like Mr. or Dr.',
    placeholder: 'e.g. Smith',
    hint: 'Initials are not enough. Say: ROBERT JOHNSON. Not: R.W. JOHNSON.',
    fieldKey: 'claimantSurname',
    skipIf: isOrg,
  },
  {
    id: 'claimant_firstname',
    sectionId: 'claimant',
    question: 'What is your first name (and middle name if you use it)?',
    placeholder: 'e.g. Jane  or  Jane Marie',
    fieldKey: 'claimantFirstName',
    skipIf: isOrg,
  },
  {
    id: 'claimant_orgname',
    sectionId: 'claimant',
    question: 'What is the full registered name of the organization?\n\nUse the exact name from your incorporation or registration documents.',
    placeholder: 'e.g. Acme Contractors Ltd.',
    hint: 'You can verify the registered name at BC Registry Services (bcregistry.gov.bc.ca).',
    fieldKey: 'claimantOrgName',
    skipIf: isIndiv,
  },
  {
    id: 'claimant_street',
    sectionId: 'claimant',
    question: 'What is your street address? Include apartment or suite number if applicable.',
    placeholder: 'e.g. 123 Main Street  or  Suite 400 – 789 Fort St',
    hint: 'This is where the court registry will send all official notices. Keep it up to date.',
    fieldKey: 'claimantStreet',
  },
  {
    id: 'claimant_city',
    sectionId: 'claimant',
    question: 'What city or town are you in?',
    placeholder: 'e.g. Victoria',
    fieldKey: 'claimantCity',
  },
  {
    id: 'claimant_postal',
    sectionId: 'claimant',
    question: 'What is your postal code?',
    placeholder: 'e.g. V8W 1A1',
    fieldKey: 'claimantPostal',
  },
  {
    id: 'claimant_phone',
    sectionId: 'claimant',
    question: 'What is your contact phone number? (This is optional — press Enter or type "skip" to continue.)',
    placeholder: 'e.g. 250-555-0100  or  skip',
    fieldKey: 'claimantPhone',
    optional: true,
  },

  // ── DEFENDANT ──────────────────────────────────────────────────────────────
  {
    id: 'defendant_intro',
    sectionId: 'defendant',
    question: "Great — now let's capture the defendant's information.\n\nThe defendant is the person or business you are making the claim against. Be careful to use their exact legal name — if it is wrong you may win but be unable to collect your judgment.\n\nIs the defendant an **individual** or an **organization** (company, corporation, society)?",
    placeholder: 'Choose below or type Individual or Organization',
    fieldKey: 'defendantType',
    choices: ['Individual', 'Organization'],
  },
  {
    id: 'defendant_surname',
    sectionId: 'defendant',
    question: "What is the defendant's surname (last name)?",
    placeholder: 'e.g. Johnson',
    hint: 'Use the full legal name. Do not use initials.',
    fieldKey: 'defendantSurname',
    skipIf: defIsOrg,
  },
  {
    id: 'defendant_firstname',
    sectionId: 'defendant',
    question: "What is the defendant's first name (and middle name if known)?",
    placeholder: 'e.g. Robert  or  Robert William',
    fieldKey: 'defendantFirstName',
    skipIf: defIsOrg,
  },
  {
    id: 'defendant_orgname',
    sectionId: 'defendant',
    question: "What is the full registered name of the defendant organization?\n\nIf you are suing a company, get the exact registered name from a company search.",
    placeholder: 'e.g. Island View Auto Repairs Ltd.',
    hint: 'You may need to do a company search at BC Registry Services to confirm the exact name.',
    fieldKey: 'defendantOrgName',
    skipIf: defIsIndiv,
  },
  {
    id: 'defendant_street',
    sectionId: 'defendant',
    question: "What is the defendant's street address? The court needs this to serve them with your claim.",
    placeholder: 'e.g. 456 Oak Avenue, Victoria  or  unknown',
    hint: 'If you do not know the address, type "unknown". You may need to find it before filing.',
    fieldKey: 'defendantStreet',
  },
  {
    id: 'defendant_city',
    sectionId: 'defendant',
    question: "What city or town is the defendant in? (Type \"unknown\" if unsure.)",
    placeholder: 'e.g. Victoria  or  unknown',
    fieldKey: 'defendantCity',
  },
  {
    id: 'defendant_postal',
    sectionId: 'defendant',
    question: "What is the defendant's postal code? (Type \"unknown\" if unsure.)",
    placeholder: 'e.g. V9A 2B2  or  unknown',
    fieldKey: 'defendantPostal',
  },

  // ── WHAT HAPPENED ─────────────────────────────────────────────────────────
  {
    id: 'claim_category',
    sectionId: 'what_happened',
    question: "Now let's describe what happened. First, choose the category that best fits your claim.",
    placeholder: 'Choose one below',
    fieldKey: 'claimCategory',
    choices: [
      '1. Personal Injury – Motor Vehicle Accident',
      '2. Personal Injury – Other',
      '3. Loan of Money',
      '4. NSF (Dishonoured) Cheque',
      '5. Defective Repairs or Construction',
      '6. Goods and Services Unpaid',
      '7. Defective Goods / Services',
      '8. Wrongful Dismissal from Employment',
      '9. Real Estate',
      '10. Other',
    ],
  },
  {
    id: 'narrative',
    sectionId: 'what_happened',
    question: "Describe the goods or services the defendant agreed to provide, or what the defendant was supposed to do.\n\nTell the facts clearly and in order. The judge will read this. Use plain language — no legal jargon needed.",
    placeholder: 'e.g. Maya Chen paid Island View Auto Repairs Ltd. $2,400 to replace the transmission in her 2013 Honda Civic. The shop said the repair would be completed by April 12, 2026...',
    hint: 'Think about: what was agreed, what was paid, what went wrong, and when.',
    fieldKey: 'narrative',
  },
  {
    id: 'agreement_written',
    sectionId: 'what_happened',
    question: 'Was your agreement with the defendant in writing? (e.g. a contract, invoice, text messages, or email.)',
    placeholder: 'Choose below or type Yes or No',
    fieldKey: 'agreementWritten',
    choices: ['Yes', 'No'],
  },
  {
    id: 'amount_agreed',
    sectionId: 'what_happened',
    question: 'How much did you agree to pay, or how much is owed to you?',
    placeholder: 'e.g. $2,400.00',
    fieldKey: 'amountAgreed',
  },
  {
    id: 'wrong_description',
    sectionId: 'what_happened',
    question: 'Describe what was wrong with the goods or services, or what the defendant failed to do.',
    placeholder: 'e.g. After she picked up the car, it stopped working again the same day. A second mechanic confirmed the original faulty transmission was never replaced...',
    fieldKey: 'wrongDescription',
  },
  {
    id: 'defendant_corrected',
    sectionId: 'what_happened',
    question: 'Has the defendant taken any steps to correct the problem or make it right?',
    placeholder: 'Choose below or type Yes or No',
    fieldKey: 'defendantCorrected',
    choices: ['Yes', 'No'],
  },

  // ── WHERE & WHEN ───────────────────────────────────────────────────────────
  {
    id: 'location_city',
    sectionId: 'where_when',
    question: "Where did this happen? Give the city or municipality in British Columbia.\n\nYou must file your claim at the small claims registry nearest to either where the defendant lives or carries out business, or where the event happened.",
    placeholder: 'e.g. Victoria',
    fieldKey: 'locationCity',
  },
  {
    id: 'date_range',
    sectionId: 'where_when',
    question: 'When did this happen? Provide the date or approximate date range.',
    placeholder: 'e.g. April 2026  or  between January and April 2026',
    fieldKey: 'dateRange',
  },

  // ── REMEDY ─────────────────────────────────────────────────────────────────
  {
    id: 'remedy_items',
    sectionId: 'remedy',
    question: "What are you claiming? List each item with a description and dollar amount.\n\nFor example:\n  a) Value paid for transmission — $2,400.00\n  b) Towing — $100.00\n  c) Inspection — $200.00\n\nThe maximum in BC Small Claims Court is **$35,000**.",
    placeholder: 'a) Description — $amount\nb) Description — $amount\n...',
    hint: 'List interest separately. Do not include filing or service fees in your total — those are added by the court.',
    fieldKey: 'remedyItems',
  },
  {
    id: 'remedy_interest',
    sectionId: 'remedy',
    question: 'Are you also claiming interest? If so, describe the interest and the amount. Type "none" if not claiming interest.',
    placeholder: 'e.g. Contractual interest at 2% per month on $2,400 from April 14, 2026  or  none',
    fieldKey: 'remedyInterest',
    optional: true,
  },

  // ── FILING ─────────────────────────────────────────────────────────────────
  {
    id: 'registry_location',
    sectionId: 'filing',
    question: "Which court registry will you file at? Choose the one nearest to where the defendant lives or carries out business, or where the event happened.",
    placeholder: 'Choose a registry below',
    hint: 'You can also mail your claim to the registry. Bring the Notice of Claim, a Form 38 (Address for Service), and the required filing fee.',
    fieldKey: 'registryLocation',
    choices: [
      'Victoria Law Courts',
      'Vancouver Law Courts',
      'Surrey Provincial Court',
      'Burnaby Provincial Court',
      'Nanaimo Law Courts',
      'Kelowna Law Courts',
      'Prince George Law Courts',
      'Kamloops Law Courts',
      'Abbotsford Law Courts',
      'Other BC Registry',
    ],
  },

  // ── OPTIONS TO SETTLE ─────────────────────────────────────────────────────
  {
    id: 'settle_info',
    sectionId: 'settle',
    question: "**Before filing, you should know about settlement options.**\n\nBC Small Claims Court offers opportunities to settle without going to trial:\n\n**Mediation (claims $10,000–$35,000):** You can require the other party to attend mediation by delivering a Notice to Mediate. Both parties share the cost.\n\n**Settlement Conference:** Before any trial, you will be required to attend a settlement conference held by a judge. All parties must attend and have authority to settle.\n\nKeeping these options in mind may help you resolve the dispute faster and at lower cost.\n\nType anything to continue to review your answers.",
    placeholder: 'Press Enter or type anything to continue…',
    fieldKey: '_info',
    isInfo: true,
  },
]

// ─── Clarification responses ──────────────────────────────────────────────────

export const CLARIFICATIONS: Array<{ keywords: string[]; response: string }> = [
  {
    keywords: ['claimant', 'who am i', 'who is the claimant'],
    response: 'A claimant is the person or organization bringing the claim — that is you. You can file as an individual or as a business entity.',
  },
  {
    keywords: ['individual', 'person', 'myself'],
    response: 'An individual claimant is a natural person (not a company). Enter your full legal name as it appears on government-issued ID. Do not use initials or titles like Mr. or Dr.',
  },
  {
    keywords: ['organization', 'company', 'corporation', 'business', 'society'],
    response: 'An organization can be a corporation, partnership, society, or other legal entity. Use the full registered name exactly as it appears on your incorporation documents. You can verify this at BC Registry Services (bcregistry.gov.bc.ca).',
  },
  {
    keywords: ['company search', 'registered name', 'bc registry'],
    response: 'You can search for a company\'s official registered name at BC Registry Services (bcregistry.gov.bc.ca). Using the exact registered name is critical — if it is wrong you may win but be unable to collect your judgment.',
  },
  {
    keywords: ['defendant', 'suing', 'who am i suing'],
    response: 'The defendant is the person or business you believe owes you money or caused you harm. You need their full legal name and a mailing address so the court can serve them with notice of your claim.',
  },
  {
    keywords: ['serve', 'service', 'served', 'deliver'],
    response: 'Serving means formally delivering court documents to the defendant. The court registry assists with this. That is why a defendant address is required — without it, service is not possible.',
  },
  {
    keywords: ['category', 'type of claim', 'which category', 'what category'],
    response: 'Choose the category that most closely describes your situation. If none fit exactly, choose "10. Other" and describe the details in the narrative. Category 7 (Defective Goods / Services) covers most contractor or repair disputes.',
  },
  {
    keywords: ['written agreement', 'contract', 'written'],
    response: 'A written agreement includes contracts, quotes, invoices, emails, or text messages that show what was agreed. Verbal agreements are also valid but harder to prove. The court wants to know whether there is written evidence.',
  },
  {
    keywords: ['interest', 'claim interest'],
    response: 'You can claim contractual interest (if your contract states an interest rate) or court order interest (set by regulation). List interest as a separate line item from the main claim amount.',
  },
  {
    keywords: ['remedy', 'amount', 'claiming', '35000', '35,000', 'maximum'],
    response: 'The maximum claim in BC Small Claims Court is $35,000 (not including interest or filing fees). If your claim is higher, you must either reduce it or file in BC Supreme Court instead.',
  },
  {
    keywords: ['registry', 'where to file', 'file at', 'filing fee'],
    response: 'Filing fees depend on the amount claimed: $0–$3,000 is $100; $3,001–$10,000 is $200; $10,001–$35,000 is $300. To file: bring your Notice of Claim, a Form 38 (Address for Service), and your fee to the nearest small claims registry.',
  },
  {
    keywords: ['mediation', 'settlement', 'settle', 'trial'],
    response: 'You do not have to go to trial. For claims between $10,000 and $35,000 you can require mediation. All claims go through a settlement conference with a judge before trial. Many cases settle at that stage.',
  },
  {
    keywords: ['form 38', 'address for service'],
    response: 'Form 38 (Address for Service) is a required companion document when filing. It tells the court and the defendant where to send your copy of the Notice of Claim. You can find it at justice.gov.bc.ca.',
  },
  {
    keywords: ['lawyer', 'legal advice', 'solicitor', 'should i'],
    response: 'I can help you understand what the form asks for, but I cannot give legal advice. For guidance, consider contacting Access Pro Bono BC (accessprobono.ca) or the Justice Education Society (justiceeducation.ca) — both offer free resources for self-represented litigants.',
  },
]

export const FALLBACK_CLARIFICATION =
  "Good question. I can clarify what the form requires, but I can't give legal advice. Could you tell me more about what you're unsure of? Or type \"continue\" to move on to the next question."

// ─── Summary builder ──────────────────────────────────────────────────────────

export function buildSummary(d: PartialCase): string {
  const claimantName = d.claimantType === 'Organization'
    ? d.claimantOrgName
    : [d.claimantSurname, d.claimantFirstName].filter(Boolean).join(', ')

  const claimantAddr = [d.claimantStreet, d.claimantCity, 'BC', d.claimantPostal]
    .filter((v) => v && v.toLowerCase() !== 'skip').join(', ')

  const defendantName = d.defendantType === 'Organization'
    ? d.defendantOrgName
    : [d.defendantSurname, d.defendantFirstName].filter(Boolean).join(', ')

  const defendantAddr = [d.defendantStreet, d.defendantCity, d.defendantPostal]
    .filter((v) => v && v.toLowerCase() !== 'unknown').join(', ') || 'unknown'

  const lines: string[] = [
    'Here is a summary of your Notice of Claim. Please review everything carefully.\n',
    '**CLAIMANT (You)**',
    `Name: ${claimantName || '[missing]'}`,
    `Address: ${claimantAddr || '[missing]'}`,
    d.claimantPhone && d.claimantPhone.toLowerCase() !== 'skip' ? `Phone: ${d.claimantPhone}` : '',
    '',
    '**DEFENDANT**',
    `Name: ${defendantName || '[missing]'}`,
    `Address: ${defendantAddr}`,
    '',
    '**CLAIM**',
    `Category: ${d.claimCategory || '[missing]'}`,
    `What happened: ${d.narrative ? d.narrative.slice(0, 120) + (d.narrative.length > 120 ? '…' : '') : '[missing]'}`,
    `Written agreement: ${d.agreementWritten || '[missing]'}`,
    `Amount involved: ${d.amountAgreed || '[missing]'}`,
    '',
    '**WHERE & WHEN**',
    `Location: ${d.locationCity || '[missing]'}, BC`,
    `Date/period: ${d.dateRange || '[missing]'}`,
    '',
    '**REMEDY CLAIMED**',
    d.remedyItems || '[missing]',
    d.remedyInterest && d.remedyInterest.toLowerCase() !== 'none' ? `Interest: ${d.remedyInterest}` : '',
    '',
    '**FILING**',
    `Registry: ${d.registryLocation || '[missing]'}`,
    '',
    'Does everything look correct? Reply **"confirm"** to proceed, or tell me what needs to be changed.',
  ]

  return lines.filter((l) => l !== '').join('\n')
}
