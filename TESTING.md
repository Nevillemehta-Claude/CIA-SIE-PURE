# CIA-SIE Test Suite Documentation

## Overview

This document describes the test structure and guidelines for the CIA-SIE project. Tests are designed to ensure both functional correctness and **constitutional compliance** with the Gold Standard Specification.

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and pytest configuration
├── unit/                          # Unit tests (fast, isolated)
│   ├── test_models.py             # Core domain models
│   ├── test_enums.py              # Enum definitions
│   ├── test_exceptions.py         # Custom exceptions
│   ├── test_config.py             # Configuration
│   ├── test_security.py           # Security utilities
│   ├── test_dal_models.py         # Database models
│   ├── test_dal_repositories.py   # Repository pattern
│   ├── test_api_app.py            # FastAPI app
│   ├── test_api_routes.py         # API route handlers
│   ├── test_webhook_handler.py    # Webhook processing
│   ├── test_signal_normalizer.py  # Signal normalization
│   ├── test_freshness.py          # Freshness calculation
│   ├── test_contradiction_detector.py  # Contradiction detection
│   ├── test_confirmation_detector.py   # Confirmation detection
│   ├── test_relationship_exposer.py    # Relationship exposure
│   ├── test_claude_client.py      # Claude API client
│   ├── test_prompt_builder.py     # Narrative prompts
│   ├── test_narrative_generator.py # Narrative generation
│   ├── test_response_validator.py  # AI response validation
│   ├── test_platforms.py          # Platform adapters
│   ├── test_usage_tracker.py      # AI usage tracking
│   └── test_constitutional_compliance.py  # CRITICAL compliance tests
└── integration/                   # Integration tests (full stack)
    ├── conftest.py                # Integration test fixtures
    ├── test_api.py                # Basic API tests
    └── test_full_api.py           # Comprehensive API tests
```

## Running Tests

```bash
# Run all unit tests
poetry run pytest tests/unit/ -v

# Run all integration tests
poetry run pytest tests/integration/ -v

# Run with coverage
poetry run pytest tests/ -v --cov=cia_sie --cov-report=term-missing

# Run only constitutional compliance tests
poetry run pytest tests/ -v -m constitutional

# Run fast tests only
poetry run pytest tests/ -v -m "not slow"
```

## Constitutional Compliance Tests

**CRITICAL**: The CIA-SIE system operates under strict constitutional constraints defined in the Gold Standard Specification Section 0B.

### Prohibited Features (NEVER implement)

| Feature | Reason |
|---------|--------|
| Weights on charts/signals | All signals must have equal standing |
| Confidence scores | Implies certainty that doesn't exist |
| Aggregation/net signals | User must see all individual signals |
| Recommendations | System describes, user decides |
| Contradiction resolution | Contradictions are exposed, never resolved |

### Constitutional Test Categories

1. **No Weights**: `TestNoWeightsAnywhere`
   - Verifies no model has `weight`, `priority`, or `importance` fields

2. **No Confidence**: `TestNoConfidenceScores`
   - Verifies no model has `confidence`, `score`, or `strength` fields

3. **No Aggregation**: `TestNoAggregation`
   - Verifies no `overall_direction`, `net_signal`, or aggregation methods

4. **No Recommendations**: `TestNoRecommendations`
   - Verifies no `recommend`, `advise`, or prescriptive methods

5. **Contradictions Exposed**: `TestContradictionsExposed`
   - Verifies contradictions have no `resolution` or `winner` fields

### Adding New Features

When adding new features:

1. **Check constitutional compliance FIRST**
2. Add tests in `test_constitutional_compliance.py`
3. Use the `@pytest.mark.constitutional` marker
4. Run `pytest -m constitutional` before committing

## Test Fixtures

### Shared Fixtures (conftest.py)

```python
# Sample IDs
sample_instrument_id  # Consistent UUID for testing
sample_silo_id
sample_chart_id

