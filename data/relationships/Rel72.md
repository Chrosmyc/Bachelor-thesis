---
id: Rel72
type: Relationship

source_risk_id: R29 (Data Synchronization Failure Between Legacy and Modernized Systems)
target_mitigation_id: M25 (Synchronous Database Replication)

relationship_type: Prevents
influence_strength: Medium
confidence_level: Medium

evidence_type: Expert Opinion

---

# Secondary Risk Created
Legacy performance risks via triggers.

# Applicability Conditions
Parallel operations.

# Observed Outcome
Reduces synchronization inconsistencies.

# Reasoning Notes
Row-level replication via triggers guarantees that a write in one system is instantly enforced in the other.

# Standardized Relationship Entry
IF synchronous replication triggers are active THEN data synchronization failures during coexistence are prevented.
