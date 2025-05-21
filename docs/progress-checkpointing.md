# Progress Checkpointing Guidelines

This document explains how to use semantic commit markers and module version tags to track
the evolution of the Codex Web-Native architecture.

## Semantic Commit Markers

- Prefix every commit message with a **coherence marker** such as `[feat]`, `[fix]`, or
  `[docs]`.
- Use these markers to indicate the nature of the change and to trigger CI checks.
- Mark significant milestones with a descriptive commit message, for example:
  
  ```
  [feat] Checkpoint 1: basic workflow chaining achieved
  ```
- Pull request titles should reflect the primary marker, e.g. `[feat] Codex architecture v1.0 release`.

## Module Versioning

- Each prompt module includes a `version` field in its front matter.
- Increment the version whenever the prompt or functionality changes.
- Use semantic versioning (`major.minor`):
  - Increment the **minor** version for small improvements.
  - Increment the **major** version for significant changes in behavior.
- Update both the module file and the registry entry when changing a version.

## Repository Tags

- Aggregate multiple changes into a release by tagging the repository.
- Example: `codex-web-native-v1.0` marks the point where multi-agent workflows became functional.

## Documentation and Logs

- Record major checkpoints in `audits/history.log.md`.
- Update the README changelog or milestone table when a new version is released.

These practices create a clear timeline of the architecture's progress and ensure that
changes are traceable across commits, modules, and tags.
