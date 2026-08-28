# WSQ — AI for Network Security

[![WSQ Course](https://img.shields.io/badge/WSQ-TGS--2024051414-1F6FEB?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-ai-for-network-security.html)
[![Duration](https://img.shields.io/badge/Duration-2%20Days%20%C2%B7%2016%20Hours-10B981?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-ai-for-network-security.html)
[![SkillsFuture](https://img.shields.io/badge/SkillsFuture-Claimable-F59E0B?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-ai-for-network-security.html)
[![Level](https://img.shields.io/badge/Level-Beginner-7C3AED?style=for-the-badge)](https://www.tertiarycourses.com.sg/wsq-ai-for-network-security.html)

> Apply artificial intelligence to network monitoring, threat detection, vulnerability
> assessment and incident response — and learn to defend the AI itself.

**[→ Register for this course](https://www.tertiarycourses.com.sg/wsq-ai-for-network-security.html)**

Conducted by **Tertiary Infotech Academy Pte Ltd** · UEN 201200696W

---

## About This Course

Attacks now move at machine speed and at a volume no analyst can read. Signature-based
detection only finds what someone has already named, and a security team can only triage
so many alerts an hour. This course closes both gaps.

Over two days you use AI to analyse network configurations, baseline normal traffic,
detect anomalies, prioritise vulnerabilities, score risk, design and implement controls,
triage alerts and document incidents. You also do something most AI courses skip: you
attack your own detection model with evasion and poisoning, measure how far it degrades,
and then harden it against those attacks using the NIST and NSA/CISA guidance.

Everything is hands-on. The twelve labs form **one continuous engagement** — each
deliverable feeds the next, and the final assessment rehearses the same chain.

## Skills Framework Alignment

| | |
|---|---|
| **Course Reference** | TGS-2024051414 |
| **TSC Title** | Network Security |
| **TSC Code** | ICT-DIT-4024-1.1 |
| **Duration** | 2 days · 8 instructional hours per day |
| **Level** | Beginner |
| **Assessment** | Written Assessment (SAQ) 1 hr + Case Study 1 hr, both open book |

## Learning Outcomes

| | Outcome |
|---|---|
| **LO1** | Identify and assess network threats and vulnerabilities by analysing ICT configurations |
| **LO2** | Evaluate organisational assets and develop risk management plans addressing infrastructure weaknesses |
| **LO3** | Design and implement security measures for network components by managing security phases |
| **LO4** | Document security incidents and apply incident response configurations based on established procedures |

## Course Outline

| Topic | Covers | Weight |
|---|---|---|
| **1 · AI-Assisted Network Threat and Vulnerability Analysis** | ICT networks & configuration · the AI threat landscape · pattern-of-life baselines · NDR · AI vulnerability prioritisation | 25% |
| **2 · AI-Powered Network Risk Assessment and Management Planning** | Asset discovery & classification · CIA business impact · AI risk scoring · risk registers · NIST CSF & AI RMF | 25% |
| **3 · Designing and Implementing AI-Enhanced Network Security Measures** | Defence in depth · the three security phases · segmentation & zero trust · AI firewalls, IDS/IPS, UEBA · securing the AI itself | 30% |
| **4 · AI-Assisted Security Incident Documentation and Response** | Logging & syslog · SIEM/SOAR · AI alert triage · NIST SP 800-61 lifecycle · incident documentation · playbooks | 20% |

## Hands-On Labs

Twelve labs, each building on the last. Full step-by-step procedures are in the
[Learner Guide](LG-AI-for-Network-Security.md); each lab folder under [`labs/`](labs/)
carries its own guide.

| # | Lab | Topic | Produces |
|---|---|---|---|
| 1 | Map the ICT Network and Analyse Its Configuration | 1 | Network configuration inventory + weakness list |
| 2 | Baseline Normal Traffic and Detect an Anomaly with AI | 1 | Isolation Forest anomaly report, TP/FP verified |
| 3 | AI-Assisted Vulnerability Analysis and Prioritisation | 1 | Prioritised CVE worklist (CVSS × criticality × KEV) |
| 4 | Build an Asset Register and Classify What Needs Protecting | 2 | Classified asset register with C/I/A ratings |
| 5 | AI-Assisted Risk Scoring and the Risk Register | 2 | Scored register with inherent + residual risk |
| 6 | Develop the Risk Management Plan | 2 | Treatment plan mapped to the NIST CSF |
| 7 | Design the Layered Architecture Across the Three Security Phases | 3 | Segmented design + zone access matrix |
| 8 | Implement AI-Enhanced Controls — Firewall Policy, IDS and Adaptive Access | 3 | Default-deny ruleset + tuned detections |
| 9 | Secure the AI Itself — Adversarial ML and the NSA/CISA Deployment Controls | 3 | Demonstrated evasion + poisoning, hardening checklist |
| 10 | Centralise Logs and Triage Alerts with AI | 4 | Logging specification + triaged alert queue |
| 11 | Document a Security Incident to the Standard | 4 | Evidence-based incident record |
| 12 | Implement the Incident Response Configuration and Playbook | 4 | Tested playbook + measured containment time |

## Repository Contents

**Current version: v1.1 · 29 August 2026**

| File | What it is |
|---|---|
| `courseware/AI-for-Network-Security-v1.1.pptx` | Trainer slide deck — 151 slides |
| `courseware/AI-for-Network-Security-v1.1.pdf` | Learner slides (PDF of the deck) |
| `courseware/LP-AI-for-Network-Security.docx` / `.pdf` | Lesson Plan |
| `courseware/LG-AI-for-Network-Security.docx` / `.pdf` | Learner Guide |
| `LG-AI-for-Network-Security.md` | Learner Guide, Markdown mirror of the DOCX |
| `labs/` | 12 lab folders, each with its own step-by-step README |
| `courseware/archive/` | Superseded versions, retained but not current |

> Assessment material is confidential, held on Google Drive only, and is **not**
> published in this repository.

## Tools Used

`Nmap` · `Wireshark / tshark` · `Python 3` with `pandas` and `scikit-learn` ·
a generative AI assistant (Claude, ChatGPT or Copilot) · a spreadsheet · a modern browser

## Reference Sources

The AI content is grounded in authoritative guidance:

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework)
- [NIST AI 100-2e2025 — Adversarial Machine Learning](https://csrc.nist.gov/pubs/ai/100/2/e2025/final)
- [NSA / CISA / FBI — Deploying AI Systems Securely](https://www.cisa.gov/news-events/alerts/2024/04/15/joint-guidance-deploying-ai-systems-securely)
- [CISA Artificial Intelligence](https://www.cisa.gov/ai)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST SP 800-61 — Incident Handling](https://csrc.nist.gov/pubs/sp/800/61/r2/final)
- [CISA Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

## Responsible Use

Every scanning, capture and testing technique in this course must only be run against
systems you own or have **written authorisation** to test. Unauthorised access to a
computer is a criminal offence under the Singapore Computer Misuse Act and its
equivalents elsewhere.

## Funding

SkillsFuture Credit (SFC), SkillsFuture Enterprise Credit (SFEC) and PSEA are applicable
to eligible participants. A minimum of **75% attendance** and a **Competent** result on
both assessment components are required for funding and certification.

Participants receive a Certificate of Achievement from Tertiary Infotech Academy and an
OpenCert Statement of Achievement from SkillsFuture Singapore.

## Contact

**Tertiary Infotech Academy Pte Ltd** · UEN 201200696W
📧 enquiry@tertiaryinfotech.com · 📞 +65 6100 0613
🌐 [www.tertiarycourses.com.sg](https://www.tertiarycourses.com.sg)

---

© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.
