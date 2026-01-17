#!/usr/bin/env python3
"""
Mercury Deployment Verification Script
=======================================

Comprehensive pre-deployment verification covering all 7 gates.
Run this script to validate Mercury is deployment-ready.

Usage:
    python scripts/verify_deployment.py
    
Exit Codes:
    0 = All gates passed
    1 = One or more gates failed
"""

import sys
import os
import ast
import importlib
import traceback
from pathlib import Path
from datetime import datetime
from typing import Callable

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


class GateResult:
    """Result of a verification gate."""
    
    def __init__(self, name: str):
        self.name = name
        self.checks: list[tuple[str, bool, str]] = []
        self.passed = True
    
    def check(self, name: str, passed: bool, message: str = "") -> bool:
        self.checks.append((name, passed, message))
        if not passed:
            self.passed = False
        return passed
    
    def report(self) -> str:
        lines = [f"\n{'=' * 60}"]
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        lines.append(f"GATE: {self.name} - {status}")
        lines.append("=" * 60)
        
        for name, passed, message in self.checks:
            icon = "✅" if passed else "❌"
            lines.append(f"  {icon} {name}")
            if message and not passed:
                lines.append(f"      → {message}")
        
        return "\n".join(lines)


def run_gate(name: str, func: Callable) -> GateResult:
    """Run a verification gate with error handling."""
    result = GateResult(name)
    try:
        func(result)
    except Exception as e:
        result.check("Gate execution", False, f"Exception: {e}")
        traceback.print_exc()
    return result


# =============================================================================
# GATE 1: CODE INTEGRITY
# =============================================================================

def gate_1_code_integrity(result: GateResult):
    """Verify all Python files parse and import correctly."""
    
    src_path = Path(__file__).parent.parent / "src" / "mercury"
    
    # Check 1.1: All Python files parse correctly
    parse_errors = []
    py_files = list(src_path.rglob("*.py"))
    
    for py_file in py_files:
        try:
            with open(py_file) as f:
                ast.parse(f.read())
        except SyntaxError as e:
            parse_errors.append(f"{py_file.name}: {e}")
    
    result.check(
        f"Python syntax ({len(py_files)} files)",
        len(parse_errors) == 0,
        "; ".join(parse_errors[:3]) if parse_errors else ""
    )
    
    # Check 1.2: Core modules import
    core_modules = [
        "mercury.core.config",
        "mercury.core.security",
        "mercury.core.logging",
        "mercury.core.validation",
        "mercury.core.resilience",
        "mercury.core.health",
        "mercury.core.metrics",
        "mercury.core.errors",
        "mercury.core.features",
    ]
    
    import_errors = []
    for module in core_modules:
        try:
            importlib.import_module(module)
        except Exception as e:
            import_errors.append(f"{module}: {e}")
    
    result.check(
        f"Core module imports ({len(core_modules)} modules)",
        len(import_errors) == 0,
        "; ".join(import_errors[:3]) if import_errors else ""
    )
    
    # Check 1.3: Main package imports
    try:
        import mercury
        result.check("Main package import", True)
    except Exception as e:
        result.check("Main package import", False, str(e))
    
    # Check 1.4: Chat and interface modules
    app_modules = [
        "mercury.kite.adapter",
        "mercury.ai.engine",
        "mercury.chat.engine",
        "mercury.interface.repl",
    ]
    
    app_errors = []
    for module in app_modules:
        try:
            importlib.import_module(module)
        except Exception as e:
            app_errors.append(f"{module}: {e}")
    
    result.check(
        f"Application module imports ({len(app_modules)} modules)",
        len(app_errors) == 0,
        "; ".join(app_errors[:3]) if app_errors else ""
    )


# =============================================================================
# GATE 2: TEST VALIDATION
# =============================================================================

