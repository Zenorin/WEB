# Profile Schema Reference

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
