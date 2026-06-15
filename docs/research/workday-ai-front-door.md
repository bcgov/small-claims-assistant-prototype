# Workday: The AI Front Door

Source: https://medium.com/workday-engineering/the-ai-front-door-is-already-here-its-becoming-the-enterprise-execution-layer-105c067ca081

## What the article says

Workday argues that enterprise AI has a fragmentation problem, not a capability problem. The fix is one unified front door rather than a pile of isolated copilots and bots.

The article also draws a hard line between knowledge and execution. A useful front door needs both. It should answer questions, guide users, draft work, and also plan, preview, approve, and act when permissions allow.

## Main takeaways

- Fragmented copilots create a cognitive tax.
- A front door needs knowledge mode and execution mode.
- Agent identity has to be durable, not just buried in a prompt.
- Orchestration is the product once agents can act.
- Governance, audit, and permissioning are part of the core design.

## Why it matters here

This is a close match for the BC Gov architecture.

It reinforces three repo ideas:

- one front door instead of many isolated assistants
- specialist agents behind the front door, each with clear identity and boundaries
- a control plane that keeps execution safe, auditable, and predictable

The article’s SOUL.md idea is especially relevant. It supports the same basic direction as SKILL.md: durable agent identity files that travel with the agent and define how it should behave.
