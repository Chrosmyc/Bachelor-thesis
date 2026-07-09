---
id: Rel48
type: Relationship

source_risk_id: R21 (Downtime During Migration)
target_mitigation_id: M13 (Rollback Planning)

relationship_type: Recovers
influence_strength: High
confidence_level: High

evidence_type: Expert Opinion


# Secondary Risk Created
Reverting loses new data entered.

# Applicability Conditions
Mission-critical migrations.

# Observed Outcome
Restores previous system state rapidly.

# Reasoning Notes
If migration triggers downtime, predefined rollback scripts instantly restore the legacy environment to resume operations.

# Standardized Relationship Entry
IF a migration causes critical downtime THEN rollback execution rapidly restores legacy operations.
