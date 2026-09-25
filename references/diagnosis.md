# Diagnosis: name the cause before choosing a response

Load this reference when something is going wrong and the right response is not obvious. Causes come in two kinds, and they call for different moves:

- **Inherent limits** — properties of the model or the tooling that no wording removes. Design around them, and stop trying to prompt them away.
- **Usage errors** — patterns in how the work is set up. These are correctable, and correcting them is usually the highest-leverage move available.

Use the table to pick a response. Keep the labels internal: the user needs the response, not the vocabulary.

| Symptom you can observe | Cause | Kind | Response |
| --- | --- | --- | --- |
| Progress is claimed complete, then collapses on inspection | False completion (own vocabulary) | Usage error | Write the evidence record before the claim, require a gate that has been shown to fail, and hold `? UNKNOWN` until the requirement check passes. |
| The same bug is "fixed" again and again, each attempt messier | Sunk cost | Usage error | Apply the disposal threshold: revert to the last commit and restart with a sharper constraint. |
| A rule is written down and still ignored | Selective hearing | Inherent limit | Move the rule out of prose into a mechanism: a script, a hook, or a gate that fires at the moment it applies. |
| The agent gets worse the longer a session runs | Context rot | Inherent limit | Checkpoint, write state to disk, reset the session, and reload only what the next step needs. |
| Failing tests explained away as "expected" or "will pass later" | Degrading codebase (own vocabulary) | Signal | Read the struggle as evidence about the code, not the agent: plan a refactor before retrying. |
| Two documents disagree about what the project is | Silent misalignment | Usage error | Write both claims down, have the agent state its understanding, and resolve the conflict explicitly. |
| Many things started, nothing finished | Cognitive overload | Usage error | Limit work in progress: keep one `CURRENT`, and park the rest. |
| A delivery nobody can review | Flying blind | Usage error | Run the splitting pass and hand over reviewable units. |
| The same instructions have to be repeated every session | Cannot learn | Inherent limit | Move them into durable state or `AGENTS.md` once, then reference them. |
| Confident claims about a library or API that turn out wrong | Perfect recall fallacy | Usage error | Check the current documentation, or run a small experiment, before building on the claim. |
| A single incident becomes a global rule | Obsess over rules | Usage error | Promote only recurring lessons; keep local incidents local. |

## Using the table

1. Name the symptom with evidence, not with a feeling.
2. Separate the two kinds: an inherent limit changes the **mechanism** you use; a usage error changes the **setup**.
3. Choose one response, record it in the decision log, and re-check the symptom after the next step.
4. If the symptom returns after the response, the cause was misidentified. Return to step 1 with the new evidence.

Labels in the Cause column that come from the upstream pattern collection are attributed in [CREDITS.md](../CREDITS.md).
