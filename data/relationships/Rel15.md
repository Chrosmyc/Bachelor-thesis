---
id: Rel15
type: Relationship

source_risk_id: R2 (Scarcity of Experts and Documentation)
target_mitigation_id: M4 (Improvement of Architectural Refactoring Tools)

relationship_type: Detects / Recovers
influence_strength: High
confidence_level: Medium

evidence_type: Expert Opinion / Research Opportunity


# Secondary Risk Created
Requires high-quality input for LLM analysis.

# Applicability Conditions
Codebases with missing structural documentation.

# Observed Outcome
Code smell detection can automate manual processes.

# Reasoning Notes
LLMs can analyze legacy logic and detect code smells, bridging the knowledge gap left by departed experts.

# Standardized Relationship Entry
IF experts are missing THEN LLM-assisted tools automate smell detection and compensate for lost knowledge.