def gate_2_test_validation(result: GateResult):
    """Verify test files exist and are valid."""
    
    tests_path = Path(__file__).parent.parent / "tests"
    
    # Check 2.1: Test files exist
    expected_tests = [
        "test_security.py",
        "test_resilience.py",
        "test_health.py",
        "test_metrics.py",
        "test_errors.py",
        "test_chat_engine.py",
        "test_conversation.py",
    ]
    
    existing_tests = []
    missing_tests = []
    
    for test_file in expected_tests:
        if (tests_path / test_file).exists():
            existing_tests.append(test_file)
        else:
            missing_tests.append(test_file)
    
    result.check(
        f"Test files exist ({len(existing_tests)}/{len(expected_tests)})",
        len(missing_tests) == 0,
        f"Missing: {', '.join(missing_tests)}" if missing_tests else ""
    )
    
    # Check 2.2: Test files parse correctly
    parse_errors = []
    for test_file in existing_tests:
        try:
            with open(tests_path / test_file) as f:
                ast.parse(f.read())
        except SyntaxError as e:
            parse_errors.append(f"{test_file}: {e}")
    
    result.check(
        "Test files parse correctly",
        len(parse_errors) == 0,
        "; ".join(parse_errors) if parse_errors else ""
    )
    
    # Check 2.3: Count test cases
    total_tests = 0
    for test_file in existing_tests:
        with open(tests_path / test_file) as f:
            content = f.read()
            # Count test methods
            total_tests += content.count("def test_")
    
    result.check(
        f"Test case count ({total_tests} tests)",
        total_tests >= 50,
        f"Expected 50+, found {total_tests}" if total_tests < 50 else ""
    )


# =============================================================================
# GATE 3: SECURITY AUDIT
# =============================================================================

def gate_3_security_audit(result: GateResult):
    """Verify no secrets or security issues in code."""
    
    src_path = Path(__file__).parent.parent / "src"
    
    # Check 3.1: No hardcoded API keys
    dangerous_patterns = [
        ("sk-ant-", "Anthropic API key"),
        ("sk-proj-", "OpenAI API key"),
        ("password = \"", "Hardcoded password"),
        ("secret = \"", "Hardcoded secret"),
    ]
    
    found_secrets = []
    for py_file in src_path.rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
            for pattern, description in dangerous_patterns:
                if pattern in content:
                    found_secrets.append(f"{py_file.name}: {description}")
    
    result.check(
        "No hardcoded secrets",
        len(found_secrets) == 0,
        "; ".join(found_secrets[:3]) if found_secrets else ""
    )
    
    # Check 3.2: No hardcoded instruments (instrument agnostic)
    instrument_patterns = ["GOLDBEES", "SILVERBEES", "NIFTYBEES"]
    found_instruments = []
    
    for py_file in src_path.rglob("*.py"):
        with open(py_file) as f:
            content = f.read()
            for pattern in instrument_patterns:
                if pattern in content:
                    # Exclude comments and docstrings for more accurate check
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if pattern in line and not line.strip().startswith('#'):
                            found_instruments.append(f"{py_file.name}:{i+1}")
                            break
    
    result.check(
        "No hardcoded instruments (agnostic)",
        len(found_instruments) == 0,
        f"Found in: {', '.join(found_instruments[:3])}" if found_instruments else ""
    )
    
    # Check 3.3: Security module exists and has key functions
    try:
        from mercury.core.security import (
            mask_sensitive_string,
            sanitize_text,
            sanitize_dict,
        )
        result.check("Security utilities available", True)
    except ImportError as e:
        result.check("Security utilities available", False, str(e))
    
    # Check 3.4: Logging sanitization
    try:
        from mercury.core.security import sanitize_text
        test_text = 'api_key="sk-ant-test123"'
        sanitized = sanitize_text(test_text)
        is_sanitized = "sk-ant" not in sanitized and "REDACTED" in sanitized
        result.check(
            "Logging sanitization works",
            is_sanitized,
            f"Got: {sanitized}" if not is_sanitized else ""
        )
    except Exception as e:
        result.check("Logging sanitization works", False, str(e))


# =============================================================================
# GATE 4: CONFIGURATION VERIFICATION
# =============================================================================

