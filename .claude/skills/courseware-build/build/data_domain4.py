"""
Topic 4 — AI-Assisted Security Incident Documentation and Response.
LO4 · K4 · A8, A9.  Labs 10-12.
"""

DOMAIN4 = [
    dict(
        num=10, topic=4,
        stages=[
            "Write the log spec",
            "List required events",
            "Synchronise the clocks",
            "Protect log integrity",
            "Load the alert set",
        ],
        title="Centralise Logs and Triage Alerts with AI",
        objective="A7 · K4 — Design the auditing arrangement that makes incident response possible, then use AI to reduce a flood of raw alerts into a ranked, workable queue.",
        desc=("Incident response is only as good as the evidence available when it starts. In this lab you define what "
              "must be logged and for how long, work with a realistic multi-source log set, and then attack the actual "
              "bottleneck of a security operation: alert volume. You deduplicate, cluster and enrich the alerts, use an "
              "AI assistant to rank them and explain its reasoning, and then measure whether the ranking was any good."),
        build="A logging and audit specification, plus a triaged alert queue ranked by priority with an AI-generated rationale for each and your own verification of the top ten.",
        services="syslog, Windows Event Log, Python, pandas, a generative AI assistant",
        steps=[
            ("Write the logging specification: for each asset class name the log source, the events that must be captured, the retention period and where the log is centralised.", ""),
            ("Include the events that matter for investigation — authentication success and failure, privilege escalation, configuration change, firewall deny, and process or service creation. A log of only failures cannot reconstruct an intrusion.", ""),
            ("Specify time synchronisation. Every source must use NTP against the same reference, because a correlation across sources with skewed clocks is worthless.",
             "timedatectl set-ntp true && timedatectl status"),
            ("Confirm the log integrity controls: append-only or write-once storage, restricted access, and forwarding off the host — an attacker with local admin will clear the local log first.", ""),
            ("Load the provided multi-source alert set into pandas and look at the raw volume. This is the problem the rest of the lab solves.",
             "python3 triage.py   # provided in labs/lab-10/"),
            ("Deduplicate: collapse identical alerts on the same source, destination and signature within a time window into one alert with a count. Record how much this alone reduces the queue.",
             "df.groupby(['src','dst','signature']).agg(count=('ts','size'), first=('ts','min'), last=('ts','max'))"),
            ("Cluster the remaining alerts by source and by time so that a burst from one host reads as one incident rather than forty unrelated events.", ""),
            ("Enrich each cluster with context from your earlier labs — the asset criticality from Lab 4 and the risk score from Lab 5. Context is what turns an alert into a priority.", ""),
            ("Ask your AI assistant to rank the clusters and explain each ranking.",
             "Prompt: 'Here are deduplicated, enriched security alert clusters with asset criticality. Rank them by investigation priority. For each, state the likely attack technique, the evidence supporting it, and what a responder should check first. Flag any cluster where the evidence is ambiguous.'"),
            ("Verify the top ten yourself against the raw logs. Count how many were genuinely high priority — that number is your triage precision, and it is what you report.", ""),
            ("Write down the two alert types the AI ranked poorly and say what context it was missing. That gap is the enrichment you add next time.", ""),
        ],
        test=("Your logging specification names the source, events, retention and central destination for every asset "
              "class. Deduplication and clustering reduce the queue by a measurable percentage that you can state, "
              "and you can report the triage precision of the top ten with the evidence that decided each one."),
        troubleshoot=("Deduplication removes real incidents — your window is too wide; a repeated login failure over "
                      "hours is a different event from forty in ten seconds. Everything ranks as critical — the "
                      "asset-criticality join failed and every alert inherited the default. Timestamps do not line up — sources are in different time zones; normalise to UTC before correlating."),
    ),
    dict(
        num=11, topic=4,
        stages=[
            "Open the incident record",
            "Reconstruct the timeline",
            "Separate fact from inference",
            "Classify the severity",
            "List affected assets",
        ],
        title="Document a Security Incident to the Standard",
        objective="A8 · K4 — Produce an incident record that is complete enough to hand to a manager, an auditor or a regulator without a conversation attached.",
        desc=("An incident that is badly documented is an incident that teaches nothing and proves nothing. Working "
              "from the top-priority cluster in Lab 10, you reconstruct the timeline from the raw evidence, classify "
              "the severity against defined criteria, and write the full incident record: what happened, when, to "
              "which assets, what was done, what the evidence is and who was accountable. You use AI to draft the "
              "narrative and then you correct it against the log — because the draft will confidently state things the evidence does not."),
        build="A complete incident record with a reconstructed evidence-based timeline, a justified severity classification, the actions taken, the evidence inventory and the notification decisions.",
        services="Lab 10 alert queue and raw logs, NIST SP 800-61, an incident record template, a generative AI assistant",
        steps=[
            ("Open an incident record and fill the header: incident ID, date and time of detection, detected by, reporter, current status and the assigned handler.", ""),
            ("Reconstruct the timeline from the raw logs in UTC. Every entry needs a timestamp, the event, the source system and the log line that proves it. A timeline entry with no evidence reference is a claim, not a finding.", ""),
            ("Separate what you know from what you infer. Write inferences as inferences — 'the account was used from an unrecognised address, which suggests credential compromise' is honest; stating the compromise as fact is not.", ""),
            ("Classify the severity against written criteria: assets affected, data classification involved, business impact and whether the activity is ongoing. State the criteria you applied so the rating can be reviewed.", ""),
            ("List the affected assets by name from the Lab 4 register, with their criticality and the data classification each one holds.", ""),
            ("Record the response actions taken with a timestamp and the name of the person who took each one. Include the actions that were considered and rejected, and why — a reviewer will ask.", ""),
            ("Build the evidence inventory: log extracts, packet captures, screenshots and system images, each with where it is stored, its hash and who has access. This is what makes the record defensible.",
             "shasum -a 256 evidence/*.pcapng evidence/*.log > evidence/MANIFEST.sha256"),
            ("Record the notification decisions — who was informed, when, and which obligations were considered. In Singapore, consider whether the PDPA data-breach notification obligation to the PDPC and affected individuals is engaged, and record the reasoning either way.", ""),
            ("Ask your AI assistant to draft the incident narrative from your timeline.",
             "Prompt: 'Draft a factual incident narrative from this evidence timeline. Use only what the timeline supports. Mark every inference explicitly as an inference. Do not speculate about attribution.'"),
            ("Check the draft line by line against the timeline. Delete every statement the evidence does not support and every attribution claim. Record what you removed — that edit is the professional skill this lab teaches.", ""),
            ("Write the lessons-learned section: what detected it, what delayed the response, and the one control change that would have prevented or caught it earlier. Feed that change back into the Lab 6 plan.", ""),
        ],
        test=("Every timeline entry cites its evidence source, inferences are marked as inferences, the severity "
              "classification states the criteria used, and the evidence inventory carries a hash for every item. "
              "You can name at least one unsupported statement you removed from the AI draft."),
        troubleshoot=("The timeline has gaps — that is a finding about your logging, so record the gap rather than "
                      "guessing what filled it. Severity is contested — that means the criteria were not written down "
                      "before the incident. The AI names an attacker group — remove it; attribution needs intelligence you do not have."),
    ),
    dict(
        num=12, topic=4,
        stages=[
            "Write the containment",
            "Verify it works",
            "Record collateral impact",
            "Write the playbook",
            "Set automation levels",
        ],
        title="Implement the Incident Response Configuration and Playbook",
        objective="A9 · A7 · K4 — Implement configurations aligned to the incident response design: containment controls, an automated playbook and the human-approval boundary.",
        desc=("The final lab closes the loop. You take the incident from Lab 11 and implement the response as "
              "configuration: the containment controls that would stop it recurring, a documented SOAR-style playbook "
              "with explicit automation and approval steps, and detection rules derived from what you actually saw. "
              "You then test the playbook against a replayed scenario, measure the response time, and confirm that no "
              "automated action can cause more damage than the incident it responds to."),
        build="Implemented containment configurations, a tested incident response playbook with a defined human-approval boundary, new detection rules, and a measured response time from detection to containment.",
        services="Firewall and host configuration, playbook template, Lab 8 detection rules, a generative AI assistant",
        steps=[
            ("Write the containment configuration for the Lab 11 incident: the firewall rules, account actions and host isolation steps that stop this specific attack path, as commands rather than prose.",
             "iptables -I FORWARD 1 -s 192.168.56.101 -j DROP -m comment --comment 'INC-2026-001 containment'"),
            ("Verify each containment control actually works, and record the verification command and its output. An untested containment control is an assumption.", ""),
            ("Record the collateral impact of each containment action before it is ever needed. Isolating a host stops the attacker and also stops that host's business function — the responder must know which they are trading.", ""),
            ("Write the playbook with the standard phases: Detect, Triage, Contain, Eradicate, Recover, Review. Each step names the trigger, the action, the owner and the expected duration.", ""),
            ("Mark each step Automated, Automated-with-approval or Manual. Reversible, low-blast-radius actions can be automated; anything that takes production offline needs a named approver.", ""),
            ("Define the escalation path with names and contact methods, and the time threshold that triggers each escalation. A playbook with no named person is a document, not a capability.", ""),
            ("Add the detection rules from this incident to your Lab 8 ruleset so the same attack is caught earlier next time, and record the expected false-positive rate of each new rule.", ""),
            ("Test the playbook against a replayed scenario. Walk every step, time it, and note where it stalls — the stall is where the playbook is wrong.", ""),
            ("Measure detection-to-containment time and compare it against your target. If there is no target, set one now — a response time nobody is accountable for will drift.", ""),
            ("Ask your AI assistant to review the playbook for gaps and dangerous automation.",
             "Prompt: 'Review this incident response playbook. Identify missing steps, any automated action whose blast radius exceeds the incident it responds to, and any step with no named owner. For each finding, say what you would change.'"),
            ("Fix every genuine gap. For any automated action flagged as too broad, either narrow its scope or move it behind human approval, and record the decision.", ""),
            ("Feed the whole result back: update the Lab 6 risk management plan with the control changes and re-score the affected risks. The loop from incident back to plan is what makes this a management system rather than a set of documents.", ""),
        ],
        test=("Every containment control has a verification command and a recorded output, every playbook step names "
              "an owner and an automation level, and you can state a measured detection-to-containment time against "
              "a target. No automated step can take a production service offline without a named approver."),
        troubleshoot=("The containment rule does not take effect — check the rule order; an earlier ACCEPT will win. "
                      "The playbook test stalls waiting for a decision — that is the finding, so add the decision "
                      "authority. The AI proposes automating everything — apply the blast-radius test yourself; that judgement is not delegable."),
    ),
]
