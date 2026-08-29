"""
SINGLE SOURCE OF TRUTH — TGS-2024051414 · AI for Network Security.

Every artifact (PPT, LP, LG, LG.md, labs index, assessment) is generated from
this file + data_domain1..4.py so they stay 100% aligned.

Content lineage:
  * Network-security substance  — the two reference decks in courseware/reference/
        (WSQ Network Securities for Beginners v13.1; WSQ Master Trainer Slides —
         Pearson Vue Certified IT Specialist Network Security Training)
  * AI layer — Check Point (AI in Network Security), Fortinet (AI in
        Cybersecurity), Vectra AI, Darktrace, Gigamon, Akamai, NetBrain, SC World,
        NIST AI 100-2e2025 (Adversarial ML), NSA/CISA CSI "Deploying AI Systems
        Securely" (Apr 2024) + CISA AI Data Security (2025), MITRE ATLAS, CISA AI.
  * Structure — the course's own Assessment Plan v2.0 (K1-K4 / A1-A9) and the
        published outline at tertiarycourses.com.sg/wsq-ai-for-network-security.html
"""

# ------------------------------------------------------------------ metadata
TITLE        = "AI for Network Security"
SHORT_TITLE  = "AI-for-Network-Security"
COURSE_CODE  = "TGS-2024051414"
VERSION      = "v1.2"
VERSION_DATE = "29 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 2

TSC_TITLE    = "Network Security"
TSC_CODE     = "ICT-DIT-4024-1.1"
COURSE_URL   = "https://www.tertiarycourses.com.sg/wsq-ai-for-network-security.html"
LMS_URL      = "https://lms-tms.tertiaryinfotech.com"
EXAM_URL     = "https://exams.tertiaryinfotech.com"
REPO_URL     = "https://github.com/tertiarycourses/TGS-2024051414-AI-for-Network-Security"

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Identify and assess network threats and vulnerabilities by analysing ICT configurations.",
    "LO2: Evaluate organisational assets and develop risk management plans to address network infrastructure weaknesses effectively.",
    "LO3: Design and implement security measures for network components by managing security phases.",
    "LO4: Document security incidents and apply incident response configurations to manage risks based on established procedures.",
]

# Short forms for the tile-grid learning-outcome slides
LO_TILES = [
    ("LO1 · Threats & vulnerabilities",
     "Analyse ICT configurations with AI assistance to identify network threats and vulnerabilities."),
    ("LO2 · Assets & risk plans",
     "Evaluate organisational assets and build AI-informed risk management plans for infrastructure weaknesses."),
    ("LO3 · Security measures",
     "Design and implement AI-enhanced security measures across the planning, building and management phases."),
    ("LO4 · Incidents & response",
     "Document security incidents and apply incident response configurations using AI-assisted triage."),
]

# ------------------------------------------------------------------ underpinning knowledge / abilities
KNOWLEDGE = [
    ("K1", "Infocomm Technology (ICT) networks and their configuration"),
    ("K2", "Types of network attacks, vulnerabilities and related weaknesses of installed infrastructure"),
    ("K3", "Types and techniques of network security measures"),
    ("K4", "Network security implementation risk management plans and procedures"),
]

ABILITIES = [
    ("A1", "Identify threats to network security"),
    ("A2", "Analyse security risks"),
    ("A3", "Determine organisational assets that require protection"),
    ("A4", "Create risk management plans to mitigate risks"),
    ("A5", "Define planning, building and management phases for network security design"),
    ("A6", "Develop security measures for network components"),
    ("A7", "Design auditing and incident response procedures"),
    ("A8", "Document security incidents"),
    ("A9", "Implement configurations aligned with incident response procedure design"),
]

# LO -> (K codes, A codes)
LO_MAP = {
    1: (["K1"], ["A1", "A2"]),
    2: (["K2"], ["A3", "A4"]),
    3: (["K3"], ["A5", "A6", "A7"]),
    4: (["K4"], ["A8", "A9"]),
}

