# Lab guide structure

Each lab uses the following sections. First complete [Common prerequisites](00-common-setup.md) and the relevant [target setup module](00-common-setup.md#choose-a-target-setup). App installation belongs in those setup modules; lab guides link to them and keep only exercise-specific preparation.

1. **What this lab does:** target, scenario, learning objective, completion criteria and verification status.
2. **Before you begin:** lab-specific accounts, tools, starting state and safety limits. Tool lists may appear here as a `### Tools needed` subsection.
3. **Understand the scenario:** the relevant feature and security boundary.
4. **Guided walkthrough:** use numbered `###` headings for the major steps. Each step states **Where** the learner works, the action to take, and the check or expected result. Include commands or screen instructions where needed, then state the expected result or when to stop. Add a relevant screenshot after the step it illustrates. The number of steps can vary by lab.
5. **Troubleshooting:** known obstacles and safe recovery steps.
6. **Evidence:** sanitized material and findings to submit, followed by the optional collapsible **Hints** block.
7. **Vulnerability and Impact:** describe the security weakness, the demonstrated or potential impact, and the limits of the evidence.
8. **Cleanup and review:** restore changed state and answer questions about remediation.

A walkthrough is written for someone who has never used the tool. Commands must be complete and runnable in order, including the variables they depend on, and each one must be followed by the output or screen state that shows it worked. Prefer a concrete value the learner can paste over a description of the value. Do not make the core exercise depend on external help: reserve escalation for an environment that does not match the setup, an unsafe state, or a step the learner is not authorized to perform.

### Step and placeholder conventions

- Begin each numbered walkthrough step with a **Where:** line naming the host shell, the emulator screen, the browser, or the repository checkout.
- Define a placeholder at its first use. Use `<angle-brackets>` for a value the learner reads from their own environment, and `$UPPER_CASE` for a shell variable the learner sets. Never leave a placeholder in a command without saying where its value comes from.
- Put the observable check in an `!!! success "Expected"` or `!!! info "Expected"` callout immediately after the command or screen action.
- When a result is source-derived rather than observed in the documented run, label it as source-derived in that step.

### Evidence checklist format

Write the Evidence section as a fill-in checklist. Each item names the artifact or observation, cites the step or command that produces it, and follows the existing redaction rules:

```markdown
- [ ] **Profile response:** the redacted `200` body from the request in Step 2.
- [ ] **Comparison:** the status codes from Steps 4 and 5.
```

Do not add an Evidence item that the documented setup cannot produce.

Use screenshots from an actual run, redact sensitive data, and place each image next to the step it explains. A screenshot, duration or observed result must come from that run. Where a result is source-derived rather than observed, say so in the step.
