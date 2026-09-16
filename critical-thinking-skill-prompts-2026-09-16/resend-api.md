# Resend API: Absence-and-Authorization Prompt

## Abstract

Assess a proposed transactional-email operation by first testing whether the Resend capability is installed, authorized, and supplied with current delivery evidence.

## Pre-Answer Examination

1. Verify that the skill and its executable route actually exist before composing an operation.
2. Treat missing credentials, sender identity, recipient, idempotency, and explicit execute flag as separate blockers.
3. Distinguish non-send validation from accepted or delivered mail.

## Required Response

Return the exact unavailable-capability or authorization blocker and a sanitized request schema. Do not use historical addresses, message identifiers, or claimed delivery evidence.
