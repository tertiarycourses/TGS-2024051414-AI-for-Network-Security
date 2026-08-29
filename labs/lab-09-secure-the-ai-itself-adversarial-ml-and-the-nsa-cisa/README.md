# Lab 9 — Secure the AI Itself — Adversarial ML and the NSA/CISA Deployment Controls

**Topic 03 — Designing and Implementing AI-Enhanced Network Security Measures**  ·  LO3  ·  knowledge K3  ·  abilities A5, A6, A7

## Maps to

A5 · A6 · A7 · K3 — Recognise that the AI you deploy is an attack surface, and apply the recognised controls for deploying an AI system securely.

## Goal

Every previous lab used AI as a defensive tool. This one turns the question around: what happens when the AI is the target? You run an evasion attack against your own Lab 2 anomaly model and watch it go blind, simulate a poisoning attack on its training data, then work through the NIST AI 100-2 attack taxonomy and the NSA/CISA 'Deploying AI Systems Securely' controls to produce a hardening checklist for the AI components in your Lab 7 design.

## What you'll produce

A demonstrated evasion and a demonstrated poisoning attack against your own model, plus an AI security hardening checklist mapped to the NSA/CISA three categories and the NIST AI 100-2 attack classes.

**Tools:** Lab 2 model, Python, scikit-learn, NIST AI 100-2e2025, NSA/CISA CSI, MITRE ATLAS

## Step-by-step

1. Reload your Lab 2 Isolation Forest and confirm it still detects the port scan. This is your control condition — you cannot show an attack worked without it.
2. Evasion attack: slow the scan down. Regenerate the scan features with a long inter-packet delay so the connection rate falls inside the baseline, then re-score it.

   ```bash
   nmap -sS -T1 --scan-delay 5s -p 1-1024 192.168.56.101
   ```

3. Record what happened. The traffic is functionally identical, the intent is identical, and the model no longer flags it — that is an evasion attack, and it needed no access to the model at all.
4. Poisoning attack: inject slow-scan traffic into the training window, refit the model, and re-score the original fast scan. Measure how far the detection degrades.

   ```bash
   X_poisoned = np.vstack([X_baseline, X_slowscan])
   model_p = IsolationForest(contamination=0.02, random_state=42).fit(X_poisoned)
   ```

5. Record the degradation as a number — detection rate before poisoning versus after. 'The model got worse' is an anecdote; a measured drop is evidence.
6. Map both attacks onto the NIST AI 100-2e2025 taxonomy — evasion, poisoning, privacy and misuse — and state which class each belongs to and at what stage of the ML lifecycle it lands.

   → <https://csrc.nist.gov/pubs/ai/100/2/e2025/final>

7. Look up the matching tactics and techniques in MITRE ATLAS, the adversarial threat knowledge base for AI systems, and note the mitigations it lists.

   → <https://atlas.mitre.org/>

8. Work through the NSA/CISA 'Deploying AI Systems Securely' controls under its three categories — secure the deployment environment, continuously protect the AI system, and secure AI operation and maintenance.

   → <https://www.cisa.gov/news-events/alerts/2024/04/15/joint-guidance-deploying-ai-systems-securely>

9. Add the CISA/NSA AI data-security controls that protect the training pipeline: data provenance tracking, cryptographic integrity verification, digital signatures on dataset revisions, access control by classification, encryption in transit and at rest, and continuous risk assessment.
10. Produce the hardening checklist for the AI components in your Lab 7 design. Every item names the control, the attack class it addresses, who owns it and how it is verified.
11. Add the one control that no framework will hand you: define what the security operation does when the AI is unavailable or untrusted. A detection capability with no manual fallback is a single point of failure.

## Test it

You can demonstrate the slowed scan evading a model that detected the fast one, and you can state the measured detection drop after poisoning. Your checklist covers all three NSA/CISA categories, names an owner and a verification method for every control, and includes a stated fallback for when the AI is down.

## If it doesn't work

The slow scan is still detected — your feature set does not include a rate term, so slowing it changes nothing; add connections-per-second and retry. Poisoning shows no effect — your injected sample is too small relative to the baseline; raise the proportion and re-measure. Results vary between runs — set random_state so the comparison is fair.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
