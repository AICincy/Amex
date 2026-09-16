# CourtListener API: Coverage-Skepticism Prompt

## Abstract

Investigate a public court-record question while treating search coverage as incomplete and an empty result as non-dispositive.

## Pre-Answer Examination

1. Compare the requested record type to CourtListener and RECAP coverage.
2. Ask whether a null result reflects absent data, an unsuitable query, authentication, or a source limitation.
3. Verify that every endpoint, result identity, and rate-limit claim comes from the current response.

## Required Response

Start with dry run. Report query, endpoint, source URL, record identity, coverage limitations, and exact null-result interpretation. Never characterize absence as a clean criminal record or expose a token.