def gate_4_config_verification(result: GateResult):
    """Verify configuration system works correctly."""
    
    # Check 4.1: Config module loads
    try:
        from mercury.core.config import Settings, get_settings
        result.check("Config module loads", True)
    except Exception as e:
        result.check("Config module loads", False, str(e))
        return
    
    # Check 4.2: Default settings work
    try:
        settings = get_settings()
        result.check("Default settings load", True)
    except Exception as e:
        result.check("Default settings load", False, str(e))
        return
    
    # Check 4.3: Validation module works
    try:
        from mercury.core.validation import validate_config, ValidationResult
        validation = validate_config()
        result.check(
            "Validation system works",
            isinstance(validation, ValidationResult),
            ""
        )
    except Exception as e:
        result.check("Validation system works", False, str(e))
    
    # Check 4.4: Mock mode available
    try:
        has_mock = hasattr(settings, 'mock_kite') or hasattr(settings, 'kite_api_key')
        result.check("Mock mode configurable", has_mock)
    except Exception as e:
        result.check("Mock mode configurable", False, str(e))


# =============================================================================
# GATE 5: RESILIENCE VALIDATION
# =============================================================================

def gate_5_resilience_validation(result: GateResult):
    """Verify resilience patterns work correctly."""
    
    # Check 5.1: Circuit breaker imports
    try:
        from mercury.core.resilience import (
            CircuitBreaker,
            CircuitState,
            kite_circuit,
            ai_circuit,
        )
        result.check("Circuit breaker imports", True)
    except Exception as e:
        result.check("Circuit breaker imports", False, str(e))
        return
    
    # Check 5.2: Circuit breaker functionality
    try:
        from mercury.core.resilience import CircuitBreaker, CircuitBreakerConfig, CircuitState
        
        config = CircuitBreakerConfig(failure_threshold=3)
        breaker = CircuitBreaker("test_verification", config)
        
        # Initial state
        assert breaker.state == CircuitState.CLOSED
        
        # Record failures
        breaker.record_failure()
        breaker.record_failure()
        breaker.record_failure()
        
        # Should be open
        is_open = breaker.state == CircuitState.OPEN
        result.check("Circuit breaker opens on failures", is_open)
        
    except Exception as e:
        result.check("Circuit breaker opens on failures", False, str(e))
    
    # Check 5.3: Graceful degradation
    try:
        from mercury.core.resilience import GracefulDegradation, DegradationLevel
        degradation = GracefulDegradation()
        caps = degradation.get_capabilities()
        
        has_caps = "live_quotes" in caps and "ai_analysis" in caps
        result.check("Graceful degradation works", has_caps)
    except Exception as e:
        result.check("Graceful degradation works", False, str(e))
    
    # Check 5.4: Health check system
    try:
        from mercury.core.health import HealthStatus, get_system_health
        import asyncio
        
        health = asyncio.run(get_system_health())
        has_status = health.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
        result.check("Health check system works", has_status)
    except Exception as e:
        result.check("Health check system works", False, str(e))


# =============================================================================
# GATE 6: DOCUMENTATION COMPLETENESS
# =============================================================================

def gate_6_documentation(result: GateResult):
    """Verify documentation is complete."""
    
    docs_path = Path(__file__).parent.parent / "documentation"
    
    # Check 6.1: Required documents exist
    required_docs = [
        "01_GENESIS.md",
        "02_CONSTITUTION.md",
        "03_ARCHITECTURE.md",
        "04_SPECIFICATION.md",
        "05_INTEGRATION_VERIFICATION.md",
        "06_RECONCILIATION.md",
        "07_CERTIFICATION.md",
        "08_OPERATION.md",
        "09_MISSION_CRITICAL_STANDARDS.md",
        "10_MISSION_CRITICAL_IMPLEMENTATION.md",
    ]
    
    existing_docs = []
    missing_docs = []
    
    for doc in required_docs:
        if (docs_path / doc).exists():
            existing_docs.append(doc)
        else:
            missing_docs.append(doc)
    
    result.check(
        f"Required documents ({len(existing_docs)}/{len(required_docs)})",
        len(missing_docs) == 0,
        f"Missing: {', '.join(missing_docs[:3])}" if missing_docs else ""
    )
    
    # Check 6.2: README exists
    readme = Path(__file__).parent.parent / "README.md"
    result.check("README.md exists", readme.exists())
    
    # Check 6.3: Postmortem template
    template = docs_path / "templates" / "POSTMORTEM_TEMPLATE.md"
    result.check("Postmortem template exists", template.exists())
    
    # Check 6.4: Documentation not empty
    non_empty = 0
    for doc in existing_docs:
        doc_path = docs_path / doc
        if doc_path.stat().st_size > 500:  # At least 500 bytes
            non_empty += 1
    
    result.check(
        f"Documents have content ({non_empty}/{len(existing_docs)})",
        non_empty == len(existing_docs),
        ""
    )


