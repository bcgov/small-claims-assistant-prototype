# Anthropic: How We Built Our Multi-Agent Research System

Source: https://www.anthropic.com/engineering/multi-agent-research-system

## What the article says

Anthropic describes a research system built around a lead agent and multiple subagents. The lead agent plans the work, breaks it into parts, and sends those parts out in parallel. The subagents search, compare, and gather information. The lead agent then synthesizes the results.

The key point is simple. Open-ended research is not a straight line. It needs parallel exploration, memory, and coordination.

## Main takeaways

- Multi-agent systems work well for broad, open-ended research.
- Parallel subagents help cover more ground than a single pass.
- Search is not just retrieval. It is a process of finding, testing, narrowing, and synthesizing.
- Tool design, prompt design, and evaluation matter as much as the model.
- Production systems need checkpoints, memory, observability, and reliable handoff patterns.

## Why it matters here

This supports the broader BC Gov framing in two ways.

First, the front-door router should not only hand off form work. It should also identify the knowledge domain behind a citizen request and route it to the best specialist agent.

Second, the specialist agent should be able to use the right retrieval strategy for the job. That may be:

- indexed document retrieval
- RAG over curated content
- semantic search
- recursive or deep search across linked material
- direct reasoning over the gathered evidence

The point is not to force every request through the same path. The point is to route the request well, then let the specialist use the best search method available.
