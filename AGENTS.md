# Working on this collection

This repository contains reusable agent skills and workflows. The delivery
workflow originated as an adaptation of
[michaelshimeles/skills](https://github.com/michaelshimeles/skills).

For ordinary work in this repository, read the skill files affected by the task
as reference. Editing a skill does not activate it. Preserve the user's current
workspace and uncommitted work; this repository does not require automatic task
branches or worktrees.

Apply [the delivery workflow](software-factory/WORKFLOW.md) only when the user
explicitly invokes the `software-factory` skill or asks for it by name. Its
isolation and delivery stages are not default repository behavior. A request to
edit workflow files is not an invocation of the workflow.

The bundled workflow is the single source of delivery rules when selected.
Installing this collection does not replace another project's `AGENTS.md` or
grant permissions. Keep project-specific architecture, branch policy and test
permissions in that project's own documents.

Update the README and affected references when changing skill behavior. Preserve
upstream attribution and bundled licenses for retained content. Do not update
user-level installed copies or publish changes unless requested.

See [Pi-specific instructions](software-factory/WORKFLOW.md#pi-specific-instructions)
for invocation and skill discovery.
