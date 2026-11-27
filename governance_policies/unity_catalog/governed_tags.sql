-- ============================================================================
-- Phase 1: Unity Catalog Governed Tag Taxonomy & Agentic Inventory Registry
-- Compliant with SR 11-7 / SR 26-2 Section III & NIST AI RMF GOVERN 1 / MAP 1
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS IDENTIFIER(:mrm_catalog || '.mrm_inventory_' || :env_tier) -- noqa: LT01
COMMENT 'SR 11-7 and NIST AI RMF Agentic Asset Inventory and Control Metadata';

-- Master registry table capturing every agent, model, prompt, and MCP tool
CREATE TABLE IF NOT EXISTS IDENTIFIER( -- noqa: LT01
    :mrm_catalog || '.mrm_inventory_' || :env_tier || '.agentic_asset_registry' -- noqa: LT01
) (
    asset_id STRING NOT NULL,
    asset_type STRING NOT NULL
    COMMENT 'AGENT | FOUNDATION_MODEL | PROMPT | VECTOR_INDEX | MCP_SERVER',
    uc_securable_name STRING NOT NULL COMMENT 'Three-level Unity Catalog namespace path',
    asset_version STRING NOT NULL,
    mrm_tier STRING NOT NULL COMMENT 'tier_1_high | tier_2_medium | tier_3_low',
    nist_risk_profile STRING NOT NULL COMMENT 'MINIMAL | LIMITED | HIGH | UNACCEPTABLE',
    validation_status STRING NOT NULL COMMENT 'DRAFT | IN_CHALLENGE | APPROVED | REVOKED',
    owner_principal STRING NOT NULL,
    validator_principal STRING,
    inherent_risk_score DECIMAL(5, 2) NOT NULL,
    registered_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    last_reviewed_ts TIMESTAMP,
    CONSTRAINT pk_agentic_asset PRIMARY KEY (asset_id, asset_version) NOT ENFORCED
)
USING DELTA
TBLPROPERTIES (
    'delta.enableChangeDataFeed' = 'true',
    'delta.appendOnly' = 'false',
    'governance.framework' = 'SR11-7_NIST-AI-RMF'
);

-- Seed baseline governed tag definitions (Unity Catalog DDL)
CREATE TAG IF NOT EXISTS mrm_tier ALLOWED_VALUES ('tier_1_high', 'tier_2_medium', 'tier_3_low'); -- noqa: PRS
CREATE TAG IF NOT EXISTS validation_status ALLOWED_VALUES ( -- noqa: PRS
    'DRAFT', 'IN_CHALLENGE', 'APPROVED', 'REVOKED' -- noqa: PRS
); -- noqa: PRS
CREATE TAG IF NOT EXISTS nist_rmf_function ALLOWED_VALUES ('GOVERN', 'MAP', 'MEASURE', 'MANAGE'); -- noqa: PRS
