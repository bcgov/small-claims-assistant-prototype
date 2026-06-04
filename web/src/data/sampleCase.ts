export const sampleCase = {
  schemaVersion: '1.0.0',
  formType: 'bc-small-claims-notice-of-claim',
  jurisdiction: {
    country: 'CA',
    province: 'BC',
    court: 'Small Claims Court',
    registryLocation: 'Vancouver',
  },
  caseMetadata: {
    draftId: 'noc-web-001',
    status: 'ready-for-review',
    intakeChannel: 'web',
    language: 'en',
  },
  claimants: [
    {
      id: 'claimant-1',
      type: 'individual',
      name: { full: 'Jane Example' },
      contact: {
        addressLines: ['123 Main Street'],
        city: 'Vancouver',
        province: 'BC',
        postalCode: 'V6B 1A1',
        email: 'jane@example.com',
      },
    },
  ],
  defendants: [
    {
      id: 'defendant-1',
      type: 'business',
      name: { full: 'ABC Renovations Ltd.' },
      contact: {
        addressLines: ['456 Industrial Way'],
        city: 'Burnaby',
        province: 'BC',
        postalCode: 'V5C 2B2',
      },
    },
  ],
  claim: {
    category: 'goods-or-services',
    summary: 'Renovation work was paid for but not completed.',
    facts: 'The defendant agreed to complete kitchen renovation work by March 15, 2026.',
    location: {
      city: 'Vancouver',
      province: 'BC',
      country: 'CA',
    },
    incidentDate: {
      type: 'single',
      start: '2026-03-15',
      end: null,
    },
  },
  remedies: [
    {
      id: 'remedy-1',
      type: 'money',
      description: 'Refund for incomplete renovation work',
      amount: {
        currency: 'CAD',
        value: 3500,
      },
    },
  ],
  attachments: [],
  service: {
    certificateRequired: true,
    notes: 'Reserved for later package expansion.',
  },
  validation: {
    isComplete: true,
    missingFields: [],
    warnings: [],
  },
  generation: {
    pdf: {
      ready: true,
      templateVersion: 'bc-scc-form1-v1',
    },
    filingPayload: {
      ready: true,
    },
  },
} as const