# ------------------------------------------------------------------ topics (= learning units)
TOPICS = [
    dict(num=1, code="01",
         title="AI-Assisted Network Threat and Vulnerability Analysis",
         subtitle="ICT networks & configuration · the AI threat landscape · AI anomaly detection · NDR · AI-assisted vulnerability analysis",
         weighting="25%",
         los=["LO1"], ks=["K1"], abil=["A1", "A2"],
         concepts=[
            "An ICT network is a layered system — hosts, switches, routers, firewalls, wireless, servers and cloud edges — and every layer carries its own configuration and its own attack surface.",
            "Traditional signature-based detection fails against zero-day exploits, polymorphic malware and Living-off-the-Land (LOTL) techniques; AI closes the gap by learning behaviour rather than matching known strings.",
            "AI network monitoring gives real-time visibility across hybrid and multi-cloud estates, flags misconfigurations and surfaces vulnerable assets before an incident escalates.",
            "AI anomaly detection learns the 'pattern of life' of a network — who normally talks to whom, when, and how much — then reports statistically significant deviations as candidate intrusions.",
            "Network Detection and Response (NDR) applies behavioural AI to reconnaissance, credential abuse, lateral movement and data staging across the whole attack lifecycle.",
            "AI-assisted vulnerability analysis adds contextual prioritisation to a raw scan: predicted exploitability and business impact turn a 900-line report into a ranked worklist.",
         ]),
    dict(num=2, code="02",
         title="AI-Powered Network Risk Assessment and Management Planning",
         subtitle="Asset discovery & classification · CIA impact · AI risk scoring · risk registers · treatment plans · NIST CSF & AI RMF",
         weighting="25%",
         los=["LO2"], ks=["K2"], abil=["A3", "A4"],
         concepts=[
            "You cannot protect what you have not inventoried — AI-driven asset discovery continuously fingerprints every identity, device and workload rather than relying on a stale spreadsheet.",
            "Asset criticality is a business judgement expressed against the CIA triad: what does a loss of confidentiality, integrity or availability actually cost this organisation?",
            "Risk = Likelihood x Impact. AI improves the likelihood term with exploit-prediction models and threat-intelligence correlation, and improves the impact term with real dependency mapping.",
            "A risk register is the working artefact of risk management: asset, threat, vulnerability, existing control, inherent risk, treatment, owner, target date and residual risk.",
            "The four treatment options are mitigate, transfer, avoid and accept — every entry on the register must land on one of them, with a named owner.",
            "The NIST Cybersecurity Framework (Govern, Identify, Protect, Detect, Respond, Recover) and the NIST AI Risk Management Framework (Govern, Map, Measure, Manage) give the planning scaffold.",
         ]),
    dict(num=3, code="03",
         title="Designing and Implementing AI-Enhanced Network Security Measures",
         subtitle="Defence in depth · planning/building/management phases · segmentation & zero trust · AI firewalls, IDS/IPS, NAC · AI security itself",
         weighting="30%",
         los=["LO3"], ks=["K3"], abil=["A5", "A6", "A7"],
         concepts=[
            "Defence in depth layers physical, technical and administrative controls so that the failure of any single control does not become a breach.",
            "Network security design runs in three phases — planning (requirements, risk, architecture), building (configure, harden, test) and management (monitor, tune, review).",
            "Segmentation and zero trust shrink the blast radius: VLANs, DMZs and micro-segmentation stop lateral movement, and 'never trust, always verify' removes implicit network trust.",
            "AI-powered firewalls and NGFW policy engines adapt rule sets to observed traffic instead of relying purely on static, hand-written rules.",
            "AI-enhanced IDS/IPS, UEBA and adaptive access control score every session on device, behaviour, location and time, and step up authentication when risk rises.",
            "The AI you deploy is itself an asset to defend — NIST AI 100-2 catalogues evasion, poisoning, privacy and misuse attacks, and the NSA/CISA guidance tells you how to deploy AI securely.",
         ]),
    dict(num=4, code="04",
         title="AI-Assisted Security Incident Documentation and Response",
         subtitle="Logging & syslog · SIEM/SOAR · AI alert triage · the NIST IR lifecycle · incident documentation · playbooks & post-incident review",
         weighting="20%",
         los=["LO4"], ks=["K4"], abil=["A8", "A9"],
         concepts=[
            "Logging is the evidence base of incident response — syslog, Windows Event Log, flow records and firewall logs must be centralised, time-synchronised and retained.",
            "SIEM correlates events into incidents; SOAR executes the response playbook — isolate the host, revoke the credential, block the address — at machine speed.",
            "AI alert triage attacks the real bottleneck: it deduplicates, clusters and contextualises so the analyst sees a handful of ranked incidents instead of thousands of raw alerts.",
            "The NIST SP 800-61 lifecycle is Preparation, Detection & Analysis, Containment/Eradication/Recovery, and Post-Incident Activity — AI accelerates each step but owns none of them.",
            "An incident record must state what happened, when, to which assets, the severity, the actions taken, the evidence, and the person accountable — this is the A8 deliverable.",
            "Human-in-the-loop approval remains mandatory for destructive or wide-blast-radius actions; AI recommends, a named responder decides.",
         ]),
]

