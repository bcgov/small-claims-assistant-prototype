import { useCallback, useEffect, useRef, useState } from 'react'
import { CLARIFICATIONS, FALLBACK_CLARIFICATION, INTAKE_STEPS } from '../data/intakeFlow'
import type { ChatMessage, IntakePhase, PartialCase } from '../types/intake'

const TYPING_DELAY_MS = 700

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
    if (entry.keywords.some((kw) => lower.includes(kw))) {
      return entry.response
    }
  }
  return null
}

function buildSummary(data: PartialCase): string {
  const lines: string[] = ['Here is a summary of what you have told me. Please review it carefully.\n']

  lines.push('**CLAIMANT (You)**')
  lines.push(`Name: ${data.claimantName ?? '[missing]'}`)
  lines.push(`Address: ${data.claimantAddress ?? '[missing]'}\n`)

  lines.push('**DEFENDANT**')
  lines.push(`Name: ${data.defendantName ?? '[missing]'}`)
  lines.push(`Address: ${data.defendantAddress ?? '[missing]'}\n`)

  lines.push('**CLAIM**')
  lines.push(`Category: ${data.claimCategory ?? '[missing]'}`)
  lines.push(`Location: ${data.location ?? '[missing]'}`)
  lines.push(`Date / period: ${data.dateRange ?? '[missing]'}`)
  lines.push(`What happened: ${data.narrative ?? '[missing]'}\n`)

  lines.push('**REMEDY**')
  lines.push(`Amount claimed: ${data.remedyTotal ?? '[missing]'}\n`)

  lines.push('Does everything look correct? Reply **"confirm"** to proceed to the next step, or tell me what needs to be changed.')

  return lines.join('\n')
}

export function useIntakeChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [stepIndex, setStepIndex] = useState(0)
  const [caseData, setCaseData] = useState<PartialCase>({})
  const [phase, setPhase] = useState<IntakePhase>('intake')
  const [isTyping, setIsTyping] = useState(false)
  const [input, setInput] = useState('')
  const initialized = useRef(false)

  const addAssistantMessage = useCallback(
    (content: string, extra?: Partial<ChatMessage>) => {
      setMessages((prev) => [
        ...prev,
        { id: uid(), role: 'assistant', content, type: 'text', ...extra },
      ])
    },
    [],
  )

  const simulateTyping = useCallback(
    (content: string, extra?: Partial<ChatMessage>) => {
      setIsTyping(true)
      setTimeout(() => {
        setIsTyping(false)
        setMessages((prev) => [
          ...prev,
          { id: uid(), role: 'assistant', content, type: 'text', ...extra },
        ])
      }, TYPING_DELAY_MS)
    },
    [],
  )

  // Bootstrap the conversation with the welcome message
  useEffect(() => {
    if (initialized.current) return
    initialized.current = true

    const welcome =
      'Welcome to the BC Small Claims Notice of Claim assistant.\n\nI will guide you through Form 1 step by step. You can type your answers, and if you have a question at any point, just ask — I will do my best to explain what the form needs.\n\nLet\'s get started.'

    setTimeout(() => {
      setMessages([{ id: uid(), role: 'assistant', content: welcome, type: 'text' }])

      const firstStep = INTAKE_STEPS[0]
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          {
            id: uid(),
            role: 'assistant',
            content: firstStep.question,
            type: firstStep.choices ? 'choice' : 'text',
            choices: firstStep.choices,
            hint: firstStep.hint,
          },
        ])
      }, TYPING_DELAY_MS)
    }, 400)
  }, [])

  const send = useCallback(
    (text: string) => {
      const trimmed = text.trim()
      if (!trimmed || isTyping) return

      // Add user message
      const userMsg: ChatMessage = { id: uid(), role: 'user', content: trimmed, type: 'text' }
      setMessages((prev) => [...prev, userMsg])
      setInput('')

      if (phase === 'complete') return

      if (phase === 'confirming') {
        const lower = trimmed.toLowerCase()
        if (lower.includes('confirm') || lower === 'yes' || lower === 'y') {
          setPhase('complete')
          simulateTyping(
            'Your intake is confirmed. The next step is to generate your Notice of Claim PDF. You can download the draft and review it before filing at the BC court registry.',
          )
        } else {
          setPhase('intake')
          simulateTyping(
            'No problem — let\'s go back through your answers. Which section would you like to update? (For example: "claimant name", "defendant address", "what happened", etc.)',
          )
        }
        return
      }

      // Intake phase — check if user is asking a question
      if (isQuestion(trimmed)) {
        const clarification = findClarification(trimmed) ?? FALLBACK_CLARIFICATION
        setIsTyping(true)
        setTimeout(() => {
          setIsTyping(false)
          setMessages((prev) => [
            ...prev,
            { id: uid(), role: 'assistant', content: clarification, type: 'text' },
          ])

          // Re-ask the current step after a second delay
          const step = INTAKE_STEPS[stepIndex]
          setTimeout(() => {
            setMessages((prev) => [
              ...prev,
              {
                id: uid(),
                role: 'assistant',
                content: `To continue: ${step.question}`,
                type: step.choices ? 'choice' : 'text',
                choices: step.choices,
                hint: step.hint,
              },
            ])
          }, TYPING_DELAY_MS)
        }, TYPING_DELAY_MS)
        return
      }

      // Save the answer
      const step = INTAKE_STEPS[stepIndex]
      const updated: PartialCase = { ...caseData, [step.fieldKey]: trimmed }
      setCaseData(updated)

      const nextIndex = stepIndex + 1

      if (nextIndex >= INTAKE_STEPS.length) {
        // All steps done — show summary
        setPhase('confirming')
        setIsTyping(true)
        setTimeout(() => {
          setIsTyping(false)
          setMessages((prev) => [
            ...prev,
            { id: uid(), role: 'assistant', content: buildSummary(updated), type: 'summary' },
          ])
        }, TYPING_DELAY_MS)
      } else {
        // Advance to next step
        setStepIndex(nextIndex)
        const nextStep = INTAKE_STEPS[nextIndex]
        simulateTyping(nextStep.question, {
          type: nextStep.choices ? 'choice' : 'text',
          choices: nextStep.choices,
          hint: nextStep.hint,
        })
      }
    },
    [caseData, isTyping, phase, simulateTyping, stepIndex],
  )

  return {
    messages,
    stepIndex,
    caseData,
    phase,
    isTyping,
    input,
    setInput,
    send,
    steps: INTAKE_STEPS,
  }
}
