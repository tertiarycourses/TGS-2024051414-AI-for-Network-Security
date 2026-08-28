# Lab 11 — Document a Security Incident to the Standard

**Topic 04 — AI-Assisted Security Incident Documentation and Response**  ·  LO4  ·  knowledge K4  ·  abilities A8, A9

## Maps to

A8 · K4 — Produce an incident record that is complete enough to hand to a manager, an auditor or a regulator without a conversation attached.

## Goal

An incident that is badly documented is an incident that teaches nothing and proves nothing. Working from the top-priority cluster in Lab 10, you reconstruct the timeline from the raw evidence, classify the severity against defined criteria, and write the full incident record: what happened, when, to which assets, what was done, what the evidence is and who was accountable. You use AI to draft the narrative and then you correct it against the log — because the draft will confidently state things the evidence does not.

## What you'll produce

A complete incident record with a reconstructed evidence-based timeline, a justified severity classification, the actions taken, the evidence inventory and the notification decisions.

**Tools:** Lab 10 alert queue and raw logs, NIST SP 800-61, an incident record template, a generative AI assistant

## Step-by-step

1. Open an incident record and fill the header: incident ID, date and time of detection, detected by, reporter, current status and the assigned handler.
2. Reconstruct the timeline from the raw logs in UTC. Every entry needs a timestamp, the event, the source system and the log line that proves it. A timeline entry with no evidence reference is a claim, not a finding.
3. Separate what you know from what you infer. Write inferences as inferences — 'the account was used from an unrecognised address, which suggests credential compromise' is honest; stating the compromise as fact is not.
4. Classify the severity against written criteria: assets affected, data classification involved, business impact and whether the activity is ongoing. State the criteria you applied so the rating can be reviewed.
5. List the affected assets by name from the Lab 4 register, with their criticality and the data classification each one holds.
6. Record the response actions taken with a timestamp and the name of the person who took each one. Include the actions that were considered and rejected, and why — a reviewer will ask.
7. Build the evidence inventory: log extracts, packet captures, screenshots and system images, each with where it is stored, its hash and who has access. This is what makes the record defensible.

   ```bash
   shasum -a 256 evidence/*.pcapng evidence/*.log > evidence/MANIFEST.sha256
   ```

8. Record the notification decisions — who was informed, when, and which obligations were considered. In Singapore, consider whether the PDPA data-breach notification obligation to the PDPC and affected individuals is engaged, and record the reasoning either way.
9. Ask your AI assistant to draft the incident narrative from your timeline.

   ```bash
   Prompt: 'Draft a factual incident narrative from this evidence timeline. Use only what the timeline supports. Mark every inference explicitly as an inference. Do not speculate about attribution.'
   ```

10. Check the draft line by line against the timeline. Delete every statement the evidence does not support and every attribution claim. Record what you removed — that edit is the professional skill this lab teaches.
11. Write the lessons-learned section: what detected it, what delayed the response, and the one control change that would have prevented or caught it earlier. Feed that change back into the Lab 6 plan.

## Test it

Every timeline entry cites its evidence source, inferences are marked as inferences, the severity classification states the criteria used, and the evidence inventory carries a hash for every item. You can name at least one unsupported statement you removed from the AI draft.

## If it doesn't work

The timeline has gaps — that is a finding about your logging, so record the gap rather than guessing what filled it. Severity is contested — that means the criteria were not written down before the incident. The AI names an attacker group — remove it; attribution needs intelligence you do not have.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
