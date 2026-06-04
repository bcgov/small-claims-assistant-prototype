# Acceptance Criteria

- The skill activates for guided Notice of Claim intake requests and other first-pass Form 1 interview prompts.
- The skill asks questions in small batches rather than presenting a full checklist all at once.
- The skill reflects back captured facts before moving to the next intake section.
- The skill produces concise user-facing intake updates with captured facts, unresolved gaps, and next follow-up questions while keeping the canonical case draft internal unless the user asks to inspect it.
- When intake is sufficiently complete, the skill asks the user to confirm the summary and then offers plain-language next-step handoffs such as PDF generation or filing-adapter preparation.
- The skill does not expose black-box technical details such as canonical JSON, payloads, renderer handoffs, file paths, commands, status flags, or system-generated metadata in normal user-facing replies.
- Unknown values are marked clearly instead of being inferred.
- The skill does not claim to provide legal advice, render PDFs, or silently complete missing facts.