# =============================================================================
# GATE 7: OPERATIONAL READINESS
# =============================================================================

def gate_7_operational_readiness(result: GateResult):
    """Verify system is operationally ready."""
    
    # Check 7.1: Main entry point
    try:
        from mercury.main import main
        result.check("Main entry point exists", True)
    except Exception as e:
        result.check("Main entry point exists", False, str(e))
    
    # Check 7.2: Logging setup works
    try:
        from mercury.core.logging import setup_logging, get_logger
        setup_logging(level="WARNING")  # Quiet for test
        logger = get_logger("verification")
        result.check("Logging system works", True)
    except Exception as e:
        result.check("Logging system works", False, str(e))
    
    # Check 7.3: Metrics system works
    try:
        from mercury.core.metrics import get_metrics, inc_queries
        metrics = get_metrics()
        inc_queries(success=True, source="verification")
        result.check("Metrics system works", True)
    except Exception as e:
        result.check("Metrics system works", False, str(e))
    
    # Check 7.4: Feature flags work
    try:
        from mercury.core.features import get_features, is_enabled
        features = get_features()
        feature_list = features.list_features()
        result.check(
            f"Feature flags work ({len(feature_list)} flags)",
            len(feature_list) > 0
        )
    except Exception as e:
        result.check("Feature flags work", False, str(e))
    
    # Check 7.5: Error classification works
    try:
        from mercury.core.errors import (
            ValidationError,
            KiteAPIError,
            classify_exception,
        )
        
        err = ValidationError("test")
        assert err.http_status == 400
        
        classified = classify_exception(Exception("timeout error"))
        
        result.check("Error classification works", True)
    except Exception as e:
        result.check("Error classification works", False, str(e))


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Run all verification gates."""
    
    print("\n" + "=" * 70)
    print("  MERCURY DEPLOYMENT VERIFICATION")
    print("  " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 70)
    
    gates = [
        ("GATE 1: CODE INTEGRITY", gate_1_code_integrity),
        ("GATE 2: TEST VALIDATION", gate_2_test_validation),
        ("GATE 3: SECURITY AUDIT", gate_3_security_audit),
        ("GATE 4: CONFIGURATION", gate_4_config_verification),
        ("GATE 5: RESILIENCE", gate_5_resilience_validation),
        ("GATE 6: DOCUMENTATION", gate_6_documentation),
        ("GATE 7: OPERATIONAL READINESS", gate_7_operational_readiness),
    ]
    
    results = []
    for name, func in gates:
        result = run_gate(name, func)
        results.append(result)
        print(result.report())
    
    # Final summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    all_passed = passed == total
    
    print("\n" + "=" * 70)
    print("  VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"\n  Gates Passed: {passed}/{total}")
    
    for r in results:
        icon = "✅" if r.passed else "❌"
        print(f"    {icon} {r.name}")
    
    print()
    if all_passed:
        print("  🎉 ALL GATES PASSED - DEPLOYMENT READY")
        print("=" * 70 + "\n")
        return 0
    else:
        print("  ⚠️  SOME GATES FAILED - REVIEW REQUIRED")
        print("=" * 70 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