# ------------------------------------------------------------------ day themes (8 instructional hours/day)
DAY_THEMES = {
    1: "AI-Assisted Threat & Vulnerability Analysis · AI-Powered Risk Assessment and Management Planning",
    2: "Designing & Implementing AI-Enhanced Security Measures · AI-Assisted Incident Documentation and Response",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment — Short-Answer Questions (WA-SAQ) · 1 hour · open book. Assesses the underpinning knowledge K1–K4.",
    practical="Case Study (CS) · 1 hour · open book. Assesses the abilities A1–A9 against a realistic organisational scenario.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)

ASSESSMENT_METHODS = [
    ("WA-SAQ", "Written Assessment — Short-Answer Questions", "1 hr", "K1, K2, K3, K4"),
    ("CS", "Case Study", "1 hr", "A1–A9"),
]

# ------------------------------------------------------------------ browser / lab tooling
LAB_TOOLS = [
    ("Wireshark", "Packet capture and protocol analysis for the traffic-baseline and anomaly labs."),
    ("Nmap", "Host discovery, port and service scanning for the configuration-analysis labs."),
    ("Python 3 + pandas / scikit-learn", "Runs the AI anomaly-detection and log-triage notebooks."),
    ("A generative AI assistant", "Claude, ChatGPT or Copilot — used as the AI analyst copilot throughout the labs."),
    ("A spreadsheet", "Excel, Numbers or Google Sheets for the asset register and risk register labs."),
    ("A modern browser", "For the CVE lookup and the seven browser-based practice tools — no install needed, and the PCAP Analyzer processes your capture locally without uploading it."),
]

BROWSER_TOOLS = [
    ("IP Calculator  ·  Labs 1 & 7",
     "Scope the scan and carve one subnet per security zone — alfredang.github.io/ipcalculator"),
    ("PCAP Analyzer  ·  Labs 2 & 11",
     "Read a capture in the browser: protocol mix, top talkers, conversations — alfredang.github.io/pcapanalyzer"),
    ("Cybersecurity Simulator  ·  Lab 5",
     "Run phishing, SQLi and social-engineering attacks to ground your likelihood scores — alfredang.github.io/cybersecuritysimulator"),
    ("Cryptography Toolkit  ·  Labs 8 & 11",
     "AES/DES/RSA and hashing — the confidentiality and integrity controls, and why a hash is tamper-evident — alfredang.github.io/cryptography-toolkit"),
    ("RegexLab  ·  Lab 10",
     "Write and TEST the log filters that drive alert triage, including the negative test — alfredang.github.io/regexgenerator"),
    ("Hacklab  ·  optional extension",
     "A scripted 10-phase penetration-test walkthrough. Not assessed — run it to see what an attacker learns about you — alfredang.github.io/ethnicalhacking"),
    ("FauxBank  ·  optional extension",
     "A safe, deliberately vulnerable banking app with a simulated scanner and report generator. Not assessed — pentest-fauxbank.vercel.app"),
]
