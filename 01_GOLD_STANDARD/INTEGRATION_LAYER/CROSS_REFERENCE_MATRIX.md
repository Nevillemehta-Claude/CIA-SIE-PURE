# CROSS-REFERENCE MATRIX
## Which Bible Modules Apply to Which Lifecycle Phases

**Classification:** INTEGRATION_LAYER
**Version:** 1.0
**Purpose:** Map relationships between Bible modules and Lifecycle phases

---

## MATRIX VIEW

| Lifecycle Phase | GOVERNANCE | ARCHITECTURE | DEVELOPMENT | VERIFICATION | INTEGRATION | DOCUMENTATION | OPERATIONS |
|-----------------|:----------:|:------------:|:-----------:|:------------:|:-----------:|:-------------:|:----------:|
| **Phase 1: Ideation** | PRIMARY | - | - | - | - | Reference | - |
| **Phase 2: Concept** | PRIMARY | Reference | - | - | - | Reference | - |
| **Phase 3: Requirements** | PRIMARY | Reference | - | Reference | Reference | Reference | - |
| **Phase 4: Architecture** | Reference | PRIMARY | - | Reference | PRIMARY | Reference | - |
| **Phase 5: Specification** | Reference | PRIMARY | PRIMARY | Reference | PRIMARY | Reference | - |
| **Phase 6: Development** | - | Reference | PRIMARY | PRIMARY | Reference | Reference | - |
| **Phase 7: Integration** | - | Reference | Reference | PRIMARY | PRIMARY | Reference | - |
| **Phase 8: Verification** | - | - | Reference | PRIMARY | Reference | Reference | - |
| **Phase 9: Documentation** | Reference | Reference | Reference | Reference | Reference | PRIMARY | - |
| **Phase 10: Deployment** | Reference | Reference | - | Reference | - | Reference | PRIMARY |
| **Phase 11: Operations** | Reference | Reference | - | Reference | - | Reference | PRIMARY |

**Legend:**
- **PRIMARY:** Must read and apply fully in this phase
- **Reference:** May consult as needed
- **-:** Not typically needed in this phase

---

## DETAILED PHASE-TO-MODULE MAPPING

### Phase 1: IDEATION

**Primary Modules:**
- `BIBLE_MODULES/GOVERNANCE/` - How to capture and evaluate ideas

**Reference Modules:**
- `BIBLE_MODULES/DOCUMENTATION/` - How to document the idea

**Relevant Principles:**
- Law 1: Meaning Precedes Implementation
- Principle 1: NASA-Style Rigour (even ideas need clarity)

---

### Phase 2: CONCEPT CRYSTALLIZATION

**Primary Modules:**
- `BIBLE_MODULES/GOVERNANCE/` - How to refine concepts

**Reference Modules:**
- `BIBLE_MODULES/ARCHITECTURE/` - Initial structural thinking
- `BIBLE_MODULES/DOCUMENTATION/` - Concept documentation

**Relevant Principles:**
- Law 1: Meaning Precedes Implementation
- Principle 7: Single Source of Truth (define the concept once)

---

### Phase 3: REQUIREMENTS ANALYSIS

**Primary Modules:**
- `BIBLE_MODULES/GOVERNANCE/` - Requirements management

**Reference Modules:**
- `BIBLE_MODULES/ARCHITECTURE/` - Architectural requirements
- `BIBLE_MODULES/VERIFICATION/` - Testability of requirements
- `BIBLE_MODULES/INTEGRATION/` - Integration requirements
- `BIBLE_MODULES/DOCUMENTATION/` - Requirements documentation

**Relevant Principles:**
- Principle 5: Full Bidirectional Traceability
- Law 1: Meaning Precedes Implementation

---

### Phase 4: ARCHITECTURE DESIGN

**Primary Modules:**
- `BIBLE_MODULES/ARCHITECTURE/` - All architecture content
- `BIBLE_MODULES/INTEGRATION/` - Integration patterns

**Reference Modules:**
- `BIBLE_MODULES/GOVERNANCE/` - Architecture decision governance
- `BIBLE_MODULES/VERIFICATION/` - Architecture validation
- `BIBLE_MODULES/DOCUMENTATION/` - Architecture documentation

**Relevant Principles:**
- All six Architecture Principles
- Law 2: Structure Precedes Intelligence
- Modularity Doctrine

---

### Phase 5: SPECIFICATION

**Primary Modules:**
- `BIBLE_MODULES/ARCHITECTURE/` - Component design
- `BIBLE_MODULES/DEVELOPMENT/` - Specification standards
- `BIBLE_MODULES/INTEGRATION/` - Interface specifications

