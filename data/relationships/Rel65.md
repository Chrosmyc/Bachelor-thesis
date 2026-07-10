---
id: Rel65
type: Relationship

source_risk_id: R33 (Absence of Fallback Mechanism)
target_mitigation_id: M22 (Preserve Legacy Code Until Full Migration Completion)

relationship_type: Prevents
influence_strength: Medium
confidence_level: Medium

evidence_type: Expert Opinion

---

# Secondary Risk Created
Increases coexistence complexity.

# Applicability Conditions
Transaction-based migration.

# Observed Outcome
Reduces instability caused by premature removal.

# Reasoning Notes
Keeping the code running passively guarantees that a fallback environment is physically present if the modern app crashes.

# Standardized Relationship Entry
IF legacy code is retained during increment release THEN an immediate operational fallback mechanism remains available.
