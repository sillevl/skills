# Independent reviewers in Pi

Use this setup when Pi lacks parallel sub-agent support for the factory's external
`code-review` dependency. It uses Pi's official subagent extension example, not a
copy of Matt Pocock's review instructions. Other integrations are acceptable when
they provide separate reviewer contexts and satisfy the external skill.

## Install the delegation mechanism

The example ships with the npm-installed Pi coding-agent package. Read its
`examples/extensions/subagent/README.md`, `index.ts` and `agents.ts` before loading
it. Extensions execute with Pi's operating-system permissions. The setup below
links to the installed package; retest it after updating Pi.

From this collection's root, with Pi installed globally through npm:

```bash
example="$(npm root -g)/@earendil-works/pi-coding-agent/examples/extensions/subagent"
test -f "$example/index.ts" && test -f "$example/agents.ts"
mkdir -p ~/.pi/agent/extensions/subagent ~/.pi/agent/agents
ln -s "$example/index.ts" ~/.pi/agent/extensions/subagent/index.ts
ln -s "$example/agents.ts" ~/.pi/agent/extensions/subagent/agents.ts
cp -n software-factory/references/factory-reviewer.md ~/.pi/agent/agents/factory-reviewer.md
```

Inspect existing files before replacing anything; these commands deliberately do
not force overwrites. For another Pi distribution, locate its matching official
example rather than assuming the npm path exists.

The supplied [reviewer profile](factory-reviewer.md) enables only `read`, `grep`,
`find` and `ls`. It omits a model setting so the extension inherits the dispatching
session's active model and thinking level. This limits model-callable tools; it
is not an operating-system sandbox or a restriction on which files can be read.
Only the extension and this reviewer profile are needed. Leave the example's
worker agents and workflow prompts uninstalled unless separately wanted.

Run `/reload` or start a new session. Confirm `subagent` is exposed, then ask it to
run two short independent tasks in parallel using `factory-reviewer` with
`agentScope: "user"`. Verify both actually complete. A successful CLI smoke test
does not prove that a different embedding or existing session exposes the tool.

## Use it for the two review axes

Read Matt Pocock's installed `code-review` and prepare its Standards and Spec
prompts unchanged in substance. The parent agent resolves the comparison SHA,
commit list, project standards and requirements source before dispatch.

The reviewer has no shell tool. The parent captures the specified Git diff and
commit list into temporary artifacts and supplies their paths, exact commands,
base SHA and reviewed HEAD SHA to both tasks. Give each task the sources its axis
requires, including the full smell baseline for Standards. Keep artifacts outside
the tracked workspace and inspect them for secrets before passing them on.

Use one `subagent` call with `tasks` containing two entries, both using
`factory-reviewer` and the owned task workspace as `cwd`. Give one the Standards
prompt and the other the Spec prompt, with `agentScope: "user"`. They run as
separate processes even though they share a profile name. Do not pass one
reviewer's findings into the other reviewer's prompt. Follow the external skill
if no spec is available; report the skipped axis rather than inventing one.

Inspect each child's completion and error state, not merely the parent tool's
success. Preserve separate Standards and Spec reports and follow the external
skill's aggregation rules. The parent owns authorized builds, fixes, reruns and
publishing; the reviewers only inspect the supplied state.

To disable this setup, remove only the two extension symlinks and the installed
`factory-reviewer.md` profile created above, then reload. Leave unrelated agents,
extensions, skill installations and authentication untouched.
