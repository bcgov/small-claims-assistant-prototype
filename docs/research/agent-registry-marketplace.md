# 21st.dev: Introducing the Agent Registry

Source: https://21st.dev/community/blog/agent-registry

## What the article says

The article describes a marketplace for Anthropic Managed Agent configurations. In practice, that means a reusable YAML or JSON definition for a Claude agent, including the model, system prompt, and MCP server connections.

The main idea is reuse. Teams keep rebuilding the same agents from scratch, so a registry makes the useful ones easy to publish, discover, and copy.

## Main takeaways

- Agent configs are real engineering assets.
- Prompt work takes iteration.
- MCP server combinations are reusable once someone has done the setup work.
- Discovery matters as much as authoring.
- A registry lowers the cost of reusing good agent patterns.

## Why it matters here

This supports the BC Gov architecture in a second way.

The platform should not only route citizens to the right knowledge or form agent. It should also make good agents easy to reuse across ministries and domains. A registry gives the system a place to publish, discover, and govern those agents.

That lines up with the broader capability registry idea in this repo:

- agents
- skills
- connectors
- templates
- domain-specific research helpers

In practice, this makes the platform more than a front door. It becomes a distribution layer for good government agents.
