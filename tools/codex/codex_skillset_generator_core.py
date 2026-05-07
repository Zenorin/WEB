#!/usr/bin/env python3
"""
Codex Skillset Starter v4.9 — final-candidate, essential-pruned, hard-policy-safe, scale-aware, module-aware.

Purpose
-------
Generate efficient project-local Codex guidance from a JSON profile:
- Root AGENTS.md / PLANS.md / .codex config and policy lock.
- .agents/skills/<skill>/SKILL.md with agents/openai.yaml metadata.
- Module-local AGENTS.md with frontend/backend/data/extension-specific preferred skills.
- Project-size aware optional commands/references/personas/governance.

Design philosophy
-----------------
Not too much. Not too little.
Use a small universal workflow, score candidate skills, enforce a size/metadata budget,
route work by module path, and write pruned skills to optional-skills.md instead of overloading Codex.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

VERSION = "4.9-final-candidate"

PROJECT_SIZES: Dict[str, Dict[str, Any]] = {
    "micro": {
        "description": "Tiny script/tool/proof-of-concept. Minimum guidance only.",
        "core": [
            "using-agent-skills", "spec-driven-development", "incremental-implementation",
            "debugging-and-error-recovery", "consistency-guard", "evidence-pack",
        ],
        "max_project_skills": 7,
        "max_module_skills": 5,
        "max_initial_metadata_chars": 2200,
        "include_commands": False,
        "include_references": False,
        "include_personas": False,
        "include_governance": False,
    },
    "small": {
        "description": "Small app/library maintained by one or a few developers.",
        "core": [
            "using-agent-skills", "spec-driven-development", "planning-and-task-breakdown",
            "source-driven-development", "incremental-implementation", "test-driven-development",
            "debugging-and-error-recovery", "consistency-guard", "evidence-pack",
        ],
        "max_project_skills": 12,
        "max_module_skills": 6,
        "max_initial_metadata_chars": 3600,
        "include_commands": False,
        "include_references": False,
        "include_personas": False,
        "include_governance": False,
    },
    "medium": {
        "description": "Multi-module product with meaningful tests and release flow.",
        "core": [
            "using-agent-skills", "spec-driven-development", "planning-and-task-breakdown",
            "context-engineering", "source-driven-development", "incremental-implementation",
            "test-driven-development", "debugging-and-error-recovery", "code-review-and-quality",
            "consistency-guard", "evidence-pack",
        ],
        "max_project_skills": 18,
        "max_module_skills": 7,
        "max_initial_metadata_chars": 5200,
        "include_commands": True,
        "include_references": True,
        "include_personas": False,
        "include_governance": False,
    },
    "large": {
        "description": "Team-owned product with multiple module boundaries.",
        "core": [
            "using-agent-skills", "spec-driven-development", "planning-and-task-breakdown",
            "context-engineering", "source-driven-development", "incremental-implementation",
            "test-driven-development", "debugging-and-error-recovery", "code-review-and-quality",
            "security-and-hardening", "consistency-guard", "evidence-pack",
        ],
        "max_project_skills": 28,
        "max_module_skills": 8,
        "max_initial_metadata_chars": 7200,
        "include_commands": True,
        "include_references": True,
        "include_personas": True,
        "include_governance": True,
    },
    "enterprise": {
        "description": "Multi-team/compliance-sensitive/high-risk system. Strongest governance.",
        "core": [
            "using-agent-skills", "spec-driven-development", "planning-and-task-breakdown",
            "context-engineering", "source-driven-development", "incremental-implementation",
            "test-driven-development", "debugging-and-error-recovery", "code-review-and-quality",
            "security-and-hardening", "risk-review", "observability-update",
            "consistency-guard", "evidence-pack",
        ],
        "max_project_skills": 34,
        "max_module_skills": 9,
        "max_initial_metadata_chars": 8200,
        "include_commands": True,
        "include_references": True,
        "include_personas": True,
        "include_governance": True,
    },
}

SIZE_BUDGET_KEYS = {"max_project_skills", "max_module_skills", "max_initial_metadata_chars"}

SAFE_SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")


def is_safe_skill_name(skill: str) -> bool:
    """Return True only for path-safe skill identifiers.

    Skill names become directory names under `.agents/skills/<skill>`, so custom
    names must not contain path separators, traversal segments, whitespace, or
    shell-sensitive punctuation.
    """
    return isinstance(skill, str) and bool(SAFE_SKILL_RE.fullmatch(skill))


def is_safe_relative_path(path: str) -> bool:
    """Return True only for repository-relative module paths.

    Module paths become `<module>/AGENTS.md`. Reject absolute paths, Windows
    drive paths, home-directory shortcuts, and `.`/`..` traversal segments.
    """
    if not isinstance(path, str):
        return False
    raw = path.strip()
    if not raw or raw.startswith("/") or raw.startswith("~") or WINDOWS_ABSOLUTE_PATH_RE.match(raw):
        return False
    parts = [part for part in raw.replace("\\", "/").split("/") if part]
    if not parts:
        return False
    return not any(part in {".", ".."} for part in parts)


def yaml_quote(value: str) -> str:
    """Quote short scalar strings for generated YAML/front-matter safety."""
    value = str(value).replace("\\", "\\\\").replace('"', '\"').replace("\n", " ")
    return f'"{value}"'

BUNDLES: Dict[str, List[str]] = {
    "web-saas": [
        "frontend-product-ui", "ui-a11y-check", "browser-smoke", "api-contract-change",
        "api-error-handling-review", "db-migration", "authz-security-review",
        "backend-test-matrix", "service-repository-boundary-check",
    ],
    "frontend-product-ui": [
        "frontend-product-ui", "design-system-consistency", "ui-state-coverage",
        "responsive-layout-review", "form-table-filter-ux", "browser-smoke",
        "visual-regression-plan", "accessibility-check",
    ],
    "backend-api": [
        "api-contract-change", "api-error-handling-review", "authz-security-review",
        "db-migration", "backward-compat-check", "observability-update", "incident-hotfix",
        "backend-test-matrix", "service-repository-boundary-check",
    ],
    "shared-contracts": [
        "api-contract-change", "backward-compat-check", "documentation-and-adrs", "consistency-guard",
    ],
    "ai-product": [
        "eval-regression", "prompt-contract", "safety-review", "cost-latency-budget",
        "offline-online-rollout", "model-output-contract",
    ],
    "legacy-monolith": [
        "codebase-map", "characterization-tests", "thin-refactor", "deprecation-and-migration",
        "risk-review", "backward-compat-check", "no-feature-deletion-guard",
    ],
    "library-sdk": [
        "api-contract-change", "backward-compat-check", "deprecation-and-migration",
        "documentation-and-adrs", "release-checklist-sdk",
    ],
    "data-pipeline": [
        "schema-contract-check", "data-quality-gate", "backfill-rollout",
        "idempotency-check", "observability-update",
    ],
    "browser-extension": [
        "extension-permission-review", "content-script-boundary", "message-contract-review",
        "privacy-boundary-review", "browser-smoke",
    ],
    "electron-desktop": [
        "electron-ipc-security", "preload-api-contract", "renderer-main-boundary",
        "desktop-packaging-check", "security-and-hardening",
    ],
    "crawler-session": [
        "crawler-contract-review", "session-boundary-security", "idempotency-check",
        "privacy-boundary-review", "anti-bot-compliance-check",
    ],
    "local-only-tool": [
        "local-only-hardlock", "data-egress-review", "privacy-regression-check",
        "offline-analyzer-contract", "manual-export-only",
    ],
    "clean-room-rebuild": [
        "clean-room-reference-analysis", "reference-role-report", "contract-extraction",
        "source-copy-audit", "no-feature-deletion-guard", "pass-manifest-verification",
        "characterization-tests",
    ],
}

POLICY_PACK_SKILLS: Dict[str, List[str]] = {
    "local-only": BUNDLES["local-only-tool"],
    "clean-room": BUNDLES["clean-room-rebuild"],
    "no-feature-deletion": ["no-feature-deletion-guard"],
    "privacy-boundary": ["privacy-boundary-review", "data-egress-review"],
    "destructive-operation": ["destructive-operation-review", "risk-review", "evidence-pack", "shipping-and-launch"],
    "regulated-private-data": ["privacy-boundary-review", "security-and-hardening", "data-egress-review", "risk-review"],
}

EXPLICIT_ONLY_SKILLS = {
    "shipping-and-launch", "ci-cd-and-automation", "db-migration", "incident-hotfix",
    "offline-online-rollout", "deprecation-and-migration", "backfill-rollout",
    "clean-room-reference-analysis", "source-copy-audit", "local-only-hardlock",
    "data-egress-review", "pass-manifest-verification", "destructive-operation-review",
}

SKILL_DESCRIPTIONS: Dict[str, str] = {
    "using-agent-skills": "Select the minimum relevant skills, modules, commands, references, and policy packs for the current task.",
    "idea-refine": "Clarify a vague idea into goals, non-goals, risks, constraints, and acceptance criteria.",
    "spec-driven-development": "Write or update a specification, PRD, interface contract, or acceptance criteria before implementation.",
    "planning-and-task-breakdown": "Split work into small, verifiable vertical slices with dependencies and validation steps.",
    "context-engineering": "Decide what project context to load, summarize, defer, or reference before coding.",
    "source-driven-development": "Use primary sources, official docs, local tests, and existing code before changing behavior.",
    "incremental-implementation": "Build the smallest coherent slice and keep changes reversible.",
    "test-driven-development": "Prove added or changed behavior with tests or explicit verification evidence.",
    "debugging-and-error-recovery": "Handle failures, regressions, flaky behavior, and confusing output with evidence.",
    "code-review-and-quality": "Review correctness, maintainability, contracts, risks, tests, and documentation.",
    "code-simplification": "Reduce complexity without changing observable behavior.",
    "security-and-hardening": "Review auth, permissions, secrets, user data, networking, IPC, storage, and execution boundaries.",
    "performance-optimization": "Improve latency, memory, rendering, payload size, database load, or cost with measurement.",
    "git-workflow-and-versioning": "Keep branch, commit, changelog, versioning, and release history clean.",
    "ci-cd-and-automation": "Maintain CI workflows, automation, deploy pipelines, and release gates.",
    "deprecation-and-migration": "Plan compatibility breaks, migration paths, data migration, API deprecation, and cleanup.",
    "documentation-and-adrs": "Write durable decisions, interface notes, operations docs, and user-facing docs.",
    "shipping-and-launch": "Final go/no-go before release, merge, deploy, publish, or customer handoff.",
    "consistency-guard": "Keep file paths, symbols, APIs, DTOs, events, routes, and domain terms aligned.",
    "evidence-pack": "Collect files changed, commands run, validation results, risks, and next steps before completion.",
    "frontend-product-ui": "Design and implement polished, reusable, accessible product UI without dropping states or behavior.",
    "design-system-consistency": "Keep spacing, typography, component variants, colors, radius, and interaction patterns consistent.",
    "ui-state-coverage": "Ensure loading, empty, error, success, disabled, and permission-denied states are complete.",
    "responsive-layout-review": "Check desktop, tablet, and mobile layout behavior before completion.",
    "form-table-filter-ux": "Review forms, tables, filters, sorting, pagination, validation, and bulk actions.",
    "browser-smoke": "Run or describe browser-facing smoke checks for routes, forms, states, and flows.",
    "visual-regression-plan": "Plan visual checks or screenshots for UI-sensitive changes.",
    "accessibility-check": "Review keyboard flow, labels, semantics, focus states, contrast, and ARIA usage.",
    "ui-a11y-check": "Review browser UI for accessibility and complete interaction states.",
    "api-contract-change": "Plan and review REST/RPC/GraphQL/events/DTO/schema changes for compatibility.",
    "api-error-handling-review": "Review status codes, error envelopes, validation errors, retries, and client-facing failure semantics.",
    "backend-test-matrix": "Choose backend unit, integration, contract, migration, auth, and regression tests for the change.",
    "service-repository-boundary-check": "Keep handler/controller, service, repository, schema, and client responsibilities separated.",
    "db-migration": "Plan safe schema/data migrations, rollback/fallback, compatibility windows, and validation.",
    "authz-security-review": "Review authentication, authorization, tenant/resource scoping, and auditability.",
    "observability-update": "Check logs, metrics, traces, dashboards, alerts, and runbook impact.",
    "incident-hotfix": "Apply a minimal hotfix with low blast radius, rapid verification, and rollback.",
    "backward-compat-check": "Detect compatibility risks for downstream consumers and public behavior.",
    "eval-regression": "Compare AI changes against offline baselines and known failure cases.",
    "prompt-contract": "Define prompt/tool/output schema constraints and tests.",
    "safety-review": "Review AI behavior and tool usage for policy, injection, data leakage, and misuse.",
    "cost-latency-budget": "Estimate and constrain model/tool cost and latency before shipping.",
    "offline-online-rollout": "Move AI behavior from offline validation to guarded online rollout.",
    "model-output-contract": "Keep model outputs schema-locked, deterministic where needed, and testable.",
    "codebase-map": "Map legacy entry points, coupling, contracts, side effects, and risk zones.",
    "characterization-tests": "Capture current behavior before refactoring brittle or unclear code.",
    "thin-refactor": "Refactor one structural concern at a time while preserving behavior.",
    "risk-review": "Assess hidden coupling, blast radius, reversibility, and mitigation.",
    "release-checklist-sdk": "Review SDK/library release readiness, docs, examples, semver, and migration notes.",
    "schema-contract-check": "Review dataset/schema changes for owners, compatibility, and downstream impact.",
    "data-quality-gate": "Define freshness, null, row-count, distribution, and business-rule checks.",
    "backfill-rollout": "Plan bounded historical backfill with stop conditions, monitoring, and cleanup.",
    "idempotency-check": "Review retry, timeout, duplicate execution, and exactly-once/at-least-once assumptions.",
    "extension-permission-review": "Minimize extension permissions and justify host/script/storage access.",
    "content-script-boundary": "Keep content script, page context, background, and UI boundaries explicit.",
    "message-contract-review": "Review extension/Electron message names, payloads, replies, errors, and versioning.",
    "privacy-boundary-review": "Review data collection, storage, logging, export, egress, and user consent boundaries.",
    "electron-ipc-security": "Review Electron IPC, preload exposure, context isolation, and main/renderer trust boundaries.",
    "preload-api-contract": "Keep preload-exposed API small, typed, documented, and versioned.",
    "renderer-main-boundary": "Separate renderer UI from privileged main-process behavior.",
    "desktop-packaging-check": "Review packaging, update, signing, asset, and platform runtime assumptions.",
    "crawler-contract-review": "Review crawler selectors, headers, fallback paths, return schema, errors, and rate/ban signals.",
    "session-boundary-security": "Review cookie/session/token storage, manual login boundaries, and credential handling.",
    "anti-bot-compliance-check": "Check that automation respects access controls, CAPTCHA boundaries, and allowed use.",
    "local-only-hardlock": "Enforce local-only behavior when explicitly configured.",
    "data-egress-review": "Review external transmission, telemetry, reports, webhooks, uploads, and logs.",
    "privacy-regression-check": "Verify changes do not introduce new collection, retention, sharing, or leakage.",
    "offline-analyzer-contract": "Keep analyzer behavior local and deterministic unless explicitly approved.",
    "manual-export-only": "Require manual export instead of automatic external reporting when local-only policy applies.",
    "clean-room-reference-analysis": "Analyze reference behavior while keeping implementation independent.",
    "reference-role-report": "Document why reference files/paths exist before including or excluding behavior.",
    "contract-extraction": "Extract interfaces, inputs, outputs, errors, and invariants from references without copying implementation.",
    "source-copy-audit": "Check that generated implementation does not copy restricted source text/assets/identifiers.",
    "no-feature-deletion-guard": "Prevent deletion/hiding of behavior without role trace, replacement, migration, or approval.",
    "pass-manifest-verification": "Verify staged pass/manifests and evidence before declaring phase completion.",
    "keyword-strategy-prelisting": "Plan keyword/product listing strategy before relying on post-sale ad reports.",
    "coupang-experimental-gate": "Gate Coupang-specific crawling/automation experiments behind explicit evidence and safety checks.",
    "progress-cancel-compatibility": "Keep progress/cancel contracts backward-compatible across UI, backend, and worker layers.",
    "destructive-operation-review": "Gate delete, overwrite, migration, purge, publish, or irreversible operations with explicit scope, backup, rollback, and evidence.",
}

SPECIAL_APPENDIX: Dict[str, str] = {
    "using-agent-skills": """
