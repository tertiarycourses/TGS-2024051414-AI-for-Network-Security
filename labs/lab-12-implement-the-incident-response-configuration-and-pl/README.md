# Lab 12 — Implement the Incident Response Configuration and Playbook

**Topic 04 — AI-Assisted Security Incident Documentation and Response**  ·  LO4  ·  knowledge K4  ·  abilities A8, A9

## Maps to

A9 · A7 · K4 — Implement configurations aligned to the incident response design: containment controls, an automated playbook and the human-approval boundary.

## Goal

The final lab closes the loop. You take the incident from Lab 11 and implement the response as configuration: the containment controls that would stop it recurring, a documented SOAR-style playbook with explicit automation and approval steps, and detection rules derived from what you actually saw. You then test the playbook against a replayed scenario, measure the response time, and confirm that no automated action can cause more damage than the incident it responds to.

## What you'll produce

Implemented containment configurations, a tested incident response playbook with a defined human-approval boundary, new detection rules, and a measured response time from detection to containment.

**Tools:** Firewall and host configuration, playbook template, Lab 8 detection rules, a generative AI assistant

## Step-by-step

1. Write the containment configuration for the Lab 11 incident: the firewall rules, account actions and host isolation steps that stop this specific attack path, as commands rather than prose.

   ```bash
   iptables -I FORWARD 1 -s 192.168.56.101 -j DROP -m comment --comment 'INC-2026-001 containment'
   ```

2. Verify each containment control actually works, and record the verification command and its output. An untested containment control is an assumption.
3. Record the collateral impact of each containment action before it is ever needed. Isolating a host stops the attacker and also stops that host's business function — the responder must know which they are trading.
4. Write the playbook with the standard phases: Detect, Triage, Contain, Eradicate, Recover, Review. Each step names the trigger, the action, the owner and the expected duration.
5. Mark each step Automated, Automated-with-approval or Manual. Reversible, low-blast-radius actions can be automated; anything that takes production offline needs a named approver.
6. Define the escalation path with names and contact methods, and the time threshold that triggers each escalation. A playbook with no named person is a document, not a capability.
7. Add the detection rules from this incident to your Lab 8 ruleset so the same attack is caught earlier next time, and record the expected false-positive rate of each new rule.
8. Test the playbook against a replayed scenario. Walk every step, time it, and note where it stalls — the stall is where the playbook is wrong.
9. Measure detection-to-containment time and compare it against your target. If there is no target, set one now — a response time nobody is accountable for will drift.
10. Ask your AI assistant to review the playbook for gaps and dangerous automation.

   ```bash
   Prompt: 'Review this incident response playbook. Identify missing steps, any automated action whose blast radius exceeds the incident it responds to, and any step with no named owner. For each finding, say what you would change.'
   ```

11. Fix every genuine gap. For any automated action flagged as too broad, either narrow its scope or move it behind human approval, and record the decision.
12. Feed the whole result back: update the Lab 6 risk management plan with the control changes and re-score the affected risks. The loop from incident back to plan is what makes this a management system rather than a set of documents.

## Test it

Every containment control has a verification command and a recorded output, every playbook step names an owner and an automation level, and you can state a measured detection-to-containment time against a target. No automated step can take a production service offline without a named approver.

## If it doesn't work

The containment rule does not take effect — check the rule order; an earlier ACCEPT will win. The playbook test stalls waiting for a decision — that is the finding, so add the decision authority. The AI proposes automating everything — apply the blast-radius test yourself; that judgement is not delegable.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
