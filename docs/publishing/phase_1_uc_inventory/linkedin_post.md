
```text

"Prompt-in-a-notebook" breaks banking compliance on Day 1.

In traditional ML model risk management (FRB SR 11-7), a model was a single artifact URI with deterministic outputs and an annual review cycle.

Enterprise AI agents don't work like that. An agent is a dynamic runtime graph:
→ A foundation model endpoint
→ Versioned system prompts
→ A retrieval vector index
→ Model Context Protocol (MCP) tools capable of reading PII or mutating production records

If you don't inventory every node in that graph as a governed asset, you have already failed SR 11-7 Section III and NIST AI RMF (GOVERN 1 / MAP 1) before running a single evaluation.

I just shipped Phase 1 of an open-source reference architecture (`agentic-mrm-lifecycle-governance`) showing how to enforce banking-grade MRM natively on Databricks Unity Catalog:

1. Policy-as-Code Crosswalk: Mapping SR 11-7 / SR 26-2 & NIST AI RMF controls into a version-controlled YAML ruleset that both Risk Committees and CI/CD pipelines read.
2. Deterministic Inherent Risk Tiering: A Python scoring engine that automatically classifies agents into Tier 1/2/3—with a hard rule elevating any regulated-domain agent with write-capable MCP tools to Tier 1 (mandatory HITL + independent validation).
3. Unified UC Securable Registry: Deploying Governed Tags (`mrm_tier`, `validation_status`, `nist_rmf_function`) and a Change-Data-Feed-enabled Delta registry via Databricks Asset Bundles.

Next up in Phase 2: Building the Data Vault 2.0 audit backbone to capture immutable point-in-time lineage across OpenTelemetry agent spans.

Question for fellow data architects and MRM practitioners: How is your organization currently inventorying MCP servers and system prompts—centralized catalog securables, or still tracked manually in spreadsheets?

Links to the Phase 1 GitHub release (`v0.1.0-phase1`) and full technical breakdown in the comments below. 👇

#ModelRiskManagement #AIGovernance #Databricks #UnityCatalog #NISTAIRMF #SR117 #DataEngineering #AgenticAI
```
