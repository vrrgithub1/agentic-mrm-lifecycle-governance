from enum import StrEnum

from pydantic import BaseModel, Field


class MRMTier(StrEnum):
    TIER_1_HIGH = "tier_1_high"
    TIER_2_MEDIUM = "tier_2_medium"
    TIER_3_LOW = "tier_3_low"


class AgentRiskQuestionnaire(BaseModel):
    agent_name: str = Field(..., min_length=3)
    customer_facing: bool = Field(..., description="Directly interacts with external customers")
    autonomous_write_tools: bool = Field(
        ..., description="Has MCP tools capable of mutating state, transactions, or records"
    )
    regulated_domain: bool = Field(
        ..., description="Used in credit, underwriting, AML/BSA, capital, or financial reporting"
    )
    handles_pii_or_pci: bool = Field(..., description="Processes sensitive customer PII/PCI data")
    human_in_the_loop_enforced: bool = Field(
        default=False, description="Requires explicit human approval before action execution"
    )


class MaterialityAssessment(BaseModel):
    agent_name: str
    inherent_risk_score: float
    assigned_tier: MRMTier
    requires_independent_challenge: bool
    requires_hitl_approval: bool
    rationale: list[str]


def score_agent_materiality(inputs: AgentRiskQuestionnaire) -> MaterialityAssessment:
    """Calculate deterministic SR 11-7 / SR 26-2 inherent risk score (0-100) and MRM tier."""
    score = 10.0
    rationale: list[str] = []

    if inputs.regulated_domain:
        score += 35.0
        rationale.append("Operates in regulated banking/financial domain (+35)")
    if inputs.autonomous_write_tools:
        score += 30.0
        rationale.append("Equipped with state-mutating MCP write tools (+30)")
    if inputs.customer_facing:
        score += 15.0
        rationale.append("External customer-facing exposure (+15)")
    if inputs.handles_pii_or_pci:
        score += 15.0
        rationale.append("Processes regulated PII/PCI data (+15)")
    if inputs.human_in_the_loop_enforced:
        score -= 10.0
        rationale.append("Compensating HITL control enabled (-10)")

    bounded_score = max(0.0, min(100.0, score))

    if bounded_score >= 60.0 or (inputs.regulated_domain and inputs.autonomous_write_tools):
        tier = MRMTier.TIER_1_HIGH
    elif bounded_score >= 30.0:
        tier = MRMTier.TIER_2_MEDIUM
    else:
        tier = MRMTier.TIER_3_LOW

    return MaterialityAssessment(
        agent_name=inputs.agent_name,
        inherent_risk_score=bounded_score,
        assigned_tier=tier,
        requires_independent_challenge=tier in {MRMTier.TIER_1_HIGH, MRMTier.TIER_2_MEDIUM},
        requires_hitl_approval=tier == MRMTier.TIER_1_HIGH,
        rationale=rationale,
    )
