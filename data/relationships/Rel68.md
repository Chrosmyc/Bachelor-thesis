---
id: Rel68
type: Relationship

source_risk_id: R20 (API and Data Incompatibility)
target_mitigation_id: M23 (Use Shells and Adapters)

relationship_type: Prevents
influence_strength: High
confidence_level: High

evidence_type: Expert Opinion

---

# Secondary Risk Created
Adds architectural complexity.

# Applicability Conditions
Application-based incremental migration.

# Observed Outcome
Preserves legacy interfaces while migrating.

# Reasoning Notes
Wrappers translate modern API calls into formats the legacy system understands, structurally resolving incompatibility.

# Standardized Relationship Entry
IF wrappers and adapters are utilized THEN API incompatibility between cloud and legacy layers is bridged.
