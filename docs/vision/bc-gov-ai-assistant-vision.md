# BC Government AI Assistant Vision
## A Unified Front-Door Agent Architecture for Public Services

**Author:** Richard Fremmerlid, Business Architect  
**Date:** 2026-06-15  
**Status:** Vision / Strategic Proposal

---

## Executive Summary

BC Government is starting to experiment with AI assistants inside individual applications, usually as form-filler chatbots bolted onto existing workflows. The early demos are promising, but they point toward an **unsustainable pattern**: one bespoke app per form, repeated across thousands of government services.

This document proposes a simpler path: a **single, unified AI front-door agent** backed by a registry of modular, open-standard skills and sub-agents. Instead of building and maintaining thousands of separate applications, the government keeps **one routing orchestrator, one consistent UI, and a growing library of pluggable capabilities**. That is cheaper to build, easier to maintain, better for citizens, and closer to where the industry is headed.

A working proof of concept, a *Small Claims Notice of Claim assistant* built as an open-standard plugin with no UI dependency, already shows the model in practice.

The same front door should also broker government knowledge. Sometimes the citizen does not need a form at all. They need the right policy, program, or service answer. In that case, the router should identify the knowledge domain and send the request to the agent that knows that content best.

---

## The Problem: Bespoke App Proliferation

### What We're Seeing

Early AI assistant experiments in BC Gov (e.g., LCRB Liquor & Cannabis Licensing, BC Courts Online Filing Assistant) demonstrate that AI can help users complete government forms through conversational interaction. The LCRB demo, for example, uses Azure AI Foundry to power a sidebar chatbot that walks users through licence applications.

### Why It Doesn't Scale

Building a bespoke AI-assisted application for every government form creates four critical problems:

1. **Can't scale support.** Government has thousands of forms across dozens of ministries. We cannot build, staff, secure, and maintain thousands of separate AI-enabled applications. The operational burden is unsustainable.

2. **Terrible discoverability.** Citizens would need to search across dozens of websites to find the right app for their specific need. Most won't find it. The experience is fragmented by design.

3. **Inconsistent experience.** Each team builds its own UI, its own interaction patterns, its own branding treatment. Nothing looks or feels the same. Citizens experience government as a disconnected collection of one-off tools.

4. **Non-portable architecture.** Every bespoke app is tightly coupled to its own stack. When the delivery paradigm shifts, and it will, none of these apps can be repurposed. They are throwaway investments in a technology trajectory that is already obsolete.

### The Forms Paradigm Is Already Obsolete

The deeper issue is that these experiments remain **wedded to the form**. An AI assistant that helps you fill out a form is an improvement, but it's still forcing the citizen into a data-entry paradigm. The same problem shows up when answers are buried in program guides, policy pages, and service content. An AI assistant can:

- Ask clarifying questions conversationally
- Summarize and confirm answers
- Call an API directly once information is validated
- Output a PDF, JSON payload, or filing submission

**The form itself is unnecessary.** The citizen's intent is the input. Structured data is the output. The form is a legacy intermediary that adds friction without adding value.

---

## The Vision: One Front Door, Many Capabilities

### Core Concept

Replace thousands of bespoke applications with a **single, intelligent routing agent** that serves as the front door to all BC Government services and knowledge. The citizen has one conversation. The system figures out where to route them.

### How It Works

1. **Citizen states their goal.** "I need to file a small claims notice of claim" or "I want to renew my liquor licence"
2. **The routing agent resolves intent.** It does not try to do everything itself. It identifies what the citizen needs.
3. **The router searches a registry.** A database of available agents, skills, and connectors, each described by standardized metadata
4. **The router delegates.** The citizen is routed to the appropriate specialized sub-agent or skill, which handles the domain-specific interaction
5. **The sub-agent completes the workflow.** Intake, validation, PDF generation, API submission, whatever the service requires
6. **Results return through the same interface.** The citizen never leaves the unified experience

### Architecture Pillars

