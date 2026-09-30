# Skills

A collection of reusable agent skills and workflows, derived from
[michaelshimeles/skills](https://github.com/michaelshimeles/skills).

The `software-factory` skill is the manual entry point for the delivery workflow.
Other skills can be added independently. External collections can remain
installed from their original sources.

The goal is repeatable delivery with clear human involvement. The workflow is independent of model and coding-agent harness. OpenAI, Anthropic and other model choices follow the same delivery rules. Harness-specific instructions belong in separate sections, starting with Pi.

Each skill is a folder containing `SKILL.md` with frontmatter and instructions, using the [Agent Skills format](https://agentskills.io/specification). Discovery, automatic loading and command syntax depend on the harness.

## Scope of this fork

The workflow is opt-in through the manual `software-factory` skill. Ordinary requests, including edits to this repository, do not activate its task-branch or worktree requirements. Within the selected workflow, worktree handling depends on the workspace capabilities actually provided, not a particular harness or model name.

The web screenshot-comparison skill and its upload scripts have been removed. Evidence should fit the change: test output, serial logs, protocol traces, terminal captures or hardware observations. A screenshot comparison table is not a required delivery artifact.

Branch selection now follows project-specific policy, with `origin/main` and a PR to `main` as the fallback. Overlap handling is now a trial risk-based policy: inspect relevant changes, proceed with compatible independent edits, and ask about unclear compatibility, conflicting behavior or unresolved dependencies. Each task agent owns compatibility with its agreed base; cross-branch coordination and published-history rewrites require user agreement. Verification now focuses on software tests, with no bundled media recorder. Delivery includes Matt Pocock's separate Standards and Spec review, followed by verification and review summaries in the PR handoff. Project review requirements still apply; there is no third-party confidence-score gate. The consuming project's architecture, permissions and test-execution policy take precedence over this collection's generic guidance.

## Software factory skills

The factory uses these bundled skills for defined responsibilities. Their detailed
instructions remain in their own files; this overview does not replace them.

| Skill | Factory responsibility | Expected outcome |
| --- | --- | --- |
| `software-factory` | Manual entry point and stage routing | A task follows the maintained workflow and project permissions |
| `new-feature` | Branch selection, workspace isolation and overlap assessment | An owned task workspace with an agreed base, PR target and integration plan |
| `code-structure` | Architecture-aware implementation guidance | Cohesive ownership and public contracts within project boundaries |
| `evidence-driven-testing` | Test selection, regression coverage, compilation and result reporting | A verification summary with evidence sources and explicit gaps |
| `unslop` | Editing human-facing prose | Clear task reports, documentation and commit/PR text |

The factory also requires Matt Pocock's external `code-review` skill for separate
Standards and Spec review before delivery. It is not bundled or owned here; see
[the review dependency and its prerequisites](#external-review-dependency).

### [software-factory](software-factory/SKILL.md)

Manual entry point for the complete delivery workflow. It reads the bundled
[WORKFLOW.md](software-factory/WORKFLOW.md), follows the target project's rules
and loads component skills at the relevant stages. Its frontmatter sets
`disable-model-invocation: true`; the agent should not start it automatically.

Install it together with `new-feature`, `code-structure`, `evidence-driven-testing`
and `unslop` from the same version of this collection. The bundled workflow travels
with the skill, so an installed copy does not depend on this repository's root
`AGENTS.md` being present.

### [code-structure](code-structure/SKILL.md)

Architecture-aware guidance for ownership, public contracts and shared capabilities. Read the project's architectural rules and inspect existing modules before choosing a boundary. Service-layer extraction is an option, not a required layout.

Use it when:

- Deciding which module owns behavior or shared policy
- Evaluating whether similar code represents a genuinely shared capability
- Designing dependencies, lifetimes and failure semantics at a public interface
- Refactoring callers incrementally without creating speculative abstractions

The skill preserves project terminology and dependency rules, requires agreement before architectural deviations, and follows the project's test-execution policy.

### [evidence-driven-testing](evidence-driven-testing/SKILL.md)

Software-test verification using the project's existing frameworks and commands. Map changed acceptance criteria to relevant unit, integration or end-to-end tests, add regression coverage, and run checks only within project authorization. Use standing project permission without asking again for each allowed run; otherwise provide commands or request authorization. Select production compilation checks too when host tests cannot cover the changed code.

Permissions belong in the target project's agent instructions. Suite choices, commands and prerequisites belong in its maintained testing guide. This collection does not hard-code a firmware project's host, emulation or physical-target scheme.

Use it when implementing features, fixing bugs, refactoring or preparing verification for review. Reports identify the tested revision, commands, environment, results and whether evidence was agent-observed, user-reported or CI-observed. Missing checks, skipped suites and limits of emulation or fakes remain explicit.

The skill name is retained for continuity, but screen recording, browser-capture instructions, upload tooling and recorder-specific tests have been removed. It has no bundled runtime dependencies; the target project's test tooling supplies them. Physical behavior may still need separate validation, which software-test results must not claim to prove.

### [new-feature](new-feature/SKILL.md)

The manual-only isolation stage of an explicitly selected `software-factory` workflow. It starts a task in an isolated Git worktree after searching the project's instructions and development documentation for branching policy. It states the starting base and PR target before creating the workspace, defaults to `origin/main` and a PR to `main` when no policy or override exists, and asks when selection is ambiguous or depends on an unmerged feature. It also covers unique task naming, risk-based overlap assessment, integration responsibility, dependency setup and cleanup after merge. See its [overlap rules](new-feature/SKILL.md#overlap-assessment); shared filenames alone no longer block work.

The factory reads this skill during its isolation stage. It is not an automatic
trigger for new features or ordinary repository work. Invoking the component
alone does not authorize its isolation stage outside the factory workflow.

The skill verifies workspace assignment, branch policy and ownership before creating isolation. If an isolated task worktree is already supplied, it preserves that workspace and leaves harness-managed cleanup to the harness. Otherwise, the agent creates and manages its own task worktree. Isolated edits do not eliminate integration conflicts between branches.

### [unslop](unslop/SKILL.md)

Edits prose to remove AI tells and put a human voice back in. It names 31 patterns to catch (puffery, filler, hedging, chatbot phrases, em dashes, colons as connectors, bold and emoji overuse, abstract metaphor nouns, passive voice) and a short checklist for adding opinion and rhythm, applied as a four-step loop: scan, rewrite, add soul, self-audit.

Use it when:

- Writing anything a person will read: commit messages, PR titles and bodies, docs, README edits, code comments, chat replies
- Cleaning up existing text that reads machine-made

> Vendored from [cursor/plugins (pstack)](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop) (MIT, license included in the folder). The body matches upstream; the frontmatter has two edits so agents apply the skill on their own instead of waiting for a typed `/unslop`. We dropped the `disable-model-invocation: true` line, and the description now names the trigger (text you write or edit for a human reader) in place of upstream's "any writing. Must always apply.", so auto-invocation matches the scope `AGENTS.md` gives it. Restore the flag if you want slash-command-only behavior.

## Optional companion skills

These references point to useful skills from
[Matt Pocock's collection](https://github.com/mattpocock/skills). Keep them installed
and updated from their original source rather than copying them here. They are
not additional factory dependencies or mandatory stages.

### Requirements, planning and exploration

| Skill | Useful for |
| --- | --- |
| `grilling` | Resolving open requirements and design decisions through an interview |
| `grill-with-docs` | Clarifying decisions while maintaining ADRs and glossary documentation |
| `wayfinder` | Mapping larger work into decision tickets and resolving dependencies over multiple sessions |
| `to-spec` | Turning an agreed conversation into a specification |
| `to-tickets` | Breaking a plan or specification into executable tickets with blocking edges |
| `prototype` | Exploring a design question with a throwaway implementation |
| `research` | Investigating uncertain facts against primary sources |

### Implementation and problem-solving

| Skill | Useful for |
| --- | --- |
| `codebase-design` | Exploring interface depth, testability and seam placement |
| `tdd` | An explicitly chosen test-first implementation approach |
| `diagnosing-bugs` | Building a reproducible feedback loop for difficult failures |
| `resolving-merge-conflicts` | Handling an active merge or rebase conflict |
| `wizard` | Guiding a human through setup steps the agent cannot perform itself |
| `implement` | An alternative spec/ticket-driven execution process; inspect its rules before combining it with the factory |

### Maintenance and continuity

| Skill | Useful for |
| --- | --- |
| `writing-for-agents` | Maintaining predictable, concise agent instructions |
| `handoff` | Preparing a fresh session to continue without duplicating existing artifacts |
| `retro` | Reviewing completed sessions and proposing improvements to the agent environment |

Consult a companion when its purpose fits the task or the user explicitly selects
it, not simply because it appears in this list. This reference does not change
upstream frontmatter, invocation settings or project permissions. Read the actual
skill before use: tracker publication, human checkpoints, sub-agents and other
capabilities may have prerequisites or side effects. Preserve project vocabulary
and architecture; resolve conflicting execution rules before combining workflows.

Other skills in Matt Pocock's collection remain available independently; this
list is a reference selection, not a replacement catalog or an instruction to
install everything.

## Workflow

[`software-factory/WORKFLOW.md`](software-factory/WORKFLOW.md) is the authoritative workflow for this collection; [`AGENTS.md`](AGENTS.md) makes its activation explicitly opt-in, including for repository work. It connects isolate (`new-feature`), build (`code-structure`), prove (`evidence-driven-testing`) and review/ship using Matt Pocock's external `code-review` skill and a PR handoff, with `unslop` for human-facing text. Project review and merge requirements still apply; opening a PR is not review approval.

Within an explicitly invoked factory run, normal task commits and pushes remain
enabled unless project or task instructions restrict them. Published-history
rewrites and merging still need the applicable authorization. Delivery verifies
the destination and explicitly targets the agreed repository when creating a PR,
rather than relying on fork defaults.

To use it in another project, reference or adapt it alongside that project's existing instructions. Keep project architecture and safety rules authoritative rather than replacing them with this file. Read the workflow and relevant skills instead of pasting an older upstream prompt into each task.

## Maintaining this collection

Run the collection checks before handing off changes. They need Python 3.10 or
newer and the pinned development dependency; skill installation does not need
Python or PyYAML.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python tools/check_collection.py
git diff --check
```

Run these from the repository root. The checker validates required skill files,
YAML frontmatter, matching names, manual-only flags, bundled references and local
inline Markdown links with ATX heading anchors. It rejects removed skill
directories and their `/skill:` invocations. External URLs, reference-style links
and arbitrary prose/code file references are outside its scope. GitHub Actions
runs the same tests and checks on pushes and pull requests.

For runtime capability checks, use the bundled
[factory prerequisites guide](software-factory/PREREQUISITES.md). For behavioral
validation, use [the trial scenarios and record format](docs/trials.md). Collection
checks cannot prove that an agent follows the workflow. No trial or review result
is implied by a successful packaging check.

## Installation

This collection uses standard `SKILL.md` directories and is compatible with the
[`skills` CLI](https://github.com/vercel-labs/skills). No custom installer or
installation skill is required. You need Node.js with npm/npx, access to the source
and permission to write to the selected installation directory.

Install the delivery workflow's five skills: `software-factory`, `new-feature`,
`code-structure`, `evidence-driven-testing` and `unslop`. The entry point needs its
component skills and bundled `WORKFLOW.md` from the same version.

### External review dependency

Install [Matt Pocock's `code-review`](https://github.com/mattpocock/skills)
separately if it is not already present:

```bash
npx skills add mattpocock/skills --global --agent pi --skill code-review
```

Keep it managed from its original source rather than vendoring it here. The
review skill requires a fixed comparison point, a requirements source and
parallel sub-agent capability, and includes project issue-tracker setup guidance.
Read its installed instructions for current prerequisites. If the harness cannot
perform the required review, the factory reports the gap and asks for direction.
It does not fabricate an independent review or silently replace it. For Pi,
[the optional reviewer setup](software-factory/references/pi-review.md) explains
how to enable its official subagent extension with a read-only reviewer profile.

Removal or update commands for this collection's five skills below do not remove
or update this external dependency. Review dependency updates separately.

### Install from a local checkout

While developing this workflow, install the current local files. From this
repository's root:

```bash
npx skills add . --global --agent pi --skill \
  software-factory new-feature code-structure evidence-driven-testing unslop
```

Or supply the checkout's absolute path from any directory:

```bash
npx skills add /path/to/skills \
  --global --agent pi --skill \
  software-factory new-feature code-structure evidence-driven-testing unslop
```

The explicit names select only the delivery workflow's skills, even as this
repository grows. Use `--skill '*'` only if you intend to install every skill in
this repository. These commands do not remove unrelated collections. Review any
overwrite prompts if an identically named skill is installed from another source.

### Install from GitHub

After publishing the intended version to this fork's default branch:

```bash
npx skills add sillevl/skills \
  --global --agent pi --skill \
  software-factory new-feature code-structure evidence-driven-testing unslop
```

This installs published files, not unpushed commits or local edits. Use local
installation while changes exist only in your checkout. For a deliberate
non-default branch, tag or commit, use a GitHub tree URL for that revision as the
source rather than assuming the shorthand selects it.

Before installing, inspect the skills the source exposes:

```bash
npx skills add sillevl/skills --list
```

To use existing SSH authentication, the source can instead be
`git@github.com:sillevl/skills.git`.

### Scope and other harnesses

`--global --agent pi` installs to Pi's user-level skills location,
`~/.agents/skills/`, so the workflow is available across projects and worktrees.
Omit `--global` to install project-locally; review generated skill files and
installer metadata before committing them to a consuming project.

For another supported harness, replace `pi` with its installer agent identifier.
Model provider selection is separate from the harness. Avoid `--all` unless you
intend to install to every supported agent, not just Pi.

The installer can link agent directories to its canonical installed copies or
copy files with `--copy`. Those links do not imply a live link to your development
checkout. Installing skills does not activate the entire workflow or replace a
project's instructions. Review the skills before enabling them, especially rules
that run commands or publish changes.

### Updates

For local development, rerun the local `skills add` command after changing this
checkout. Do not assume installed copies track local edits automatically.

For a published installation, update only this collection's skills:

```bash
npx skills update --global \
  software-factory new-feature code-structure evidence-driven-testing unslop
```

Review the recorded source and any prompts. Updates follow installer provenance;
if it still identifies the original upstream or a local source, reinstall from
the intended fork/version instead. An unrestricted `npx skills update` can also
update unrelated collections, such as Matt Pocock's skills.

After installation or updates, run `/reload` in Pi or restart it. Inspect startup
diagnostics and confirm `/skill:software-factory` is available.

### Inspect and remove

List installed user-level skills for Pi:

```bash
npx skills list --global --agent pi
```

Remove only this collection's five skills through the installer:

```bash
npx skills remove --global --agent pi --skill \
  software-factory new-feature code-structure evidence-driven-testing unslop
```

This preserves unrelated skills. Reload or restart Pi after removal. Prefer the
installer's remove command over deleting directories manually so installation
records are managed too. Inspect any remaining metadata when cleaning up a
previous manual deletion.

These commands are installation guidance, not evidence that an installation or
update has been performed.

### Pi-specific usage

Pi can discover user-level skills under `~/.agents/skills/` and project skills under `.agents/skills/`. Project discovery stops at the Git repository root, so a sibling clone is not automatically an installed skill collection. Use user-level installation when skills must also be available in new worktrees.

Invoke a discovered skill explicitly with Pi's command syntax:

```text
/skill:code-structure <design question>
```

Start the complete workflow manually:

```text
/skill:software-factory Implement <feature and acceptance criteria>
```

The entry point and `new-feature` isolation component are manual-only. Task branches and worktrees are required by this collection only within the explicitly selected factory workflow. Other component skills retain their existing invocation settings; calling a component alone does not start the complete workflow. Run `/reload` after changing installed skills. Other supporting harnesses use their own explicit invocation syntax.

If the skill is not installed, explicitly ask the agent to follow `software-factory/SKILL.md` in this checkout. It reads the same bundled rules; there is no need to paste the workflow into your prompt.

See the [Pi instructions in the workflow](software-factory/WORKFLOW.md#pi-specific-instructions) and [Pi skill documentation](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md). Editing this clone does not update existing copies in `~/.agents/skills/`.

## Adding a new skill

1. Create a folder named after the skill (kebab-case).
2. Add a `SKILL.md` with `name` and `description` frontmatter. Make the description trigger-focused ("Use when...") so a supporting harness can advertise when the skill applies.
3. Keep instructions concise and actionable; link out to reference files in the folder if they get long.
