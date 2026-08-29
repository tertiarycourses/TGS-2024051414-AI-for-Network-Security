# Lab 5 — AI-Assisted Risk Scoring and the Risk Register

**Topic 02 — AI-Powered Network Risk Assessment and Management Planning**  ·  LO2  ·  knowledge K2  ·  abilities A3, A4

## Maps to

A2 · A4 · K4 — Combine the asset register and the vulnerability worklist into a scored risk register, using AI to sharpen the likelihood estimate.

## Goal

A risk is not a vulnerability. A risk is a threat exploiting a vulnerability against an asset, with a likelihood and an impact. In this lab you join Lab 3's vulnerabilities to Lab 4's assets to produce a proper risk register, score each entry on a 5x5 likelihood-impact matrix, and use an AI assistant to pressure-test your likelihood estimates against current threat intelligence. You end with a heat map that shows management where the real exposure is.

## What you'll produce

A scored risk register with inherent risk, existing controls and residual risk for every entry, plus a 5x5 heat map showing the distribution.

**Tools:** Lab 3 worklist, Lab 4 asset register, the Cybersecurity Simulator (alfredang.github.io/cybersecuritysimulator), a spreadsheet, a generative AI assistant

## Step-by-step

1. Create the risk register with the columns Risk ID, Asset, Threat, Vulnerability, Existing Controls, Likelihood (1-5), Impact (1-5), Inherent Risk, Treatment, Owner, Target Date, Residual Risk.
2. Write each risk as a full sentence before you score it: 'A [threat actor] exploits [vulnerability] on [asset], resulting in [consequence].' A risk you cannot phrase this way is not yet a risk.
3. Before you score likelihood from a spreadsheet, see the attacks work. Open the Cybersecurity Simulator and run the Phishing, SQL Injection and Social Engineering modules — note for each how little the attacker needs and how plausible the lure is. Likelihood is a judgement about human and technical reality, not a number you invent.

   → <https://alfredang.github.io/cybersecuritysimulator/>

4. Use the simulator's Password Strength Lab to test three passwords of the kind your organisation actually allows. Record the estimated crack time — that figure is the evidence behind any credential-attack likelihood score you write.

   → <https://alfredang.github.io/cybersecuritysimulator/>

5. Score Likelihood 1-5 using evidence — is the vulnerability on the CISA KEV list, is the asset internet-facing, is there a public exploit, does an existing control reduce the chance, and what did the simulator show you about how easily this attack lands?
6. Score Impact 1-5 from the asset's criticality in Lab 4, adjusted for what this specific threat would actually do to it.
7. Compute Inherent Risk as Likelihood x Impact, and band it: 1-4 Low, 5-9 Medium, 10-14 High, 15-25 Critical.

   ```bash
   Inherent Risk = Likelihood × Impact
   ```

8. Record the controls already in place for each risk, then re-score to get Residual Risk. The gap between inherent and residual is exactly what your existing controls are buying you.
9. Ask your AI assistant to challenge your likelihood scores against current threat activity.

   ```bash
   Prompt: 'Here is a risk register with likelihood scores from 1 to 5. For each risk, state whether current threat intelligence suggests my likelihood is too high, too low or about right, and give the reason. Note where you are uncertain.'
   ```

10. Adjust the scores you agree with and document the ones you rejected. A risk register that is never challenged is a risk register nobody believes.
11. Build the 5x5 heat map — likelihood on one axis, impact on the other, each cell counting the risks that land in it — and identify which quadrant carries your exposure.
12. Sort by residual risk and confirm the top five are the risks you would genuinely lose sleep over. If they are not, your scoring is wrong.

## Test it

Every risk is written as a complete threat-vulnerability-asset-consequence sentence and carries both an inherent and a residual score. Your heat map shows a real spread rather than everything clustered in one cell, and you can justify your top five to a manager.

## If it doesn't work

Inherent and residual are identical everywhere — you have not recorded the existing controls. All risks land in the same band — your 1-5 scales are being used as 3-4; force the extremes. The AI is confidently wrong about a threat — treat its output as a prompt to check the source, never as the source.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
