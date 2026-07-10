---
id: Rel55
type: Relationship

source_risk_id: R21 (Downtime During Migration)
target_mitigation_id: M17 (Phased Migration Strategy)

relationship_type: Prevents
influence_strength: High
confidence_level: High

evidence_type: Expert Opinion

---

# Secondary Risk Created
Longer migration timelines.

# Applicability Conditions
Mission-critical environments.

# Observed Outcome
Supports business continuity.

# Reasoning Notes
Shifting modules incrementally (e.g., Strangler Pattern) means core services remain online throughout the transition.

# Standardized Relationship Entry
IF systems are modernized gradually THEN business disruption and migration downtime are virtually eliminated.