## Skill selection process
1. Classify the task phase: Define, Plan, Build, Verify, Review, or Ship.
2. Match the working path to a module using `recommend --path` when possible.
3. Use the smallest useful skill set: normally one workflow skill, one domain skill, and `$evidence-pack`.
4. Apply policy-pack skills only when the profile, module, docs, or user explicitly requires them.
5. Do not load every skill by default.
""".strip(),
    "frontend-product-ui": """
## Product UI workflow
1. Identify the screen goal, primary action, secondary actions, and user risk.
2. Preserve existing functionality; do not remove controls just to simplify the UI.
3. Use reusable components and consistent spacing, typography, radius, and state styles.
4. Implement loading, empty, error, success, disabled, and permission-denied states when relevant.
5. Validate responsive behavior and one browser-facing smoke flow.
""".strip(),
    "api-error-handling-review": """
## API error checklist
- Status code matches failure class.
- Error envelope shape is stable and documented.
- Validation errors identify fields without leaking secrets.
- Frontend/client behavior for each failure mode is clear.
- Retries do not create duplicate side effects.
""".strip(),
    "backend-test-matrix": """
## Backend test selection
Choose the smallest credible matrix:
- Unit test for pure service logic.
- Integration test for route/database/auth boundary.
- Contract test for response/error shapes.
- Migration test or rollback note for persistence changes.
- Regression test for a reproduced bug.
""".strip(),
    "service-repository-boundary-check": """
## Boundary rules
- Route/controller: parse request, auth boundary, call service, map response.
- Service: business rules, orchestration, transactions.
- Repository/client: persistence or external IO only.
- Schema/DTO: validation and contract shape.
Do not bury authorization or response-shape decisions in repositories.
""".strip(),
    "clean-room-reference-analysis": """
## Clean-room constraints
- Treat reference code/assets as read-only.
- Extract roles, behavior, contracts, fixtures, and tests.
- Do not copy proprietary source text, comments, identifiers, secrets, or assets verbatim.
- Write a role report before excluding any observed behavior.
""".strip(),
    "no-feature-deletion-guard": """
## Deletion gate
Before deleting, hiding, disabling, or replacing any UI option, fallback, debug/mock path, or legacy behavior:
1. Trace usage or role.
2. Identify replacement or migration.
3. Add/adjust tests when behavior matters.
4. Obtain explicit approval or document the deprecation path.
""".strip(),
    "local-only-hardlock": """
## Local-only hard constraints
Use only when profile policy pack includes `local-only`.
- No telemetry, analytics, crash reports, remote upload, cloud sync, webhook, or automatic external notification.
- Analysis and generated artifacts stay local unless explicitly approved.
- Export is manual file export unless explicitly approved.
""".strip(),
    "destructive-operation-review": """
