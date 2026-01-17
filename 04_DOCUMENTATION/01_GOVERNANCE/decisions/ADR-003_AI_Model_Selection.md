# ADR-003: Dynamic AI Model Selection

## Status
ACCEPTED

## Date
27 December 2025

## Context
The CIA-SIE system uses Claude AI for generating descriptive narratives. The choice of AI model affects:
- Cost per analysis
- Quality of narrative
- Response latency
- Capability for complex analysis

## Decision
We implemented **Dynamic Model Selection** with four options:
1. **Auto**: System selects based on task complexity
2. **Haiku**: Fast, cost-effective for simple queries
3. **Sonnet**: Balanced for most analysis tasks
4. **Opus**: Most capable for complex analysis

## Rationale
- **Cost Control**: Users can optimize for cost vs. quality
- **Flexibility**: Different tasks have different requirements
- **User Choice**: Aligns with Data Repository philosophy of user authority
- **Budget Management**: Enables daily/monthly budget controls

## Implementation
```python
# Model selection in AI module
MODELS = {
    "haiku": "claude-3-haiku-20240307",
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-5-20251101"
}
```

## Consequences
### Positive
- Users control cost/quality tradeoff
- Transparent pricing display
- Usage statistics and budget alerts
- Auto mode for convenience

### Negative
- More complex UI for model selection
- Users must understand model differences
- Auto-selection algorithm needs tuning

## Cost Structure (per 1M tokens)
| Model | Input | Output |
|-------|-------|--------|
| Haiku | $0.25 | $1.25 |
| Sonnet | $3.00 | $15.00 |
| Opus | $15.00 | $75.00 |
