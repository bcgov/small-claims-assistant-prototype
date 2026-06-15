# Research Index

This folder collects short summaries of articles and papers that shape the BC Small Claims assistant vision.
Each note links back to the original source for the full article.

Use it for two things:

1. quick summaries of the source material
2. the practical takeaway for this repo

## Current notes

- [Anthropic multi-agent research system](anthropic-multi-agent-research-system.md)
- [Agent Registry marketplace pattern](agent-registry-marketplace.md)
- [Microsoft: From apps to agents](microsoft-from-apps-to-agents.md)
- [Microsoft: Frontier Transformation](microsoft-frontier-transformation.md)
- [Microsoft Build 2026 platform analysis](microsoft-build-2026-platform-analysis.md)
- [Workday: The AI Front Door](workday-ai-front-door.md)

## Why this exists

The platform is not just for form assistants. It also has to broker government knowledge.

That means the front-door router should first identify the knowledge domain, then route to the agent that knows that domain best. From there, the agent can use the right retrieval mode for the job:

- RAG over indexed content
- semantic search
- recursive or deep search across related material
- direct specialist reasoning when retrieval is not enough

The research notes in this folder capture the sources behind that framing.
