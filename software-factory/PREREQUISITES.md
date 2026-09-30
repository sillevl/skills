# Factory prerequisites

Use this guide at the start of an explicitly selected factory run. Check the
actual session's capabilities, not just installed packages or advertised tools.
Record each applicable item as available, unavailable or not yet checked, with
a short reason. Model provider choice is not a capability check.

| Stage | Required | What to check |
| --- | --- | --- |
| Start | Bundled entry point, workflow and four component skills from the intended version | Locate and read their actual files; confirm the installation source/version |
| Start | Project instructions and inspectable task requirements | Identify the architecture, branch policy, permissions and acceptance criteria sources |
| Isolate | Git and an owned task workspace | Inspect the repository, base revision, PR target, existing worktrees and workspace assignment |
| Build and prove | Tools selected by the target project's build and testing guide | Check relevant compiler/runtime versions, dependencies, services and execution permission |
| Review | Matt Pocock's separately installed `code-review` and its current prerequisites | Read its installed instructions; identify standards, requirements and a fixed comparison SHA |
| Review | Parallel sub-agent capability usable in the current session | Confirm how two separate reviewer agents will be launched and receive the review sources |
| Ship | Repository write access and an authenticated PR mechanism | Verify the intended remote, push branch, PR repository and target branch before publishing |

A skill installation supplies instructions, not a compiler, authenticated service
or delegation mechanism. Two parallel tool calls are not two independent reviewer
agents. If delegation is configured but untested, record that uncertainty; only
an actual review run establishes that reviewers completed their work.

Browser control, MCP services, extra planning skills and media capture are optional
unless the target task or project requires them. Physical-device access is never
implied by factory invocation or by a tool being available.

For Pi without a delegation integration, see
[the optional independent-reviewer setup](references/pi-review.md). It supplies
the mechanism, not the external review instructions or proof of a completed
review. Other harnesses need their own compatible mechanism.

## Missing prerequisites

Disclose known gaps before starting implementation so the user can decide whether
to configure the missing capability or authorize partial work. Pause the affected
operation until its prerequisite is available or the user agrees on a different
scope. A partial run is not a completed factory run.

Read the external review skill for its tracker configuration and reviewer setup;
this guide does not replace those instructions. If independent review cannot run,
ask for direction and report it as unavailable. Label any separately authorized
self-review as self-review, not as the factory's Standards and Spec review.

## Verification limits

Collection checks validate packaging and selected metadata rules. They do not
confirm consuming-project permissions, tool availability, reviewer independence,
installation correctness in a particular session, or agent compliance. Keep
software results separate from physical validation and from project-required
human approval.
