# Reddit AutoModerator YAML adversarial prompt

Audit a supplied AutoModerator YAML configuration containing an invalid regex,
an overbroad removal rule, a duplicate action, and a rule that risks exposing
moderator logic. Re-fetch current official Reddit and AutoModerator guidance
where required. Produce corrected reviewable YAML, explain each rule's trigger
and failure mode, and provide positive and negative test cases. Detect YAML
syntax and regex hazards without publishing or pasting to Reddit. Do not infer
current subreddit policy from bundled examples or claim a wiki update occurred.
