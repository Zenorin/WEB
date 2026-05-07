#!/usr/bin/env python3
"""Codex Skillset Starter v4.9.5-dev-ops-r1.

Wraps the v4.9 final-candidate generator and adds first-class project
workstreams, decision-gated development scaffold generation, and full
dev-kit validation commands.
"""
from __future__ import annotations

import argparse
import json
import sys
import re
import shutil
import tempfile
import tomllib
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codex_skillset_generator_core as _base
from codex_skillset_generator_core import *  # re-export v4.9 API and constants

VERSION = "4.9.5-dev-ops-r1"
PACKAGE_MANAGERS = {"pnpm", "npm", "yarn"}
STACK_SELECTION_MODES = {"decision-first", "preset-fixed", "manual"}
SCAFFOLD_GENERATION_POLICIES = {"blocked_until_stack_selected", "allow_preset_stack", "manual_override"}
PINNED_PACKAGE_MANAGERS = {"pnpm": "9.12.3", "npm": "10.8.2", "yarn": "1.22.22"}
PINNED_TS_DEV_DEPENDENCIES = {"typescript": "^5.5.4"}
PINNED_WEB_DEPENDENCIES = {"react": "^18.3.1", "react-dom": "^18.3.1"}
PINNED_WEB_DEV_DEPENDENCIES = {"@vitejs/plugin-react": "^4.3.0", "vite": "^5.4.0", **PINNED_TS_DEV_DEPENDENCIES}
PINNED_FASTIFY_DEPENDENCIES = {"fastify": "^4.28.1"}
PINNED_FASTIFY_DEV_DEPENDENCIES = {"tsx": "^4.16.2", **PINNED_TS_DEV_DEPENDENCIES}
API_RUNTIME_STACKS = {"fastapi-python", "fastify-typescript"}
FRONTEND_RUNTIME_STACKS = {"react-vite-typescript"}
EXTENSION_RUNTIME_STACKS = {"chrome-mv3-typescript"}
SECRETISH_KEY_RE = re.compile(r"(?i)(api[_-]?key|secret|password|passwd|access[_-]?token|private[_-]?key|cookie|session)")
SAFE_PLACEHOLDER_RE = re.compile(r"(?i)^(|<[^>]+>|changeme|change-me|placeholder|example|todo|none|null|your[_-].*)$")
CLEAN_ROOM_BLOCKED_RE = re.compile(r"(^|/)(_next/static/chunks/|.*\.map$|background\.js$|preload\.js$)")
PYPROJECT_SPEC_RE = re.compile(r"^[A-Za-z0-9_.-]+(?:\[[A-Za-z0-9_,.-]+\])?(?:[<>=!~]=?\d+(?:\.\d+){0,2}(?:[-+][0-9A-Za-z.-]+)?(?:,\s*[<>=!~]=?\d+(?:\.\d+){0,2}(?:[-+][0-9A-Za-z.-]+)?)*)$")
COMMON_SKILL_WORKFLOW_DOC = "docs/skillset/common-skill-workflow.md"
SEMVERISH_SPEC_RE = re.compile(r"^(?:[\^~]?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?|workspace:\*|workspace:[\^~]?\d+\.\d+\.\d+|file:.+|link:.+)$")


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value))


PRESETS: Dict[str, Dict[str, Any]] = _copy(_base.PRESETS)
PRESETS["web-clean-room-workstreams"] = {
    "project_type": "web-clean-room-workstreams",
    "project_size": "large",
    "bundles": ["web-saas", "browser-extension", "crawler-session", "clean-room-rebuild", "shared-contracts"],
    "policy_packs": ["clean-room", "no-feature-deletion", "privacy-boundary"],
    "allow_custom_skills": True,
    "package_manager": "pnpm",
    "runtime_stack": {"frontend": "react-vite-typescript", "api": "fastapi-python", "extension": "chrome-mv3-typescript"},
    "stack_selection_mode": "decision-first",
    "stack_decision_required": True,
    "selected_stack": {"frontend": "react-vite-typescript", "api": "fastapi-python", "extension": "chrome-mv3-typescript", "package_manager": "pnpm"},
    "stack_candidates": [
        {"name": "react-vite-fastapi", "frontend": "react-vite-typescript", "api": "fastapi-python", "extension": "chrome-mv3-typescript", "package_manager": "pnpm", "reason": "Default for clean-room web plus local Python API prototyping."},
        {"name": "react-vite-fastify", "frontend": "react-vite-typescript", "api": "fastify-typescript", "extension": "chrome-mv3-typescript", "package_manager": "pnpm", "reason": "Use when a single TypeScript runtime is preferred."}
    ],
    "stack_decision_reason": "Selected React/Vite web, FastAPI Python API, Chrome MV3 extension, and pnpm workspace as the default dev-ready clean-room stack. Change selected_stack before scaffold when project evidence requires a different API runtime or package manager.",
    "scaffold_generation_policy": "blocked_until_stack_selected",
    "generate_project_scaffold": True,
    "max_project_skills": 38,
    "max_initial_metadata_chars": 8600,
    "commands": {
        "install": "pnpm install && cd apps/api && python -m pip install -e .[dev]",
        "dev_web": "pnpm --filter web dev",
        "dev_api": "cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000",
        "dev_extension": "pnpm --filter extension build",
        "test": "pnpm -r test && cd apps/api && pytest",
        "build": "pnpm -r build",
        "validate_scaffold": "python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .",
    },
    "modules": [
        {"name": "web", "path": "apps/web", "module_type": "frontend-product-ui", "bundles": ["frontend-product-ui"], "preferred_skills": ["project-frontend-design", "frontend-product-ui", "design-system-consistency", "ui-state-coverage", "responsive-layout-review", "browser-smoke"]},
        {"name": "api", "path": "apps/api", "module_type": "backend-api", "bundles": ["backend-api"], "preferred_skills": ["project-backend-api", "api-contract-change", "api-error-handling-review", "backend-test-matrix", "service-repository-boundary-check", "authz-security-review"]},
        {"name": "extension", "path": "apps/extension", "module_type": "browser-extension", "bundles": ["browser-extension"], "preferred_skills": ["project-extension-bridge", "extension-permission-review", "content-script-boundary", "message-contract-review", "privacy-boundary-review"]},
        {"name": "contracts", "path": "packages/contracts", "module_type": "shared-contracts", "bundles": ["shared-contracts"], "preferred_skills": ["project-contracts", "api-contract-change", "backward-compat-check", "consistency-guard"]},
        {"name": "core", "path": "packages/core", "module_type": "data-pipeline", "bundles": ["data-pipeline"], "preferred_skills": ["project-core-pipeline", "schema-contract-check", "data-quality-gate", "idempotency-check"]},
        {"name": "collectors", "path": "packages/collectors", "module_type": "crawler-session", "bundles": ["crawler-session"], "preferred_skills": ["project-market-collectors", "crawler-contract-review", "session-boundary-security", "anti-bot-compliance-check"]},
        {"name": "reference-analysis", "path": "tools/reference-analysis", "module_type": "clean-room-rebuild", "bundles": ["clean-room-rebuild"], "preferred_skills": ["project-reference-mapper", "clean-room-reference-analysis", "reference-role-report", "contract-extraction", "source-copy-audit"]},
    ],
    "workstreams": [
        {"skill": "project-development-bootstrap", "name": "Project Development Bootstrap", "module_paths": ["."], "objective": "Create and validate the repo bootstrap, workspace, env template, and shared build scripts without overriding workstream routing.", "workflow": ["Create root package/workspace/env/check files.", "Do not decide feature implementation details for app/package modules.", "Validate scaffold paths against module/workstream routing."], "quality_gates": ["Root package/workspace files exist.", "No secret values are committed.", "validate-scaffold passes."]},
        {"skill": "project-frontend-design", "name": "Project Frontend Design", "module_paths": ["apps/web"], "objective": "Own UI composition, screen states, responsive layout, and browser smoke checks for the web app.", "workflow": ["Review screen goal, route, states, and primary action.", "Implement reusable React/Vite components without dropping UX states.", "Run build/typecheck or document blockers."], "quality_gates": ["Web build or blocker evidence exists.", "Loading/empty/error/success states are covered."]},
        {"skill": "project-backend-api", "name": "Project Backend API", "module_paths": ["apps/api"], "objective": "Own API entrypoints, error envelopes, persistence boundary, authz, and backend test matrix.", "workflow": ["Define request/response/error contracts.", "Keep handler/service/repository responsibilities separated.", "Run backend tests or document blockers."], "quality_gates": ["Health route exists.", "API contract changes have tests or explicit evidence."]},
        {"skill": "project-contracts", "name": "Project Contracts", "module_paths": ["packages/contracts"], "objective": "Own shared DTO/schema/event contracts and compatibility notes.", "workflow": ["Define stable public shapes.", "Check downstream impact before changing fields.", "Document migrations for breaking changes."], "quality_gates": ["Contract package builds.", "Breaking changes include migration notes."]},
        {"skill": "project-core-pipeline", "name": "Project Core Pipeline", "module_paths": ["packages/core"], "objective": "Own deterministic core processing, pipeline state, and idempotent execution contracts.", "workflow": ["Separate pure core logic from IO.", "Define retry/cancel/error behavior.", "Add deterministic tests for core transformations."], "quality_gates": ["Core package builds.", "Idempotency risks reviewed."]},
        {"skill": "project-extension-bridge", "name": "Project Extension Bridge", "module_paths": ["apps/extension"], "objective": "Own extension permissions, message contracts, content/background boundaries, and privacy review.", "workflow": ["Minimize manifest permissions.", "Define message payload/reply/error shapes.", "Keep content scripts separated from privileged background logic."], "quality_gates": ["Manifest permissions are justified.", "Message contract is documented."]},
        {"skill": "project-market-collectors", "name": "Project Market Collectors", "module_paths": ["packages/collectors"], "objective": "Own collector contracts, selector fallbacks, session boundaries, and compliance checks.", "workflow": ["Define allowed inputs/outputs/errors.", "Avoid brittle selector-only assumptions.", "Respect session/access-control boundaries."], "quality_gates": ["Collector output schema is stable.", "Anti-bot and session boundaries reviewed."]},
        {"skill": "project-reference-mapper", "name": "Project Reference Mapper", "module_paths": ["tools/reference-analysis"], "objective": "Own clean-room reference role reports, contract extraction, and source-copy audit evidence.", "workflow": ["Treat reference files as read-only.", "Extract roles/contracts without copying implementation.", "Write role reports before excluding observed behavior."], "quality_gates": ["Role report exists.", "Source-copy audit passes."]},
    ],
    "dev_modules": [
        {"name": "web", "path": "apps/web", "kind": "app", "entrypoints": ["package.json", "index.html", "src/main.tsx"]},
        {"name": "api", "path": "apps/api", "kind": "api", "entrypoints": ["pyproject.toml", "app/main.py"]},
        {"name": "extension", "path": "apps/extension", "kind": "extension", "entrypoints": ["package.json", "manifest.json", "src/background.ts"]},
        {"name": "contracts", "path": "packages/contracts", "kind": "package", "entrypoints": ["package.json", "src/index.ts"]},
        {"name": "core", "path": "packages/core", "kind": "package", "entrypoints": ["package.json", "src/index.ts"]},
        {"name": "collectors", "path": "packages/collectors", "kind": "package", "entrypoints": ["package.json", "src/index.ts"]},
        {"name": "reference-analysis", "path": "tools/reference-analysis", "kind": "tool", "entrypoints": ["package.json", "src/index.ts"]},
    ],
}


def normalized_repo_path(path: str) -> str:
    raw = str(path).replace("\\", "/").strip().strip("/")
    return "." if raw in {"", "."} else raw


def is_safe_workstream_path(path: str) -> bool:
    if path == ".":
        return True
    return _base.is_safe_relative_path(path)


def path_matches(base: str, candidate: str) -> bool:
    base_norm = normalized_repo_path(base)
    cand_norm = normalized_repo_path(candidate)
    if base_norm == ".":
        return cand_norm == "."
    return cand_norm == base_norm or cand_norm.startswith(base_norm + "/")


