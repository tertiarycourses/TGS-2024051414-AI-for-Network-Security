"""
Topic 3 — Designing and Implementing AI-Enhanced Network Security Measures.
LO3 · K3 · A5, A6, A7.  Labs 7-9.
"""

DOMAIN3 = [
    dict(
        num=7, topic=3,
        stages=[
            "Write requirements",
            "Record constraints",
            "Define trust zones",
            "Draw the architecture",
            "Write the access matrix",
        ],
        title="Design the Layered Architecture Across the Three Security Phases",
        objective="A5 · K3 — Define the planning, building and management phases for a network security design, and express the design as layered defence-in-depth controls.",
        desc=("Security design is a phased engineering activity, not a shopping list. In this lab you take the risk "
              "management plan from Lab 6 and produce an actual design: you write the requirements and constraints "
              "in the planning phase, draw a segmented target architecture with the controls placed at each layer, "
              "and define the management phase that keeps the design honest after go-live. You use an AI assistant "
              "as a design reviewer and then defend the design against its objections."),
        build="A three-phase security design: a planning-phase requirements table, a segmented target architecture diagram with controls at every layer, and a management-phase operating model.",
        services="Lab 6 plan, the IP Calculator (alfredang.github.io/ipcalculator), a diagramming tool (draw.io or paper), a generative AI assistant",
        steps=[
            ("Planning phase — write the security requirements the design must satisfy, each traced back to a specific risk ID from Lab 5. A requirement with no risk behind it is a preference.", ""),
            ("Planning phase — record the constraints: budget, existing equipment, skills available, downtime tolerance and any regulatory obligation. Constraints are what make a design real.", ""),
            ("Planning phase — define the trust zones: Internet, DMZ, internal user network, server network, management network and any OT or guest segment. State what each zone is allowed to reach.", ""),
            ("Planning phase — turn those zones into real address space. Use the IP Calculator's recursive subnet splitting to carve your allocation into one subnet per zone, sized to the hosts each actually needs. Record the CIDR, usable range and host count per zone — a segmentation design with no addressing plan cannot be implemented.",
             "https://alfredang.github.io/ipcalculator/"),
            ("Building phase — draw the target architecture with the zones as segments and place the controls at each layer: perimeter firewall, DMZ, internal segmentation, host controls and data controls.", ""),
            ("Building phase — write the zone-to-zone access matrix. Rows are source zones, columns are destination zones, cells hold the permitted protocols. Default deny: every empty cell is blocked.", ""),
            ("Building phase — classify every control you have placed as physical, technical or administrative, and confirm you have all three. A design with no administrative controls has no way to stay correct.", ""),
            ("Management phase — define what happens after go-live: who monitors what, the review cadence, the change-control path, and the trigger that forces a redesign.", ""),
            ("Ask your AI assistant to review the design as an attacker would.",
             "Prompt: 'Here is a segmented network security design with a zone access matrix. Acting as an attacker, describe three paths you would take through this architecture and name the control that would have to fail at each step. Then identify the weakest zone boundary.'"),
            ("Answer each attack path in writing: either add a control that closes it, or record why the residual risk is acceptable and who accepts it.", ""),
            ("Trace every High and Critical risk from Lab 5 to at least one control in the design. Any risk with no control is either untreated or was accepted — and it must say which.", ""),
        ],
        test=("Every security requirement traces to a risk ID, the access matrix is default-deny with justified "
              "exceptions, all three control categories are present, and every High or Critical risk maps to a "
              "control or a documented acceptance. You can answer all three of the AI's attack paths."),
        troubleshoot=("The matrix has more allow cells than deny — you are documenting today's flat network rather "
                      "than designing a segmented one. No management phase — a design with no operating model "
                      "degrades within a quarter. The AI's attack paths seem unrealistic — say why in writing; that reasoning is the deliverable."),
    ),
    dict(
        num=8, topic=3,
        stages=[
            "Translate the access matrix",
            "Write the allow rules",
            "Add deny-and-log rules",
            "Review for shadowed rules",
            "Write detection rules",
        ],
        title="Implement AI-Enhanced Controls — Firewall Policy, IDS and Adaptive Access",
        objective="A6 · K3 — Develop the security measures for the network components: build a default-deny firewall policy, tune detection rules, and specify adaptive AI-driven access control.",
        desc=("This is where the design becomes configuration. You write a default-deny firewall ruleset from the "
              "Lab 7 access matrix, run detection against real traffic to see what your rules actually catch, and "
              "specify the risk-based conditions under which an AI-driven access control should step up "
              "authentication or block outright. You then compare a static rule against a behavioural model on the "
              "same traffic — and see exactly where each one wins."),
        build="A default-deny firewall ruleset derived from the access matrix, a tuned detection ruleset with its true/false positive counts, and an adaptive access-control policy specification.",
        services="Firewall rule syntax (iptables or a NGFW policy table), the Cryptography Toolkit (alfredang.github.io/cryptography-toolkit), Wireshark, Python, a generative AI assistant",
        steps=[
            ("Translate the Lab 7 access matrix into an ordered firewall ruleset. Specific allow rules first, the default deny last — order is the whole game in a firewall.",
             "# Rule 1: allow established return traffic\niptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT\n# Rule N: default deny (must be last)\niptables -P FORWARD DROP"),
            ("Write each allow rule with source zone, destination zone, protocol, port, and a comment naming the business reason. An uncommented rule becomes permanent because nobody dares delete it.",
             "iptables -A FORWARD -s 10.0.10.0/24 -d 10.0.30.0/24 -p tcp --dport 443 -j ACCEPT -m comment --comment 'Users to app servers HTTPS - REQ-004'"),
            ("Add explicit deny-and-log rules for the traffic you most want to know about — management protocols crossing a zone boundary, and any outbound connection from the server zone.", ""),
            ("Review the ruleset for shadowed rules: any rule that can never match because an earlier rule already covers its traffic. Shadowed rules are the most common firewall defect there is.", ""),
            ("Your ruleset controls WHO may connect; encryption controls what an interceptor can read. Use the Cryptography Toolkit to encrypt a sample management credential with AES-256 (CBC), then decrypt it. Then try the same string with DES and RC4 — both are flagged insecure for a reason. Record why your design mandates AES for management traffic.",
             "https://alfredang.github.io/cryptography-toolkit/"),
            ("Now the detection layer. Write three detection rules against the Lab 2 capture — one for a port scan, one for a large outbound transfer, and one for a connection to a management port from a user subnet.", ""),
            ("Run each rule over the capture and count the true positives and false positives. A rule with more false positives than true is worse than no rule, because it trains the analyst to ignore alerts.",
             "tshark -r traffic.pcapng -Y 'tcp.flags.syn==1 && tcp.flags.ack==0' -T fields -e ip.src | sort | uniq -c | sort -rn"),
            ("Compare the static rule against the Lab 2 anomaly model on the same traffic. Record where the rule wins (precision on known patterns) and where the model wins (unnamed behaviour).", ""),
            ("Specify the adaptive access-control policy: the signals (device posture, location, time, behaviour deviation, resource sensitivity), the risk bands, and the action at each band — allow, step-up MFA, restrict, or block.", ""),
            ("State the human-in-the-loop boundary explicitly. Which actions may the system take autonomously, and which require a named person to approve? Automatic blocking of a production server needs an owner.", ""),
            ("Ask your AI assistant to review the firewall ruleset for shadowed rules, overly broad allows and missing egress controls, then verify each finding by reading the rule yourself.",
             "Prompt: 'Review this ordered firewall ruleset. Identify shadowed rules that can never match, allow rules that are broader than their stated business reason, and any missing egress control. Quote the rule number for each finding.'"),
        ],
        test=("Your ruleset ends in an explicit default deny, every allow rule carries a business-reason comment "
              "traced to a requirement, and you have no shadowed rules. You can state the true/false positive count "
              "for each detection rule and say which of the static rule or the AI model you would deploy for each "
              "of the three detections, and why."),
        troubleshoot=("The default deny is not last — everything after it is dead code. All traffic is blocked — you "
                      "are missing the ESTABLISHED,RELATED rule, so return traffic never gets back. The detection "
                      "rule fires constantly — your threshold is tuned to a quiet lab, not to production; raise it against the baseline."),
    ),
    dict(
        num=9, topic=3,
        stages=[
            "Establish the control",
            "Run an evasion attack",
            "Record the evasion",
            "Run a poisoning attack",
            "Measure the degradation",
        ],
        title="Secure the AI Itself — Adversarial ML and the NSA/CISA Deployment Controls",
        objective="A5 · A6 · A7 · K3 — Recognise that the AI you deploy is an attack surface, and apply the recognised controls for deploying an AI system securely.",
        desc=("Every previous lab used AI as a defensive tool. This one turns the question around: what happens when "
              "the AI is the target? You run an evasion attack against your own Lab 2 anomaly model and watch it go "
              "blind, simulate a poisoning attack on its training data, then work through the NIST AI 100-2 attack "
              "taxonomy and the NSA/CISA 'Deploying AI Systems Securely' controls to produce a hardening checklist "
              "for the AI components in your Lab 7 design."),
        build="A demonstrated evasion and a demonstrated poisoning attack against your own model, plus an AI security hardening checklist mapped to the NSA/CISA three categories and the NIST AI 100-2 attack classes.",
        services="Lab 2 model, Python, scikit-learn, NIST AI 100-2e2025, NSA/CISA CSI, MITRE ATLAS",
        steps=[
            ("Reload your Lab 2 Isolation Forest and confirm it still detects the port scan. This is your control condition — you cannot show an attack worked without it.", ""),
            ("Evasion attack: slow the scan down. Regenerate the scan features with a long inter-packet delay so the connection rate falls inside the baseline, then re-score it.",
             "nmap -sS -T1 --scan-delay 5s -p 1-1024 192.168.56.101"),
            ("Record what happened. The traffic is functionally identical, the intent is identical, and the model no longer flags it — that is an evasion attack, and it needed no access to the model at all.", ""),
            ("Poisoning attack: inject slow-scan traffic into the training window, refit the model, and re-score the original fast scan. Measure how far the detection degrades.",
             "X_poisoned = np.vstack([X_baseline, X_slowscan])\nmodel_p = IsolationForest(contamination=0.02, random_state=42).fit(X_poisoned)"),
            ("Record the degradation as a number — detection rate before poisoning versus after. 'The model got worse' is an anecdote; a measured drop is evidence.", ""),
            ("Map both attacks onto the NIST AI 100-2e2025 taxonomy — evasion, poisoning, privacy and misuse — and state which class each belongs to and at what stage of the ML lifecycle it lands.",
             "https://csrc.nist.gov/pubs/ai/100/2/e2025/final"),
            ("Look up the matching tactics and techniques in MITRE ATLAS, the adversarial threat knowledge base for AI systems, and note the mitigations it lists.", "https://atlas.mitre.org/"),
            ("Work through the NSA/CISA 'Deploying AI Systems Securely' controls under its three categories — secure the deployment environment, continuously protect the AI system, and secure AI operation and maintenance.",
             "https://www.cisa.gov/news-events/alerts/2024/04/15/joint-guidance-deploying-ai-systems-securely"),
            ("Add the CISA/NSA AI data-security controls that protect the training pipeline: data provenance tracking, cryptographic integrity verification, digital signatures on dataset revisions, access control by classification, encryption in transit and at rest, and continuous risk assessment.", ""),
            ("Produce the hardening checklist for the AI components in your Lab 7 design. Every item names the control, the attack class it addresses, who owns it and how it is verified.", ""),
            ("Add the one control that no framework will hand you: define what the security operation does when the AI is unavailable or untrusted. A detection capability with no manual fallback is a single point of failure.", ""),
        ],
        test=("You can demonstrate the slowed scan evading a model that detected the fast one, and you can state "
              "the measured detection drop after poisoning. Your checklist covers all three NSA/CISA categories, "
              "names an owner and a verification method for every control, and includes a stated fallback for when the AI is down."),
        troubleshoot=("The slow scan is still detected — your feature set does not include a rate term, so slowing it "
                      "changes nothing; add connections-per-second and retry. Poisoning shows no effect — your "
                      "injected sample is too small relative to the baseline; raise the proportion and re-measure. "
                      "Results vary between runs — set random_state so the comparison is fair."),
    ),
]
