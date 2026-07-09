---
id: Rel50
type: Relationship

source_risk_id: R24 (Single Point of Failure)
target_mitigation_id: M14 (Component Decoupling)

relationship_type: Prevents
influence_strength: High
confidence_level: High

evidence_type: Expert Opinion


# Secondary Risk Created
Increased architectural complexity.

# Applicability Conditions
Monolithic legacy systems.

# Observed Outcome
Improves scalability and fault isolation.

# Reasoning Notes
Breaking logic into microservices ensures that the crash of one component does not bring down the entire system.

# Standardized Relationship Entry
IF monoliths are decoupled into services THEN fault isolation is improved and single points of failure are removed.
