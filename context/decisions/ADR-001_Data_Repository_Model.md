# ADR-001: Data Repository Model (Not Intelligence Engine)

## Status
ACCEPTED

## Date
27 December 2025

## Context
The CIA-SIE system needed to determine its fundamental operating model. Two approaches were considered:
1. **Intelligence Engine**: Aggregate signals, compute scores, make recommendations
2. **Data Repository**: Store, expose, and describe signals without aggregation

## Decision
We chose the **Data Repository Model**.

The system will:
- Store all signals with full fidelity
- Expose contradictions without resolving them
- Provide descriptive AI narratives (not prescriptive)
- Never aggregate, score, or weight signals
- Preserve user authority over all decisions

## Rationale
- **User Authority**: The user must retain complete decision-making power
- **Transparency**: All signals visible, none hidden by aggregation
- **Liability**: No recommendations means no liability for outcomes
- **Flexibility**: Users can apply their own judgment and weighting
- **Constitutional Requirement**: Section 0B of Gold Standard Specification prohibits scoring/weighting

## Consequences
### Positive
- Complete transparency in signal presentation
- No "black box" decision-making
- User maintains full control
- Clear liability boundaries

### Negative
- Users must interpret signals themselves
- No "quick answer" for trading decisions
- Requires user expertise to interpret

## References
- Gold Standard Specification, Section 0A-0D
- IMPLEMENTATION_ROADMAP_v2.1.md
