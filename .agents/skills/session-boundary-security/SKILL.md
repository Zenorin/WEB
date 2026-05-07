---
name: "session-boundary-security"
description: "Review cookie/session/token storage, manual login boundaries, and credential handling."
---

# Session Boundary Security

## Session boundary rules
- Do not ask for or store credentials unless the local app explicitly owns that flow.
- Prefer manual login/session bootstrap for third-party sites.
- Do not log tokens, cookies, passwords, or secret headers.
- Document expiration, reset, and user-controlled revocation.

## Handoff
- Summarize changes, evidence, risks, and next steps.
- Cite relevant project docs or source files by path.
