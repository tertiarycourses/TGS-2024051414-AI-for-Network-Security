# Lab 6 — Develop the Risk Management Plan

**Topic 02 — AI-Powered Network Risk Assessment and Management Planning**  ·  LO2  ·  knowledge K2  ·  abilities A3, A4

## Maps to

A4 · K4 — Turn the scored register into a risk management plan with treatments, owners, dates and a monitoring cadence that survives contact with reality.

## Goal

A register records risk; a plan does something about it. In this lab you assign each risk one of the four treatments — mitigate, transfer, avoid or accept — select the specific controls that implement the mitigation, name an owner and a target date for each, and map the whole plan onto the NIST Cybersecurity Framework functions so that the coverage gaps become visible. You then use AI to draft the management summary and you edit it into something you would actually sign.

## What you'll produce

A risk management plan: treatment decisions with named controls, owners, target dates and success criteria; a NIST CSF coverage map; and a one-page management summary.

**Tools:** Lab 5 risk register, NIST CSF 2.0, a spreadsheet, a generative AI assistant

## Step-by-step

1. Assign each risk in the register one of the four treatments — Mitigate, Transfer, Avoid or Accept. Every risk gets exactly one; nothing may be left blank.
2. Every Accept decision needs a named accepting authority and a written rationale. An accepted risk with no name against it is an ignored risk.
3. For each Mitigate decision, name the specific control that will reduce the risk — not 'improve security', but 'disable Telnet on the three switches and enforce SSHv2 with key authentication'.
4. State the control type for each: preventive, detective or corrective. A plan made only of detective controls will find every breach and stop none of them.
5. Add an owner, a target date and a success criterion to every treatment. The success criterion must be testable — 'no Telnet listener on any managed switch, verified by Nmap' is testable; 'switches hardened' is not.
6. Map every planned control onto the NIST CSF 2.0 functions — Govern, Identify, Protect, Detect, Respond, Recover — and count the controls in each. The thin function is your real gap.

   → <https://www.nist.gov/cyberframework>

7. Fill the thinnest function with at least one concrete control. Most first-draft plans are heavy on Protect and empty on Recover.
8. Set the monitoring cadence: which risks are reviewed monthly, which quarterly, and what event forces an out-of-cycle review.
9. Ask your AI assistant to draft a one-page management summary of the plan for a non-technical audience.

   ```bash
   Prompt: 'Summarise this risk management plan for a non-technical executive in under 400 words: the top three exposures in business terms, what we are doing about each, what it needs, and what happens if we do nothing. No jargon.'
   ```

10. Edit the draft hard. Cut anything the register does not support, and add the one thing the AI could not know — what this actually costs and who has to approve it.

## Test it

Every risk carries a treatment, and every Mitigate carries a named control, an owner, a date and a testable success criterion. Your NIST CSF map has at least one control under all six functions, and the management summary states the top three exposures in business language without jargon.

## If it doesn't work

Everything is Mitigate — some risks are genuinely cheaper to accept or transfer; a plan that mitigates everything will be funded for nothing. Success criteria are unverifiable — rewrite each one as a test someone could run. Recover is empty — add backup restoration testing.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
