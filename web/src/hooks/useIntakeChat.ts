import { useCallback, useEffect, useRef, useState } from 'react'
import {
  buildSummary,
  CLARIFICATIONS,
  FALLBACK_CLARIFICATION,
  INTAKE_SECTIONS,
  INTAKE_STEPS,
} from '../data/intakeFlow'
import type { ChatMessage, IntakePhase, PartialCase } from '../types/intake'

const TYPING_DELAY_MS = 650

function uid() {
  return `${Date.now()}-${Math.random().toString(36).slice(2)}`
}

function isQuestion(text: string): boolean {
  const lower = text.trim().toLowerCase()
  if (lower.endsWith('?')) return true
  return /^(what|how|why|when|where|who|which|is|are|can|do|does|will|should|would|could|may|might)\s/.test(lower)
}

function findClarification(text: string): string | null {
  const lower = text.toLowerCase()
  for (const entry of CLARIFICATIONS) {
    if (entry.keywords.some((kw) => lower.includes(kw))) return entry.response
  }
  return null
}

function nextStepIndex(fromIndex: number, data: PartialCase): number {
  let i = fromIndex + 1
  while (i < INTAKE_STEPS.length && INTAKE_STEPS[i].skipIf?.(data)) i++
  return i
}

export function useIntakeChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [stepIndex, setStepIndex] = useState(0)
  const [caseData, setCaseData] = useState<PartialCase>({})
  const [phase, setPhase] = useState<IntakePhase>('intake')
  const [isTyping, setIsTyping] = useState(false)
  const [input, setInput] = useState('')
  const initialized = useRef(false)

  const pushAssistant = useCallback((content: string, extra?: Partial<ChatMessage>) => {
    setMessages((prev) => [
      ...prev,
      { id: uid(), role: 'assistant', content, type: 'text', ...extra },
    ])
  }, [])

  const typeAssistant = useCallback((content: string, extra?: Partial<ChatMessage>, delay = TYPING_DELAY_MS) => {
    setIsTyping(true)
    setTimeout(() => {
      setIsTyping(false)
      setMessages((prev) => [
        ...prev,
        { id: uid(), role: 'assistant', content, type: 'text', ...extra },
      ])
    }, delay)
  }, [])

  // Boot the conversation
  useEffect(() => {
    if (initialized.current) return
    initialized.current = true
    const first = INTAKE_STEPS[0]
    setTimeout(() => {
      setMessages([{
        id: uid(),
        role: 'assistant',
        content: first.question,
        type: first.choices ? 'choice' : 'text',
        choices: first.choices,
        hint: first.hint,
      }])
    }, 300)
  }, [])

  const send = useCallback((text: string) => {
    const trimmed = text.trim()
    if (!trimmed || isTyping) return

    setMessages((prev) => [...prev, { id: uid(), role: 'user', content: trimmed, type: 'text' }])
    setInput('')

    if (phase === 'complete') return

    if (phase === 'confirming') {
      const lower = trimmed.toLowerCase()
      if (lower === 'confirm' || lower === 'yes' || lower === 'y' || lower === 'looks good' || lower === 'correct') {
        setPhase('complete')
        typeAssistant(
          "Your intake is confirmed.\n\nThe next step is to generate your **Notice of Claim PDF**. You will need:\n\n1. The Notice of Claim (Form 1) — generated from your answers\n2. A Form 38 (Address for Service) — available at justice.gov.bc.ca\n3. Your filing fee\n\nTake these to your chosen registry, or mail them in. The registry will process your claim and arrange service on the defendant.",
        )
      } else {
        setPhase('intake')
        typeAssistant("No problem — let's go back and update your answers. Which section would you like to change?\n(e.g. \"claimant address\", \"defendant name\", \"what happened\", \"remedy\", etc.)")
      }
      return
    }

    // Intake phase
    const step = INTAKE_STEPS[stepIndex]

    // Info step — any input advances
    if (step.isInfo) {
      const updated = caseData
      const ni = nextStepIndex(stepIndex, updated)
      if (ni >= INTAKE_STEPS.length) {
        setPhase('confirming')
        typeAssistant(buildSummary(updated), { type: 'summary' })
      } else {
        setStepIndex(ni)
        const next = INTAKE_STEPS[ni]
        typeAssistant(next.question, {
          type: next.choices ? 'choice' : 'text',
          choices: next.choices,
          hint: next.hint,
        })
      }
      return
    }

    // User is asking a question — static keyword lookup handles common terms at zero AI cost.
    // TODO: replace findClarification() with an Azure Copilot API call for production.
    //   Pass { userMessage: trimmed, currentStep: step.id, currentSection: step.sectionId,
    //          capturedSoFar: caseData } so the model can give a context-aware answer
    //   (e.g. it knows the user is on "defendant address" and has already captured their name).
    //   See PlumbingPoC packages/frontend/src/features/requests/components/QuoteAgentModal.tsx
    //   for the reference pattern: POST /agents/quote/run with messages + context payload,
    //   handle streaming or single-shot response, then re-ask the current step.
    if (isQuestion(trimmed)) {
      const clarification = findClarification(trimmed) ?? FALLBACK_CLARIFICATION
      setIsTyping(true)
      setTimeout(() => {
        setIsTyping(false)
        setMessages((prev) => [
          ...prev,
          { id: uid(), role: 'assistant', content: clarification, type: 'text' },
        ])
        // Re-ask current step after second delay
        setTimeout(() => {
          setMessages((prev) => [
            ...prev,
            {
              id: uid(),
              role: 'assistant',
              content: `To continue — ${step.question}`,
              type: step.choices ? 'choice' : 'text',
              choices: step.choices,
              hint: step.hint,
            },
          ])
        }, TYPING_DELAY_MS)
      }, TYPING_DELAY_MS)
      return
    }

    // Save answer (skip info steps and _info fieldKey)
    const updated: PartialCase = step.fieldKey === '_info'
      ? caseData
      : { ...caseData, [step.fieldKey]: trimmed }
    setCaseData(updated)

    const ni = nextStepIndex(stepIndex, updated)

    if (ni >= INTAKE_STEPS.length) {
      setPhase('confirming')
      typeAssistant(buildSummary(updated), { type: 'summary' })
    } else {
      setStepIndex(ni)
      const next = INTAKE_STEPS[ni]

      // Detect section change and add a brief transition message
      const prevSection = step.sectionId
      const nextSection = next.sectionId
      if (prevSection !== nextSection) {
        const section = INTAKE_SECTIONS.find((s) => s.id === nextSection)
        setIsTyping(true)
        setTimeout(() => {
          setIsTyping(false)
          // Section transition acknowledgement — lightweight
          const ack = getSectionAck(nextSection)
          setMessages((prev) => [
            ...prev,
            { id: uid(), role: 'assistant', content: ack, type: 'text' },
          ])
          setTimeout(() => {
            setMessages((prev) => [
              ...prev,
              {
                id: uid(),
                role: 'assistant',
                content: next.question,
                type: next.choices ? 'choice' : 'text',
                choices: next.choices,
                hint: next.hint,
              },
            ])
          }, TYPING_DELAY_MS)
        }, TYPING_DELAY_MS)
      } else {
        typeAssistant(next.question, {
          type: next.choices ? 'choice' : 'text',
          choices: next.choices,
          hint: next.hint,
        })
      }
    }
  }, [caseData, isTyping, phase, stepIndex, typeAssistant])

  // Current section index for sidebar
  const currentSectionIndex = INTAKE_SECTIONS.findIndex(
    (s) => s.stepIds.includes(INTAKE_STEPS[stepIndex]?.id ?? ''),
  )

  return {
    messages,
    stepIndex,
    currentSectionIndex: phase === 'confirming' || phase === 'complete'
      ? INTAKE_SECTIONS.length - 1
      : Math.max(0, currentSectionIndex),
    caseData,
    phase,
    isTyping,
    input,
    setInput,
    send,
    sections: INTAKE_SECTIONS,
  }
}

function getSectionAck(sectionId: string): string {
  const map: Record<string, string> = {
    defendant: "Got it — I have your information.\n\nNow let's capture the defendant's details.",
    what_happened: "Defendant information recorded.\n\nNow let's describe what happened.",
    where_when: "Good. Now I need a couple of details about where and when this occurred.",
    remedy: "Almost there. Now let's capture what you are claiming.",
    filing: "Great. One last section — let's confirm where you will file your claim.",
    settle: "Filing details noted.\n\nBefore we wrap up, here is some important information about settlement options.",
  }
  return map[sectionId] ?? "Let's continue."
}
