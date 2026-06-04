import type { IntakeStep } from '../types/intake'

export const INTAKE_STEPS: IntakeStep[] = [
  {
    id: 'claimant_name',
    label: 'Who You Are',
    shortLabel: 'Your Name',
    question:
      "Let's start with you. What is your full legal name?\n\nIf you're filing on behalf of a business or organization, provide the full registered name.",
    placeholder: 'e.g. Jane Marie Smith  or  Acme Contractors Ltd.',
    hint: 'Use the name exactly as it appears on government-issued ID or corporate registration.',
    fieldKey: 'claimantName',
  },
  {
    id: 'claimant_address',
    label: 'Your Address',
    shortLabel: 'Your Address',
    question:
      'What is your current mailing address in BC? The court registry will send all notices here.',
    placeholder: '123 Main St, Victoria, BC  V8W 1A1',
    hint: 'If your address changes at any time, you must notify the registry and all parties to the lawsuit.',
    fieldKey: 'claimantAddress',
  },
  {
    id: 'defendant_name',
    label: 'Who You Are Suing',
    shortLabel: 'Defendant',
    question:
      'Who are you making this claim against? Please provide their full legal name or, if it is a company, their full registered business name.',
    placeholder: 'e.g. John Robert Doe  or  Pacific Home Services Inc.',
    hint: 'If suing a company, you may need to do a company search at BC Registry Services to confirm the exact registered name.',
    fieldKey: 'defendantName',
  },
  {
    id: 'defendant_address',
    label: 'Defendant Address',
    shortLabel: 'Def. Address',
    question:
      "What is the defendant's mailing address? The court needs this to serve them with your claim.",
    placeholder: '456 Oak Ave, Vancouver, BC  V6B 2T4  (or type "unknown")',
    fieldKey: 'defendantAddress',
  },
  {
    id: 'claim_category',
    label: 'Claim Category',
    shortLabel: 'Category',
    question: 'What best describes the nature of your claim?',
    placeholder: 'Choose one below or type your own',
    fieldKey: 'claimCategory',
    choices: [
      'Unpaid debt or loan',
      'Property damage',
      'Services not rendered',
      'Security deposit dispute',
      'Personal injury',
      'Other',
    ],
  },
  {
    id: 'narrative',
    label: 'What Happened',
    shortLabel: 'What Happened',
    question:
      'In your own words, describe what happened. Include key events, any agreements or contracts, and how the defendant is responsible. Be as specific as you can.',
    placeholder:
      'e.g. On March 1, 2024 I hired the defendant to renovate my bathroom. They took a $4,500 deposit but left the work incomplete and stopped responding…',
    fieldKey: 'narrative',
  },
  {
    id: 'location',
    label: 'Where',
    shortLabel: 'Location',
    question: 'Where did the issue primarily occur? Provide the city or municipality in British Columbia.',
    placeholder: 'e.g. Victoria',
    fieldKey: 'location',
  },
  {
    id: 'date_range',
    label: 'When',
    shortLabel: 'When',
    question: 'When did this happen? Provide the date or date range when the events that led to your claim occurred.',
    placeholder: 'e.g. March 15, 2024  or  between January and April 2024',
    fieldKey: 'dateRange',
  },
  {
    id: 'remedy',
    label: 'What You Are Asking For',
    shortLabel: 'Amount',
    question:
      'What remedy are you seeking? List what you are claiming and the dollar amounts. The maximum in BC Small Claims Court is $35,000.',
    placeholder: 'e.g. $4,500 deposit not returned + $200 materials I paid for = $4,700 total',
    fieldKey: 'remedyTotal',
  },
]

// Contextual clarification responses keyed by keyword
export const CLARIFICATIONS: Array<{ keywords: string[]; response: string }> = [
  {
    keywords: ['claimant', 'who am i'],
    response:
      'A claimant is the person or organization bringing the claim — that is you. You can file as an individual or as a business entity.',
  },
  {
    keywords: ['organization', 'business', 'corporation', 'company'],
    response:
      'If you are suing as a business, use the full registered name exactly as it appears on your incorporation documents. You can verify this at BC Registry Services (bcregistry.gov.bc.ca).',
  },
  {
    keywords: ['company search', 'registered name', 'registry'],
    response:
      'You can search for a company\'s official registered name at BC Registry Services (bcregistry.gov.bc.ca). Using the exact registered name is important — the claim may be dismissed if the name is wrong.',
  },
  {
    keywords: ['address', 'postal', 'mailing'],
    response:
      'Use a mailing address where you can reliably receive mail. The court registry will send all documents and notices there. A PO Box is acceptable.',
  },
  {
    keywords: ['defendant', 'who am i suing', 'suing'],
    response:
      'The defendant is the person or business you believe owes you money or caused you harm. You need their full legal name and a mailing address so the court can serve them with notice of your claim.',
  },
  {
    keywords: ['serve', 'service', 'served'],
    response:
      'Serving means formally delivering court documents to the defendant. The court registry assists with this — you do not do it yourself. That is why the defendant\'s address is required.',
  },
  {
    keywords: ['small claims', 'limit', 'maximum', 'how much'],
    response:
      'BC Small Claims Court handles disputes up to $35,000. If your claim exceeds that amount, you may need to consider BC Supreme Court instead. The filing fee depends on the amount claimed.',
  },
  {
    keywords: ['form 1', 'notice of claim', 'what is form'],
    response:
      'Form 1 (Notice of Claim) is the document that formally starts a small claims case. It identifies the parties, describes what happened, and states the remedy you are seeking. This assistant helps you prepare it.',
  },
  {
    keywords: ['category', 'type of claim', 'what kind'],
    response:
      'The claim category helps the court understand the nature of the dispute. Choose the one that most closely matches your situation. If none fit, select "Other" and describe it in your narrative.',
  },
  {
    keywords: ['narrative', 'description', 'what to write', 'what do i write'],
    response:
      'Write clearly and in order — what happened first, what was agreed to, what went wrong, and what the defendant did or failed to do. Stick to facts. The court relies on what you write here.',
  },
  {
    keywords: ['remedy', 'amount', 'damages', 'asking for'],
    response:
      'List each item you are claiming separately with a dollar amount, then give a total. For example: "$3,000 unpaid loan + $150 interest = $3,150." Only include amounts you can justify with evidence.',
  },
  {
    keywords: ['lawyer', 'legal advice', 'advice', 'should i'],
    response:
      'I can help you understand what the form asks for, but I cannot give legal advice. For legal guidance, consider contacting Access Pro Bono BC (accessprobono.ca) or the Justice Education Society (justiceeducation.ca) — both offer free resources for self-represented litigants.',
  },
]

export const FALLBACK_CLARIFICATION =
  "That's a good question. I can help clarify what the form requires, but I'm not able to give legal advice. Could you tell me more about what you're unsure of? Or if you're ready, you can continue with the next part of the form."
