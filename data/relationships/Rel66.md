---
id: Rel66
type: Relationship

source_risk_id: R27 (Knowledge Loss Between Modernization Increments)
target_mitigation_id: M22 (Preserve Legacy Code Until Full Migration Completion)

relationship_type: Reduces
influence_strength: Medium
confidence_level: Medium

evidence_type: Expert Opinion


# Secondary Risk Created
Code branching complexity.

# Applicability Conditions
Multi-phase modernization.

# Observed Outcome
Maintains reference architecture.

# Reasoning Notes
New teams joining later increments can study the operational legacy code to understand the target requirements.

# Standardized Relationship Entry
IF legacy modules remain queryable THEN knowledge transfer between changing increment teams is safeguarded.
