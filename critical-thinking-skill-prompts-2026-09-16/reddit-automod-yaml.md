# Reddit AutoModerator YAML: Rule-Failure Prompt

## Abstract

Audit AutoModerator YAML by presuming that an apparently narrow rule may have a bypass, false-positive path, syntax fault, or hidden policy disclosure.

## Pre-Answer Examination

1. Compile every regex and parse every YAML document.
2. For each rule, state a positive match, negative match, bypass candidate, and false-positive risk.
3. Separate repository policy from verified current subreddit policy.

## Required Response

Produce corrected reviewable YAML, rule rationale, and tests. Do not publish, paste, or claim a live wiki update.
