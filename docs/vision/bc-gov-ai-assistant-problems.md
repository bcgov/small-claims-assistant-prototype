# BC Government AI Assistant: Problems to Not Underestimate

This is the short list of things the main vision should not gloss over.

## 1. Routing is the hardest part

Real citizen requests are ambiguous. The router needs disambiguation, multi-turn narrowing, confidence thresholds, and a safe fallback when the domain is unclear.

Rebuttal: the router is an LLM. It can ask clarifying questions the same way a human service desk does. Multi-turn narrowing is a core conversational pattern, not a blocker.

## 2. This is a platform, not one app

The goal is not “one app instead of 1,000.” The real shape is a shared platform with a gateway, router, registry, skills, agents, connectors, and operations behind one citizen-facing surface.

Rebuttal: “one app” means one citizen-facing entry point. The back-office platform is a separate operational and funding discussion, not a flaw in the front-door vision.

## 3. Governance will decide whether this gets adopted

Ministries own their data, budgets, and touchpoints. Any shared model needs registry governance, funding, participation incentives, and cross-ministry agreement on standards and data boundaries.

Rebuttal: valid concern, but it is a governance and change-management problem, not an architecture flaw. The design already supports incremental adoption, with ministries publishing skills at their own pace.

## 4. The PoC proves one thing, not everything

The small-claims plugin shows skill portability and a clean contract. It does not prove cross-domain routing, registry discovery at scale, human escalation, or production governance.

Rebuttal: correct by design. The PoC was meant to prove skill portability, the canonical data contract, no-UI authoring, and web-app reuse. It should be explicit about that.

## 5. Forms are not dead

The interaction pattern is changing. The legal and data contract still matters. The form survives as a requirement set, even if the user no longer has to interact with it directly.

Rebuttal: the vision is not saying outputs disappear. It is saying the form as an interaction paradigm is dying. The conversational agent still produces structured output, PDFs, and API submissions.

## 6. Human handoff is required

Government work often needs review, approval, override, or escalation. The architecture needs a clear human-in-the-loop path for complex, risky, or binding actions.

Rebuttal: supported by the architecture. A sub-agent can escalate to a human the same way it delegates to another tool or agent. The handoff should be made explicit.

## 7. Reliability and liability need a plan

LLM behavior can change. Legally consequential work needs deterministic fallback, regression testing, audit trails, and a clear accountability model.

Rebuttal: valid government-specific concern. The hybrid approach already reduces risk by using deterministic question flows first and AI only for clarification. Human review gates and regression tests still need to be documented.

## 8. Cost needs a real model

Per-skill cost is only half the picture. The platform has fixed costs too. The business case needs a break-even view, not a simple app-vs-skill comparison.

Rebuttal: agreed. The honest framing is high fixed platform cost plus low marginal skill cost, with a break-even point after N skills.

## 9. Some assumptions are still speculative

MCP maturity, phone-native agent consumption, and open registry adoption are promising, but not guaranteed. They should be framed as strategic bets, not certainties.

Rebuttal: MCP is one option, not a dependency. The architecture can also use REST, gRPC, SOAP, or direct links to existing apps. Phone-native agent consumption is already being demonstrated through voice-to-text, skill invocation, response, and text-to-voice pipelines. The real question is whether the ecosystem is open or closed. Portable skills still make sense either way.

## 10. The example set is still narrow

The current examples lean heavily toward intake and form filling. Status checks, scheduling, payments, appeals, complaints, and case management should also be represented.

Rebuttal: fair point. That is a presentation gap, not an architecture gap. The skill model is interaction-agnostic and can support those other patterns too.

## What the main docs should add

- a disambiguation flow for ambiguous requests
- a human escalation pattern
- a governance and funding model
- a clearer PoC scope statement
- a TCO / break-even note
- a broader interaction pattern taxonomy
