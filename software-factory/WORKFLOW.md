# Agent-assisted delivery workflow

This workflow is derived from
[michaelshimeles/skills](https://github.com/michaelshimeles/skills). Apply it only
when the user explicitly invokes `software-factory` or requests that skill by
name. It is not default behavior for work in this collection or a consuming
project. Reading or editing workflow files does not activate its isolation or
delivery stages.

## Scope and precedence

The core workflow is independent of model provider and coding-agent harness.
Model choice does not change delivery rules. Put harness-specific behavior in
its own section; apply [Pi instructions](#pi-specific-instructions) only in Pi.

Follow the consuming project's architecture, permissions and test-execution
policy before this collection's generic guidance. Flag conflicts before acting.
Invoking a skill or this workflow does not override an existing approval boundary.
Use the project's standing permission for checks without requesting approval on
every run; honor narrower task instructions. If execution is reserved for the
user or permission is unclear, request authorization or provide commands.
Project agent instructions define permissions; maintained testing documentation
defines commands, prerequisites and check-selection guidance.

This bundled file is the workflow source of truth for this fork and its installed
entry-point skill. Read the applicable skills at their stages. Skill names in the
core are references, not portable slash commands; read `../<skill-name>/SKILL.md`
relative to this directory. If components are installed elsewhere, locate their
actual files and confirm they belong to the intended workflow version. Resolve bundled scripts and references relative to the
skill directory. If instructions are unavailable, report that instead of
inventing them.

The adaptations so far separate scope and harness guidance, remove the web
screenshot-comparison skill and make branch selection project-aware. Overlap
handling now uses a trial risk assessment rather than a blanket stop.
Verification focuses on software tests. Delivery uses a PR handoff and the
consuming project's review requirements, with no external confidence-score gate.

## Workflow

1. **Isolate.** Read `../new-feature/SKILL.md` and follow its branch-selection rules.
   Find the project's policy and state the starting base and PR target. Verify
   an assigned isolated task workspace or create one when none is supplied,
   following the skill's ownership and cleanup rules. Without project rules or a task override,
   the default is `origin/main` with a PR targeting `main`. Record the resolved
   starting commit SHA, intended repository and task requirements for review and
   delivery; a moving branch name alone is not a fixed review point.
2. **Build.** Read `../code-structure/SKILL.md`. Establish the project's architecture,
   choose cohesive ownership and explicit public contracts, and refactor shared
   behavior only when justified. Service-layer extraction is an option, not a
   required layout. Get agreement before departing from established boundaries.
3. **Prove.** Read `../evidence-driven-testing/SKILL.md`. Map acceptance criteria to
   software tests, add or update relevant coverage, and select production builds
   or other checks when compilation also needs verification. Execute under standing
   project permission or explicit authorization. Report the tested state, commands,
   environment, outcomes and evidence source. Hand off unexecuted checks with their commands
   and distinguish software verification from physical validation.
4. **Review and ship.** Follow the review handoff below, then open the PR with
   the software-test verification summary, review results and any relevant
   supplementary evidence. Screenshots and video are not required. State missing
   verification explicitly. Follow the project's review requirements and report
   their current status; opening a PR is not approval to merge. Finish by
   presenting the PR URL and any outstanding checks or review.

## Review handoff

Use Matt Pocock's `code-review` skill from
[mattpocock/skills](https://github.com/mattpocock/skills). It is an external
installation, not a bundled copy of this collection. Locate its installed
`SKILL.md`, verify the intended source and read it fully before review.

- Supply the task's fixed starting commit SHA and the requirements/spec source.
  Review task commits against that fixed point, not a guessed `main` or a moving
  branch tip. Commit the intended changes locally before review so a HEAD-based
  review includes them; identify any outstanding uncommitted changes separately.
- Follow the skill's separate Standards and Spec reviews and preserve both in
  the handoff. Project standards override generic smell heuristics. Ensure the
  task requirements are available as a source the reviewers can inspect.
- Check the skill's prerequisites, including its issue-tracker guidance and
  parallel sub-agent capability. If requirements cannot be met, report the
  missing capability and ask for direction. Do not silently substitute a
  self-review or claim independent reviewers ran when they did not.
- Address confirmed findings within task scope. Ask about findings that require
  new product decisions, architectural deviations or changes outside scope.
  Recheck affected behavior under the project's testing policy and review the
  updated commits after fixes. If review or fixes cannot finish, report the
  remaining findings and ask rather than claiming a completed review.

This review provides findings, not a numerical confidence gate or permission to
merge. Project-required human review and CI remain separate requirements.

## Writing for humans

Read `../unslop/SKILL.md` and apply it to anything a person will read before you commit, post, or
send it: commit messages, the PR title and body, README and doc edits, code
comments, and the closing reply. It strips AI tells (em dashes, filler,
hedging, chatbot phrases, puffery, bold-label lists) and replaces fancy
words with plain ones and passive voice with active. Apply it to text you
wrote or changed, not to prose you didn't touch.

## Multi-agent rules

- Commit task changes on their assigned branch, not directly on the integration
  branch selected as their base or PR target.
- One worktree and one branch per task and per agent — never reuse or modify
  another agent's worktree, branch, or uncommitted work.
- Before implementation, follow the
  [overlap assessment](../new-feature/SKILL.md#overlap-assessment) and
  [integration responsibility](../new-feature/SKILL.md#integration-responsibility)
  rules. Inspect relevant changes, proceed with explained low-risk overlap,
  and ask about uncertain compatibility or conflicting behavior. Pause only
  affected work; shared filenames alone do not require a stop.
- Never force-push an integration branch or use plain `--force`. Use
  `--force-with-lease` only on your own task branch and within project permissions.
- Resolve lockfile conflicts by regenerating, never by hand-merging.
- Worktrees don't isolate shared resources: confirm a dev-server port
  answers *your* process before trusting it, and don't run schema
  experiments against a shared database.
- If a conflict can't be resolved confidently, stop and report instead of
  guessing.

## Completing a task

1. Keep changes limited to the assigned task.
2. Run the repo's checks within its authorization policy. Otherwise list the
   commands for the user and mark them unexecuted. Get exact commands from the
   project's maintained documentation.
3. Assemble the evidence captured along the way. Include before/after results
   when they help demonstrate the change; no screenshot table is required.
4. Commit with a clear message. If rebasing is appropriate under the project's
   policy, use the task's selected base rather than hard-coded `origin/main`.
   Resolve any changed dependency or target first. Rerun checks only within the
   project's authorization policy.
5. Complete the review handoff above before the delivery push. Commit review
   fixes and update verification where needed.
6. Normal task commits and pushes are permitted within an explicitly selected
   factory run unless project or task instructions restrict them. Verify the
   destination remote and branch match the agreed repository before pushing.
   Rewriting published history still requires agreement under the integration
   rules; use `--force-with-lease` only when authorized.
7. Open the PR explicitly in the agreed repository and targeting the agreed
   branch. For GitHub, pass `--repo <owner/repository>` and `--base <target>` to
   `gh pr create`; do not rely on fork/upstream defaults or a generic compare
   link. Ask before changing the destination. The body must explain what changed,
   how it was tested, Standards and Spec findings, missing verification, and
   risks or follow-up work. Apply `unslop` before posting.
8. Report the status of project-required checks and review, including pending,
   failed or unavailable requirements. Do not claim approval that has not occurred.
9. End by presenting the PR URL, verification and review summaries, and outstanding
   work.

Do not merge the PR unless explicitly instructed. Preserve the task worktree
until the PR is merged or closed, following the workspace-management rules in
`new-feature`. Leave harness-managed cleanup to the harness.

## Pi-specific instructions

Apply this section only when running in Pi. Keep these mechanics out of the
model-neutral core.

- Discover skills through the configured Pi locations. User-level
  `~/.agents/skills/` supports reuse across projects and worktrees; project
  `.agents/skills/` discovery stops at the repository root. A separate clone is
  not automatically a discovered skill installation.
- Use `/skill:<name>` for explicit skill invocation, such as
  `/skill:new-feature`. Automatic loading depends on discovery and frontmatter.
  `disable-model-invocation: true` makes a skill explicit-only. Do not assume
  upstream `/new-feature` command syntax is a Pi command.
- Invoke `/skill:software-factory <task>` to select the full workflow explicitly.
  Read this bundled file and component skills by their actual paths; a component
  command selects only that component. The entry point is manual-only through
  `disable-model-invocation: true`.
- Use `/reload` after editing installed skills. Changes to this clone do not
  update separately installed skill copies.
- Inspect the current branch, worktree and harness instructions before managing
  Git workspaces. In ordinary Pi sessions, create the task worktree yourself
  according to the isolation policy. If an integration already assigned a task
  worktree, use it rather than creating another one or changing another agent's
  workspace. This is a harness difference, not a model-provider difference.
- Use the tools actually exposed in the session. Browser controls, MCP services
  and delegation are optional integrations; report missing capabilities rather
  than assuming they exist or weakening the required checks silently.

## Repo-specific sections to add

Keep project-specific guidance in the target project's own instructions and
maintained documentation: commands and checks, security and architecture rules,
environment setup, test infrastructure and anything that cannot be tested locally.
Read those documents when starting a task instead of modifying this generic
workflow for each consuming project.

## Skill sources

| Skill | Source |
|---|---|
| `new-feature`, `code-structure`, `evidence-driven-testing` | this repo |
| `code-review` | External dependency from [mattpocock/skills](https://github.com/mattpocock/skills); install separately |
| `unslop` | this repo, vendored from [cursor/plugins (pstack)](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop); frontmatter edited so agents apply it unprompted (`disable-model-invocation` dropped, description scoped to text the agent writes or edits for people), body untouched |
