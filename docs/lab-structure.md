# Lab guide structure

Each lab uses the following sections. First complete [Common prerequisites](00-common-setup.md) and the relevant [target setup module](00-common-setup.md#choose-a-target-setup). App installation belongs in those setup modules; lab guides link to them and keep only exercise-specific preparation.

1. **What this lab does:** target, scenario, learning objective, completion criteria and verification status.
2. **Before you begin:** lab-specific accounts, tools, starting state and safety limits.
3. **Understand the scenario:** the relevant feature and security boundary.
4. **Guided walkthrough:** use numbered `###` headings for the major steps. Each step says where to work, what to do, and what to check. Include commands or screen instructions where needed, then state the expected result or when to stop. Add a relevant screenshot after the step it illustrates. The number of steps can vary by lab.
5. **Hints and troubleshooting:** optional guidance and known obstacles.
6. **Evidence:** sanitized material and findings to submit.
7. **Vulnerability and Impact:** describe the security weakness, the demonstrated or potential impact, and the limits of the evidence.
8. **Cleanup and review:** restore changed state and answer questions about remediation.

A walkthrough is written for someone who has never used the tool. Commands must be complete and runnable in order, including the variables they depend on, and each one must be followed by the output or screen state that shows it worked. Prefer a concrete value the learner can paste over a description of the value. Do not make the core exercise depend on asking the instructor: reserve escalation for an environment that does not match the setup, an unsafe state, or a step the learner is not authorized to perform.

Use screenshots from an actual pilot, redact sensitive data, and place each image next to the step it explains. Screenshots, durations and observed results require a pilot. Label source-derived expectations as unverified until the exercise has been run, and say which parts of a partly piloted lab were observed.