## Destructive operation gate
Use this skill for deletes, overwrites, migrations, backfills, deploys, publishes, permission changes, or other high-impact operations.

Before acting:
1. Define exact target scope and non-targets.
2. Confirm backup, restore, rollback, or revert path.
3. Prefer dry-run, diff, or preview mode when available.
4. Record irreversible steps and required human approval.
5. Verify post-condition and preserve evidence.
""".strip(),
    "crawler-contract-review": """
## Crawler contract review
- Define allowed entry pages, inputs, outputs, error codes, retry rules, and fallback paths.
- Do not rely on brittle selectors without fallback or evidence.
- Respect login/session/manual boundaries and access-control signals.
- Keep raw capture and normalized result schemas separate.
""".strip(),
    "session-boundary-security": """
## Session boundary rules
- Do not ask for or store credentials unless the local app explicitly owns that flow.
- Prefer manual login/session bootstrap for third-party sites.
- Do not log tokens, cookies, passwords, or secret headers.
- Document expiration, reset, and user-controlled revocation.
""".strip(),
}

GENERIC_BODY = """
## Use when
- The task matches this skill's description.
- The change may affect durable behavior, tests, docs, public contracts, operations, or user experience.

## Workflow
1. Identify scope, target files, contracts, and non-goals.
2. Read the closest `AGENTS.md` and relevant docs before editing.
3. Make the smallest coherent change.
4. Add or update tests, checks, docs, or evidence.
5. Record unresolved risks and next steps.

## Quality gates
- Do not declare completion without verification evidence.
- Do not delete behavior solely because it looks unused.
- Do not hide, stub, or fake success to pass checks.
- Do not broaden public interfaces without compatibility notes.

## Evidence required
- Files read and changed.
- Commands run and outcomes.
- Test or validation coverage.
- Known risks and explicit exclusions.

## Forbidden rationalizations
- "Tests can wait."
- "This path looks unused."
- "A mock success is enough."
- "The old behavior is probably not important."
- "The implementation is obvious, so no source check is needed."
""".strip()

COMMANDS = {
    "spec.md": "Use `$spec-driven-development`. Clarify goals, non-goals, acceptance criteria, boundaries, and risks before coding.",
    "plan.md": "Use `$planning-and-task-breakdown`. Produce small vertical slices, dependencies, validation, and rollback notes.",
    "build.md": "Use `$incremental-implementation`. Build the smallest useful slice and keep changes reversible.",
    "test.md": "Use `$test-driven-development` and `$debugging-and-error-recovery`. Prove behavior with tests and evidence.",
    "review.md": "Use `$code-review-and-quality`. Review correctness, contracts, security, compatibility, and maintainability.",
    "code-simplify.md": "Use `$code-simplification`. Reduce complexity without changing observable behavior.",
    "ship.md": "Use `$shipping-and-launch`. Final go/no-go, release notes, verification evidence, and risks.",
}
REFERENCES = {
    "testing-patterns.md": "# Testing Patterns\n\n- Prefer behavior tests over implementation snapshots.\n- Cover happy path, boundary, failure, and regression cases.\n- Record commands and outcomes.\n",
    "security-checklist.md": "# Security Checklist\n\n- Secrets not committed.\n- Inputs validated at boundaries.\n- Auth/authz enforced server-side or trusted boundary.\n- Logs redact sensitive data.\n- IPC/extension permissions minimized.\n",
    "performance-checklist.md": "# Performance Checklist\n\n- Define baseline and budget.\n- Measure before optimizing.\n- Watch memory, payload, DB queries, rendering, and cost.\n",
    "accessibility-checklist.md": "# Accessibility Checklist\n\n- Keyboard navigation.\n- Labels and names.\n- Contrast.\n- Focus states.\n- Loading/empty/error states.\n",
    "orchestration-patterns.md": "# Orchestration Patterns\n\n- Keep long-running jobs cancellable.\n- Track partial failure, retry, timeout, and idempotency.\n",
}
PERSONAS = {
    "code-reviewer.md": "# Code Reviewer\n\nFocus on correctness, maintainability, naming, contracts, edge cases, and compatibility.\n",
    "test-engineer.md": "# Test Engineer\n\nFocus on test strategy, fixtures, regression coverage, flaky risk, and evidence.\n",
    "security-auditor.md": "# Security Auditor\n\nFocus on trust boundaries, secrets, permissions, auth/authz, data exposure, and logs.\n",
    "frontend-ux-reviewer.md": "# Frontend UX Reviewer\n\nFocus on usability, states, accessibility, responsive layout, visual hierarchy, and interaction flows.\n",
    "backend-architect.md": "# Backend Architect\n\nFocus on API boundaries, service/repository separation, migrations, error envelopes, idempotency, and test matrix.\n",
}

PRESETS: Dict[str, Dict[str, Any]] = {
    "universal": {"project_type": "universal", "project_size": "small", "bundles": [], "modules": []},
    "web-saas": {
        "project_type": "web-saas", "project_size": "medium", "bundles": ["web-saas"],
        "modules": [
            {"name": "frontend", "path": "apps/web", "module_type": "frontend-product-ui", "bundles": ["frontend-product-ui"],
             "preferred_skills": ["frontend-product-ui", "design-system-consistency", "ui-state-coverage", "responsive-layout-review", "browser-smoke"],
             "commands": {"dev": "pnpm --filter web dev", "test": "pnpm --filter web test", "build": "pnpm --filter web build"},
             "local_boundaries": ["Keep page files thin and move business logic into hooks/services.", "Do not duplicate backend authorization rules in browser code.", "Visible states must cover loading, empty, error, success, and permission-denied when relevant."],
             "quality_gates": ["Build passes.", "Primary UI flow smoke checked.", "Responsive layout reviewed."]},
            {"name": "backend", "path": "services/api", "module_type": "backend-api", "bundles": ["backend-api"],
             "preferred_skills": ["api-contract-change", "api-error-handling-review", "backend-test-matrix", "service-repository-boundary-check", "authz-security-review"],
             "commands": {"test": "pnpm --filter api test", "build": "pnpm --filter api build"},
             "local_boundaries": ["Keep handler, service, repository, and schema responsibilities separated.", "Public response and error envelopes are contracts.", "Schema changes require migration and rollback notes."],
             "quality_gates": ["Unit/integration tests pass.", "Contract tests updated for API changes.", "Migration risk reviewed if persistence changed."]},
            {"name": "shared", "path": "packages/shared", "module_type": "shared-contracts", "bundles": ["shared-contracts"],
             "preferred_skills": ["api-contract-change", "backward-compat-check", "consistency-guard"],
             "commands": {"test": "pnpm --filter shared test", "build": "pnpm --filter shared build"},
             "local_boundaries": ["Keep shared package framework-light and stable.", "Breaking shared contract changes require migration notes."],
             "quality_gates": ["Shared package build passes.", "Downstream contract impact reviewed."]},
        ],
    },
    "frontend-product-ui": {"project_type": "frontend-product-ui", "project_size": "medium", "bundles": ["frontend-product-ui"],
        "modules": [{"name": "frontend", "path": "apps/web", "module_type": "frontend-product-ui", "bundles": ["frontend-product-ui"], "preferred_skills": ["frontend-product-ui", "design-system-consistency", "ui-state-coverage", "responsive-layout-review", "browser-smoke"]}]},
    "backend-api": {"project_type": "backend-api", "project_size": "medium", "bundles": ["backend-api"],
        "modules": [{"name": "api", "path": "services/api", "module_type": "backend-api", "bundles": ["backend-api"], "preferred_skills": ["api-contract-change", "api-error-handling-review", "backend-test-matrix", "service-repository-boundary-check", "authz-security-review"]}]},
    "ai-product": {"project_type": "ai-product", "project_size": "large", "bundles": ["ai-product"],
        "modules": [{"name": "orchestrator", "path": "services/orchestrator", "module_type": "ai-product", "bundles": ["ai-product"], "preferred_skills": ["prompt-contract", "eval-regression", "safety-review", "cost-latency-budget"]}]},
    "legacy-monolith": {"project_type": "legacy-monolith", "project_size": "large", "bundles": ["legacy-monolith"], "modules": []},
    "library-sdk": {"project_type": "library-sdk", "project_size": "medium", "bundles": ["library-sdk"], "modules": [{"name": "sdk", "path": "src", "module_type": "library-sdk", "bundles": ["library-sdk"], "preferred_skills": ["api-contract-change", "backward-compat-check", "documentation-and-adrs"]}]},
    "data-pipeline": {"project_type": "data-pipeline", "project_size": "large", "bundles": ["data-pipeline"], "modules": [{"name": "pipelines", "path": "pipelines", "module_type": "data-pipeline", "bundles": ["data-pipeline"], "preferred_skills": ["schema-contract-check", "data-quality-gate", "backfill-rollout", "observability-update"]}]},
    "browser-extension": {"project_type": "browser-extension", "project_size": "medium", "bundles": ["browser-extension"], "modules": [{"name": "extension", "path": "apps/extension", "module_type": "browser-extension", "bundles": ["browser-extension"], "preferred_skills": ["extension-permission-review", "content-script-boundary", "message-contract-review", "privacy-boundary-review"]}]},
    "electron-desktop": {"project_type": "electron-desktop", "project_size": "medium", "bundles": ["electron-desktop"], "modules": [{"name": "desktop", "path": "apps/desktop", "module_type": "electron-desktop", "bundles": ["electron-desktop"], "preferred_skills": ["electron-ipc-security", "preload-api-contract", "renderer-main-boundary"]}]},
    "local-only-tool": {"project_type": "local-only-tool", "project_size": "small", "bundles": ["local-only-tool"], "policy_packs": ["local-only"], "modules": []},
    "clean-room-rebuild": {"project_type": "clean-room-rebuild", "project_size": "large", "bundles": ["clean-room-rebuild"], "policy_packs": ["clean-room", "no-feature-deletion"], "modules": []},
    "autometa-clean-room-rebuild": {
        "project_type": "autometa-clean-room-rebuild", "project_size": "large", "bundles": ["web-saas", "electron-desktop", "browser-extension", "crawler-session", "clean-room-rebuild"], "policy_packs": ["clean-room", "no-feature-deletion"],
        "modules": [
            {"name": "web", "path": "apps/web", "module_type": "frontend-product-ui", "bundles": ["frontend-product-ui"], "preferred_skills": ["frontend-product-ui", "design-system-consistency", "ui-state-coverage", "responsive-layout-review", "browser-smoke"]},
            {"name": "api", "path": "services/api", "module_type": "backend-api", "bundles": ["backend-api"], "preferred_skills": ["api-contract-change", "api-error-handling-review", "backend-test-matrix", "service-repository-boundary-check", "authz-security-review"]},
            {"name": "extension", "path": "apps/extension", "module_type": "browser-extension", "bundles": ["browser-extension"], "preferred_skills": ["extension-permission-review", "content-script-boundary", "message-contract-review", "privacy-boundary-review"]},
            {"name": "desktop", "path": "apps/desktop", "module_type": "electron-desktop", "bundles": ["electron-desktop"], "preferred_skills": ["electron-ipc-security", "preload-api-contract", "renderer-main-boundary"]},
            {"name": "crawler", "path": "workers/crawler", "module_type": "crawler-session", "bundles": ["crawler-session"], "preferred_skills": ["crawler-contract-review", "session-boundary-security", "anti-bot-compliance-check", "privacy-boundary-review"]},
            {"name": "shared", "path": "packages/shared", "module_type": "shared-contracts", "bundles": ["shared-contracts"], "preferred_skills": ["api-contract-change", "backward-compat-check", "consistency-guard"]},
        ],
    },
}

DEFAULT_COMMANDS = {"install": "<fill in>", "lint": "<fill in>", "typecheck": "<fill in>", "test": "<fill in>", "build": "<fill in>"}


def slug_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def all_known_skills() -> Set[str]:
    out: Set[str] = set()
    for meta in PROJECT_SIZES.values(): out.update(meta["core"])
    for skills in BUNDLES.values(): out.update(skills)
    for skills in POLICY_PACK_SKILLS.values(): out.update(skills)
    out.update(SKILL_DESCRIPTIONS.keys())
    return out


def unique(items: Sequence[str]) -> List[str]:
    seen: Set[str] = set(); out: List[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item); out.append(item)
    return out


SKILL_PRIORITY: Dict[str, int] = {
    "using-agent-skills": 100, "spec-driven-development": 98, "planning-and-task-breakdown": 96,
    "source-driven-development": 96, "incremental-implementation": 94, "test-driven-development": 93,
    "debugging-and-error-recovery": 92, "context-engineering": 88, "code-review-and-quality": 88,
    "consistency-guard": 98, "evidence-pack": 99, "security-and-hardening": 90,
    "authz-security-review": 89, "privacy-boundary-review": 88, "data-egress-review": 88,
    "local-only-hardlock": 94, "clean-room-reference-analysis": 94, "contract-extraction": 92,
    "source-copy-audit": 92, "no-feature-deletion-guard": 93, "pass-manifest-verification": 90,
    "api-contract-change": 86, "api-error-handling-review": 84, "backend-test-matrix": 84,
    "service-repository-boundary-check": 82, "db-migration": 82, "frontend-product-ui": 84,
    "ui-state-coverage": 82, "browser-smoke": 80, "accessibility-check": 76,
    "extension-permission-review": 84, "content-script-boundary": 85, "message-contract-review": 83,
    "electron-ipc-security": 84, "preload-api-contract": 83, "crawler-contract-review": 86,
    "session-boundary-security": 89, "anti-bot-compliance-check": 85,
    "schema-contract-check": 84, "data-quality-gate": 82, "idempotency-check": 80,
    "eval-regression": 84, "prompt-contract": 83, "safety-review": 84, "cost-latency-budget": 78,
    "destructive-operation-review": 91, "shipping-and-launch": 72, "ci-cd-and-automation": 70, "performance-optimization": 70,
    "documentation-and-adrs": 76, "git-workflow-and-versioning": 68, "deprecation-and-migration": 76,
    "observability-update": 76,
}


def skill_priority(skill: str) -> int:
    return SKILL_PRIORITY.get(skill, 50)


def estimate_initial_metadata_chars(skills: Sequence[str]) -> int:
    """Approximate Codex's initial skill-list footprint: name + description + path + YAML overhead."""
    total = 0
    for skill in skills:
        desc = SKILL_DESCRIPTIONS.get(skill, f"Use this skill for project-specific workflow `{skill}`.")
        path = f".agents/skills/{skill}/SKILL.md"
        total += len(skill) + len(desc) + len(path) + 48
    return total


