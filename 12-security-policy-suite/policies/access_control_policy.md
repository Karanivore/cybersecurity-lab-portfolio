# Access Control Policy

**Document owner:** CISO | **Version:** 1.0 | **Effective:** 2026-08-01
**Review cycle:** Annual | **Classification:** Internal
**ISO 27001:2022 references:** A.5.15, A.5.16, A.5.17, A.5.18, A.8.2, A.8.5

## 1. Purpose

To ensure access to information and systems is restricted to authorized
users on a least-privilege, need-to-know basis, and is granted,
reviewed, and revoked through a controlled process.

## 2. Scope

All information systems, applications, cloud services, and data stores,
and all identities (human and non-human/service accounts).

## 3. Policy Statements

### 3.1 Identity and provisioning
- Every user is assigned a unique identifier; shared accounts are
  prohibited except for approved, logged break-glass use.
- Access is provisioned via an approved request tied to a job role and
  removed within one business day of termination or role change.

### 3.2 Least privilege and role-based access
- Access follows least privilege; privileges are granted through
  role-based access control (RBAC) rather than per-user grants.
- Administrative/privileged access is separated from day-to-day accounts
  and granted only where required (see also just-in-time elevation).

### 3.3 Authentication
- Multi-factor authentication (MFA) is required for all remote access,
  administrative access, and access to systems handling Confidential or
  Restricted data.
- Passwords meet current NIST SP 800-63B guidance (length-first, breached-
  password screening, no forced periodic rotation without cause).

### 3.4 Access reviews
- System owners review user access rights at least quarterly for
  privileged accounts and at least annually for standard accounts.
- Dormant accounts (no activity for 45 days) are disabled pending review.

### 3.5 Non-human identities
- Service accounts and API keys follow least privilege, are inventoried,
  rotated on a defined schedule, and never granted standing administrator
  (`*:*`) permissions.

## 4. Roles and Responsibilities

System Owners approve access; IT Operations provisions and reviews;
the CISO defines standards and audits compliance.

## 5. Compliance

Non-compliance is handled under the Information Security Policy.
Exceptions require documented CISO approval and a compensating control.
