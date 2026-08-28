# Lab 8 — Implement AI-Enhanced Controls — Firewall Policy, IDS and Adaptive Access

**Topic 03 — Designing and Implementing AI-Enhanced Network Security Measures**  ·  LO3  ·  knowledge K3  ·  abilities A5, A6, A7

## Maps to

A6 · K3 — Develop the security measures for the network components: build a default-deny firewall policy, tune detection rules, and specify adaptive AI-driven access control.

## Goal

This is where the design becomes configuration. You write a default-deny firewall ruleset from the Lab 7 access matrix, run detection against real traffic to see what your rules actually catch, and specify the risk-based conditions under which an AI-driven access control should step up authentication or block outright. You then compare a static rule against a behavioural model on the same traffic — and see exactly where each one wins.

## What you'll produce

A default-deny firewall ruleset derived from the access matrix, a tuned detection ruleset with its true/false positive counts, and an adaptive access-control policy specification.

**Tools:** Firewall rule syntax (iptables or a NGFW policy table), Wireshark, Python, a generative AI assistant

## Step-by-step

1. Translate the Lab 7 access matrix into an ordered firewall ruleset. Specific allow rules first, the default deny last — order is the whole game in a firewall.

   ```bash
   # Rule 1: allow established return traffic
   iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT
   # Rule N: default deny (must be last)
   iptables -P FORWARD DROP
   ```

2. Write each allow rule with source zone, destination zone, protocol, port, and a comment naming the business reason. An uncommented rule becomes permanent because nobody dares delete it.

   ```bash
   iptables -A FORWARD -s 10.0.10.0/24 -d 10.0.30.0/24 -p tcp --dport 443 -j ACCEPT -m comment --comment 'Users to app servers HTTPS - REQ-004'
   ```

3. Add explicit deny-and-log rules for the traffic you most want to know about — management protocols crossing a zone boundary, and any outbound connection from the server zone.
4. Review the ruleset for shadowed rules: any rule that can never match because an earlier rule already covers its traffic. Shadowed rules are the most common firewall defect there is.
5. Now the detection layer. Write three detection rules against the Lab 2 capture — one for a port scan, one for a large outbound transfer, and one for a connection to a management port from a user subnet.
6. Run each rule over the capture and count the true positives and false positives. A rule with more false positives than true is worse than no rule, because it trains the analyst to ignore alerts.

   ```bash
   tshark -r traffic.pcapng -Y 'tcp.flags.syn==1 && tcp.flags.ack==0' -T fields -e ip.src | sort | uniq -c | sort -rn
   ```

7. Compare the static rule against the Lab 2 anomaly model on the same traffic. Record where the rule wins (precision on known patterns) and where the model wins (unnamed behaviour).
8. Specify the adaptive access-control policy: the signals (device posture, location, time, behaviour deviation, resource sensitivity), the risk bands, and the action at each band — allow, step-up MFA, restrict, or block.
9. State the human-in-the-loop boundary explicitly. Which actions may the system take autonomously, and which require a named person to approve? Automatic blocking of a production server needs an owner.
10. Ask your AI assistant to review the firewall ruleset for shadowed rules, overly broad allows and missing egress controls, then verify each finding by reading the rule yourself.

   ```bash
   Prompt: 'Review this ordered firewall ruleset. Identify shadowed rules that can never match, allow rules that are broader than their stated business reason, and any missing egress control. Quote the rule number for each finding.'
   ```


## Test it

Your ruleset ends in an explicit default deny, every allow rule carries a business-reason comment traced to a requirement, and you have no shadowed rules. You can state the true/false positive count for each detection rule and say which of the static rule or the AI model you would deploy for each of the three detections, and why.

## If it doesn't work

The default deny is not last — everything after it is dead code. All traffic is blocked — you are missing the ESTABLISHED,RELATED rule, so return traffic never gets back. The detection rule fires constantly — your threshold is tuned to a quiet lab, not to production; raise it against the baseline.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
