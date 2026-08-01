# Session Summary: 63fce226-ea2c-48bf-bc6d-ce1ca38ab737

**Total Hook Invocations:** 8

**Session Duration:** 17h48m1.088s

## Event Breakdown

- **ConfigChange**: 1
- **InstructionsLoaded**: 2
- **PostToolUse**: 1
- **PostToolUseFailure**: 1
- **PreToolUse**: 1
- **SessionEnd**: 1
- **SubagentStart**: 1

## Decision Breakdown

- **allow**: 1

## Top 5 Slowest Hook Executions

| # | Event | Handler | Tool | Duration (ms) |
|---|-------|---------|------|---------------|
| 1 | SessionEnd | *hook.sessionEndHandler |  | 23 |
| 2 | PostToolUse | *hook.postToolHandler | Write | 13 |
| 3 | PostToolUseFailure | *hook.postToolUseFailureHandler | Bash | 2 |
| 4 | InstructionsLoaded | *hook.instructionsLoadedHandler |  | 0 |
| 5 | InstructionsLoaded | *hook.instructionsLoadedHandler |  | 0 |

## Errors (0)

_No errors recorded._

