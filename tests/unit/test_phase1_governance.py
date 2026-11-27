from pathlib import Path

import yaml

from validation.materiality_scorer import (
    AgentRiskQuestionnaire,
    MRMTier,
    score_agent_materiality,
)


def test_crosswalk_yaml_structure():
    crosswalk_path = Path("governance_policies/crosswalk/sr11_7_nist_ai_rmf_mapping.yaml")
    data = yaml.safe_load(crosswalk_path.read_text(encoding="utf-8"))

    assert "materiality_tiers" in data
    assert {"tier_1_high", "tier_2_medium", "tier_3_low"} == set(data["materiality_tiers"].keys())
    assert len(data["controls"]) >= 4


def test_tier_1_high_risk_agent():
    q = AgentRiskQuestionnaire(
        agent_name="aml-sar-drafting-agent",
        customer_facing=False,
        autonomous_write_tools=True,
        regulated_domain=True,
        handles_pii_or_pci=True,
        human_in_the_loop_enforced=False,
    )
    result = score_agent_materiality(q)
    assert result.assigned_tier == MRMTier.TIER_1_HIGH
    assert result.requires_independent_challenge is True
    assert result.requires_hitl_approval is True
    assert result.inherent_risk_score == 90.0


def test_tier_3_low_risk_agent():
    q = AgentRiskQuestionnaire(
        agent_name="internal-markdown-formatter",
        customer_facing=False,
        autonomous_write_tools=False,
        regulated_domain=False,
        handles_pii_or_pci=False,
    )
    result = score_agent_materiality(q)
    assert result.assigned_tier == MRMTier.TIER_3_LOW
    assert result.requires_independent_challenge is False