def normalize_workstream(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("workstream entries must be objects")
    if not raw.get("skill"):
        raise ValueError("workstream.skill is required")
    ws = dict(raw)
    ws.setdefault("name", _base.slug_title(ws["skill"]))
    ws.setdefault("module_paths", [])
    ws.setdefault("objective", f"Own the {ws['name']} workstream.")
    ws.setdefault("workflow", [])
    ws.setdefault("quality_gates", [])
    ws.setdefault("handoff", [])
    return ws


def normalize_dev_module(raw: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("dev_modules entries must be objects")
    if not raw.get("path"):
        raise ValueError("dev_module.path is required")
    dev = dict(raw)
    dev.setdefault("name", Path(dev["path"]).name or "module")
    dev.setdefault("kind", "package")
    dev.setdefault("entrypoints", [])
    return dev


def default_runtime_stack(profile: Dict[str, Any]) -> Dict[str, str]:
    raw = profile.get("runtime_stack", {}) if isinstance(profile.get("runtime_stack", {}), dict) else {}
    return {"frontend": raw.get("frontend", "react-vite-typescript"), "api": raw.get("api", "fastapi-python"), "extension": raw.get("extension", "chrome-mv3-typescript")}


def selected_stack_matches_runtime(profile: Dict[str, Any]) -> bool:
    selected = profile.get("selected_stack", {}) if isinstance(profile.get("selected_stack", {}), dict) else {}
    runtime = profile.get("runtime_stack", {}) if isinstance(profile.get("runtime_stack", {}), dict) else {}
    for key in ("frontend", "api", "extension"):
        if selected.get(key) != runtime.get(key): return False
    if selected.get("package_manager") and selected.get("package_manager") != profile.get("package_manager"): return False
    return True


def stack_decision_required(profile: Dict[str, Any]) -> bool:
    return bool(profile.get("stack_decision_required")) or profile.get("stack_selection_mode") == "decision-first" or profile.get("scaffold_generation_policy") == "blocked_until_stack_selected"


def render_stack_decision_doc(profile: Dict[str, Any]) -> str:
    selected = profile.get("selected_stack", {}) if isinstance(profile.get("selected_stack", {}), dict) else {}
    candidates = profile.get("stack_candidates", []) if isinstance(profile.get("stack_candidates", []), list) else []
    lines = ["# Stack Decision", "", "This file is generated from `codex-profile.json`. It must be reviewed before scaffolded code is treated as the active development baseline.", "", "## Decision mode", f"- stack_selection_mode: `{profile.get('stack_selection_mode', 'preset-fixed')}`", f"- stack_decision_required: `{bool(profile.get('stack_decision_required'))}`", f"- scaffold_generation_policy: `{profile.get('scaffold_generation_policy', 'allow_preset_stack')}`", "", "## Selected stack"]
    if selected:
        for key in ["frontend", "api", "extension", "package_manager"]: lines.append(f"- {key}: `{selected.get(key, '')}`")
    else:
        lines.append("- Not selected. Scaffold generation is blocked when stack decision is required.")
    lines += ["", "## Decision reason", profile.get("stack_decision_reason") or "- Fill this before approving the scaffold baseline.", "", "## Candidate stacks"]
    if candidates:
        for cand in candidates:
            if isinstance(cand, dict): lines.append(f"- `{cand.get('name', 'candidate')}`: frontend=`{cand.get('frontend', '')}`, api=`{cand.get('api', '')}`, extension=`{cand.get('extension', '')}`, package_manager=`{cand.get('package_manager', '')}` — {cand.get('reason', '')}")
    else: lines.append("- No candidates recorded.")
    lines += ["", "## Gate", "Scaffold is approved only when `selected_stack` is present, matches `runtime_stack` and `package_manager`, and this decision file is present in `docs/decisions/stack-decision.md`."]
    return "\n".join(lines).rstrip()+"\n"


def default_dev_modules(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    if profile.get("dev_modules"):
        return list(profile["dev_modules"])
    paths = {m["path"] for m in profile.get("modules", [])}
    defaults: List[Dict[str, Any]] = []
    api_entries = ["pyproject.toml", "app/main.py"] if default_runtime_stack(profile).get("api") == "fastapi-python" else ["package.json", "src/server.ts"]
    preferred = [
        ("apps/web", "app", ["package.json", "index.html", "src/main.tsx"]),
        ("apps/api", "api", api_entries),
        ("apps/extension", "extension", ["package.json", "manifest.json", "src/background.ts"]),
        ("packages/contracts", "package", ["package.json", "src/index.ts"]),
        ("packages/core", "package", ["package.json", "src/index.ts"]),
        ("packages/collectors", "package", ["package.json", "src/index.ts"]),
        ("tools/reference-analysis", "tool", ["package.json", "src/index.ts"]),
    ]
    for path, kind, entrypoints in preferred:
        if path in paths or profile.get("project_type") == "web-clean-room-workstreams":
            defaults.append({"name": Path(path).name, "path": path, "kind": kind, "entrypoints": entrypoints})
    return defaults


def module_paths(profile: Dict[str, Any]) -> Set[str]:
    return {normalized_repo_path(m["path"]) for m in profile.get("modules", [])}


def workstream_skill_map(profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {ws["skill"]: ws for ws in profile.get("workstreams", [])}


def workstreams_for_module_path(profile: Dict[str, Any], module_path: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for ws in profile.get("workstreams", []):
        for wpath in ws.get("module_paths", []):
            if wpath != "." and path_matches(wpath, module_path):
                out.append(ws)
                break
    return out


def normalize_profile(raw: Dict[str, Any]) -> Dict[str, Any]:
    profile = _base.normalize_profile(raw)
    profile.setdefault("workstreams", [])
    profile.setdefault("runtime_stack", {})
    profile.setdefault("package_manager", "pnpm")
    profile.setdefault("generate_project_scaffold", False)
    profile.setdefault("dev_modules", [])
    profile.setdefault("stack_selection_mode", "preset-fixed")
    profile.setdefault("stack_decision_required", False)
    profile.setdefault("selected_stack", {})
    profile.setdefault("stack_candidates", [])
    profile.setdefault("stack_decision_reason", "")
    profile.setdefault("scaffold_generation_policy", "allow_preset_stack")
    profile["workstreams"] = [normalize_workstream(w) for w in profile.get("workstreams", [])]
    profile["runtime_stack"] = default_runtime_stack(profile)
    if not isinstance(profile.get("selected_stack"), dict): profile["selected_stack"] = {}
    if profile.get("stack_selection_mode") == "preset-fixed" and not profile.get("selected_stack"):
        profile["selected_stack"] = {**profile["runtime_stack"], "package_manager": profile.get("package_manager", "pnpm")}
    profile["dev_modules"] = [normalize_dev_module(m) for m in default_dev_modules(profile)]
    return profile


def preset_profile(preset: str, size: Optional[str] = None) -> Dict[str, Any]:
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: {preset}")
    if preset in _base.PRESETS and preset != "web-clean-room-workstreams":
        profile = _base.preset_profile(preset, size)
        return normalize_profile(profile)
    base = _copy(PRESETS[preset])
    if size:
        base["project_size"] = size
    profile = {
        "project_name": preset.replace("-", " ").title(),
        **base,
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
    if "commands" not in profile:
        profile["commands"] = dict(_base.DEFAULT_COMMANDS)
    if "local-only" in profile.get("policy_packs", []):
        profile["forbidden_defaults"] = _base.unique(list(profile.get("forbidden_defaults", [])) + ["telemetry", "analytics", "crash report", "remote upload", "cloud sync", "webhook", "automatic external notification"])
    if "clean-room" in profile.get("policy_packs", []):
        profile["boundaries"].extend(["Reference files are read-only.", "Extract behavior contracts; do not copy source text verbatim.", "Write role reports before excluding behavior."])
    return normalize_profile(profile)


def validate_profile(profile: Dict[str, Any]) -> List[str]:
    errors = _base.validate_profile(profile)
    try:
        p = normalize_profile(profile)
    except Exception as exc:
        return [str(exc)]
    if p.get("package_manager") not in PACKAGE_MANAGERS:
        errors.append(f"Unknown package_manager: {p.get('package_manager')}. Expected one of {sorted(PACKAGE_MANAGERS)}")
    if p.get("stack_selection_mode") not in STACK_SELECTION_MODES:
        errors.append(f"Unknown stack_selection_mode: {p.get('stack_selection_mode')}. Expected one of {sorted(STACK_SELECTION_MODES)}")
    if p.get("scaffold_generation_policy") not in SCAFFOLD_GENERATION_POLICIES:
        errors.append(f"Unknown scaffold_generation_policy: {p.get('scaffold_generation_policy')}. Expected one of {sorted(SCAFFOLD_GENERATION_POLICIES)}")
    runtime_stack = p.get("runtime_stack", {})
    if runtime_stack.get("frontend") not in FRONTEND_RUNTIME_STACKS:
        errors.append(f"Unknown runtime_stack.frontend: {runtime_stack.get('frontend')}")
    if runtime_stack.get("api") not in API_RUNTIME_STACKS:
        errors.append(f"Unknown runtime_stack.api: {runtime_stack.get('api')}")
    if runtime_stack.get("extension") not in EXTENSION_RUNTIME_STACKS:
        errors.append(f"Unknown runtime_stack.extension: {runtime_stack.get('extension')}")
    selected = p.get("selected_stack", {}) if isinstance(p.get("selected_stack", {}), dict) else {}
    if stack_decision_required(p) and not selected:
        errors.append("selected_stack is required when stack_decision_required=true or scaffold_generation_policy=blocked_until_stack_selected")
    if selected:
        if selected.get("frontend") not in FRONTEND_RUNTIME_STACKS: errors.append(f"Unknown selected_stack.frontend: {selected.get('frontend')}")
        if selected.get("api") not in API_RUNTIME_STACKS: errors.append(f"Unknown selected_stack.api: {selected.get('api')}")
        if selected.get("extension") not in EXTENSION_RUNTIME_STACKS: errors.append(f"Unknown selected_stack.extension: {selected.get('extension')}")
        if selected.get("package_manager") not in PACKAGE_MANAGERS: errors.append(f"Unknown selected_stack.package_manager: {selected.get('package_manager')}")
        if not selected_stack_matches_runtime(p): errors.append("selected_stack must match runtime_stack and package_manager before scaffold generation")
    if stack_decision_required(p) and not str(p.get("stack_decision_reason", "")).strip():
        errors.append("stack_decision_reason is required when stack decision gate is active")
    seen_ws: Set[str] = set()
    known_module_paths = module_paths(p)
    for ws in p.get("workstreams", []):
        skill = ws.get("skill", "")
        if not _base.is_safe_skill_name(skill):
            errors.append(f"Unsafe workstream.skill name: {skill}. Use lowercase slug form.")
        if skill in seen_ws:
            errors.append(f"Duplicate workstream.skill: {skill}")
        seen_ws.add(skill)
        if not ws.get("module_paths"):
            errors.append(f"workstream.module_paths is required for {skill}")
        for wpath in ws.get("module_paths", []):
            norm = normalized_repo_path(wpath)
            if not is_safe_workstream_path(norm):
                errors.append(f"Unsafe workstream.module_path in {skill}: {wpath}")
            elif norm != "." and norm not in known_module_paths:
                errors.append(f"workstream.module_path does not match a configured module.path in {skill}: {wpath}")
    for dev in p.get("dev_modules", []):
        if not _base.is_safe_relative_path(dev.get("path", "")):
            errors.append(f"Unsafe dev_module.path in {dev.get('name')}: {dev.get('path')}")
    return errors


def compute_skill_plan(profile: Dict[str, Any]) -> Dict[str, Any]:
    profile = normalize_profile(profile)
    if not profile.get("workstreams"):
        return _base.compute_skill_plan(profile)
    size_meta = _base.PROJECT_SIZES[profile["project_size"]]
    max_count = int(profile.get("max_project_skills", size_meta["max_project_skills"]))
    max_chars = int(profile.get("max_initial_metadata_chars", size_meta["max_initial_metadata_chars"]))
    core = list(size_meta["core"])
    policy_required = _base.skills_for_policy_packs(profile.get("policy_packs", []))
    explicit_required = list(profile.get("extra_skills", []))
    workstream_required = [ws["skill"] for ws in profile.get("workstreams", [])]
    required = _base.unique(core + policy_required + explicit_required + workstream_required)
    max_count = max(max_count, len(required))
    max_chars = max(max_chars, _base.estimate_initial_metadata_chars(required))
    module_selected: Dict[str, List[str]] = {}
    module_optional: Dict[str, List[str]] = {}
    module_candidates: List[str] = []
    for module in profile.get("modules", []):
        selected, optional = _base.compute_module_skill_plan(module, profile["project_size"])
        selected = _base.unique([ws["skill"] for ws in workstreams_for_module_path(profile, module["path"])] + selected)
        module_selected[module["path"]] = selected
        module_optional[module["path"]] = optional
        module_candidates.extend(selected)
    candidates = _base.unique(required + _base.skills_for_bundles(profile.get("bundles", [])) + module_candidates)
    selected, optional = _base.select_essential_skills(candidates, required=required, max_count=max_count, max_metadata_chars=max_chars)
    selected_set = set(selected)
    routed_module_selected = {path: [s for s in skills if s in selected_set] for path, skills in module_selected.items()}
    routed_module_optional = {path: _base.unique([s for s in module_selected.get(path, []) + module_optional.get(path, []) if s not in selected_set]) for path in module_selected}
    all_optional = _base.unique(optional + [s for skills in routed_module_optional.values() for s in skills])
    module_budgets = {}
    for module in profile.get("modules", []):
        size_meta_module = _base.PROJECT_SIZES.get(profile["project_size"], _base.PROJECT_SIZES["small"])
        module_max_count = int(module.get("max_skills", size_meta_module.get("max_module_skills", 6)))
        module_max_chars = int(module.get("max_initial_metadata_chars", max(1600, size_meta_module.get("max_initial_metadata_chars", 3600) // 2)))
        routed = routed_module_selected.get(module["path"], [])
        module_budgets[module["path"]] = {
            "max_module_skills": max(module_max_count, len(routed)),
            "max_initial_metadata_chars": max(module_max_chars, _base.estimate_initial_metadata_chars(routed)),
            "estimated_initial_metadata_chars": _base.estimate_initial_metadata_chars(routed),
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
            "estimated_initial_metadata_chars": _base.estimate_initial_metadata_chars(selected),
            "selected_count": len(selected),
            "optional_count": len(all_optional),
        },
    }


def compute_project_skills(profile: Dict[str, Any]) -> List[str]:
    return compute_skill_plan(profile)["selected"]


def compute_optional_skills(profile: Dict[str, Any]) -> List[str]:
    return compute_skill_plan(profile)["optional"]


def render_workstream_skill(ws: Dict[str, Any]) -> str:
    skill = ws["skill"]
    workflow = ws.get("workflow", []) or ["Clarify scope.", "Implement the smallest safe slice.", "Verify and record evidence."]
    quality_gates = ws.get("quality_gates", []) or ["Relevant validation passes or blockers are documented."]
    handoff = ws.get("handoff", []) or ["Changed files, commands, evidence, risks, and next steps are summarized."]
    module_paths_text = ", ".join(f"`{p}`" for p in ws.get("module_paths", [])) or "not configured"
    lines = [
        "---", f"name: {_base.yaml_quote(skill)}", f"description: {_base.yaml_quote(ws.get('objective', f'Own the {skill} workstream.'))}", "---", "",
        f"# {ws.get('name', _base.slug_title(skill))}", "", "## Scope", f"- module_paths: {module_paths_text}", f"- objective: {ws.get('objective', '')}", "", "## Workflow",
    ]
    lines.extend(f"{i}. {step}" for i, step in enumerate(workflow, start=1))
    lines += ["", "## Quality gates"]
    lines.extend(f"- {gate}" for gate in quality_gates)
    lines += ["", "## Routing discipline", "- Do not replace the root workflow skills; use this workstream as the project-specific owner for its module paths.", "- Keep generated scaffold paths aligned with `module_paths` and module-local `AGENTS.md`.", "- Do not move active policy-pack skills into optional/pruned output.", "", "## Handoff"]
    lines.extend(f"- {item}" for item in handoff)
    return "\n".join(lines).rstrip()+"\n"


def render_workstream_openai_yaml(ws: Dict[str, Any]) -> str:
    skill = ws["skill"]
    desc = ws.get("objective", f"Own the {skill} workstream.")[:160]
    return f'''interface:
  display_name: {_base.yaml_quote(ws.get('name', _base.slug_title(skill)))}
  short_description: {_base.yaml_quote(desc)}
  default_prompt: {_base.yaml_quote('$' + skill)}

policy:
  allow_implicit_invocation: true
'''


def render_skill_for_profile(skill: str, profile: Dict[str, Any]) -> str:
    ws = workstream_skill_map(profile).get(skill)
    return render_workstream_skill(ws) if ws else _base.render_skill(skill)


def render_openai_yaml_for_profile(skill: str, profile: Dict[str, Any]) -> str:
    ws = workstream_skill_map(profile).get(skill)
    return render_workstream_openai_yaml(ws) if ws else _base.render_openai_yaml(skill)


def scale_options(profile: Dict[str, Any]) -> Dict[str, Any]:
    return _base.scale_options(profile)


def render_policy_lock(profile: Dict[str, Any]) -> str:
    lock = {
        "version": VERSION,
        "project_name": profile["project_name"],
        "project_type": profile["project_type"],
        "project_size": profile["project_size"],
        "bundles": profile.get("bundles", []),
        "policy_packs": profile.get("policy_packs", []),
        "modules": [{"name": m["name"], "path": m["path"], "module_type": m["module_type"], "bundles": m.get("bundles", [])} for m in profile.get("modules", [])],
        "workstreams": [{"skill": w["skill"], "name": w.get("name"), "module_paths": w.get("module_paths", [])} for w in profile.get("workstreams", [])],
        "scaffold": {"package_manager": profile.get("package_manager"), "runtime_stack": profile.get("runtime_stack"), "generate_project_scaffold": profile.get("generate_project_scaffold", False)},
        "stack_decision": {"mode": profile.get("stack_selection_mode"), "required": bool(profile.get("stack_decision_required")), "selected_stack": profile.get("selected_stack", {}), "scaffold_generation_policy": profile.get("scaffold_generation_policy"), "reason": profile.get("stack_decision_reason", "")},
        "allowed_external_hosts": profile.get("allowed_external_hosts", []),
        "note": "Hard policies are opt-in via policy_packs, not universal defaults.",
    }
    return json.dumps(lock, indent=2, ensure_ascii=False)+"\n"


def render_manifest(profile: Dict[str, Any], skills: Sequence[str], opts: Dict[str, Any]) -> str:
    plan = compute_skill_plan(profile)
    return json.dumps({
        "version": VERSION,
        "skills": list(skills),
        "optional_skills": plan["optional"],
        "budget": plan["budget"],
        "scale_options": opts,
        "workstreams": [{"skill": w["skill"], "name": w.get("name"), "module_paths": w.get("module_paths", []), "objective": w.get("objective", "")} for w in profile.get("workstreams", [])],
        "scaffold": {"package_manager": profile.get("package_manager"), "runtime_stack": profile.get("runtime_stack"), "generate_project_scaffold": profile.get("generate_project_scaffold", False), "dev_modules": profile.get("dev_modules", [])},
        "stack_decision": {"mode": profile.get("stack_selection_mode"), "required": bool(profile.get("stack_decision_required")), "selected_stack": profile.get("selected_stack", {}), "scaffold_generation_policy": profile.get("scaffold_generation_policy"), "reason": profile.get("stack_decision_reason", "")},
        "modules": [{"name": m["name"], "path": m["path"], "skills": plan["module_selected"].get(m["path"], []), "optional_skills": plan["module_optional"].get(m["path"], []), "workstreams": [w["skill"] for w in workstreams_for_module_path(profile, m["path"])], "budget": plan["module_budget"].get(m["path"], {})} for m in profile.get("modules", [])],
    }, indent=2, ensure_ascii=False)+"\n"


def render_workstream_split_guide(profile: Dict[str, Any]) -> str:
    lines = ["# Workstream Split Guide", "", "Project-specific workstreams are first-class skills. They do not replace universal workflow or policy-pack skills; they route actual repo paths to the correct development owner.", ""]
    if not profile.get("workstreams"):
        lines.append("No workstreams configured.")
        return "\n".join(lines).rstrip()+"\n"
    for ws in profile.get("workstreams", []):
        lines += [f"## ${ws['skill']} — {ws.get('name', _base.slug_title(ws['skill']))}", f"- module_paths: {', '.join('`'+p+'`' for p in ws.get('module_paths', []))}", f"- objective: {ws.get('objective', '')}", "- quality_gates:"]
        lines.extend(f"  - {gate}" for gate in ws.get("quality_gates", []) or ["Relevant validation passes or blockers are documented."])
        lines.append("")
    return "\n".join(lines).rstrip()+"\n"


def render_module_routing_guide(profile: Dict[str, Any], available_skills: Optional[Set[str]] = None) -> str:
    lines=["# Module Routing Guide\n", "Use module-local AGENTS.md files to route Codex work by path. This guide lists generated route skills, optional/pruned skills, and project-specific workstreams.\n"]
    plan = compute_skill_plan(profile)
    for m in profile.get("modules", []):
        selected = plan["module_selected"].get(m["path"], [])
        optional = plan["module_optional"].get(m["path"], [])
        ws = [w["skill"] for w in workstreams_for_module_path(profile, m["path"])]
        if available_skills is not None:
            optional = _base.unique(optional + [s for s in selected if s not in available_skills])
            selected = [s for s in selected if s in available_skills]
        lines.append(f"## {m['name']} — `{m['path']}`\n- type: `{m['module_type']}`\n- workstreams: {', '.join('$'+s for s in ws) or 'none'}\n- generated skills: {', '.join('$'+s for s in selected) or 'none'}\n- optional/pruned: {', '.join('$'+s for s in optional) or 'none'}\n")
    return "\n".join(lines).rstrip()+"\n"


def render_module_agents(module: Dict[str, Any], profile_size: str = "small", available_skills: Optional[Set[str]] = None, profile: Optional[Dict[str, Any]] = None) -> str:
    text = _base.render_module_agents(module, profile_size, available_skills)
    if profile is None:
        return text
    ws = [w["skill"] for w in workstreams_for_module_path(profile, module["path"])]
    if not ws:
        return text
    insert = "\n## Project workstreams\n" + "\n".join(f"- `${s}`" for s in ws) + "\n"
    return text.replace("\n## Local commands\n", insert + "\n## Local commands\n")


def render_optional_skills(profile: Dict[str, Any]) -> str:
    return _base.render_optional_skills(profile)


def generate(profile: Dict[str, Any], root: Path, mode: str = "skip", also_codex_skills: bool = False) -> None:
    profile = normalize_profile(profile)
    errors = validate_profile(profile)
    if errors:
        raise ValueError("Invalid profile:\n- " + "\n- ".join(errors))
    skills = compute_project_skills(profile); opts = scale_options(profile)
    _base.write_file(root/"AGENTS.md", _base.render_agents_md(profile, skills, opts), mode)
    _base.write_file(root/"PLANS.md", _base.render_plans_md(profile), mode)
    _base.write_file(root/".codex"/"config.toml", _base.render_config(profile), mode)
    _base.write_file(root/".codex"/"policy.lock.json", render_policy_lock(profile), mode)
    _base.write_file(root/".codex"/"skillset-manifest.json", render_manifest(profile, skills, opts), mode)
    _base.write_file(root/"docs"/"skillset"/"optional-skills.md", render_optional_skills(profile), mode)
    for skill in skills:
        _base.write_file(root/".agents"/"skills"/skill/"SKILL.md", render_skill_for_profile(skill, profile), mode)
        _base.write_file(root/".agents"/"skills"/skill/"agents"/"openai.yaml", render_openai_yaml_for_profile(skill, profile), mode)
        if also_codex_skills:
            _base.write_file(root/".codex"/"skills"/skill/"SKILL.md", render_skill_for_profile(skill, profile), mode)
            _base.write_file(root/".codex"/"skills"/skill/"agents"/"openai.yaml", render_openai_yaml_for_profile(skill, profile), mode)
    _base.write_file(root/"docs"/"glossary.md", _base.render_glossary(profile), mode)
    _base.write_file(root/"docs"/"rules"/"naming-and-consistency.md", _base.render_rules(), mode)
    _base.write_file(root/"docs"/"rules"/"engineering-laws.md", _base.render_engineering_laws(), mode)
    _base.write_file(root/"docs"/"rules"/"review-checklist.md", _base.render_review_checklist(), mode)
    _base.write_file(root/"docs"/"architecture"/"boundaries.md", "# Architecture Boundaries\n\n"+"\n".join(f"- {b}" for b in profile.get("boundaries", [])), mode)
    _base.write_file(root/"docs"/"skillset"/"scale-selection-guide.md", _base.render_scale_selection_guide(), mode)
    _base.write_file(root/"docs"/"skillset"/"module-routing-guide.md", render_module_routing_guide(profile, set(skills)), mode)
    if profile.get("workstreams"):
        _base.write_file(root/"docs"/"skillset"/"workstream-split-guide.md", render_workstream_split_guide(profile), mode)
    if stack_decision_required(profile) or profile.get("selected_stack"):
        _base.write_file(root/"docs"/"decisions"/"stack-decision.md", render_stack_decision_doc(profile), mode)
    _base.write_file(root/"docs"/"skillset"/"project-document-analysis-guide.md", _base.render_project_analysis_guide(), mode)
    _base.write_file(root/"docs"/"skillset"/"profile-schema-reference.md", _base.render_profile_schema_reference(), mode)
    _base.write_file(root/"docs"/"skillset"/"gpts-operator-guide.md", _base.render_gpts_operator_guide(), mode)
    _base.write_file(root/"docs"/"skillset"/"project-source-integration-guide.md", _base.render_source_integration_guide(), mode)
    if opts.get("include_commands"):
        for name, content in _base.COMMANDS.items():
            _base.write_file(root/"commands"/name, f"# /{name[:-3]}\n\n{content}", mode)
    if opts.get("include_references"):
        for name, content in _base.REFERENCES.items():
            _base.write_file(root/"references"/name, content, mode)
    if opts.get("include_personas"):
        for name, content in _base.PERSONAS.items():
            _base.write_file(root/"agents"/name, content, mode)
    if opts.get("include_governance"):
        _base.write_file(root/"docs"/"governance"/"change-control.md", "# Change Control\n\n- Major behavior, contract, data, or release changes need a written plan and evidence pack.", mode)
    for module in profile.get("modules", []):
        _base.write_file(root/module["path"]/"AGENTS.md", render_module_agents(module, profile["project_size"], set(skills), profile), mode)


def validate_generated(root: Path) -> List[str]:
    errors = _base.validate_generated(root)
    manifest = root/".codex"/"skillset-manifest.json"
    if not manifest.exists():
        return errors
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        return errors
    if data.get("workstreams") and not (root/"docs"/"skillset"/"workstream-split-guide.md").exists():
        errors.append("Missing workstream split guide for configured workstreams")
    stack_decision = data.get("stack_decision", {}) if isinstance(data.get("stack_decision", {}), dict) else {}
    if stack_decision.get("required") and not (root/"docs"/"decisions"/"stack-decision.md").exists():
        errors.append("Missing docs/decisions/stack-decision.md for required stack decision gate")
    declared = set(data.get("skills", []))
    for ws in data.get("workstreams", []):
        skill = ws.get("skill", "")
        if skill not in declared:
            errors.append(f"Workstream skill missing from manifest skills: {skill}")
        for wpath in ws.get("module_paths", []):
            norm = normalized_repo_path(wpath)
            if not is_safe_workstream_path(norm):
                errors.append(f"Unsafe workstream path in manifest: {wpath}")
            elif norm != "." and not (root/norm/"AGENTS.md").exists():
                errors.append(f"Workstream path lacks module AGENTS.md: {wpath}")
    return errors


def recommendation(profile: Dict[str, Any], path: Optional[str]=None) -> Dict[str, Any]:
    profile = normalize_profile(profile); opts = scale_options(profile); plan = compute_skill_plan(profile)
    out: Dict[str, Any] = {"project_type": profile["project_type"], "project_size": profile["project_size"], "scale_options": opts, "policy_packs": profile.get("policy_packs", []), "budget": plan["budget"]}
    if path:
        module = _base.match_module_by_path(profile, path)
        if module:
            out.update({"matched_module": module["name"], "module_path": module["path"], "module_type": module["module_type"], "skills": plan["module_selected"].get(module["path"], []), "optional_skills": plan["module_optional"].get(module["path"], []), "workstreams": [w["skill"] for w in workstreams_for_module_path(profile, module["path"])], "commands": module.get("commands", {})})
        else:
            out.update({"matched_module": None, "skills": plan["selected"], "optional_skills": plan["optional"], "commands": profile.get("commands", {})})
    else:
        out.update({"skills": plan["selected"], "optional_skills": plan["optional"], "modules": [{"name": m["name"], "path": m["path"], "module_type": m["module_type"], "skills": plan["module_selected"].get(m["path"], []), "optional_skills": plan["module_optional"].get(m["path"], []), "workstreams": [w["skill"] for w in workstreams_for_module_path(profile, m["path"])]} for m in profile.get("modules", [])]})
    return out


def json_dump(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)+"\n"


def root_package_json(profile: Dict[str, Any]) -> Dict[str, Any]:
    pm = profile.get("package_manager", "pnpm")
    scripts = {
        "build": "pnpm -r build" if pm == "pnpm" else "npm run build --workspaces",
        "test": "pnpm -r test" if pm == "pnpm" else "npm run test --workspaces --if-present",
        "typecheck": "pnpm -r typecheck" if pm == "pnpm" else "npm run typecheck --workspaces --if-present",
        "validate:scaffold": "python -S codex_skillset_generator.py validate-scaffold --root .",
    }
    scripts["dev:api"] = "cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" if profile.get("runtime_stack", {}).get("api") == "fastapi-python" else ("pnpm --filter api dev" if pm == "pnpm" else "npm run dev --workspace apps/api")
    scripts["dev:web"] = "pnpm --filter web dev" if pm == "pnpm" else "npm run dev --workspace apps/web"
    scripts["build:extension"] = "pnpm --filter extension build" if pm == "pnpm" else "npm run build --workspace apps/extension"
    pm_version = PINNED_PACKAGE_MANAGERS.get(pm, "0.0.0")
    return {"name": profile.get("project_name", "project").lower().replace(" ", "-"), "private": True, "version": "0.1.0", "packageManager": f"{pm}@{pm_version}", "workspaces": ["apps/*", "packages/*", "tools/*"], "scripts": scripts}


def write_ts_package(root: Path, rel: str, name: str, mode: str, *, app: bool = False) -> None:
    pkg = {"name": name, "private": True, "version": "0.1.0", "type": "module", "scripts": {"build": "tsc -p tsconfig.json", "test": "echo \"No tests configured yet\"", "typecheck": "tsc -p tsconfig.json --noEmit"}, "dependencies": {}, "devDependencies": dict(PINNED_TS_DEV_DEPENDENCIES)}
    if app:
        pkg["scripts"]["dev"] = "vite"
        pkg["scripts"]["build"] = "vite build"
        pkg["dependencies"] = dict(PINNED_WEB_DEPENDENCIES)
        pkg["devDependencies"] = dict(PINNED_WEB_DEV_DEPENDENCIES)
    _base.write_file(root/rel/"package.json", json_dump(pkg), mode)
    _base.write_file(root/rel/"tsconfig.json", '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": {"outDir": "dist", "rootDir": "src"},\n  "include": ["src"]\n}\n', mode)
    _base.write_file(root/rel/"src"/"index.ts", "export const packageReady = true;\n", mode)


def write_web_app(root: Path, mode: str) -> None:
    write_ts_package(root, "apps/web", "web", mode, app=True)
    _base.write_file(root/"apps/web"/"index.html", '<!doctype html>\n<html><head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>Web</title></head><body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>\n', mode)
    _base.write_file(root/"apps/web"/"vite.config.ts", 'import { defineConfig } from "vite";\nimport react from "@vitejs/plugin-react";\n\nexport default defineConfig({ plugins: [react()] });\n', mode)
    _base.write_file(root/"apps/web"/"src"/"main.tsx", 'import React from "react";\nimport { createRoot } from "react-dom/client";\nimport { App } from "./App";\n\ncreateRoot(document.getElementById("root")!).render(<React.StrictMode><App /></React.StrictMode>);\n', mode)
    _base.write_file(root/"apps/web"/"src"/"App.tsx", 'export function App() {\n  return <main><h1>Project Web App</h1><p>Ready for Codex-guided development.</p></main>;\n}\n', mode)


def write_fastapi_app(root: Path, mode: str) -> None:
    _base.write_file(root/"apps/api"/"pyproject.toml", '[project]\nname = "api"\nversion = "0.1.0"\ndependencies = ["fastapi", "uvicorn"]\n\n[project.optional-dependencies]\ndev = ["pytest"]\n', mode)
    _base.write_file(root/"apps/api"/"app"/"__init__.py", "", mode)
    _base.write_file(root/"apps/api"/"app"/"main.py", 'from fastapi import FastAPI\n\napp = FastAPI(title="Project API")\n\n@app.get("/health")\ndef health() -> dict[str, str]:\n    return {"status": "ok"}\n', mode)
    _base.write_file(root/"apps/api"/"tests"/"test_health.py", 'from app.main import health\n\ndef test_health() -> None:\n    assert health()["status"] == "ok"\n', mode)


def write_fastify_app(root: Path, mode: str) -> None:
    pkg = {"name": "api", "private": True, "version": "0.1.0", "type": "module", "scripts": {"dev": "tsx src/server.ts", "build": "tsc -p tsconfig.json", "test": "echo \"No tests configured yet\"", "typecheck": "tsc -p tsconfig.json --noEmit"}, "dependencies": dict(PINNED_FASTIFY_DEPENDENCIES), "devDependencies": dict(PINNED_FASTIFY_DEV_DEPENDENCIES)}
    _base.write_file(root/"apps/api"/"package.json", json_dump(pkg), mode)
    _base.write_file(root/"apps/api"/"tsconfig.json", '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": {"outDir": "dist", "rootDir": "src"},\n  "include": ["src"]\n}\n', mode)
    _base.write_file(root/"apps/api"/"src"/"server.ts", 'import Fastify from "fastify";\n\nconst app = Fastify();\napp.get("/health", async () => ({ status: "ok" }));\n\napp.listen({ port: Number(process.env.PORT ?? 8000), host: "0.0.0.0" });\n', mode)


def write_extension(root: Path, mode: str) -> None:
    pkg = {"name": "extension", "private": True, "version": "0.1.0", "type": "module", "scripts": {"build": "tsc -p tsconfig.json", "test": "echo \"No tests configured yet\"", "typecheck": "tsc -p tsconfig.json --noEmit"}, "devDependencies": dict(PINNED_TS_DEV_DEPENDENCIES)}
    _base.write_file(root/"apps/extension"/"package.json", json_dump(pkg), mode)
    _base.write_file(root/"apps/extension"/"manifest.json", json_dump({"manifest_version": 3, "name": "Project Extension", "version": "0.1.0", "permissions": ["storage"], "background": {"service_worker": "dist/background.js", "type": "module"}, "action": {"default_title": "Project Extension"}}), mode)
    _base.write_file(root/"apps/extension"/"tsconfig.json", '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": {"outDir": "dist", "rootDir": "src"},\n  "include": ["src"]\n}\n', mode)
    _base.write_file(root/"apps/extension"/"src"/"background.ts", 'chrome.runtime.onInstalled.addListener(() => {\n  console.log("Extension installed");\n});\n', mode)
    _base.write_file(root/"apps/extension"/"src"/"content.ts", 'export {};\n', mode)


def render_scaffold_manifest(profile: Dict[str, Any]) -> str:
    return json_dump({"version": VERSION, "package_manager": profile.get("package_manager"), "runtime_stack": profile.get("runtime_stack"), "dev_modules": profile.get("dev_modules", []), "workstreams": [{"skill": w["skill"], "module_paths": w.get("module_paths", [])} for w in profile.get("workstreams", [])], "module_paths": [m["path"] for m in profile.get("modules", [])], "stack_decision": {"mode": profile.get("stack_selection_mode"), "required": bool(profile.get("stack_decision_required")), "selected_stack": profile.get("selected_stack", {}), "scaffold_generation_policy": profile.get("scaffold_generation_policy"), "reason": profile.get("stack_decision_reason", "")}, "clean_room_blocked_patterns": ["background.js", "preload.js", "*.map", "_next/static/chunks"]})


def scaffold(profile: Dict[str, Any], root: Path, mode: str = "skip") -> None:
    profile = normalize_profile(profile)
    errors = validate_profile(profile)
    if errors:
        raise ValueError("Invalid profile:\n- " + "\n- ".join(errors))
    if stack_decision_required(profile) and not profile.get("selected_stack"):
        raise ValueError("scaffold is blocked until selected_stack is present")
    if stack_decision_required(profile) and not str(profile.get("stack_decision_reason", "")).strip():
        raise ValueError("scaffold is blocked until stack_decision_reason is present")
    pm = profile.get("package_manager", "pnpm")
    _base.write_file(root/"package.json", json_dump(root_package_json(profile)), mode)
    if pm == "pnpm":
        _base.write_file(root/"pnpm-workspace.yaml", "packages:\n  - 'apps/*'\n  - 'packages/*'\n  - 'tools/*'\n", mode)
    _base.write_file(root/"tsconfig.base.json", '{\n  "compilerOptions": {"target": "ES2022", "module": "ESNext", "moduleResolution": "Bundler", "strict": true, "skipLibCheck": true}\n}\n', mode)
    _base.write_file(root/".nvmrc", "20\n", mode)
    _base.write_file(root/".gitignore", "node_modules/\ndist/\nbuild/\n.env\n.env.*\n!.env.example\n__pycache__/\n.pytest_cache/\n*.pyc\n", mode)
    _base.write_file(root/".env.example", "# Copy to .env and fill locally. Do not commit real secrets.\nAPI_BASE_URL=http://localhost:8000\nDATABASE_URL=<local-database-url>\nSESSION_SECRET=<change-me-locally>\n", mode)
    _base.write_file(root/".codex"/"scaffold-manifest.json", render_scaffold_manifest(profile), mode)
    write_web_app(root, mode)
    if profile.get("runtime_stack", {}).get("api") == "fastapi-python":
        write_fastapi_app(root, mode)
    else:
        write_fastify_app(root, mode)
    write_extension(root, mode)
    for rel, name in [("packages/contracts", "@project/contracts"), ("packages/core", "@project/core"), ("packages/collectors", "@project/collectors"), ("tools/reference-analysis", "@project/reference-analysis")]:
        write_ts_package(root, rel, name, mode)
    _base.write_file(root/"tools"/"checks"/"clean-room-audit-notes.md", "# Clean-room Audit Notes\n\n- Do not copy restricted source text, comments, identifiers, built chunks, source maps, or secret-bearing files.\n", mode)


def load_scaffold_manifest(root: Path) -> Dict[str, Any]:
    path = root/".codex"/"scaffold-manifest.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def env_example_has_secret_values(path: Path) -> List[str]:
    errors: List[str] = []
    if not path.exists():
        return errors
    for idx, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if SECRETISH_KEY_RE.search(key) and not SAFE_PLACEHOLDER_RE.match(value.strip()):
            errors.append(f".env.example line {idx} has non-placeholder secret-like value for {key}")
    return errors


def validate_dependency_spec(spec: Any) -> bool:
    if not isinstance(spec, str): return False
    value = spec.strip()
    if not value or "latest" in value.lower(): return False
    return bool(SEMVERISH_SPEC_RE.fullmatch(value))


def validate_package_json_specs(root: Path) -> List[str]:
    errors: List[str] = []
    for path in root.rglob("package.json"):
        rel = path.relative_to(root).as_posix()
        if any(part in {"node_modules", "dist", "build"} for part in path.relative_to(root).parts): continue
        try: data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"Bad package.json JSON: {rel}: {exc}"); continue
        package_manager = data.get("packageManager")
        if package_manager is not None:
            if not isinstance(package_manager, str) or "latest" in package_manager.lower() or not re.match(r"^(pnpm|npm|yarn)@\d+\.\d+\.\d+$", package_manager): errors.append(f"Invalid or ambiguous packageManager in {rel}: {package_manager}")
        for section in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
            deps = data.get(section, {})
            if deps is None: continue
            if not isinstance(deps, dict): errors.append(f"{section} must be an object in {rel}"); continue
            for name, spec in deps.items():
                if not validate_dependency_spec(spec): errors.append(f"Invalid dependency spec in {rel}: {section}.{name}={spec!r}")
    return errors


def validate_scaffold(root: Path) -> List[str]:
    errors: List[str] = []
    manifest = load_scaffold_manifest(root)
    required = [root/"package.json", root/"tsconfig.base.json", root/".env.example", root/".gitignore", root/".codex"/"scaffold-manifest.json"]
    for path in required:
        if not path.exists():
            errors.append(f"Missing scaffold file: {path}")
    if manifest.get("package_manager") == "pnpm" and not (root/"pnpm-workspace.yaml").exists():
        errors.append("Missing pnpm-workspace.yaml for pnpm scaffold")
    for rel in ["apps/web/package.json", "apps/web/index.html", "apps/web/src/main.tsx", "apps/extension/package.json", "apps/extension/manifest.json", "apps/extension/src/background.ts", "packages/contracts/package.json", "packages/contracts/src/index.ts", "packages/core/package.json", "packages/core/src/index.ts", "packages/collectors/package.json", "packages/collectors/src/index.ts", "tools/reference-analysis/package.json", "tools/reference-analysis/src/index.ts"]:
        if not (root/rel).exists():
            errors.append(f"Missing scaffold entrypoint: {rel}")
    api_runtime = manifest.get("runtime_stack", {}).get("api")
    if api_runtime == "fastapi-python":
        for rel in ["apps/api/pyproject.toml", "apps/api/app/main.py"]:
            if not (root/rel).exists():
                errors.append(f"Missing FastAPI scaffold entrypoint: {rel}")
    elif api_runtime == "fastify-typescript":
        for rel in ["apps/api/package.json", "apps/api/src/server.ts"]:
            if not (root/rel).exists():
                errors.append(f"Missing Fastify scaffold entrypoint: {rel}")
    else:
        errors.append(f"Unknown or missing scaffold runtime_stack.api: {api_runtime}")
    for wpath in manifest.get("module_paths", []):
        if not _base.is_safe_relative_path(wpath):
            errors.append(f"Unsafe module path in scaffold manifest: {wpath}")
            continue
        if not (root/wpath).exists():
            errors.append(f"Configured module path does not exist in scaffold: {wpath}")
        if not (root/wpath/"AGENTS.md").exists():
            errors.append(f"Configured module path lacks AGENTS.md; run generate before validate-scaffold: {wpath}")
    for ws in manifest.get("workstreams", []):
        for wpath in ws.get("module_paths", []):
            norm = normalized_repo_path(wpath)
            if not is_safe_workstream_path(norm): errors.append(f"Unsafe workstream path in scaffold manifest: {wpath}")
            elif norm != "." and norm not in manifest.get("module_paths", []): errors.append(f"Workstream path does not match module_paths: {ws.get('skill')} -> {wpath}")
    stack_decision = manifest.get("stack_decision", {}) if isinstance(manifest.get("stack_decision", {}), dict) else {}
    if stack_decision.get("required"):
        if not stack_decision.get("selected_stack"): errors.append("Scaffold manifest stack_decision requires selected_stack")
        if not stack_decision.get("reason"): errors.append("Scaffold manifest stack_decision requires reason")
        if not (root/"docs"/"decisions"/"stack-decision.md").exists(): errors.append("Missing docs/decisions/stack-decision.md for scaffold stack decision gate")
        selected = stack_decision.get("selected_stack", {}) if isinstance(stack_decision.get("selected_stack", {}), dict) else {}
        runtime = manifest.get("runtime_stack", {}) if isinstance(manifest.get("runtime_stack", {}), dict) else {}
        for key in ["frontend", "api", "extension"]:
            if selected.get(key) != runtime.get(key): errors.append(f"selected_stack.{key} does not match runtime_stack.{key}")
        if selected.get("package_manager") and selected.get("package_manager") != manifest.get("package_manager"): errors.append("selected_stack.package_manager does not match package_manager")
    errors.extend(env_example_has_secret_values(root/".env.example"))
    errors.extend(validate_package_json_specs(root))
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if CLEAN_ROOM_BLOCKED_RE.search(rel):
            errors.append(f"Clean-room blocked generated/source artifact present: {rel}")
    return errors


def read_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_example_profiles(base: Path) -> None:
    out = base/"examples"/"profiles"; out.mkdir(parents=True, exist_ok=True)
    for preset in PRESETS:
        (out/f"{preset}.json").write_text(json.dumps(preset_profile(preset), indent=2, ensure_ascii=False)+"\n", encoding="utf-8")


def write_generated_examples(base: Path) -> None:
    out = base/"examples"/"generated"
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    for preset in PRESETS:
        profile = preset_profile(preset)
        target = out/preset
        generate(profile, target, mode="overwrite")
        if profile.get("generate_project_scaffold"): scaffold(profile, target, mode="overwrite")


def cmd_self_check(args: argparse.Namespace) -> int:
    root = Path(args.root)
    errors: List[str] = []
    for preset in PRESETS:
        profile = preset_profile(preset)
        errors.extend(f"profile/{preset}: {e}" for e in validate_profile(profile))
        plan = compute_skill_plan(profile)
        if set(plan["selected"]) & set(plan["optional"]):
            errors.append(f"plan/{preset}: selected and optional skills overlap")
        if args.generated_examples:
            generated = root/"examples"/"generated"/preset
            if generated.exists():
                errors.extend(f"generated/{preset}: {e}" for e in validate_generated(generated))
                if profile.get("generate_project_scaffold"): errors.extend(f"generated-scaffold/{preset}: {e}" for e in validate_scaffold(generated))
            else: errors.append(f"generated/{preset}: missing example output at {generated}")
        if args.temp_generate:
            with tempfile.TemporaryDirectory(prefix=f"codex_skillset_{preset}_") as td:
                out = Path(td)/"out"
                generate(profile, out, mode="overwrite")
                if profile.get("generate_project_scaffold"): scaffold(profile, out, mode="overwrite")
                errors.extend(f"temp-generated/{preset}: {e}" for e in validate_generated(out))
                if profile.get("generate_project_scaffold"): errors.extend(f"temp-scaffold/{preset}: {e}" for e in validate_scaffold(out))
    if errors:
        print("FAIL")
        for e in errors: print(f"- {e}")
        return 1
    checked = ["profiles"]
    if args.generated_examples: checked.append("bundled generated examples")
    if args.temp_generate: checked.append("fresh temp generation")
    print("PASS / " + ", ".join(checked) + f" / {len(PRESETS)} presets")
    return 0


def cmd_list_presets(_: argparse.Namespace) -> int:
    for name, meta in PRESETS.items(): print(f"{name}\tproject_type={meta['project_type']}\tsize={meta['project_size']}\tbundles={','.join(meta.get('bundles', []))}")
    return 0


def cmd_list_sizes(_: argparse.Namespace) -> int:
    return _base.cmd_list_sizes(_)


def cmd_list_bundles(_: argparse.Namespace) -> int:
    return _base.cmd_list_bundles(_)


def cmd_init(args: argparse.Namespace) -> int:
    Path(args.output).write_text(json.dumps(preset_profile(args.preset, args.size), indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(f"Wrote {args.output}"); return 0


def cmd_recommend(args: argparse.Namespace) -> int:
    print(json.dumps(recommendation(read_json(args.config), args.path), indent=2, ensure_ascii=False)); return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_profile(read_json(args.config))
    if errors:
        print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0


def generate_dev_kit(profile: Dict[str, Any], root: Path, mode: str = "skip", also_codex_skills: bool = False) -> List[str]:
    profile = normalize_profile(profile)
    generate(profile, root, mode, also_codex_skills=also_codex_skills)
    if profile.get("generate_project_scaffold"): scaffold(profile, root, mode)
    errors: List[str] = []
    errors.extend(validate_generated(root))
    if profile.get("generate_project_scaffold"): errors.extend(validate_scaffold(root))
    return errors


def cmd_generate(args: argparse.Namespace) -> int:
    generate(normalize_profile(read_json(args.config)), Path(args.root), args.mode, also_codex_skills=args.also_write_codex_skills)
    print(f"Generated skillset at {args.root}"); return 0


def cmd_scaffold(args: argparse.Namespace) -> int:
    scaffold(normalize_profile(read_json(args.config)), Path(args.root), args.mode)
    print(f"Generated scaffold at {args.root}"); return 0


def cmd_generate_dev_kit(args: argparse.Namespace) -> int:
    errors = generate_dev_kit(normalize_profile(read_json(args.config)), Path(args.root), args.mode, also_codex_skills=args.also_write_codex_skills)
    if errors:
        print("FAIL")
        for e in errors: print(f"- {e}")
        return 1
    print(f"Generated and validated dev kit at {args.root}")
    print("PASS")
    return 0


def cmd_validate_generated(args: argparse.Namespace) -> int:
    errors = validate_generated(Path(args.root))
    if errors:
        print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0


def cmd_validate_scaffold(args: argparse.Namespace) -> int:
    errors = validate_scaffold(Path(args.root))
    if errors:
        print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0


def cmd_write_examples(args: argparse.Namespace) -> int:
    root = Path(args.root)
    write_example_profiles(root)
    if args.generated:
        write_generated_examples(root); print(f"Wrote example profiles and generated outputs under {args.root}/examples")
    else:
        print(f"Wrote example profiles under {args.root}/examples/profiles")
    return 0



# ---- v4.9.5-dev-ops-r1 overrides: planning, command queue, self-validating scaffold ----

def render_common_skill_workflow() -> str:
    return """# Common Skill Workflow

This shared workflow keeps individual SKILL.md files compact.

1. Define scope, non-goals, target files, and relevant contracts.
2. Read the closest `AGENTS.md`, manifest, and planning docs before editing.
3. Plan the smallest coherent vertical slice.
4. Build incrementally without deleting existing behavior unless explicitly approved.
5. Verify with the smallest sufficient command set.
6. Record changed files, commands, evidence, risks, blockers, and next steps.
"""


def render_compact_base_skill(skill: str) -> str:
    if skill in getattr(_base, "SPECIAL_APPENDIX", {}):
        return _base.render_skill(skill)
    desc = _base.SKILL_DESCRIPTIONS.get(skill, f"Use this skill for project-specific workflow `{skill}`.")
    return f"""---
name: {_base.yaml_quote(skill)}
description: {_base.yaml_quote(desc)}
---

# {_base.slug_title(skill)}

## Use when
- The task matches this skill's description.
- The change may affect durable behavior, tests, docs, public contracts, operations, or user experience.

## Workflow
Use `{COMMON_SKILL_WORKFLOW_DOC}` for the common define/plan/build/verify/review/handoff loop. Keep this skill focused on: {desc}

## Evidence required
- Files read and changed.
- Commands run and outcomes.
- Test or validation coverage.
- Known risks and explicit exclusions.

## Handoff
- Summarize changes, evidence, risks, and next steps.
"""


def render_skill_for_profile(skill: str, profile: Dict[str, Any]) -> str:
    ws = workstream_skill_map(profile).get(skill)
    return render_workstream_skill(ws) if ws else render_compact_base_skill(skill)


def render_root_agents_md(profile: Dict[str, Any], skills: Sequence[str]) -> str:
    plan = compute_skill_plan(profile)
    lines = [f"# AGENTS.md — {profile['project_name']}", "", "## Purpose", "Use this repository guidance with local `.agents/skills`, planning docs, module routing, and evidence gates.", "", "## Development flow", "1. Read `docs/product/PRD.md` and `docs/planning/WBS.md` when present.", "2. Follow `docs/planning/codex-command-queue.md` by slice.", "3. Use module-local `AGENTS.md` before editing a module path.", "4. Validate generated guidance, scaffold, planning docs, and dev-flow ordering.", "", "## Module routing"]
    for m in profile.get("modules", []):
        ws = [w["skill"] for w in workstreams_for_module_path(profile, m["path"])]
        selected = plan["module_selected"].get(m["path"], [])
        optional = plan["module_optional"].get(m["path"], [])
        lines.append(f"- `{m['path']}` → `{m['module_type']}`")
        lines.append(f"  - workstreams: {', '.join('$'+s for s in ws) or 'none'}")
        lines.append(f"  - generated skills: {', '.join('$'+s for s in selected) or 'none'}")
        if optional: lines.append(f"  - optional/pruned: {', '.join('$'+s for s in optional)}")
    lines += ["", "## Planning docs", "- `docs/product/PRD.md`", "- `docs/planning/WBS.md`", "- `docs/planning/codex-command-queue.md`", "- `docs/planning/phase-gates.md`", "", "## Available project skills"]
    lines += [f"- `${s}`" for s in skills]
    lines += ["", "## Done definition", "Work is not done until changed files, validation evidence, risks, and next steps are summarized."]
    return "\n".join(lines).rstrip()+"\n"


def wbs_items(profile: Dict[str, Any]) -> List[Dict[str, Any]]:
    clean = "clean-room" in profile.get("policy_packs", [])
    items: List[Dict[str, Any]] = []
    def add(phase: str, title: str, workstream: str, module_path: str, files: List[str], validation: List[str], skills: Optional[List[str]] = None) -> None:
        idx=len(items)
        items.append({"id": f"WBS-{idx:02d}", "order": idx, "phase": phase, "title": title, "workstream": workstream, "module_path": module_path, "suggested_skills": skills or [workstream], "target_files": files, "validation_commands": validation, "depends_on": [] if idx == 0 else [items[-1]["id"]], "rollback": "Revert this slice and restore prior generated files/backups if validation fails.", "evidence": "Record changed files, commands, PASS/FAIL output, blockers, and remaining risks.", "status": "todo"})
    add("intake", "Confirm scope, secret boundary, and clean-room constraints", "project-development-bootstrap", ".", ["AGENTS.md", "docs/architecture/boundaries.md"], ["python -S tools/codex/codex_skillset_generator.py validate-generated --root ."])
    add("stack-decision", "Review and approve stack decision", "project-development-bootstrap", ".", ["docs/decisions/stack-decision.md"], ["python -S tools/codex/codex_skillset_generator.py validate-planning --root ."])
    add("bootstrap", "Generate and validate repository scaffold", "project-development-bootstrap", ".", ["package.json", "pnpm-workspace.yaml", ".codex/scaffold-manifest.json"], ["python -S tools/codex/codex_skillset_generator.py validate-scaffold --root ."])
    if clean:
        add("reference-analysis", "Write clean-room reference role report before implementation", "project-reference-mapper", "tools/reference-analysis", ["tools/reference-analysis/src/index.ts", "docs/reference/reference-role-report.md"], ["pnpm cleanroom:audit"], ["project-reference-mapper", "clean-room-reference-analysis", "reference-role-report", "source-copy-audit"])
    add("contracts", "Define shared DTO/schema contracts", "project-contracts", "packages/contracts", ["packages/contracts/src/index.ts", "docs/contracts/api-contracts.md"], ["pnpm --filter @project/contracts typecheck"])
    add("backend-api", "Implement API shell, health route, and error envelope", "project-backend-api", "apps/api", ["apps/api/app/main.py", "apps/api/tests/test_health.py"], ["cd apps/api && pytest"], ["project-backend-api", "api-contract-change"])
    add("frontend-shell", "Implement web route shell and complete UI states", "project-frontend-design", "apps/web", ["apps/web/src/App.tsx"], ["pnpm --filter web build"], ["project-frontend-design", "frontend-product-ui"])
    add("extension-bridge", "Implement extension manifest and message boundary", "project-extension-bridge", "apps/extension", ["apps/extension/manifest.json", "apps/extension/src/background.ts"], ["pnpm --filter extension build"], ["project-extension-bridge", "privacy-boundary-review"])
    add("collectors", "Define collector contract and raw/normalized split", "project-market-collectors", "packages/collectors", ["packages/collectors/src/index.ts"], ["pnpm --filter @project/collectors typecheck"], ["project-market-collectors", "crawler-contract-review"])
    add("core-pipeline", "Implement deterministic core pipeline skeleton", "project-core-pipeline", "packages/core", ["packages/core/src/index.ts"], ["pnpm --filter @project/core typecheck"], ["project-core-pipeline"])
    add("integration", "Connect contracts, API, web, extension, collectors, and core with smoke evidence", "project-development-bootstrap", ".", ["docs/planning/phase-gates.md", "docs/planning/codex-command-queue.md"], ["pnpm validate:all"], ["planning-and-task-breakdown", "evidence-pack"])
    add("handoff", "Prepare evidence pack and next-session handoff", "evidence-pack", ".", ["PLANS.md", "docs/planning/codex-command-queue.md"], ["python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root ."], ["evidence-pack"])
    return items


def render_prd(profile: Dict[str, Any]) -> str:
    lines=[f"# PRD — {profile['project_name']}", "", "## Product goal", f"Build a `{profile['project_type']}` repository that Codex can develop through explicit planning, workstream routing, scaffold validation, and evidence gates.", "", "## Non-goals", "- Do not store secrets in generated files.", "- Do not copy restricted reference source text/assets verbatim.", "- Do not treat scaffold placeholders as production implementation.", "", "## Core flows", "1. Select stack decision.", "2. Generate dev kit.", "3. Follow WBS and command queue.", "4. Validate guidance, scaffold, planning, and dev-flow.", "", "## Module responsibilities"]
    for m in profile.get("modules", []):
        ws=[w["skill"] for w in workstreams_for_module_path(profile,m["path"])]
        lines.append(f"- `{m['path']}`: `{m['module_type']}`; workstreams: {', '.join('$'+s for s in ws) or 'none'}")
    lines += ["", "## Acceptance criteria"]
    for item in wbs_items(profile): lines.append(f"- {item['id']} {item['title']}: `{'; '.join(item['validation_commands'])}`")
    return "\n".join(lines).rstrip()+"\n"


def render_requirements(profile: Dict[str, Any]) -> str:
    lines=["# Requirements", "", "## Functional requirements"]
    for item in wbs_items(profile): lines.append(f"- `{item['id']}`: {item['title']} under `{item['module_path']}`.")
    lines += ["", "## Security requirements", "- Secrets remain outside profiles, AGENTS.md, SKILL.md, commands, PRD, WBS, and generated source.", "- `.env.example` must contain placeholders only."]
    return "\n".join(lines).rstrip()+"\n"


def render_wbs(profile: Dict[str, Any]) -> str:
    lines=["# WBS", "", "| ID | Phase | Workstream | Module path | Task | Validation | Depends on |", "|---|---|---|---|---|---|---|"]
    for item in wbs_items(profile): lines.append(f"| {item['id']} | {item['phase']} | `${item['workstream']}` | `{item['module_path']}` | {item['title']} | `{'; '.join(item['validation_commands'])}` | {', '.join(item['depends_on']) or '-'} |")
    return "\n".join(lines).rstrip()+"\n"


def render_wbs_manifest(profile: Dict[str, Any]) -> str:
    return json.dumps({"version": VERSION, "items": wbs_items(profile)}, indent=2, ensure_ascii=False)+"\n"


def render_implementation_sequence(profile: Dict[str, Any]) -> str:
    return "# Implementation Sequence\n\n" + "\n".join(f"## {i['id']} — {i['title']}\n- phase: `{i['phase']}`\n- workstream: `${i['workstream']}`\n- module_path: `{i['module_path']}`\n- validation: {', '.join('`'+v+'`' for v in i['validation_commands'])}\n" for i in wbs_items(profile))


def render_phase_gates(profile: Dict[str, Any]) -> str:
    lines=["# Phase Gates", "", "| Phase | PASS condition | FAIL / blocker |", "|---|---|---|"]
    for item in wbs_items(profile): lines.append(f"| {item['phase']} | `{'; '.join(item['validation_commands'])}` passes or blocker is documented | Missing evidence, path mismatch, secret exposure, or unapproved behavior deletion |")
    return "\n".join(lines).rstrip()+"\n"


def command_for_item(item: Dict[str, Any]) -> str:
    skills=" ".join(f"${s}" for s in item.get("suggested_skills", []))
    files="\n".join(f"- `{p}`" for p in item.get("target_files", []))
    validations="\n".join(f"- `{v}`" for v in item.get("validation_commands", []))
    return f"""### {item['id']} — {item['title']}

```text
Read AGENTS.md first.
Use {skills}.

Target workstream: {item['workstream']}
Target module path: {item['module_path']}

Target files:
{files}

Allowed changes:
- Implement only this slice and directly required support files.
- Update tests, docs, contracts, and evidence for this slice.

Forbidden changes:
- Do not commit secrets or real credentials.
- Do not delete existing behavior without role trace and approval.
- Do not copy restricted reference source text/assets verbatim.

Validation commands:
{validations}

Expected evidence:
- Changed files
- Commands run and PASS/FAIL results
- Remaining risks or blockers
- Rollback note: {item['rollback']}
```
"""


def render_command_queue(profile: Dict[str, Any]) -> str:
    return "# Codex Command Queue\n\n" + "\n".join(command_for_item(i) for i in wbs_items(profile))


def render_command_queue_manifest(profile: Dict[str, Any]) -> str:
    return json.dumps({"version": VERSION, "commands": [{"id": i["id"], "workstream": i["workstream"], "module_path": i["module_path"], "suggested_skills": i["suggested_skills"], "validation_commands": i["validation_commands"]} for i in wbs_items(profile)]}, indent=2, ensure_ascii=False)+"\n"


def write_planning_docs(profile: Dict[str, Any], root: Path, mode: str) -> None:
    _base.write_file(root/"docs"/"product"/"PRD.md", render_prd(profile), mode)
    _base.write_file(root/"docs"/"product"/"requirements.md", render_requirements(profile), mode)
    _base.write_file(root/"docs"/"planning"/"WBS.md", render_wbs(profile), mode)
    _base.write_file(root/"docs"/"planning"/"wbs-manifest.json", render_wbs_manifest(profile), mode)
    _base.write_file(root/"docs"/"planning"/"implementation-sequence.md", render_implementation_sequence(profile), mode)
    _base.write_file(root/"docs"/"planning"/"phase-gates.md", render_phase_gates(profile), mode)
    _base.write_file(root/"docs"/"planning"/"ACCEPTANCE_CRITERIA.md", render_wbs(profile), mode)
    _base.write_file(root/"docs"/"planning"/"codex-command-queue.md", render_command_queue(profile), mode)
    _base.write_file(root/"docs"/"planning"/"codex-command-queue.json", render_command_queue_manifest(profile), mode)
    _base.write_file(root/"docs"/"contracts"/"api-contracts.md", "# API Contracts\n\nDefine request, response, error envelope, and compatibility notes here.\n", mode)
    _base.write_file(root/"docs"/"contracts"/"extension-message-contracts.md", "# Extension Message Contracts\n\nDefine message names, payloads, replies, errors, and versioning here.\n", mode)
    if "clean-room" in profile.get("policy_packs", []): _base.write_file(root/"docs"/"reference"/"reference-role-report.md", "# Reference Role Report\n\nRecord reference roles/contracts without copying implementation.\n", mode)


def validate_planning(root: Path) -> List[str]:
    errors=[]
    required=[root/"docs/product/PRD.md", root/"docs/planning/WBS.md", root/"docs/planning/wbs-manifest.json", root/"docs/planning/codex-command-queue.md", root/"docs/planning/codex-command-queue.json"]
    for path in required:
        if not path.exists(): errors.append(f"Missing planning file: {path}")
    manifest_path=root/".codex/skillset-manifest.json"; wbs_path=root/"docs/planning/wbs-manifest.json"; queue_path=root/"docs/planning/codex-command-queue.json"
    if not manifest_path.exists() or not wbs_path.exists(): return errors
    try:
        manifest=json.loads(manifest_path.read_text()); wbs=json.loads(wbs_path.read_text()); queue=json.loads(queue_path.read_text()) if queue_path.exists() else {"commands":[]}
    except Exception as e: errors.append(f"Bad planning JSON: {e}"); return errors
    module_paths={normalized_repo_path(m.get("path","")) for m in manifest.get("modules",[])}; module_paths.add(".")
    skills=set(manifest.get("skills",[])); optional=set(manifest.get("optional_skills",[])); workstreams={w.get("skill") for w in manifest.get("workstreams",[])}
    seen=set(); wbs_ws=set()
    for item in wbs.get("items",[]):
        iid=item.get("id")
        if not iid or iid in seen: errors.append(f"Duplicate or missing WBS id: {iid}")
        seen.add(iid); mp=normalized_repo_path(item.get("module_path","")); ws=item.get("workstream")
        if mp not in module_paths: errors.append(f"WBS item references unknown module path: {iid} -> {mp}")
        wbs_ws.add(ws)
        if isinstance(ws,str) and ws.startswith("project-") and ws not in workstreams: errors.append(f"WBS item references unknown workstream: {iid} -> {ws}")
        if not item.get("validation_commands"): errors.append(f"WBS item lacks validation commands: {iid}")
        for s in item.get("suggested_skills",[]):
            if s not in skills and s not in optional and s not in workstreams: errors.append(f"WBS item references unknown skill: {iid} -> {s}")
    for ws in sorted(w for w in workstreams if w):
        if ws not in wbs_ws and ws != "project-development-bootstrap": errors.append(f"Workstream has no WBS item: {ws}")
    qids={c.get("id") for c in queue.get("commands",[])}
    for iid in seen:
        if iid not in qids: errors.append(f"Command queue missing WBS item: {iid}")
    return errors


def validate_dev_flow(root: Path) -> List[str]:
    errors=validate_planning(root)
    if errors: return errors
    wbs=json.loads((root/"docs/planning/wbs-manifest.json").read_text())
    phases=[i.get("phase") for i in wbs.get("items",[])]
    def before(a,b):
        if a in phases and b in phases and phases.index(a)>phases.index(b): errors.append(f"Dev-flow order violation: {a} must precede {b}")
    for pair in [("stack-decision","bootstrap"),("bootstrap","contracts"),("contracts","backend-api"),("contracts","frontend-shell"),("contracts","extension-bridge"),("contracts","collectors"),("contracts","core-pipeline"),("backend-api","integration"),("frontend-shell","integration")]: before(*pair)
    if "reference-analysis" in phases:
        for b in ["contracts","backend-api","frontend-shell"]: before("reference-analysis",b)
    manifest=load_scaffold_manifest(root); module_paths=set(manifest.get("module_paths",[]))
    for ws in manifest.get("workstreams",[]):
        for p in ws.get("module_paths",[]):
            n=normalized_repo_path(p)
            if n!="." and n not in module_paths: errors.append(f"Dev-flow path divergence: {ws.get('skill')} -> {p}")
    return errors


def validate_pyproject_dependency_specs(root: Path) -> List[str]:
    errors=[]
    for path in root.rglob("pyproject.toml"):
        if any(part in {"node_modules","dist","build","__pycache__"} for part in path.relative_to(root).parts): continue
        try: data=tomllib.loads(path.read_text())
        except Exception as e: errors.append(f"Bad pyproject.toml: {path.relative_to(root).as_posix()}: {e}"); continue
        project=data.get("project",{}) if isinstance(data.get("project",{}),dict) else {}
        deps=list(project.get("dependencies",[]) or [])
        optional=project.get("optional-dependencies",{}) if isinstance(project.get("optional-dependencies",{}),dict) else {}
        for vals in optional.values(): deps.extend(list(vals or []))
        for spec in deps:
            if not isinstance(spec,str) or "latest" in spec.lower() or not PYPROJECT_SPEC_RE.match(spec.strip()) or not any(op in spec for op in [">=","==","~=",">","<"]): errors.append(f"Invalid or unpinned pyproject dependency spec in {path.relative_to(root).as_posix()}: {spec!r}")
    return errors


def write_fastapi_app(root: Path, mode: str) -> None:
    _base.write_file(root/"apps/api"/"pyproject.toml", '[project]\nname = "api"\nversion = "0.1.0"\ndependencies = [\n  "fastapi>=0.115,<1.0",\n  "uvicorn[standard]>=0.30,<1.0"\n]\n\n[project.optional-dependencies]\ndev = [\n  "pytest>=8.0,<9.0",\n  "httpx>=0.27,<1.0"\n]\n', mode)
    _base.write_file(root/"apps/api"/"app"/"__init__.py", "", mode)
    _base.write_file(root/"apps/api"/"app"/"main.py", 'from fastapi import FastAPI\n\napp = FastAPI(title="Project API")\n\n@app.get("/health")\ndef health() -> dict[str, str]:\n    return {"status": "ok"}\n', mode)
    _base.write_file(root/"apps/api"/"tests"/"test_health.py", 'from app.main import health\n\ndef test_health() -> None:\n    assert health()["status"] == "ok"\n', mode)


def root_package_json(profile: Dict[str, Any]) -> Dict[str, Any]:
    pm=profile.get("package_manager","pnpm")
    if pm=="pnpm":
        build="pnpm -r build"; test="pnpm -r test"; typecheck="pnpm -r typecheck"; dev_web="pnpm --filter web dev"; build_ext="pnpm --filter extension build"; validate_all="pnpm typecheck && pnpm build && pnpm test && pnpm validate:scaffold && pnpm validate:planning && pnpm validate:dev-flow && pnpm workspace:check && pnpm cleanroom:audit"
    else:
        build="npm run build --workspaces"; test="npm run test --workspaces --if-present"; typecheck="npm run typecheck --workspaces --if-present"; dev_web="npm run dev --workspace apps/web"; build_ext="npm run build --workspace apps/extension"; validate_all="npm run typecheck --workspaces --if-present && npm run build --workspaces && npm run test --workspaces --if-present && npm run validate:scaffold && npm run validate:planning && npm run validate:dev-flow && npm run workspace:check && npm run cleanroom:audit"
    scripts={"build":build,"test":test,"typecheck":typecheck,"validate:scaffold":"python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .","validate:planning":"python -S tools/codex/codex_skillset_generator.py validate-planning --root .","validate:dev-flow":"python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .","workspace:check":"node tools/checks/workspace-check.mjs","cleanroom:audit":"node tools/checks/cleanroom-audit.mjs","validate:all":validate_all}
    scripts["dev:api"]="cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" if profile.get("runtime_stack",{}).get("api")=="fastapi-python" else ("pnpm --filter api dev" if pm=="pnpm" else "npm run dev --workspace apps/api")
    scripts["dev:web"]=dev_web; scripts["build:extension"]=build_ext
    return {"name":profile.get("project_name","project").lower().replace(" ","-"),"private":True,"version":"0.1.0","packageManager":f"{pm}@{PINNED_PACKAGE_MANAGERS.get(pm,'0.0.0')}","workspaces":["apps/*","packages/*","tools/*"],"scripts":scripts}


def write_codex_tools(root: Path, mode: str) -> None:
    cur=Path(__file__).resolve(); core=cur.with_name("codex_skillset_generator_core.py")
    _base.write_file(root/"tools/codex/codex_skillset_generator.py", cur.read_text(encoding="utf-8"), mode)
    if core.exists(): _base.write_file(root/"tools/codex/codex_skillset_generator_core.py", core.read_text(encoding="utf-8"), mode)
    _base.write_file(root/"tools/codex/README.md", "# Codex Validation Tools\n\nCopied so generated repo can self-validate.\n", mode)


def write_check_scripts(root: Path, mode: str) -> None:
    _base.write_file(root/"tools/checks/workspace-check.mjs", """#!/usr/bin/env node
import fs from 'node:fs';
for (const p of ['package.json','tsconfig.base.json','.codex/scaffold-manifest.json']) { if (!fs.existsSync(p)) { console.error('workspace-check FAIL: missing '+p); process.exit(1); } }
const pkg=JSON.parse(fs.readFileSync('package.json','utf8'));
for (const s of ['validate:scaffold','validate:planning','validate:dev-flow','validate:all']) { if (!pkg.scripts || !pkg.scripts[s]) { console.error('workspace-check FAIL: missing script '+s); process.exit(1); } }
console.log('workspace-check PASS');
""", mode)
    _base.write_file(root/"tools/checks/cleanroom-audit.mjs", """#!/usr/bin/env node
import fs from 'node:fs'; import path from 'node:path';
const blocked=[/\\.map$/i,/(^|\\/)background\\.js$/i,/(^|\\/)preload\\.js$/i,/(^|\\/)_next\\/static\\/chunks\\//i]; const ignore=new Set(['node_modules','.git','dist','build','__pycache__']); let failures=[];
function walk(d){ for(const n of fs.readdirSync(d)){ if(ignore.has(n)) continue; const p=path.join(d,n); const rel=path.relative(process.cwd(),p).replaceAll('\\\\','/'); const st=fs.statSync(p); if(st.isDirectory()) walk(p); else if(blocked.some(rx=>rx.test(rel))) failures.push(rel); }}
walk(process.cwd()); if(failures.length){ console.error('cleanroom-audit FAIL'); for(const f of failures) console.error('- '+f); process.exit(1); } console.log('cleanroom-audit PASS');
""", mode)

_old_generate = generate
_old_scaffold = scaffold
_old_validate_scaffold = validate_scaffold


def generate(profile: Dict[str, Any], root: Path, mode: str = "skip", also_codex_skills: bool = False) -> None:
    profile=normalize_profile(profile); _old_generate(profile, root, mode, also_codex_skills=also_codex_skills)
    skills=compute_project_skills(profile)
    if mode != "skip": _base.write_file(root/"AGENTS.md", render_root_agents_md(profile, skills), "overwrite")
    _base.write_file(root/"docs/skillset/common-skill-workflow.md", render_common_skill_workflow(), mode)
    if profile.get("workstreams") or profile.get("generate_project_scaffold"): write_planning_docs(profile, root, mode)


def scaffold(profile: Dict[str, Any], root: Path, mode: str = "skip") -> None:
    _old_scaffold(profile, root, mode)
    write_codex_tools(root, mode); write_check_scripts(root, mode)


def validate_scaffold(root: Path) -> List[str]:
    errors=_old_validate_scaffold(root)
    for rel in ["tools/codex/codex_skillset_generator.py","tools/checks/workspace-check.mjs","tools/checks/cleanroom-audit.mjs"]:
        if not (root/rel).exists(): errors.append(f"Missing scaffold file: {rel}")
    errors.extend(validate_pyproject_dependency_specs(root))
    return errors


def generate_dev_kit(profile: Dict[str, Any], root: Path, mode: str = "skip", also_codex_skills: bool = False) -> List[str]:
    profile=normalize_profile(profile); generate(profile, root, mode, also_codex_skills=also_codex_skills)
    if profile.get("generate_project_scaffold"): scaffold(profile, root, mode)
    errors=[]; errors.extend(validate_generated(root))
    if profile.get("generate_project_scaffold"): errors.extend(validate_scaffold(root))
    if profile.get("workstreams") or profile.get("generate_project_scaffold"):
        errors.extend(validate_planning(root))
        if profile.get("generate_project_scaffold"): errors.extend(validate_dev_flow(root))
    return errors


def write_generated_examples(base: Path) -> None:
    out=base/"examples"/"generated"
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)
    for preset in PRESETS:
        profile=preset_profile(preset); target=out/preset; generate(profile,target,mode="overwrite")
        if profile.get("generate_project_scaffold"): scaffold(profile,target,mode="overwrite")


def cmd_generate_prd(args: argparse.Namespace) -> int:
    write_planning_docs(normalize_profile(read_json(args.config)), Path(args.root), args.mode); print(f"Generated planning docs at {args.root}"); return 0

def cmd_generate_wbs(args: argparse.Namespace) -> int:
    profile=normalize_profile(read_json(args.config)); root=Path(args.root)
    _base.write_file(root/"docs/planning/WBS.md", render_wbs(profile), args.mode); _base.write_file(root/"docs/planning/wbs-manifest.json", render_wbs_manifest(profile), args.mode); _base.write_file(root/"docs/planning/implementation-sequence.md", render_implementation_sequence(profile), args.mode); _base.write_file(root/"docs/planning/phase-gates.md", render_phase_gates(profile), args.mode); print(f"Generated WBS docs at {args.root}"); return 0

def cmd_generate_command_queue(args: argparse.Namespace) -> int:
    profile=normalize_profile(read_json(args.config)); root=Path(args.root); _base.write_file(root/"docs/planning/codex-command-queue.md", render_command_queue(profile), args.mode); _base.write_file(root/"docs/planning/codex-command-queue.json", render_command_queue_manifest(profile), args.mode); print(f"Generated Codex command queue at {args.root}"); return 0

def cmd_generate_next_command(args: argparse.Namespace) -> int:
    items=wbs_items(normalize_profile(read_json(args.config))); chosen=next((i for i in items if i["id"]==args.wbs_id), items[0] if items else None)
    if not chosen: print("FAIL\n- No matching WBS item"); return 1
    print(command_for_item(chosen).rstrip()); return 0

def cmd_repair_command(args: argparse.Namespace) -> int:
    txt="Read AGENTS.md first. Use $debugging-and-error-recovery and $evidence-pack. Reproduce the failure, patch the smallest slice, rerun validation, and report evidence."
    if args.log_file and Path(args.log_file).exists(): txt += "\n\nFailure log excerpt:\n```text\n" + Path(args.log_file).read_text(encoding="utf-8", errors="replace")[-4000:] + "\n```"
    print(txt); return 0

def cmd_validate_planning(args: argparse.Namespace) -> int:
    errors=validate_planning(Path(args.root));
    if errors: print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0

def cmd_validate_dev_flow(args: argparse.Namespace) -> int:
    errors=validate_dev_flow(Path(args.root));
    if errors: print("FAIL"); [print(f"- {e}") for e in errors]; return 1
    print("PASS"); return 0



# ---- v4.9.5-dev-ops-r1 patch: meaningful tests, API validation, state-aware commands ----
VERSION = "4.9.5-dev-ops-r1"
NOOP_TEST_RE = re.compile(r'(?i)(no tests configured|echo\s+["\']?no tests|echo\s+["\']?ok|exit\s+0|true$)')


def _json_smoke_test_script(rel: str, expected_files: Sequence[str]) -> str:
    checks = "\n".join(
        f"test('{rel} has {path}', () => {{ assert.ok(fs.existsSync('{path}')); }});"
        for path in expected_files
    )
    return """import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

""" + checks + "\n"


def write_ts_package(root: Path, rel: str, name: str, mode: str, *, app: bool = False) -> None:
    pkg = {
        "name": name,
        "private": True,
        "version": "0.1.0",
        "type": "module",
        "scripts": {
            "build": "tsc -p tsconfig.json",
            "test": "node --test test/*.test.mjs",
            "typecheck": "tsc -p tsconfig.json --noEmit",
        },
        "dependencies": {},
        "devDependencies": dict(PINNED_TS_DEV_DEPENDENCIES),
    }
    smoke_files = ["package.json", "tsconfig.json", "src/index.ts"]
    if app:
        pkg["scripts"]["dev"] = "vite"
        pkg["scripts"]["build"] = "vite build"
        pkg["dependencies"] = dict(PINNED_WEB_DEPENDENCIES)
        pkg["devDependencies"] = dict(PINNED_WEB_DEV_DEPENDENCIES)
        smoke_files = ["package.json", "index.html", "src/App.tsx", "src/main.tsx"]
    _base.write_file(root/rel/"package.json", json_dump(pkg), mode)
    _base.write_file(root/rel/"tsconfig.json", '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": {"outDir": "dist", "rootDir": "src"},\n  "include": ["src"]\n}\n', mode)
    _base.write_file(root/rel/"src"/"index.ts", "export const packageReady = true;\n", mode)
    _base.write_file(root/rel/"test"/"smoke.test.mjs", _json_smoke_test_script(rel, smoke_files), mode)


def write_fastapi_app(root: Path, mode: str) -> None:
    _base.write_file(root/"apps/api"/"pyproject.toml", '[project]\nname = "api"\nversion = "0.1.0"\ndependencies = [\n  "fastapi>=0.115,<1.0",\n  "uvicorn[standard]>=0.30,<1.0"\n]\n\n[project.optional-dependencies]\ndev = [\n  "pytest>=8.0,<9.0",\n  "httpx>=0.27,<1.0"\n]\n', mode)
    _base.write_file(root/"apps/api"/"app"/"__init__.py", "", mode)
    _base.write_file(root/"apps/api"/"app"/"main.py", 'from fastapi import FastAPI\n\napp = FastAPI(title="Project API")\n\n@app.get("/health")\ndef health() -> dict[str, str]:\n    return {"status": "ok"}\n', mode)
    _base.write_file(root/"apps/api"/"tests"/"test_health.py", 'from app.main import health\n\ndef test_health() -> None:\n    assert health()["status"] == "ok"\n', mode)


def write_fastify_app(root: Path, mode: str) -> None:
    pkg = {
        "name": "api",
        "private": True,
        "version": "0.1.0",
        "type": "module",
        "scripts": {
            "dev": "tsx src/server.ts",
            "build": "tsc -p tsconfig.json",
            "test": "node --test test/*.test.mjs",
            "typecheck": "tsc -p tsconfig.json --noEmit",
        },
        "dependencies": dict(PINNED_FASTIFY_DEPENDENCIES),
        "devDependencies": dict(PINNED_FASTIFY_DEV_DEPENDENCIES),
    }
    _base.write_file(root/"apps/api"/"package.json", json_dump(pkg), mode)
    _base.write_file(root/"apps/api"/"tsconfig.json", '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": {"outDir": "dist", "rootDir": "src"},\n  "include": ["src"]\n}\n', mode)
    _base.write_file(root/"apps/api"/"src"/"server.ts", 'import Fastify from "fastify";\n\nconst app = Fastify();\napp.get("/health", async () => ({ status: "ok" }));\n\napp.listen({ port: Number(process.env.PORT ?? 8000), host: "0.0.0.0" });\n', mode)
    _base.write_file(root/"apps/api"/"test"/"smoke.test.mjs", _json_smoke_test_script("apps/api", ["package.json", "src/server.ts"]), mode)


def write_extension(root: Path, mode: str) -> None:
    pkg = {
        "name": "extension",
        "private": True,
        "version": "0.1.0",
        "type": "module",
        "scripts": {
            "build": "tsc -p tsconfig.json",
            "test": "node --test test/*.test.mjs",
            "typecheck": "tsc -p tsconfig.json --noEmit",
        },
        "devDependencies": dict(PINNED_TS_DEV_DEPENDENCIES),
    }
    _base.write_file(root/"apps/extension"/"package.json", json_dump(pkg), mode)
    _base.write_file(root/"apps/extension"/"manifest.json", json_dump({"manifest_version": 3, "name": "Project Extension", "version": "0.1.0", "permissions": ["storage"], "background": {"service_worker": "dist/background.js", "type": "module"}, "action": {"default_title": "Project Extension"}}), mode)
    _base.write_file(root/"apps/extension"/"tsconfig.json", '{\n  "extends": "../../tsconfig.base.json",\n  "compilerOptions": {"outDir": "dist", "rootDir": "src"},\n  "include": ["src"]\n}\n', mode)
    _base.write_file(root/"apps/extension"/"src"/"background.ts", 'chrome.runtime.onInstalled.addListener(() => {\n  console.log("Extension installed");\n});\n', mode)
    _base.write_file(root/"apps/extension"/"src"/"content.ts", 'export {};\n', mode)
    _base.write_file(root/"apps/extension"/"test"/"smoke.test.mjs", _json_smoke_test_script("apps/extension", ["manifest.json", "src/background.ts", "src/content.ts"]), mode)


def root_package_json(profile: Dict[str, Any]) -> Dict[str, Any]:
    pm = profile.get("package_manager", "pnpm")
    api_runtime = profile.get("runtime_stack", {}).get("api")
    if pm == "pnpm":
        build = "pnpm -r build"
        test = "pnpm -r test"
        typecheck = "pnpm -r typecheck"
        dev_web = "pnpm --filter web dev"
        build_ext = "pnpm --filter extension build"
        api_test = "cd apps/api && pytest" if api_runtime == "fastapi-python" else "pnpm --filter api test"
        validate_all = "pnpm typecheck && pnpm build && pnpm test && pnpm test:api && pnpm validate:scaffold && pnpm validate:planning && pnpm validate:dev-flow && pnpm workspace:check && pnpm cleanroom:audit"
    else:
        build = "npm run build --workspaces"
        test = "npm run test --workspaces --if-present"
        typecheck = "npm run typecheck --workspaces --if-present"
        dev_web = "npm run dev --workspace apps/web"
        build_ext = "npm run build --workspace apps/extension"
        api_test = "cd apps/api && pytest" if api_runtime == "fastapi-python" else "npm run test --workspace apps/api"
        validate_all = "npm run typecheck --workspaces --if-present && npm run build --workspaces && npm run test --workspaces --if-present && npm run test:api && npm run validate:scaffold && npm run validate:planning && npm run validate:dev-flow && npm run workspace:check && npm run cleanroom:audit"
    scripts = {
        "build": build,
        "test": test,
        "test:api": api_test,
        "typecheck": typecheck,
        "validate:scaffold": "python -S tools/codex/codex_skillset_generator.py validate-scaffold --root .",
        "validate:planning": "python -S tools/codex/codex_skillset_generator.py validate-planning --root .",
        "validate:dev-flow": "python -S tools/codex/codex_skillset_generator.py validate-dev-flow --root .",
        "workspace:check": "node tools/checks/workspace-check.mjs",
        "cleanroom:audit": "node tools/checks/cleanroom-audit.mjs",
        "validate:all": validate_all,
    }
    scripts["dev:api"] = "cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" if api_runtime == "fastapi-python" else ("pnpm --filter api dev" if pm == "pnpm" else "npm run dev --workspace apps/api")
    scripts["dev:web"] = dev_web
    scripts["build:extension"] = build_ext
    return {"name": profile.get("project_name", "project").lower().replace(" ", "-"), "private": True, "version": "0.1.0", "packageManager": f"{pm}@{PINNED_PACKAGE_MANAGERS.get(pm,'0.0.0')}", "workspaces": ["apps/*", "packages/*", "tools/*"], "scripts": scripts}


def write_check_scripts(root: Path, mode: str) -> None:
    _base.write_file(root/"tools/checks/workspace-check.mjs", """#!/usr/bin/env node
import fs from 'node:fs';
for (const p of ['package.json','tsconfig.base.json','.codex/scaffold-manifest.json']) { if (!fs.existsSync(p)) { console.error('workspace-check FAIL: missing '+p); process.exit(1); } }
const pkg=JSON.parse(fs.readFileSync('package.json','utf8'));
for (const s of ['test:api','validate:scaffold','validate:planning','validate:dev-flow','validate:all']) { if (!pkg.scripts || !pkg.scripts[s]) { console.error('workspace-check FAIL: missing script '+s); process.exit(1); } }
if (/echo|No tests configured|exit 0|true$/.test(pkg.scripts.test || '')) { console.error('workspace-check FAIL: root test script appears to be no-op'); process.exit(1); }
console.log('workspace-check PASS');
""", mode)
    _base.write_file(root/"tools/checks/cleanroom-audit.mjs", """#!/usr/bin/env node
import fs from 'node:fs'; import path from 'node:path';
const blocked=[/\\.map$/i,/(^|\\/)background\\.js$/i,/(^|\\/)preload\\.js$/i,/(^|\\/)_next\\/static\\/chunks\\//i]; const ignore=new Set(['node_modules','.git','dist','build','__pycache__']); let failures=[];
function walk(d){ for(const n of fs.readdirSync(d)){ if(ignore.has(n)) continue; const p=path.join(d,n); const rel=path.relative(process.cwd(),p).replaceAll('\\\\','/'); const st=fs.statSync(p); if(st.isDirectory()) walk(p); else if(blocked.some(rx=>rx.test(rel))) failures.push(rel); }}
walk(process.cwd()); if(failures.length){ console.error('cleanroom-audit FAIL'); for(const f of failures) console.error('- '+f); process.exit(1); } console.log('cleanroom-audit PASS');
""", mode)


def validate_noop_test_scripts(root: Path) -> List[str]:
    errors: List[str] = []
    for path in root.rglob("package.json"):
        if any(part in {"node_modules", "dist", "build"} for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        script = str(data.get("scripts", {}).get("test", "")).strip()
        if script and NOOP_TEST_RE.search(script):
            errors.append(f"No-op test script is not allowed in generated scaffold: {rel} -> {script!r}")
        if script == "node --test test/*.test.mjs":
            if not (path.parent/"test").exists() or not list((path.parent/"test").glob("*.test.mjs")):
                errors.append(f"Test script has no generated smoke test files: {rel}")
    return errors


def validate_root_validate_all(root: Path) -> List[str]:
    errors: List[str] = []
    pkg_path = root/"package.json"
    if not pkg_path.exists():
        return errors
    try:
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"Bad root package.json: {exc}"]
    scripts = pkg.get("scripts", {}) if isinstance(pkg.get("scripts", {}), dict) else {}
    validate_all = str(scripts.get("validate:all", ""))
    if "test:api" not in scripts:
        errors.append("Root package.json lacks test:api script")
    manifest = load_scaffold_manifest(root)
    if manifest.get("runtime_stack", {}).get("api") == "fastapi-python":
        if "pytest" not in str(scripts.get("test:api", "")):
            errors.append("FastAPI scaffold requires root test:api to run pytest")
        if "test:api" not in validate_all:
            errors.append("FastAPI scaffold requires validate:all to include test:api")
    return errors


_v494_validate_scaffold = validate_scaffold

def validate_scaffold(root: Path) -> List[str]:
    errors = _v494_validate_scaffold(root)
    errors.extend(validate_noop_test_scripts(root))
    errors.extend(validate_root_validate_all(root))
    return errors


def _load_wbs_item_from_root(root: Optional[str], wbs_id: Optional[str]) -> Optional[Dict[str, Any]]:
    if not root:
        return None
    path = Path(root)/"docs/planning/wbs-manifest.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    items = data.get("items", []) if isinstance(data, dict) else []
    if wbs_id:
        return next((i for i in items if i.get("id") == wbs_id), None)
    return next((i for i in items if str(i.get("status", "todo")).lower() in {"todo", "next", "blocked"}), items[0] if items else None)


def cmd_generate_next_command(args: argparse.Namespace) -> int:
    chosen = _load_wbs_item_from_root(getattr(args, "root", None), getattr(args, "wbs_id", None))
    if chosen is None:
        items = wbs_items(normalize_profile(read_json(args.config)))
        chosen = next((i for i in items if i["id"] == getattr(args, "wbs_id", None)), items[0] if items else None)
    if not chosen:
        print("FAIL\n- No matching WBS item")
        return 1
    print(command_for_item(chosen).rstrip())
    return 0


def classify_failure_log(text: str) -> Tuple[List[str], List[str]]:
    lower = text.lower()
    skills = ["debugging-and-error-recovery", "evidence-pack"]
    actions: List[str] = []
    if "missing scaffold file" in lower or "validate-scaffold" in lower:
        skills.append("project-development-bootstrap"); actions.append("Run or repair scaffold, then rerun validate-scaffold.")
    if "invalid dependency spec" in lower or "pyproject" in lower or "package.json" in lower:
        skills.append("project-development-bootstrap"); actions.append("Patch dependency/version specs and rerun validate-scaffold.")
    if "workstream path" in lower or "module path" in lower:
        skills.append("consistency-guard"); actions.append("Align workstream module_paths, manifest modules, and scaffold paths.")
    if "cleanroom" in lower or "clean-room" in lower or "source-copy" in lower:
        skills.extend(["project-reference-mapper", "source-copy-audit"]); actions.append("Inspect clean-room blocked artifacts and remove copied/source-map/build outputs.")
    if "validate-planning" in lower or "wbs" in lower or "command queue" in lower:
        skills.append("planning-and-task-breakdown"); actions.append("Repair PRD/WBS/command queue consistency and rerun validate-planning.")
    if not actions:
        actions.append("Reproduce the failure, identify the smallest affected slice, patch, and rerun the failing validator.")
    return unique(skills), actions


def cmd_repair_command(args: argparse.Namespace) -> int:
    text = ""
    if args.log_file and Path(args.log_file).exists():
        text = Path(args.log_file).read_text(encoding="utf-8", errors="replace")[-4000:]
    skills, actions = classify_failure_log(text)
    txt = "Read AGENTS.md first.\nUse " + " ".join(f"${s}" for s in skills) + ".\n\nRepair plan:\n" + "\n".join(f"- {a}" for a in actions) + "\n- Make the smallest coherent change, rerun the failing command, then report changed files and evidence."
    if text:
        txt += "\n\nFailure log excerpt:\n```text\n" + text + "\n```"
    print(txt)
    return 0

def main(argv: Optional[Sequence[str]]=None) -> int:
    parser=argparse.ArgumentParser(description="Codex skillset generator with dev-ops planning/scaffold support")
    sub=parser.add_subparsers(dest="cmd", required=True)
    p=sub.add_parser("list-presets"); p.set_defaults(func=cmd_list_presets)
    p=sub.add_parser("list-sizes"); p.set_defaults(func=cmd_list_sizes)
    p=sub.add_parser("list-bundles"); p.set_defaults(func=cmd_list_bundles)
    p=sub.add_parser("self-check"); p.add_argument("--root", default="."); p.add_argument("--generated-examples", action="store_true"); p.add_argument("--temp-generate", action="store_true"); p.set_defaults(func=cmd_self_check)
    p=sub.add_parser("init"); p.add_argument("--preset", required=True, choices=sorted(PRESETS)); p.add_argument("--size", choices=sorted(_base.PROJECT_SIZES)); p.add_argument("--output", required=True); p.set_defaults(func=cmd_init)
    p=sub.add_parser("recommend"); p.add_argument("--config", required=True); p.add_argument("--path"); p.set_defaults(func=cmd_recommend)
    p=sub.add_parser("validate"); p.add_argument("--config", required=True); p.set_defaults(func=cmd_validate)
    p=sub.add_parser("generate"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip","backup","overwrite"], default="skip"); p.add_argument("--also-write-codex-skills", action="store_true"); p.set_defaults(func=cmd_generate)
    p=sub.add_parser("generate-dev-kit"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip","backup","overwrite"], default="skip"); p.add_argument("--also-write-codex-skills", action="store_true"); p.set_defaults(func=cmd_generate_dev_kit)
    p=sub.add_parser("scaffold"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip","backup","overwrite"], default="skip"); p.set_defaults(func=cmd_scaffold)
    p=sub.add_parser("validate-generated"); p.add_argument("--root", required=True); p.set_defaults(func=cmd_validate_generated)
    p=sub.add_parser("validate-scaffold"); p.add_argument("--root", required=True); p.set_defaults(func=cmd_validate_scaffold)
    p=sub.add_parser("generate-prd"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip","backup","overwrite"], default="skip"); p.set_defaults(func=cmd_generate_prd)
    p=sub.add_parser("generate-wbs"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip","backup","overwrite"], default="skip"); p.set_defaults(func=cmd_generate_wbs)
    p=sub.add_parser("generate-command-queue"); p.add_argument("--config", required=True); p.add_argument("--root", required=True); p.add_argument("--mode", choices=["skip","backup","overwrite"], default="skip"); p.set_defaults(func=cmd_generate_command_queue)
    p=sub.add_parser("generate-next-command"); p.add_argument("--config", required=True); p.add_argument("--wbs-id"); p.add_argument("--root"); p.set_defaults(func=cmd_generate_next_command)
    p=sub.add_parser("repair-command"); p.add_argument("--log-file"); p.set_defaults(func=cmd_repair_command)
    p=sub.add_parser("validate-planning"); p.add_argument("--root", required=True); p.set_defaults(func=cmd_validate_planning)
    p=sub.add_parser("validate-dev-flow"); p.add_argument("--root", required=True); p.set_defaults(func=cmd_validate_dev_flow)
    p=sub.add_parser("write-examples"); p.add_argument("--root", default="."); p.add_argument("--generated", action="store_true"); p.set_defaults(func=cmd_write_examples)
    args=parser.parse_args(argv); return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