# Sample Models
sample_instrument     # Complete Instrument model
sample_silo           # Complete Silo model
sample_chart          # Complete Chart model (NO weight!)
sample_signal         # Complete Signal model (NO confidence!)

# Helper Functions
make_signal(chart_id, direction, ...)   # Factory for signals
make_chart_status(chart_id, ...)        # Factory for chart status
assert_no_weight_attribute(obj)         # Constitutional check
assert_no_confidence_attribute(obj)     # Constitutional check
assert_no_recommendation(text)          # Constitutional check
```

### Integration Test Fixtures

```python
# Database
setup_database       # Auto-fixture: init and teardown DB
client               # AsyncClient for API testing

# Pre-created Entities
created_instrument   # Instrument in database
created_silo         # Silo linked to instrument
created_chart        # Chart linked to silo
```

## Writing New Tests

### Unit Test Template

```python
"""
Tests for CIA-SIE [Module Name]
================================

Validates [description].

GOVERNED BY: Section X.Y (Specification Reference)
"""

import pytest
from cia_sie.module import ClassName


class TestClassName:
    """Tests for ClassName."""

    @pytest.fixture
    def instance(self):
        """Create instance for testing."""
        return ClassName()

    def test_basic_functionality(self, instance):
        """Test basic operation."""
        result = instance.method()
        assert result == expected

    @pytest.mark.constitutional
    def test_no_prohibited_attribute(self, instance):
        """CRITICAL: Verify constitutional compliance."""
        assert not hasattr(instance, 'weight')
        assert not hasattr(instance, 'confidence')
```

### Integration Test Template

```python
@pytest.mark.asyncio
async def test_full_workflow(self, client):
    """Test complete workflow."""
    # 1. Create entities
    response = await client.post("/api/v1/...", json={...})
    assert response.status_code == 201

    # 2. Verify retrieval
    response = await client.get("/api/v1/...")
    assert response.status_code == 200

    # 3. Verify constitutional compliance
    data = response.json()
    assert "weight" not in data
    assert "confidence" not in data
```

## Coverage Goals

| Module | Target | Notes |
|--------|--------|-------|
| core/ | 90%+ | Models, enums, exceptions |
| dal/ | 80%+ | Repository pattern |
| api/ | 80%+ | Route handlers |
| ai/ | 85%+ | Critical for narratives |
| ingestion/ | 85%+ | Webhook handling |
| exposure/ | 90%+ | Constitutional critical |

## AI Assistant Instructions

When an AI assistant works on new features:

1. **Read this file first**
2. **Check `test_constitutional_compliance.py`** for prohibited patterns
3. **Add tests before implementing** (TDD preferred)
4. **Run constitutional tests** after changes: `pytest -m constitutional`
5. **Maintain coverage** at 80%+ overall

### Quick Commands

```bash
# Before starting work
poetry run pytest tests/unit/test_constitutional_compliance.py -v

# After making changes
poetry run pytest tests/ -v --cov=cia_sie

# Before committing
poetry run pytest -m constitutional && poetry run ruff check .
```

## Bug Fixes Applied

### Pydantic v2 Enum Serialization

Pydantic v2 serializes enums to strings. Code that calls `.value` on enum fields will fail.

**Fixed files:**
- `src/cia_sie/ai/prompt_builder.py` - Added `_get_enum_value()` helper
- `src/cia_sie/ai/narrative_generator.py` - Uses the helper
- `src/cia_sie/api/routes/webhooks.py` - Uses safe pattern
- `src/cia_sie/api/routes/relationships.py` - Uses safe pattern

**Pattern to use:**
```python
# Bad (fails with Pydantic v2)
direction = signal.direction.value

# Good (works with both)
direction = signal.direction.value if hasattr(signal.direction, 'value') else signal.direction

# Or use the helper in prompt_builder.py
from cia_sie.ai.prompt_builder import _get_enum_value
direction = _get_enum_value(signal.direction)
```
