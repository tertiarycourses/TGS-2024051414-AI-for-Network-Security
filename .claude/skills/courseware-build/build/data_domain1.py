"""
Topic 1 — AI-Assisted Network Threat and Vulnerability Analysis.
LO1 · K1 · A1, A2.  Labs 1-3.
"""

DOMAIN1 = [
    dict(
        num=1, topic=1,
        stages=[
            "Confirm authorisation",
            "Ping sweep",
            "Service & version scan",
            "Full port scan",
            "Export inventory",
        ],
        title="Map the ICT Network and Analyse Its Configuration",
        objective="K1 · A1 — Establish what the network actually is before judging whether it is safe: discover live hosts, open ports and services, and read the configuration for weaknesses.",
        desc=("You are handed an unfamiliar subnet and asked the question every security review starts with: "
              "what is on this network, and what is it running? You use Nmap to discover live hosts and their "
              "open ports and service versions, record the result as a structured inventory, and then read the "
              "configuration evidence for the weaknesses that matter — management ports exposed, unencrypted "
              "protocols in use, out-of-date service versions and default configurations left in place."),
        build="A network configuration inventory (host, IP, OS guess, open ports, service versions) plus a written list of the configuration weaknesses you found and why each one matters.",
        services="Nmap, Zenmap, a spreadsheet, a generative AI assistant",
        steps=[
            ("Confirm you are scanning only the lab network you have been authorised to scan. Never scan a network you do not own or have written permission to test.", ""),
            ("Discover which hosts are alive on the lab subnet with a ping sweep. Note how many hosts answer.", "nmap -sn 192.168.56.0/24"),
            ("Run a service and version scan against the live hosts to learn what each one is actually running.", "nmap -sV -O -T4 192.168.56.0/24 -oN inventory.txt"),
            ("Scan the full TCP port range on the one host that looks most interesting, so nothing above port 1024 is missed.", "nmap -sV -p- -T4 192.168.56.101 -oN host101-full.txt"),
            ("Export the scan to a machine-readable form so it can be loaded into a spreadsheet or a script.", "nmap -sV 192.168.56.0/24 -oX inventory.xml"),
            ("Build the inventory table in a spreadsheet with the columns Host, IP, OS, Open Ports, Services, Versions, Owner, Business Function.", ""),
            ("Read the inventory for configuration weaknesses. Flag every unencrypted management protocol (Telnet 23, FTP 21, HTTP 80 on an admin interface), every service version that is behind, and every port that has no business being open.", ""),
            ("Paste the sanitised Nmap output into your AI assistant and ask it to identify the configuration weaknesses and explain the risk of each. Compare its list against yours.",
             "Prompt: 'Here is Nmap output from a network I am authorised to assess. Identify configuration weaknesses, name the affected protocol or service, and explain the risk of each in one sentence.'"),
            ("Reconcile the two lists. Record anything the AI found that you missed, and anything it claimed that the evidence does not support — the second list is the more important one.", ""),
        ],
        test=("Your inventory names every live host with its open ports and service versions, and your weakness "
              "list contains at least five configuration weaknesses, each tied to specific evidence in the scan "
              "output. You can state, for each AI-suggested finding, whether the scan evidence actually supports it."),
        troubleshoot=("No hosts answer the ping sweep — the lab hosts may block ICMP; re-run with `nmap -Pn`. "
                      "The version scan is slow — narrow the port range with `-p 1-1024` or raise the timing to `-T4`. "
                      "`-O` reports 'too many fingerprints' — OS detection needs at least one open and one closed port; it is a hint, not evidence."),
    ),
    dict(
        num=2, topic=1,
        stages=[
            "Capture baseline traffic",
            "Generate the anomaly",
            "Save the capture",
            "Extract flow features",
            "Export to CSV",
        ],
        title="Baseline Normal Traffic and Detect an Anomaly with AI",
        objective="K1 · K2 · A1 — Learn what 'normal' looks like on a network, then let a machine-learning model tell you when traffic stops being normal.",
        desc=("Signature detection only finds what someone has already named. This lab builds the other half of the "
              "picture. You capture live traffic in Wireshark, turn it into per-connection features, train an "
              "unsupervised anomaly-detection model on the quiet 'pattern of life' period, and then score a period "
              "that contains a port scan and a data-staging burst. You see for yourself which events the model "
              "scores as anomalous and — just as importantly — which normal events it wrongly flags."),
        build="A labelled anomaly report: the connections your Isolation Forest model scored as anomalous, ranked by score, with your own verdict of true positive or false positive against the packet evidence.",
        services="Wireshark, tshark, Python 3, pandas, scikit-learn, a generative AI assistant",
        steps=[
            ("Start a Wireshark capture on the lab interface and leave it running while you browse and use the lab services normally for five minutes. This is your baseline period.", ""),
            ("While the capture runs, generate the anomalous period: run a port scan against a lab host and then copy a large file across the network.", "nmap -sS -p- 192.168.56.101"),
            ("Stop the capture and save it as traffic.pcapng.", ""),
            ("Export per-connection features from the capture with tshark — source, destination, port, packet count, byte count and duration.",
             "tshark -r traffic.pcapng -q -z conv,tcp > conversations.txt"),
            ("Export the same data as CSV for the model to read.",
             "tshark -r traffic.pcapng -T fields -e ip.src -e ip.dst -e tcp.dstport -e frame.len -e frame.time_relative -E header=y -E separator=, > traffic.csv"),
            ("Load traffic.csv into pandas and aggregate it per (source, destination, port) conversation: packet count, total bytes, mean packet size and duration.",
             "python3 baseline.py   # provided in labs/lab-02/"),
            ("Fit an Isolation Forest on the baseline period only, with a contamination rate of 0.02, then score every conversation in the full capture.",
             "from sklearn.ensemble import IsolationForest\nmodel = IsolationForest(contamination=0.02, random_state=42).fit(X_baseline)\ndf['score'] = model.decision_function(X_all)"),
            ("Sort by score ascending and inspect the twenty most anomalous conversations. Open each one in Wireshark using a display filter and decide what it actually was.",
             "ip.addr == 192.168.56.101 && tcp.port == 445"),
            ("Mark each of the twenty as a true positive or a false positive, and write one sentence saying what evidence decided it.", ""),
            ("Ask your AI assistant to explain the anomalies and suggest which features would separate the scan from the file copy more cleanly. Test one of its suggestions and record whether it improved the result.",
             "Prompt: 'These network conversations were scored as anomalous by an Isolation Forest. Given packet count, byte count and duration, explain what behaviour each likely represents and suggest one additional feature that would separate port scanning from a legitimate large file transfer.'"),
        ],
        test=("The port scan appears in your top-ranked anomalies — it shows as many short connections from one "
              "source to many destination ports. You can name at least one false positive and explain why the "
              "model flagged legitimate traffic, and you can state your model's precision on the twenty you reviewed."),
        troubleshoot=("tshark is not found — it ships with Wireshark; on macOS add /Applications/Wireshark.app/Contents/MacOS to PATH. "
                      "The capture is empty — you may be capturing on the wrong interface; list them with `tshark -D`. "
                      "Everything scores as anomalous — your baseline period contained the attack traffic; re-cut the baseline to the quiet window only."),
    ),
    dict(
        num=3, topic=1,
        stages=[
            "Select key services",
            "Look up CVEs",
            "Check the KEV list",
            "Rate asset criticality",
            "Compute priority score",
        ],
        title="AI-Assisted Vulnerability Analysis and Prioritisation",
        objective="K2 · A1 · A2 — Turn a raw vulnerability list into a ranked, defensible worklist by combining CVSS severity with exploitability and business context.",
        desc=("A scanner will hand you hundreds of findings and no opinion about which one to fix on Monday morning. "
              "In this lab you take the service inventory from Lab 1, look up the real CVEs affecting those service "
              "versions, and then build a prioritisation that a manager would actually accept: CVSS base score "
              "combined with known-exploited status and the business criticality of the affected asset. You use an "
              "AI assistant to accelerate the research and then verify every claim it makes against the authoritative source."),
        build="A prioritised vulnerability worklist: CVE, affected asset, CVSS score, known-exploited flag, asset criticality, computed priority and a one-line recommended fix — ranked, with the top five justified.",
        services="Nmap service inventory, NVD, CISA KEV catalogue, a spreadsheet, a generative AI assistant",
        steps=[
            ("Take the service-version list from Lab 1. Pick the six most significant services — anything internet-facing, anything running as an administrator, anything holding data.", ""),
            ("For each service version, search the NIST National Vulnerability Database for matching CVEs and record the CVE ID and CVSS v3 base score.", "https://nvd.nist.gov/vuln/search"),
            ("Check each CVE against the CISA Known Exploited Vulnerabilities catalogue. A CVE on the KEV list is being exploited in the wild right now and outranks a higher CVSS score that is not.", "https://www.cisa.gov/known-exploited-vulnerabilities-catalog"),
            ("Assign each affected asset a business criticality of High, Medium or Low, based on what a loss of confidentiality, integrity or availability would cost. Write the justification in the row.", ""),
            ("Compute a priority score for every finding so the ranking is reproducible rather than a matter of taste.",
             "Priority = CVSS x Criticality weight x KEV multiplier\n  Criticality: High=1.5, Medium=1.0, Low=0.5\n  KEV: on the catalogue=2.0, not on it=1.0"),
            ("Sort by priority and inspect the top ten. Check that the order matches your professional judgement — if it does not, your weights are wrong, so fix the weights rather than the ranking.", ""),
            ("Ask your AI assistant to summarise each of your top five CVEs and propose a remediation for each.",
             "Prompt: 'For each of these CVEs, give the vulnerability class, the attack prerequisite, the practical impact, and the recommended remediation. State the CVSS v3 base score. Flag any CVE you are not certain about.'"),
            ("Verify every AI-supplied CVSS score and remediation against the NVD entry. Correct anything wrong and note where the AI was inaccurate — this is the evidence that you validated the model rather than trusted it.", ""),
            ("Write the two-sentence justification for your number-one priority: what could happen, and why it outranks everything else on the list.", ""),
        ],
        test=("Your worklist ranks every finding by a computed priority, not by CVSS alone; a KEV-listed CVE on a "
              "high-criticality asset sits above a higher-CVSS finding on a low-criticality one. You can point to "
              "at least one AI-supplied detail you corrected against the NVD."),
        troubleshoot=("NVD returns no CVE for a version string — search the product name and major version rather than the full banner. "
                      "Every finding scores the same — your criticality ratings are all identical; force a spread by ranking assets against each other. "
                      "The AI invents a CVE ID — this is exactly why step 8 exists; a CVE that is not in the NVD does not exist."),
    ),
]
