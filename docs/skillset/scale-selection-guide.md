# Scale Selection Guide

v4.6 uses essential-pruned generation: core + explicit policy first, then priority-ranked domain skills until the size and metadata budget is reached.

## micro
- Tiny script/tool/proof-of-concept. Minimum guidance only.
- core_skills: 6
- max_project_skills: 7
- max_module_skills: 5
- max_initial_metadata_chars: 2200
- commands: False
- references: False
- personas: False
- governance: False

## small
- Small app/library maintained by one or a few developers.
- core_skills: 9
- max_project_skills: 12
- max_module_skills: 6
- max_initial_metadata_chars: 3600
- commands: False
- references: False
- personas: False
- governance: False

## medium
- Multi-module product with meaningful tests and release flow.
- core_skills: 11
- max_project_skills: 18
- max_module_skills: 7
- max_initial_metadata_chars: 5200
- commands: True
- references: True
- personas: False
- governance: False

## large
- Team-owned product with multiple module boundaries.
- core_skills: 12
- max_project_skills: 28
- max_module_skills: 8
- max_initial_metadata_chars: 7200
- commands: True
- references: True
- personas: True
- governance: True

## enterprise
- Multi-team/compliance-sensitive/high-risk system. Strongest governance.
- core_skills: 14
- max_project_skills: 34
- max_module_skills: 9
- max_initial_metadata_chars: 8200
- commands: True
- references: True
- personas: True
- governance: True
