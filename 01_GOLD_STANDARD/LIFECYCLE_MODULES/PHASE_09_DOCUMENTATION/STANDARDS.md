# PHASE 09: SECURITY REVIEW
## Standards

**Purpose:** Security standards and requirements for release approval

---

## MANDATORY SECURITY REQUIREMENTS

### Zero Tolerance Items

The following MUST have ZERO findings before release:

| Category | Requirement |
|----------|-------------|
| Critical vulnerabilities | 0 open |
| High vulnerabilities | 0 open |
| Hardcoded secrets | 0 detected |
| SQL injection | 0 detected |
| Authentication bypass | 0 detected |
| Data exposure | 0 PII/secrets exposed |

### Required Controls

Every system MUST implement:

| Control | Requirement | Evidence |
|---------|-------------|----------|
| Authentication | Industry standard | Implementation doc |
| Authorization | Least privilege | ACL tests |
| Encryption (transit) | TLS 1.2+ | Certificate config |
| Encryption (rest) | AES-256+ | Key management doc |
| Logging | Security events | Log sample |
| Input validation | All inputs | Validation code |

---

## AUTHENTICATION STANDARDS

### Password Policy

| Requirement | Minimum |
|-------------|---------|
| Length | 12 characters |
| Complexity | Upper + Lower + Number + Special |
| History | Last 10 passwords |
| Max age | 90 days |
| Lockout threshold | 5 failed attempts |
| Lockout duration | 30 minutes |

### Session Management

| Requirement | Standard |
|-------------|----------|
| Session ID | 128-bit random |
| Storage | Server-side |
| Cookie flags | Secure, HttpOnly, SameSite |
| Idle timeout | 30 minutes |
| Absolute timeout | 24 hours |
| Regeneration | After authentication |

### Multi-Factor Authentication

| Requirement | Standard |
|-------------|----------|
| Admin accounts | Required |
| Sensitive operations | Required |
| User accounts | Recommended |
| Methods | TOTP, WebAuthn |

---

## AUTHORIZATION STANDARDS

### Access Control Model

| Principle | Implementation |
|-----------|----------------|
| Default deny | No implicit permissions |
| Least privilege | Minimum necessary |
| Separation of duties | No single all-powerful role |
| Role-based | Permissions via roles |
| Resource-level | Check ownership/membership |

### Permission Checking

```markdown
## Required Authorization Checks

Every protected endpoint MUST:
1. Verify authentication
2. Check role permission
3. Verify resource ownership (if applicable)
4. Log access attempt
```

---

## CRYPTOGRAPHY STANDARDS

### Encryption Algorithms

| Purpose | Approved | Prohibited |
|---------|----------|------------|
| Symmetric | AES-256 | DES, 3DES, RC4 |
| Asymmetric | RSA-2048+, ECDSA P-256+ | RSA-1024 |
| Hashing | SHA-256+, bcrypt, Argon2 | MD5, SHA-1 |
| Key exchange | ECDHE | DHE-1024 |

### TLS Configuration

| Setting | Requirement |
|---------|-------------|
| Minimum version | TLS 1.2 |
| Preferred version | TLS 1.3 |
| Cipher suites | AEAD only |
| Certificate | Valid, not self-signed |
| HSTS | Enabled, max-age 1 year |

### Key Management

| Requirement | Standard |
|-------------|----------|
| Storage | HSM or KMS |
| Rotation | Annual minimum |
| Access | Audited, restricted |
| Backup | Encrypted, separate location |

---

## INPUT VALIDATION STANDARDS

### Validation Requirements

| Input Type | Validation |
|------------|------------|
| String | Length, character set, encoding |
| Number | Range, type, precision |
| Date | Format, range, validity |
| File | Type, size, content, name |
| Email | Format, domain |
| URL | Protocol, domain whitelist |

### Output Encoding

| Context | Encoding |
|---------|----------|
| HTML body | HTML entity encode |
| HTML attribute | Attribute encode |
| JavaScript | JavaScript encode |
| URL | URL encode |
| CSS | CSS encode |
| SQL | Parameterized queries |

---

## LOGGING STANDARDS

### Security Events to Log

| Event | Details Required |
|-------|------------------|
| Authentication success | User, time, IP, method |
| Authentication failure | User, time, IP, reason |
| Authorization failure | User, resource, action |
| Privilege change | User, old, new, by whom |
| Admin actions | User, action, target |
| Data access | User, data type, action |
| Security events | Type, severity, details |

### Log Protection

| Requirement | Standard |
|-------------|----------|
| Integrity | Write-once, append-only |
| Confidentiality | Access restricted |
| Retention | Minimum 1 year |
| Backup | Regular, encrypted |

### Log Format

```json
{
  "timestamp": "ISO-8601",
  "level": "INFO|WARN|ERROR",
  "event_type": "SECURITY|AUTH|ACCESS",
  "user_id": "uuid",
  "ip_address": "x.x.x.x",
  "action": "action_name",
  "resource": "resource_id",
  "result": "SUCCESS|FAILURE",
  "details": {}
}
```

---

## VULNERABILITY MANAGEMENT STANDARDS

### Severity Definitions

| Severity | CVSS | Response Time |
|----------|------|---------------|
| Critical | 9.0-10.0 | 24 hours |
| High | 7.0-8.9 | 7 days |
| Medium | 4.0-6.9 | 30 days |
| Low | 0.1-3.9 | 90 days |

### Scan Requirements

| Scan Type | Frequency | Blocker |
|-----------|-----------|---------|
| SAST | Every build | High+ |
| DAST | Weekly | High+ |
| Dependency | Daily | Critical |
| Container | Every build | High+ |

### Exception Process

Exceptions MUST document:
- Risk accepted
- Justification
- Mitigating controls
- Review date
- Approver signature

```markdown
## Security Exception: SEC-EXC-[NNN]

**Finding:** [Reference]
**Risk Score:** [CVSS]
**Accepted By:** [Name/Role]
**Date:** [Date]
**Review Date:** [Date]

**Justification:**
[Why this risk is acceptable]

**Mitigating Controls:**
[What reduces the risk]

**Signature:** _____________
```

---

## THIRD-PARTY SECURITY STANDARDS

### Vendor Assessment

Before integrating third-party:
- [ ] Security questionnaire completed
- [ ] SOC 2 or equivalent reviewed
- [ ] Data processing agreement signed
- [ ] API security reviewed
- [ ] Incident response plan confirmed

### Dependency Requirements

| Requirement | Standard |
|-------------|----------|
| Source | Verified repositories only |
| License | Approved license types |
| Maintenance | Actively maintained |
| Vulnerabilities | No known critical/high |
| Lock files | Version pinned |

---

## SECURITY TESTING STANDARDS

### Required Test Coverage

| Test Type | Coverage | Frequency |
|-----------|----------|-----------|
| Authentication | 100% | Every release |
| Authorization | 100% | Every release |
| Input validation | All inputs | Every release |
| Error handling | Sensitive paths | Every release |
| Cryptography | All crypto ops | Every release |

### Test Evidence

Every security control MUST have:
- Test case documented
- Test execution recorded
- Result verified
- Evidence preserved

---

*STANDARDS v1.0 | PHASE 09 | Gold Standard System*
