---
id: Rel8
type: Relationship

source_risk_id: R8 (Transfer of Legacy Flaws)
target_mitigation_id: M2 (Automated Logic Extraction)

relationship_type: Detects
influence_strength: Medium
confidence_level: Medium

evidence_type: Expert Opinion


# Secondary Risk Created
None explicitly mentioned.

# Applicability Conditions
Early stages of modernization.

# Observed Outcome
Understand functionality to avoid copying anti-patterns.

# Reasoning Notes
By visualizing the legacy logic, architects can identify and eliminate anti-patterns before rewriting them.

# Standardized Relationship Entry
IF legacy flaws are hidden in code THEN automated logic extraction exposes them to prevent transfer to the new system.
