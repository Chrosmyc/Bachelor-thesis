---
id: Rel71
type: Relationship

source_risk_id: R27 (Knowledge Loss Between Modernization Increments)
target_mitigation_id: M25 (Synchronous Database Replication)

relationship_type: Reduces
influence_strength: Medium
confidence_level: Medium

evidence_type: Expert Opinion


# Secondary Risk Created
Introduces performance overhead.

# Applicability Conditions
Trigger-based synchronization support.

# Observed Outcome
Keeps both databases live for analysis.

# Reasoning Notes
Synchronizing the data layer ensures that both old and new teams are working with identical, real-time datasets.

# Standardized Relationship Entry
IF databases replicate synchronously THEN teams interacting with either system view identical state knowledge.