| Pillar | Description |
|--------|-------------|
| **One App, One UI, One Brand** | A single consistent interface to maintain. One codebase. One design system (BC Gov). One place citizens go. |
| **Open Agent/Skill Formats** | Skills and agents are defined using open standards (e.g., `SKILL.md` per the [agentskills.io](https://agentskills.io/specification) specification). Portable, version-controlled, shareable. |
| **Capability Registry** | A searchable database of all registered agents, skills, and connectors. The routing agent queries this registry to find the right capability for each citizen request. Implementation may use MCP servers, direct database access, or a hybrid approach. |
| **Front-Door Orchestrator/Router** | An LLM-powered routing agent that resolves citizen intent and delegates to specialized sub-agents. It does not try to be an expert in everything. It is an expert in finding the right expert. |
| **Dual-Purpose Security Layer** | The same routing layer doubles as an LLM proxy for security enforcement, data loss prevention (DLP), content filtering, and audit logging. Every interaction passes through a governed gateway. |

---

## Architecture Reference

This vision aligns with a broader set of patterns already showing up across the AI ecosystem:

- **Intent-first development**: Microsoft's "From apps to agents" article makes the same core point. Users express intent, agents determine execution, and apps become trusted capabilities instead of navigation surfaces.
- **Frontier Transformation**: Microsoft's later Dynamics 365 post adds the missing third layer. The interface shifts to assistants, agents orchestrate work, and an intelligence layer unifies structured and unstructured knowledge across the organization.
- **Platform consolidation**: Microsoft Build 2026 points at the operational side of the same shift. Shared context, control planes, and agent governance are becoming core platform features, not add-ons.
- **Front door plus identity**: Workday’s front-door framing adds the execution layer. A useful front door needs knowledge mode, execution mode, and durable identity files for the agents behind it.
- **Knowledge Brokerage**: Route requests by domain first, then let the specialist agent search the best source of truth using indexed content, RAG, semantic search, or deeper recursive search
- **The Front-End AI Agent (The Conductor)**: The citizen's single conversational interface
- **The LLM Orchestrator (The Brain)**: Routes tasks using frameworks like LangChain/LangGraph
- **Specialized AI Agents (The Expert Team)**: Domain-specific agents (Motor Vehicles, Revenue & Tax, Courts, etc.), following the multi-agent pattern validated by Anthropic's internal research systems
- **Model Context Protocol (MCP) (The Nervous System)**: Open-standard inter-agent communication, as introduced by Anthropic and adopted by OpenAI
- **Security & Governance (The Shield)**: Verifiable agent identity via standards like Microsoft Entra Agent ID, with zero-trust principles applied to agent-to-agent and agent-to-data interactions

---

## Proof of Concept: Small Claims Assistant Plugin

### Approach Differences

| Aspect | LCRB Bespoke App | Small Claims Plugin |
|--------|-------------------|---------------------|
| **Starting point** | Enterprise application with embedded AI sidebar | Low-cost prototype, no UI required |
| **UI dependency** | Requires full web application to function | Works entirely within an AI coding assistant (Claude Code, GitHub Copilot), so no UI is needed |
| **Question flow** | AI generates all questions | Hybrid: JSON question set as the baseline, with AI only used when the user needs clarification |
| **Portability** | Locked to one application stack | Open-standard `SKILL.md` files; portable across any agent host |
| **Iteration model** | Requires full dev cycle to test changes | Developer or user iterates in IDE with immediate Q&A feedback |
| **Cost to build** | High (enterprise app + AI integration) | Low (skills, scripts, and a canonical JSON contract) |

### What Was Built

A Claude Code plugin (`small-claims-assistant`) with cleanly separated concerns:

- **`notice-of-claim-intake`** skill: Guided conversational intake following the BC Courts Filing Assistant question order, driven by a JSON intake definition
- **`notice-of-claim-pdf-generation`** skill: Deterministic PDF rendering by overlaying case data onto the official Form 1 template
- **`notice-of-claim-filing-adapter`** skill: Mock filing submission adapter consuming the same canonical JSON
- **`notice-of-claim-intake-agent`**: Sub-agent orchestrating the intake conversation with memory, tool restrictions, and a focused system prompt

### The Canonical Case Model

The **canonical case JSON** is the single source of truth, a shared data contract consumed by intake, validation, PDF rendering, and filing. This is the integration seam, not the UI.

### Web App as Optional Layer

A separate Next.js web application was built to demonstrate that the **same data contract and intake logic** can power a branded BC Gov web experience. The web app uses:

- `@bcgov/design-system-react-components` for consistent branding
- The same intake flow definitions and canonical JSON schema
- A one-line swap point for replacing local clarification logic with an Azure Copilot API call

**Key point:** The web app is an optional presentation layer. The underlying skills, data model, and scripts are the durable investment.

---

## Future Positioning

### Agent/Skill Marketplace

Skills authored in open formats (`SKILL.md`) can be shared through marketplaces, within government, across jurisdictions, or publicly. A skill that handles BC Small Claims intake could be adapted for other provinces with minimal changes.

Registry-style marketplaces are already becoming practical in the broader ecosystem, including agent registries that publish reusable Claude agent configurations and MCP server bundles.

### Research Notes

The research index in `docs/research` captures source articles that support the knowledge-broker, marketplace, intent-first, intelligence-layer, platform-consolidation, and front-door identity framing, including the Anthropic multi-agent research article, the agent registry article, Microsoft's "From apps to agents" article, Microsoft's Frontier Transformation post, the Microsoft Build 2026 analysis, and the Workday front-door article.

For the risks and assumptions that are easy to underestimate, see [BC Government AI Assistant: Problems to Not Underestimate](bc-gov-ai-assistant-problems.md).

### Phone-Native Agent Consumption

The industry trajectory suggests that phones will increasingly consume agents and skills directly, rather than requiring users to download and navigate thousands of separate apps. By building capabilities as portable skills rather than bespoke applications, BC Gov is positioned for this shift.

### Plug-and-Play Evolution

When the underlying AI models, protocols, or delivery platforms change, the **skills and data contracts remain stable**. A new front-end can be wired to the same registry. A new orchestrator can discover the same skills. The investment in capability definition is preserved regardless of how the technology evolves.

---

## Industry Alignment

This vision is not speculative. It reflects a convergent architectural pattern that shows up across the AI industry:

| Signal | Source |
|--------|--------|
| Agentic AI era collapsing software apps | Satya Nadella, Microsoft |
| Multi-agent orchestration outperforming monolithic AI | Anthropic Engineering (internal multi-agent research system) |
| Model Context Protocol (MCP) as open-standard agent communication | Anthropic (creator), adopted by OpenAI |
| Entra Agent ID for verifiable, sovereign agent identity | Microsoft |
| Conversational AI replacing forms in government | CloudApper, Supervity, Deloitte case studies |
| AI-powered government service transformation | Harvard Kennedy School, Snowflake, Foundever, GovNet |
| Agent Skills open specification | [agentskills.io](https://agentskills.io/specification) |

---

## Open Questions

| Question | Notes |
|----------|-------|
| **Registry implementation** | Should the capability registry be fronted by an MCP server, accessed via direct database queries, or a hybrid? MCP provides standardized discovery; direct access may be simpler initially. |
| **Authentication & identity** | How does the front-door agent authenticate citizens? BC Services Card integration? Federated identity? How are sub-agents authenticated to backend systems (Entra Agent ID pattern)? |
| **Security & DLP specifics** | What content filtering, PII detection, and data loss prevention rules apply at the routing layer? What audit trail is required? |
| **Skill governance** | Who approves new skills for the registry? What testing, review, and certification process ensures quality and security? |
| **Inter-ministry coordination** | Each ministry owns its domain data and processes. How are skill boundaries, data sharing agreements, and accountability structured? |
| **Incremental adoption** | Can ministries onboard incrementally, publishing skills to the registry as they're ready, without requiring a big-bang migration? |
| **Existing system integration** | Many backend systems (CEIS, JUSTIN, ICM, etc.) have existing APIs or no APIs at all. How do connectors bridge the gap? |

---

## Summary

| Bespoke App Per Form | Unified Front-Door Agent |
|----------------------|--------------------------|
| Thousands of apps to maintain | One app to maintain |
| Fragmented, hard-to-find experiences | One consistent entry point |
| Inconsistent UI/UX across ministries | One brand, one design system |
| Tightly coupled to current tech stack | Portable skills that survive platform shifts |
| Expensive to build and change | Low-cost skills iterated in an IDE |
| Forms as the interaction paradigm | Conversation as the interaction paradigm |
| Siloed investments | Shared, composable capability registry |

**The question is not whether this shift is coming. It is whether BC Government builds ahead of it or gets pulled into it after investing in thousands of throwaway apps.**

---

*Related reading and prior writing:*
- [Microsoft: From apps to agents](https://www.microsoft.com/en-us/power-platform/blog/2026/03/12/from-apps-to-agents-rearchitecting-enterprise-work-around-intent/)
- [Microsoft: Frontier Transformation](https://www.microsoft.com/en-us/dynamics-365/blog/business-leader/2026/03/09/a-new-way-of-working-is-taking-shape-frontier-transformation/)
- [Microsoft Build 2026 platform analysis](https://www.efficientlyconnected.com/microsoft-build-2026-developer-ai-platform-analysis/)
- [Workday: The AI Front Door](https://medium.com/workday-engineering/the-ai-front-door-is-already-here-its-becoming-the-enterprise-execution-layer-105c067ca081)
- [Anthropic multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Agent Registry marketplace pattern](https://21st.dev/community/blog/agent-registry)
- [The End of Government Forms: A Vision for an AI-Powered Public Service](https://medium.com/@richard.fremmerlid) (Fremmerlid, 2025)
- [Architecting the Future: A Technical Blueprint for a Unified Government AI Agent](https://medium.com/@richard.fremmerlid) (Fremmerlid, 2025)
- [small-claims-assistant plugin](https://github.com/) (proof of concept)