**Reference Modules:**
- `BIBLE_MODULES/GOVERNANCE/` - Specification governance
- `BIBLE_MODULES/VERIFICATION/` - Specification testability
- `BIBLE_MODULES/DOCUMENTATION/` - Specification format

**Relevant Principles:**
- Principle 3: Zero Drift Policy
- Principle 4: Living Documentation
- Law 4: Explicit Precedes Implicit

---

### Phase 6: DEVELOPMENT

**Primary Modules:**
- `BIBLE_MODULES/DEVELOPMENT/` - All development content
- `BIBLE_MODULES/VERIFICATION/` - Testing standards

**Reference Modules:**
- `BIBLE_MODULES/ARCHITECTURE/` - Component design reference
- `BIBLE_MODULES/INTEGRATION/` - Interface contracts
- `BIBLE_MODULES/DOCUMENTATION/` - Code documentation

**Relevant Principles:**
- Law 3: Validation Precedes Optimization
- Law 4: Explicit Precedes Implicit
- Verification Doctrine

---

### Phase 7: INTEGRATION

**Primary Modules:**
- `BIBLE_MODULES/INTEGRATION/` - All integration content
- `BIBLE_MODULES/VERIFICATION/` - Integration testing

**Reference Modules:**
- `BIBLE_MODULES/ARCHITECTURE/` - Integration architecture
- `BIBLE_MODULES/DEVELOPMENT/` - Component interfaces
- `BIBLE_MODULES/DOCUMENTATION/` - Integration documentation

**Relevant Principles:**
- Principle 2: Loose Coupling
- Principle 4: Explicit Contracts
- Four Pillars of Integration Assurance

---

### Phase 8: VERIFICATION

**Primary Modules:**
- `BIBLE_MODULES/VERIFICATION/` - All verification content

**Reference Modules:**
- `BIBLE_MODULES/DEVELOPMENT/` - What was built
- `BIBLE_MODULES/INTEGRATION/` - Integration verification
- `BIBLE_MODULES/DOCUMENTATION/` - Test documentation

**Relevant Principles:**
- Verification Doctrine (all layers)
- Principle 6: Evidence-Based Validation

---

### Phase 9: DOCUMENTATION

**Primary Modules:**
- `BIBLE_MODULES/DOCUMENTATION/` - All documentation content

**Reference Modules:**
- All other modules (to verify accuracy)

**Relevant Principles:**
- Principle 4: Living Documentation
- Principle 8: Defensive Documentation

---

### Phase 10: DEPLOYMENT

**Primary Modules:**
- `BIBLE_MODULES/OPERATIONS/` - Deployment procedures

**Reference Modules:**
- `BIBLE_MODULES/GOVERNANCE/` - Release governance
- `BIBLE_MODULES/ARCHITECTURE/` - Deployment architecture
- `BIBLE_MODULES/VERIFICATION/` - Deployment verification
- `BIBLE_MODULES/DOCUMENTATION/` - Deployment documentation

**Relevant Principles:**
- Law 5: Reversibility Precedes Commitment
- Principle 5: Fail-Safe Defaults

---

### Phase 11: OPERATIONS

**Primary Modules:**
- `BIBLE_MODULES/OPERATIONS/` - All operations content

**Reference Modules:**
- All modules as needed for maintenance

**Relevant Principles:**
- All principles apply to operational changes
- Continuous verification

---

## BIBLE MODULE APPLICATION SUMMARY

| Bible Module | Primary Phases | Reference Phases |
|--------------|----------------|------------------|
| GOVERNANCE | 1, 2, 3 | 4, 5, 9, 10 |
| ARCHITECTURE | 4, 5 | 2, 3, 6, 7, 10, 11 |
| DEVELOPMENT | 5, 6 | 7, 8, 9 |
| VERIFICATION | 6, 7, 8 | 3, 4, 5, 10 |
| INTEGRATION | 4, 5, 7 | 3, 6, 8 |
| DOCUMENTATION | 9 | 1, 2, 3, 4, 5, 6, 7, 8, 10, 11 |
| OPERATIONS | 10, 11 | - |

---

## HOW TO USE THIS MATRIX

1. **Identify your current phase** from LIFECYCLE_DEFINITION
2. **Find PRIMARY modules** in this matrix
3. **Load those modules** before proceeding
4. **Consult REFERENCE modules** as questions arise

---

*CROSS_REFERENCE_MATRIX v1.0 | INTEGRATION_LAYER | Gold Standard System*