def select_essential_skills(
    candidates: Sequence[str],
    *,
    required: Sequence[str] = (),
    max_count: int,
    max_metadata_chars: int,
) -> Tuple[List[str], List[str]]:
    required_list = unique(required)
    ordered_candidates = unique(list(required_list) + list(candidates))
    selected: List[str] = []
    optional: List[str] = []

    for skill in required_list:
        if skill not in selected:
            selected.append(skill)

    indexed = {skill: idx for idx, skill in enumerate(ordered_candidates)}
    remaining = [s for s in ordered_candidates if s not in set(selected)]
    remaining.sort(key=lambda s: (-skill_priority(s), indexed.get(s, 10**6), s))

    for skill in remaining:
        proposed = selected + [skill]
        if len(proposed) <= max_count and estimate_initial_metadata_chars(proposed) <= max_metadata_chars:
            selected.append(skill)
        else:
            optional.append(skill)

    for skill in ordered_candidates:
        if skill not in selected and skill not in optional:
            optional.append(skill)
    return selected, optional


def compute_module_skill_plan(module: Dict[str, Any], profile_size: str = "small") -> Tuple[List[str], List[str]]:
    size_meta = PROJECT_SIZES.get(profile_size, PROJECT_SIZES["small"])
    max_count = int(module.get("max_skills", size_meta.get("max_module_skills", 6)))
    max_chars = int(module.get("max_initial_metadata_chars", max(1600, size_meta.get("max_initial_metadata_chars", 3600) // 2)))
    preferred = list(module.get("preferred_skills", []))
    required = unique(preferred + skills_for_policy_packs(module.get("policy_packs", [])) + ["consistency-guard", "evidence-pack"])
    # Preferred/policy skills are explicit module requirements. Keep them, but raise
    # the effective local budget rather than silently dropping them.
    max_count = max(max_count, len(required))
    max_chars = max(max_chars, estimate_initial_metadata_chars(required))
    candidates = unique(required + skills_for_bundles(module.get("bundles", [])))
    return select_essential_skills(candidates, required=required, max_count=max_count, max_metadata_chars=max_chars)


def compute_skill_plan(profile: Dict[str, Any]) -> Dict[str, Any]:
    profile = normalize_profile(profile)
    size_meta = PROJECT_SIZES[profile["project_size"]]
    max_count = int(profile.get("max_project_skills", size_meta["max_project_skills"]))
    max_chars = int(profile.get("max_initial_metadata_chars", size_meta["max_initial_metadata_chars"]))

    core = list(size_meta["core"])
    policy_required = skills_for_policy_packs(profile.get("policy_packs", []))
    explicit_required = list(profile.get("extra_skills", []))
    required = unique(core + policy_required + explicit_required)
    # Explicit policy/extra skills are hard requirements. The budget is a soft cap for optional skills,
    # so raise the effective cap when required skills alone exceed the scale default.
    max_count = max(max_count, len(required))
    max_chars = max(max_chars, estimate_initial_metadata_chars(required))

    module_selected: Dict[str, List[str]] = {}
    module_optional: Dict[str, List[str]] = {}
    module_candidates: List[str] = []
    for module in profile.get("modules", []):
        selected, optional = compute_module_skill_plan(module, profile["project_size"])
        module_selected[module["path"]] = selected
        module_optional[module["path"]] = optional
        module_candidates.extend(selected)

    candidates = unique(required + skills_for_bundles(profile.get("bundles", [])) + module_candidates)
    selected, optional = select_essential_skills(candidates, required=required, max_count=max_count, max_metadata_chars=max_chars)

    selected_set = set(selected)
    routed_module_selected = {path: [s for s in skills if s in selected_set] for path, skills in module_selected.items()}
    routed_module_optional = {
        path: unique([s for s in module_selected.get(path, []) + module_optional.get(path, []) if s not in selected_set])
        for path in module_selected
    }
    all_optional = unique(optional + [s for skills in routed_module_optional.values() for s in skills])
    module_budgets = {}
    for module in profile.get("modules", []):
        size_meta_module = PROJECT_SIZES.get(profile["project_size"], PROJECT_SIZES["small"])
        module_max_count = int(module.get("max_skills", size_meta_module.get("max_module_skills", 6)))
        module_max_chars = int(module.get("max_initial_metadata_chars", max(1600, size_meta_module.get("max_initial_metadata_chars", 3600) // 2)))
        routed = routed_module_selected.get(module["path"], [])
        module_budgets[module["path"]] = {
            "max_module_skills": max(module_max_count, len(routed)),
            "max_initial_metadata_chars": max(module_max_chars, estimate_initial_metadata_chars(routed)),
            "estimated_initial_metadata_chars": estimate_initial_metadata_chars(routed),
            "selected_count": len(routed),
            "optional_count": len(routed_module_optional.get(module["path"], [])),
        }

    return {
        "selected": selected,
        "optional": all_optional,
        "module_selected": routed_module_selected,
        "module_optional": routed_module_optional,
        "module_budget": module_budgets,
        "budget": {
            "max_project_skills": max_count,
            "max_initial_metadata_chars": max_chars,
            "estimated_initial_metadata_chars": estimate_initial_metadata_chars(selected),
            "selected_count": len(selected),
            "optional_count": len(all_optional),
        },
    }


def preset_profile(preset: str, size: Optional[str] = None) -> Dict[str, Any]:
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: {preset}")
    base = json.loads(json.dumps(PRESETS[preset]))
    if size: base["project_size"] = size
    profile = {
        "project_name": preset.replace("-", " ").title(),
        **base,
        "commands": dict(DEFAULT_COMMANDS),
        "domain_terms": [
            {"canonical": "feature", "avoid": ["thing", "stuff"], "notes": "Use precise domain nouns."},
            {"canonical": "contract", "avoid": ["shape maybe"], "notes": "Use for API/IPC/schema/event boundaries."},
        ],
        "boundaries": [
            "Keep public contracts stable unless an explicit migration is included.",
            "Do not add dependencies without explaining why they are needed.",
            "Do not declare completion without verification evidence.",
        ],
        "quality_gates": [
            "Lint/typecheck/test/build commands must run or have a documented blocker.",
            "Public contract changes require docs and tests.",
            "Security-sensitive changes require security review.",
        ],
        "allowed_external_hosts": [],
        "forbidden_defaults": [],
    }
    if "local-only" in profile.get("policy_packs", []):
        profile["forbidden_defaults"] = ["telemetry", "analytics", "crash report", "remote upload", "cloud sync", "webhook", "automatic external notification"]
    if "clean-room" in profile.get("policy_packs", []):
        profile["boundaries"].extend(["Reference files are read-only.", "Extract behavior contracts; do not copy source text verbatim.", "Write role reports before excluding behavior."])
    return normalize_profile(profile)


def normalize_module(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("module entries must be objects")
    if not raw.get("path"):
        raise ValueError("module.path is required")
    module = dict(raw)
    module.setdefault("name", Path(module["path"]).name or "module")
    module.setdefault("module_type", module.get("bundles", ["universal"])[0] if module.get("bundles") else "universal")
    module.setdefault("bundles", [] if module["module_type"] == "universal" else [module["module_type"]] if module["module_type"] in BUNDLES else [])
    module.setdefault("preferred_skills", [])
    module.setdefault("commands", {})
    module.setdefault("local_boundaries", module.get("rules", []))
    module.setdefault("quality_gates", [])
    module.setdefault("policy_packs", [])
    return module


def normalize_profile(raw: Dict[str, Any]) -> Dict[str, Any]:
    profile = dict(raw)
    profile.setdefault("project_name", "My Project")
    profile.setdefault("project_type", "universal")
    profile.setdefault("project_size", "small")
    if profile["project_size"] not in PROJECT_SIZES:
        raise ValueError(f"Unknown project_size: {profile['project_size']}. Expected one of {sorted(PROJECT_SIZES)}")
    profile.setdefault("bundles", PRESETS.get(profile["project_type"], {}).get("bundles", []))
    profile.setdefault("policy_packs", [])
    profile.setdefault("extra_skills", [])
    profile.setdefault("allow_custom_skills", False)
    profile.setdefault("commands", {})
    profile.setdefault("modules", [])
    profile.setdefault("domain_terms", [])
    profile.setdefault("boundaries", [])
    profile.setdefault("quality_gates", [])
    profile.setdefault("forbidden_defaults", [])
    profile.setdefault("allowed_external_hosts", [])
    profile["modules"] = [normalize_module(m) for m in profile.get("modules", [])]
    return profile


def validate_profile(profile: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    try:
        p = normalize_profile(profile)
    except Exception as e:
        return [str(e)]
    for bundle in p.get("bundles", []):
        if bundle not in BUNDLES:
            errors.append(f"Unknown bundle: {bundle}")
    for pack in p.get("policy_packs", []):
        if pack not in POLICY_PACK_SKILLS:
            errors.append(f"Unknown policy_pack: {pack}")
    known = all_known_skills()
    for skill in p.get("extra_skills", []):
        if not is_safe_skill_name(skill):
            errors.append(f"Unsafe extra_skill name: {skill}. Use lowercase slug form such as `api-contract-change`.")
        elif not p.get("allow_custom_skills") and skill not in known:
            errors.append(f"Unknown extra_skill: {skill}. Set allow_custom_skills=true to allow custom SKILL.md generation.")
    for module in p.get("modules", []):
        if not is_safe_relative_path(module.get("path", "")):
            errors.append(f"Unsafe module.path in {module.get('name')}: {module.get('path')}. Use a repository-relative path without `..`, drive letters, or leading `/`.")
        for bundle in module.get("bundles", []):
            if bundle not in BUNDLES:
                errors.append(f"Unknown module bundle in {module.get('name')}: {bundle}")
        for pack in module.get("policy_packs", []):
            if pack not in POLICY_PACK_SKILLS:
                errors.append(f"Unknown module policy_pack in {module.get('name')}: {pack}")
        for skill in module.get("preferred_skills", []):
            if not is_safe_skill_name(skill):
                errors.append(f"Unsafe module preferred_skill in {module.get('name')}: {skill}. Use lowercase slug form.")
            elif not p.get("allow_custom_skills") and skill not in known:
                errors.append(f"Unknown module preferred_skill in {module.get('name')}: {skill}")
    if not isinstance(p.get("commands", {}), dict):
        errors.append("commands must be an object")
    return errors


def scale_options(profile: Dict[str, Any]) -> Dict[str, Any]:
    opts = {k: v for k, v in PROJECT_SIZES[profile["project_size"]].items() if k != "core"}
    for key in ["include_commands", "include_references", "include_personas", "include_governance"]:
        if key in profile: opts[key] = bool(profile[key])
    return opts


def skills_for_bundles(bundles: Sequence[str]) -> List[str]:
    out: List[str] = []
    for bundle in bundles:
        out.extend(BUNDLES.get(bundle, []))
    return out


def skills_for_policy_packs(packs: Sequence[str]) -> List[str]:
    out: List[str] = []
    for pack in packs:
        out.extend(POLICY_PACK_SKILLS.get(pack, []))
    return out


def compute_module_skills(module: Dict[str, Any], profile_size: str = "small") -> List[str]:
    selected, _ = compute_module_skill_plan(module, profile_size)
    return selected


def compute_project_skills(profile: Dict[str, Any]) -> List[str]:
    return compute_skill_plan(profile)["selected"]


def compute_optional_skills(profile: Dict[str, Any]) -> List[str]:
    return compute_skill_plan(profile)["optional"]


def match_module_by_path(profile: Dict[str, Any], path: str) -> Optional[Dict[str, Any]]:
    norm = path.replace("\\", "/").strip("/")
    matches: List[Tuple[int, Dict[str, Any]]] = []
    for module in profile.get("modules", []):
        mpath = module.get("path", "").replace("\\", "/").strip("/")
        if not mpath: continue
        if norm == mpath or norm.startswith(mpath + "/"):
            matches.append((len(mpath), module))
    if not matches: return None
    return sorted(matches, key=lambda x: x[0], reverse=True)[0][1]


def render_skill(skill: str) -> str:
    desc = SKILL_DESCRIPTIONS.get(skill, f"Use this skill for project-specific workflow `{skill}`.")
    body = SPECIAL_APPENDIX.get(skill, GENERIC_BODY)
    if skill in EXPLICIT_ONLY_SKILLS:
        body += "\n\n## Invocation policy\nUse explicitly. Do not run this skill implicitly for casual work."
    return f"""---
name: {yaml_quote(skill)}
description: {yaml_quote(desc)}
---

# {slug_title(skill)}

{body}

## Handoff
- Summarize changes, evidence, risks, and next steps.
- Cite relevant project docs or source files by path.
"""


def render_openai_yaml(skill: str) -> str:
    desc = SKILL_DESCRIPTIONS.get(skill, f"Use for project-specific workflow `{skill}`.")[:160]
    allow = "false" if skill in EXPLICIT_ONLY_SKILLS else "true"
    return f"""interface:
  display_name: {yaml_quote(slug_title(skill))}
  short_description: {yaml_quote(desc)}
  default_prompt: {yaml_quote('$' + skill)}

policy:
  allow_implicit_invocation: {allow}
"""


def render_agents_md(profile: Dict[str, Any], skills: Sequence[str], opts: Dict[str, Any]) -> str:
    lines: List[str] = [f"# AGENTS.md — {profile['project_name']}", "", "## Purpose", "Use this repository guidance with the local `.agents/skills` skillset. Keep work small, source-driven, testable, and evidence-backed.", "", "## Project classification", f"- project_type: `{profile['project_type']}`", f"- project_size: `{profile['project_size']}` — {PROJECT_SIZES[profile['project_size']]['description']}", f"- bundles: {', '.join(profile.get('bundles', [])) or 'none'}", f"- policy_packs: {', '.join(profile.get('policy_packs', [])) or 'none'}", ""]
    lines += ["## Standard workflow", "1. Define/refine requirements before implementation.", "2. Plan small vertical slices.", "3. Build incrementally.", "4. Verify with tests/checks.", "5. Review quality, security, consistency, and compatibility.", "6. Ship only with evidence and unresolved risks documented.", ""]
    lines += ["## Module routing", "When editing a file under a module path, read that module's local `AGENTS.md` first and prefer its listed skills."]
    if profile.get("modules"):
        plan = compute_skill_plan(profile)
        for m in profile["modules"]:
            routed = plan["module_selected"].get(m["path"], [])
            optional = plan["module_optional"].get(m["path"], [])
            lines.append(f"- `{m['path']}` → `{m['module_type']}`; generated skills: {', '.join('$'+s for s in routed) or 'none'}")
            if optional:
                lines.append(f"  - optional/pruned: {', '.join('$'+s for s in optional)}")
    else:
        lines.append("- No module-specific routing configured.")
    lines.append("")
    lines += ["## Anti-rationalization rules", "- Tests can wait → Add/adjust tests or document why they cannot run.", "- This path looks unused → Prove with evidence or approval before deletion.", "- A mock success is enough → Do not fake success states to pass checks.", "- Old behavior is probably not important → Treat observable behavior as a possible contract.", ""]
    if profile.get("forbidden_defaults"):
        lines.append("## Project-specific forbidden defaults")
        lines.extend(f"- {x}" for x in profile["forbidden_defaults"]); lines.append("")
    lines.append("## Commands")
    if profile.get("commands"):
        lines.extend(f"- `{k}`: `{v}`" for k, v in profile["commands"].items())
    else: lines.append("- Fill in install/lint/typecheck/test/build commands in the profile.")
    lines.append("")
    lines.append("## Quality gates")
    lines.extend(f"- {q}" for q in profile.get("quality_gates", []) or ["Verification commands must run or a blocker must be documented."])
    lines.append("")
    lines.append("## Boundaries")
    lines.extend(f"- {b}" for b in profile.get("boundaries", []) or ["Keep public interfaces stable unless a migration is included."])
    lines.append("")
    lines.append("## Canonical domain terms")
    if profile.get("domain_terms"):
        for t in profile["domain_terms"]:
            if isinstance(t, dict): lines.append(f"- `{t.get('canonical')}`; avoid: {', '.join(t.get('avoid', [])) or 'n/a'}; notes: {t.get('notes','')}")
            else: lines.append(f"- `{t}`")
    else: lines.append("- Add canonical terms to `docs/glossary.md`.")
    lines.append("")
    lines.append("## Available project skills")
    lines.extend(f"- `${s}`" for s in skills)
    if opts.get("include_commands"): lines.append("\n## Command templates\nUse `commands/` as optional cross-tool workflow prompts. Codex can call skills directly with `$skill-name`.")
    if opts.get("include_references"): lines.append("\n## References\nUse `references/` for testing, security, performance, accessibility, and orchestration checklists.")
    if opts.get("include_personas"): lines.append("\n## Personas\nUse `agents/` as optional review personas for complex tasks, not mandatory overhead.")
    lines.append("\n## Done definition\nWork is not done until changed files, validation evidence, risks, and next steps are summarized.")
    return "\n".join(lines).rstrip()+"\n"


def render_module_agents(module: Dict[str, Any], profile_size: str = "small", available_skills: Optional[Set[str]] = None) -> str:
    selected, optional = compute_module_skill_plan(module, profile_size)
    if available_skills is not None:
        optional = unique(optional + [s for s in selected if s not in available_skills])
        selected = [s for s in selected if s in available_skills]
    lines = [f"# AGENTS.md — {module['name']}", "", f"Scope: `{module['path']}`", f"Module type: `{module['module_type']}`", f"Bundles: {', '.join(module.get('bundles', [])) or 'none'}", f"Policy packs: {', '.join(module.get('policy_packs', [])) or 'none'}", "", "## Generated preferred skills"]
    if selected:
        lines.extend(f"- `${s}`" for s in selected)
    else:
        lines.append("- Use root workflow skills; this module has no generated domain-specific skill under the current budget.")
    if optional:
        lines.append("\n## Optional skills not generated under current budget")
        lines.extend(f"- `${s}`" for s in optional)
    lines.append("\n## Local commands")
    if module.get("commands"): lines.extend(f"- `{k}`: `{v}`" for k, v in module["commands"].items())
    else: lines.append("- Use root commands unless this module defines more specific ones.")
    lines.append("\n## Local boundaries")
    lines.extend(f"- {b}" for b in module.get("local_boundaries", []) or ["Follow root boundaries."])
    lines.append("\n## Local quality gates")
    lines.extend(f"- {q}" for q in module.get("quality_gates", []) or ["Run relevant module checks or document blockers."])
    lines.append("\n## Done definition")
    lines.append("- Summarize changed files, validation, unresolved risks, and next steps for this module.")
    return "\n".join(lines).rstrip()+"\n"

def render_plans_md(profile: Dict[str, Any]) -> str:
    return f"""# PLANS.md — {profile['project_name']}

Use this file for ambiguous or multi-step work.

## Goal
-

## Non-goals
-

## Current evidence
- Files/docs read:
- Relevant contracts:
- Unknowns:

## Slices
| Slice | Scope | Files | Verification | Rollback |
|---|---|---|---|---|
| 1 | | | | |

## Risks
-

## Completion evidence
- Commands run:
- Tests added/updated:
- Docs updated:
- Remaining issues:
"""


def render_config(_: Dict[str, Any]) -> str:
    return """sandbox_mode = "workspace-write"
web_search = "cached"
project_doc_max_bytes = 32768
project_root_markers = [".git"]

[sandbox_workspace_write]
network_access = false

[agents]
max_threads = 4
max_depth = 1

[analytics]
enabled = false
"""


def render_policy_lock(profile: Dict[str, Any]) -> str:
    lock = {"version": VERSION, "project_name": profile["project_name"], "project_type": profile["project_type"], "project_size": profile["project_size"], "bundles": profile.get("bundles", []), "policy_packs": profile.get("policy_packs", []), "modules": [{"name": m["name"], "path": m["path"], "module_type": m["module_type"], "bundles": m.get("bundles", [])} for m in profile.get("modules", [])], "allowed_external_hosts": profile.get("allowed_external_hosts", []), "note": "Hard policies are opt-in via policy_packs, not universal defaults."}
    return json.dumps(lock, indent=2, ensure_ascii=False)+"\n"


def render_manifest(profile: Dict[str, Any], skills: Sequence[str], opts: Dict[str, Any]) -> str:
    plan = compute_skill_plan(profile)
    return json.dumps({
        "version": VERSION,
        "skills": list(skills),
        "optional_skills": plan["optional"],
        "budget": plan["budget"],
        "scale_options": opts,
        "modules": [
            {
                "name": m["name"],
                "path": m["path"],
                "skills": plan["module_selected"].get(m["path"], []),
                "optional_skills": plan["module_optional"].get(m["path"], []),
                "budget": plan["module_budget"].get(m["path"], {}),
            }
            for m in profile.get("modules", [])
        ],
    }, indent=2, ensure_ascii=False)+"\n"

def render_glossary(profile: Dict[str, Any]) -> str:
    lines=["# Glossary\n", "Canonical terms used by this project.\n"]
    for t in profile.get("domain_terms", []):
        if isinstance(t, dict): lines += [f"## {t.get('canonical')}\n", f"- Avoid: {', '.join(t.get('avoid', [])) or 'n/a'}", f"- Notes: {t.get('notes','')}\n"]
        else: lines.append(f"- {t}")
    return "\n".join(lines).rstrip()+"\n"


def render_rules() -> str:
    return """# Naming and Consistency Rules

- One canonical domain term per concept.
- Keep API, DTO, event, database, UI, and docs terminology aligned.
- Public contract changes require tests and documentation.
- Renames must update references, docs, tests, and migration notes in the same change.
"""


def render_engineering_laws() -> str:
    return """# Engineering Laws for Agent Work

## Hyrum's Law
Every observable behavior can become a dependency. Treat outputs, errors, timing, CLI flags, schema fields, and UI states as possible contracts.

## Beyoncé Rule
If you liked it, you should have put a test on it. Critical behavior needs verification evidence.

## Chesterton's Fence
Do not remove a fence until you understand why it exists. For legacy behavior, write a role report or characterization test before deletion.
"""


def render_review_checklist() -> str:
    return """# Review Checklist

- Requirements and non-goals are clear.
- Changed behavior has tests or explicit verification evidence.
- Public contracts remain compatible or include migration notes.
- Naming follows glossary and consistency rules.
- Security/privacy boundary was reviewed when relevant.
- No fake success states, hidden regressions, or unapproved feature deletion.
"""


def render_scale_selection_guide() -> str:
    lines=["# Scale Selection Guide\n", "v4.6 uses essential-pruned generation: core + explicit policy first, then priority-ranked domain skills until the size and metadata budget is reached.\n"]
    for size, data in PROJECT_SIZES.items():
        lines.append(
            f"## {size}\n"
            f"- {data['description']}\n"
            f"- core_skills: {len(data['core'])}\n"
            f"- max_project_skills: {data['max_project_skills']}\n"
            f"- max_module_skills: {data['max_module_skills']}\n"
            f"- max_initial_metadata_chars: {data['max_initial_metadata_chars']}\n"
            f"- commands: {data['include_commands']}\n"
            f"- references: {data['include_references']}\n"
            f"- personas: {data['include_personas']}\n"
            f"- governance: {data['include_governance']}\n"
        )
    return "\n".join(lines)


def render_module_routing_guide(profile: Dict[str, Any], available_skills: Optional[Set[str]] = None) -> str:
    lines=["# Module Routing Guide\n", "Use module-local AGENTS.md files to route Codex work by path. v4.6 lists generated route skills separately from optional/pruned skills.\n"]
    plan = compute_skill_plan(profile)
    for m in profile.get("modules", []):
        selected = plan["module_selected"].get(m["path"], [])
        optional = plan["module_optional"].get(m["path"], [])
        if available_skills is not None:
            optional = unique(optional + [s for s in selected if s not in available_skills])
            selected = [s for s in selected if s in available_skills]
        lines.append(f"## {m['name']} — `{m['path']}`\n- type: `{m['module_type']}`\n- generated skills: {', '.join('$'+s for s in selected) or 'none'}\n- optional/pruned: {', '.join('$'+s for s in optional) or 'none'}\n")
    return "\n".join(lines).rstrip()+"\n"


def render_optional_skills(profile: Dict[str, Any]) -> str:
    plan = compute_skill_plan(profile)
    lines = [
        "# Optional Skills Not Generated",
        "",
        "These skills matched the profile, bundles, modules, or policy context, but were not generated because the configured skill budget was already filled.",
        "",
        "This is intentional: Codex initially sees each skill name, description, and path. Keeping this list compact improves routing reliability.",
        "",
        "## Budget",
        f"- selected_count: {plan['budget']['selected_count']}",
        f"- optional_count: {plan['budget']['optional_count']}",
        f"- max_project_skills: {plan['budget']['max_project_skills']}",
        f"- estimated_initial_metadata_chars: {plan['budget']['estimated_initial_metadata_chars']}",
        f"- max_initial_metadata_chars: {plan['budget']['max_initial_metadata_chars']}",
        "",
        "## Optional skills",
    ]
    if plan["optional"]:
        for skill in plan["optional"]:
            lines.append(f"- `${skill}` — {SKILL_DESCRIPTIONS.get(skill, 'No description available.')}")
    else:
        lines.append("- None.")
    return "\n".join(lines).rstrip()+"\n"

def render_project_analysis_guide() -> str:
    return """# Project Document to Skillset Workflow

1. Identify project type, project size, stack, commands, modules, boundaries, and risks.
2. Decide universal core first; add bundles only for actual project needs.
3. Add hard policy packs only when the project/user explicitly requires them.
4. Define modules with path, module_type, bundles, preferred_skills, commands, boundaries, and quality gates.
5. Generate the skillset and run `validate-generated`.
"""


def render_profile_schema_reference() -> str:
    return """# Profile Schema Reference

```json
{
  "project_name": "Name",
  "project_type": "web-saas",
  "project_size": "medium",
  "bundles": ["web-saas"],
  "policy_packs": [],
  "extra_skills": [],
  "allow_custom_skills": false,
  "commands": {"test": "..."},
  "modules": [
    {
      "name": "frontend",
      "path": "apps/web",
      "module_type": "frontend-product-ui",
      "bundles": ["frontend-product-ui"],
      "preferred_skills": [],
      "commands": {},
      "local_boundaries": [],
      "quality_gates": []
    }
  ]
}
```
"""


def render_gpts_operator_guide() -> str:
    return """# GPTs Operator Guide

- Generate a profile first.
- Keep universal defaults lean.
- Add project_type bundles for actual work areas.
- Add module routes for frontend/backend/data/extension/crawler boundaries.
- Do not silently apply hard policy packs.
- Use backup mode unless overwrite is explicitly approved.
- Run validation and summarize failures.
"""


def render_source_integration_guide() -> str:
    return """# Project Source Integration Guide

Recommended repository placement:

```text
AGENTS.md
PLANS.md
.codex/config.toml
.codex/policy.lock.json
.agents/skills/*/SKILL.md
<module>/AGENTS.md
docs/skillset/*.md
```

After generation: review diff, fill real commands, run `validate-generated`, then commit profile and generated guidance together.
"""


def write_file(path: Path, content: str, mode: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and mode == "skip": return
    if path.exists() and mode == "backup":
        backup = path.with_suffix(path.suffix + ".bak"); i=1
        while backup.exists():
            backup = path.with_suffix(path.suffix + f".bak{i}"); i += 1
        shutil.copy2(path, backup)
    path.write_text(content.rstrip()+"\n", encoding="utf-8")


def generate(profile: Dict[str, Any], root: Path, mode: str = "skip", also_codex_skills: bool = False) -> None:
    profile = normalize_profile(profile)
    errors = validate_profile(profile)
    if errors: raise ValueError("Invalid profile:\n- " + "\n- ".join(errors))
    skills = compute_project_skills(profile); opts = scale_options(profile)
    write_file(root/"AGENTS.md", render_agents_md(profile, skills, opts), mode)
    write_file(root/"PLANS.md", render_plans_md(profile), mode)
    write_file(root/".codex"/"config.toml", render_config(profile), mode)
    write_file(root/".codex"/"policy.lock.json", render_policy_lock(profile), mode)
    write_file(root/".codex"/"skillset-manifest.json", render_manifest(profile, skills, opts), mode)
    write_file(root/"docs"/"skillset"/"optional-skills.md", render_optional_skills(profile), mode)
    for skill in skills:
        write_file(root/".agents"/"skills"/skill/"SKILL.md", render_skill(skill), mode)
        write_file(root/".agents"/"skills"/skill/"agents"/"openai.yaml", render_openai_yaml(skill), mode)
        if also_codex_skills:
            write_file(root/".codex"/"skills"/skill/"SKILL.md", render_skill(skill), mode)
            write_file(root/".codex"/"skills"/skill/"agents"/"openai.yaml", render_openai_yaml(skill), mode)
    write_file(root/"docs"/"glossary.md", render_glossary(profile), mode)
    write_file(root/"docs"/"rules"/"naming-and-consistency.md", render_rules(), mode)
    write_file(root/"docs"/"rules"/"engineering-laws.md", render_engineering_laws(), mode)
    write_file(root/"docs"/"rules"/"review-checklist.md", render_review_checklist(), mode)
    write_file(root/"docs"/"architecture"/"boundaries.md", "# Architecture Boundaries\n\n"+"\n".join(f"- {b}" for b in profile.get("boundaries", [])), mode)
    write_file(root/"docs"/"skillset"/"scale-selection-guide.md", render_scale_selection_guide(), mode)
    write_file(root/"docs"/"skillset"/"module-routing-guide.md", render_module_routing_guide(profile, set(skills)), mode)
    write_file(root/"docs"/"skillset"/"project-document-analysis-guide.md", render_project_analysis_guide(), mode)
    write_file(root/"docs"/"skillset"/"profile-schema-reference.md", render_profile_schema_reference(), mode)
    write_file(root/"docs"/"skillset"/"gpts-operator-guide.md", render_gpts_operator_guide(), mode)
    write_file(root/"docs"/"skillset"/"project-source-integration-guide.md", render_source_integration_guide(), mode)
    if opts.get("include_commands"):
        for name, content in COMMANDS.items(): write_file(root/"commands"/name, f"# /{name[:-3]}\n\n{content}", mode)
    if opts.get("include_references"):
        for name, content in REFERENCES.items(): write_file(root/"references"/name, content, mode)
    if opts.get("include_personas"):
        for name, content in PERSONAS.items(): write_file(root/"agents"/name, content, mode)
    if opts.get("include_governance"):
        write_file(root/"docs"/"governance"/"change-control.md", "# Change Control\n\n- Major behavior, contract, data, or release changes need a written plan and evidence pack.", mode)
    for module in profile.get("modules", []):
        write_file(root/module["path"]/"AGENTS.md", render_module_agents(module, profile["project_size"], set(skills)), mode)


def read_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def config_has_top_level_network(text: str) -> bool:
    section: Optional[str] = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"): continue
        if line.startswith("[") and line.endswith("]"):
            section = line.strip("[]"); continue
        if re.match(r"^network_access\s*=", line) and section != "sandbox_workspace_write": return True
    return False


def validate_generated(root: Path) -> List[str]:
    errors: List[str] = []
    required = [root/"AGENTS.md", root/"PLANS.md", root/".codex"/"config.toml", root/".codex"/"policy.lock.json", root/".codex"/"skillset-manifest.json", root/".agents"/"skills", root/"docs"/"rules"/"engineering-laws.md", root/"docs"/"skillset"/"scale-selection-guide.md", root/"docs"/"skillset"/"module-routing-guide.md"]
    for p in required:
        if not p.exists(): errors.append(f"Missing: {p}")
    config = root/".codex"/"config.toml"
    if config.exists():
        text = config.read_text(encoding="utf-8")
        if "[sandbox_workspace_write]" not in text or not re.search(r"\[sandbox_workspace_write\][\s\S]*network_access\s*=\s*false", text): errors.append("config.toml should contain [sandbox_workspace_write] network_access = false")
        if config_has_top_level_network(text): errors.append("config.toml has top-level network_access; move it under [sandbox_workspace_write]")
    skills_dir = root/".agents"/"skills"
    if skills_dir.exists():
        for sdir in skills_dir.iterdir():
            if sdir.is_dir():
                skill_md = sdir/"SKILL.md"
                if not skill_md.exists():
                    errors.append(f"Missing SKILL.md: {sdir}")
                else:
                    skill_text = skill_md.read_text(encoding="utf-8")
                    if not skill_text.startswith("---\n") or "\n---\n" not in skill_text[4:]:
                        errors.append(f"Bad SKILL.md front matter: {skill_md}")
                    if not re.search(r"^name:\s*", skill_text, re.MULTILINE) or not re.search(r"^description:\s*", skill_text, re.MULTILINE):
                        errors.append(f"SKILL.md front matter lacks name/description: {skill_md}")
                yml = sdir/"agents"/"openai.yaml"
                if not yml.exists(): errors.append(f"Missing openai.yaml: {sdir}")
                else:
                    y = yml.read_text(encoding="utf-8")
                    if "interface:" not in y or "policy:" not in y or "allow_implicit_invocation" not in y: errors.append(f"Bad openai.yaml shape: {yml}")
    manifest = root/".codex"/"skillset-manifest.json"
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            declared_skill_list = data.get("skills", [])
            optional_skill_list = data.get("optional_skills", [])
            declared_skills = set(declared_skill_list)
            optional_skills = set(optional_skill_list)
            actual_skills = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.exists() else set()
            if len(declared_skill_list) != len(declared_skills):
                errors.append("Manifest has duplicate skills")
            if len(optional_skill_list) != len(optional_skills):
                errors.append("Manifest has duplicate optional_skills")
            overlap = declared_skills & optional_skills
            if overlap:
                errors.append(f"Manifest skills overlap optional_skills: {', '.join(sorted(overlap))}")
            for skill in sorted(declared_skills | optional_skills | actual_skills):
                if not is_safe_skill_name(skill):
                    errors.append(f"Unsafe skill directory/manifest name: {skill}")
            for skill in sorted(declared_skills - actual_skills):
                errors.append(f"Manifest skill missing on disk: {skill}")
            for skill in sorted(actual_skills - declared_skills):
                errors.append(f"Skill exists on disk but not in manifest: {skill}")
            budget = data.get("budget", {})
            if budget:
                selected_count = int(budget.get("selected_count", len(declared_skills)))
                max_count = int(budget.get("max_project_skills", selected_count))
                estimated_chars = int(budget.get("estimated_initial_metadata_chars", 0))
                max_chars = int(budget.get("max_initial_metadata_chars", max(estimated_chars, 1)))
                if selected_count > max_count:
                    errors.append(f"Skill count budget exceeded: {selected_count} > {max_count}")
                if estimated_chars > max_chars:
                    errors.append(f"Initial metadata budget exceeded: {estimated_chars} > {max_chars}")
            for m in data.get("modules", []):
                if not is_safe_relative_path(m.get("path", "")):
                    errors.append(f"Unsafe module path in manifest: {m.get('path')}")
                    continue
                magents = root/m["path"]/"AGENTS.md"
                if not magents.exists(): errors.append(f"Missing module AGENTS.md: {magents}")
                else:
                    txt = magents.read_text(encoding="utf-8")
                    if "## Generated preferred skills" not in txt or "## Local commands" not in txt or "## Local quality gates" not in txt:
                        errors.append(f"Module AGENTS.md lacks required sections: {magents}")
                module_budget = m.get("budget", {})
                if module_budget:
                    module_selected_count = int(module_budget.get("selected_count", len(m.get("skills", []))))
                    module_max_count = int(module_budget.get("max_module_skills", module_selected_count))
                    module_estimated_chars = int(module_budget.get("estimated_initial_metadata_chars", 0))
                    module_max_chars = int(module_budget.get("max_initial_metadata_chars", max(module_estimated_chars, 1)))
                    if module_selected_count > module_max_count:
                        errors.append(f"Module skill count budget exceeded: {m.get('path')} {module_selected_count} > {module_max_count}")
                    if module_estimated_chars > module_max_chars:
                        errors.append(f"Module metadata budget exceeded: {m.get('path')} {module_estimated_chars} > {module_max_chars}")
                for skill in m.get("skills", []):
                    if skill not in declared_skills:
                        errors.append(f"Module references skill not generated in manifest: {m.get('path')} -> {skill}")
        except Exception as exc: errors.append(f"Bad manifest JSON: {exc}")
    return errors


def write_example_profiles(base: Path) -> None:
    out = base/"examples"/"profiles"; out.mkdir(parents=True, exist_ok=True)
    for preset in PRESETS:
        (out/f"{preset}.json").write_text(json.dumps(preset_profile(preset), indent=2, ensure_ascii=False)+"\n", encoding="utf-8")


def write_generated_examples(base: Path) -> None:
    out = base/"examples"/"generated"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    for preset in PRESETS:
        generate(preset_profile(preset), out/preset, mode="overwrite")

def cmd_self_check(args: argparse.Namespace) -> int:
    root = Path(args.root)
    errors: List[str] = []
    for preset in PRESETS:
        profile = preset_profile(preset)
        profile_errors = validate_profile(profile)
        errors.extend(f"profile/{preset}: {e}" for e in profile_errors)
        plan = compute_skill_plan(profile)
        if set(plan["selected"]) & set(plan["optional"]):
            errors.append(f"plan/{preset}: selected and optional skills overlap")
        if args.generated_examples:
            generated = root/"examples"/"generated"/preset
            if generated.exists():
                errors.extend(f"generated/{preset}: {e}" for e in validate_generated(generated))
            else:
                errors.append(f"generated/{preset}: missing example output at {generated}")
        if args.temp_generate:
            with tempfile.TemporaryDirectory(prefix=f"codex_skillset_{preset}_") as td:
                out = Path(td)/"out"
                generate(profile, out, mode="overwrite")
                errors.extend(f"temp-generated/{preset}: {e}" for e in validate_generated(out))
    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    checked = ["profiles"]
    if args.generated_examples:
        checked.append("bundled generated examples")
    if args.temp_generate:
        checked.append("fresh temp generation")
    print("PASS / " + ", ".join(checked) + f" / {len(PRESETS)} presets")
    return 0


def cmd_list_presets(_: argparse.Namespace) -> int:
    for name, meta in PRESETS.items(): print(f"{name}\tproject_type={meta['project_type']}\tsize={meta['project_size']}\tbundles={','.join(meta.get('bundles', []))}")
    return 0

def cmd_list_sizes(_: argparse.Namespace) -> int:
    for name, meta in PROJECT_SIZES.items(): print(f"{name}\t{meta['description']}\tmax_skills={meta['max_project_skills']}\tmetadata_budget={meta['max_initial_metadata_chars']}")
    return 0

def cmd_list_bundles(_: argparse.Namespace) -> int:
    for name, skills in BUNDLES.items(): print(f"{name}\t{len(skills)} skills")
    return 0

def cmd_init(args: argparse.Namespace) -> int:
    profile = preset_profile(args.preset, args.size)
    Path(args.output).write_text(json.dumps(profile, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0

def recommendation(profile: Dict[str, Any], path: Optional[str]=None) -> Dict[str, Any]:
    profile = normalize_profile(profile); opts = scale_options(profile); plan = compute_skill_plan(profile)
    out: Dict[str, Any] = {
        "project_type": profile["project_type"],
        "project_size": profile["project_size"],
        "scale_options": opts,
        "policy_packs": profile.get("policy_packs", []),
        "budget": plan["budget"],
    }
    if path:
        module = match_module_by_path(profile, path)
        if module:
            out.update({
                "matched_module": module["name"],
                "module_path": module["path"],
                "module_type": module["module_type"],
                "skills": plan["module_selected"].get(module["path"], []),
                "optional_skills": plan["module_optional"].get(module["path"], []),
                "commands": module.get("commands", {}),
            })
        else:
            out.update({"matched_module": None, "skills": plan["selected"], "optional_skills": plan["optional"], "commands": profile.get("commands", {})})
    else:
        out.update({
            "skills": plan["selected"],
            "optional_skills": plan["optional"],
            "modules": [
                {
                    "name": m["name"],
                    "path": m["path"],
                    "module_type": m["module_type"],
                    "skills": plan["module_selected"].get(m["path"], []),
                    "optional_skills": plan["module_optional"].get(m["path"], []),
                }
                for m in profile.get("modules", [])
            ],
        })
    return out

def cmd_recommend(args: argparse.Namespace) -> int:
    print(json.dumps(recommendation(read_json(args.config), args.path), indent=2, ensure_ascii=False))
    return 0

def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_profile(read_json(args.config))
    if errors:
        print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0

def cmd_generate(args: argparse.Namespace) -> int:
    profile = normalize_profile(read_json(args.config))
    generate(profile, Path(args.root), args.mode, also_codex_skills=args.also_write_codex_skills)
    print(f"Generated skillset at {args.root}"); return 0

def cmd_validate_generated(args: argparse.Namespace) -> int:
    errors = validate_generated(Path(args.root))
    if errors:
        print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0

def cmd_write_examples(args: argparse.Namespace) -> int:
    root = Path(args.root)
    write_example_profiles(root)
    if args.generated:
        write_generated_examples(root)
        print(f"Wrote example profiles and generated outputs under {args.root}/examples")
    else:
        print(f"Wrote example profiles under {args.root}/examples/profiles")
    return 0

def main(argv: Optional[Sequence[str]]=None) -> int:
    parser = argparse.ArgumentParser(description="Codex-lean scale-aware module-aware agent skillset generator")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("list-presets"); p.set_defaults(func=cmd_list_presets)
    p=sub.add_parser("list-sizes"); p.set_defaults(func=cmd_list_sizes)
    p=sub.add_parser("list-bundles"); p.set_defaults(func=cmd_list_bundles)
    p=sub.add_parser("self-check"); p.add_argument("--root", default="."); p.add_argument("--generated-examples", action="store_true"); p.add_argument("--temp-generate", action="store_true"); p.set_defaults(func=cmd_self_check)
    p=sub.add_parser("init"); p.add_argument("--preset", required=True, choices=sorted(PRESETS)); p.add_argument("--size", choices=sorted(PROJECT_SIZES)); p.add_argument("--output", required=True); p.set_defaults(func=cmd_init)
    p=sub.add_parser("recommend"); p.add_argument("--config", required=True); p.add_argument("--path"); p.set_defaults(func=cmd_recommend)
    p=sub.add_parser("validate"); p.add_argument("--config", required=True); p.set_defaults(func=cmd_validate)
    p=sub.add_parser("generate"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip", "backup", "overwrite"], default="skip"); p.add_argument("--also-write-codex-skills", action="store_true"); p.set_defaults(func=cmd_generate)
    p=sub.add_parser("validate-generated"); p.add_argument("--root", required=True); p.set_defaults(func=cmd_validate_generated)
    p=sub.add_parser("write-examples"); p.add_argument("--root", default="."); p.add_argument("--generated", action="store_true"); p.set_defaults(func=cmd_write_examples)
    args = parser.parse_args(argv); return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
