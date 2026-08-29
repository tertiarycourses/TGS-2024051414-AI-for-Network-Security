# Lab 10 — Centralise Logs and Triage Alerts with AI

**Topic 04 — AI-Assisted Security Incident Documentation and Response**  ·  LO4  ·  knowledge K4  ·  abilities A8, A9

## Maps to

A7 · K4 — Design the auditing arrangement that makes incident response possible, then use AI to reduce a flood of raw alerts into a ranked, workable queue.

## Goal

Incident response is only as good as the evidence available when it starts. In this lab you define what must be logged and for how long, work with a realistic multi-source log set, and then attack the actual bottleneck of a security operation: alert volume. You deduplicate, cluster and enrich the alerts, use an AI assistant to rank them and explain its reasoning, and then measure whether the ranking was any good.

## What you'll produce

A logging and audit specification, plus a triaged alert queue ranked by priority with an AI-generated rationale for each and your own verification of the top ten.

**Tools:** syslog, Windows Event Log, RegexLab (alfredang.github.io/regexgenerator), Python, pandas, a generative AI assistant

## Step-by-step

1. Write the logging specification: for each asset class name the log source, the events that must be captured, the retention period and where the log is centralised.
2. Include the events that matter for investigation — authentication success and failure, privilege escalation, configuration change, firewall deny, and process or service creation. A log of only failures cannot reconstruct an intrusion.
3. Specify time synchronisation. Every source must use NTP against the same reference, because a correlation across sources with skewed clocks is worthless.

   ```bash
   timedatectl set-ntp true && timedatectl status
   ```

4. Confirm the log integrity controls: append-only or write-once storage, restricted access, and forwarding off the host — an attacker with local admin will clear the local log first.
5. Load the provided multi-source alert set into pandas and look at the raw volume. This is the problem the rest of the lab solves.

   ```bash
   python3 triage.py   # provided in labs/lab-10/
   ```

6. Before filtering at scale, build the pattern and prove it works. Paste a representative log line into RegexLab, write a regex that extracts the source IP and the event type, and check the live match count and the match explanation. A filter you have not tested against real lines is how a triage pipeline silently drops evidence.

   → <https://alfredang.github.io/regexgenerator/>

7. Use the same tool to write a pattern that catches authentication FAILURES but not successes, then deliberately test it against a success line to confirm it does not match. Record both results — the negative test is the one that matters.

   → <https://alfredang.github.io/regexgenerator/>

8. Deduplicate: collapse identical alerts on the same source, destination and signature within a time window into one alert with a count. Record how much this alone reduces the queue.

   ```bash
   df.groupby(['src','dst','signature']).agg(count=('ts','size'), first=('ts','min'), last=('ts','max'))
   ```

9. Cluster the remaining alerts by source and by time so that a burst from one host reads as one incident rather than forty unrelated events.
10. Enrich each cluster with context from your earlier labs — the asset criticality from Lab 4 and the risk score from Lab 5. Context is what turns an alert into a priority.
11. Ask your AI assistant to rank the clusters and explain each ranking.

   ```bash
   Prompt: 'Here are deduplicated, enriched security alert clusters with asset criticality. Rank them by investigation priority. For each, state the likely attack technique, the evidence supporting it, and what a responder should check first. Flag any cluster where the evidence is ambiguous.'
   ```

12. Verify the top ten yourself against the raw logs. Count how many were genuinely high priority — that number is your triage precision, and it is what you report.
13. Write down the two alert types the AI ranked poorly and say what context it was missing. That gap is the enrichment you add next time.

## Test it

Your logging specification names the source, events, retention and central destination for every asset class. Deduplication and clustering reduce the queue by a measurable percentage that you can state, and you can report the triage precision of the top ten with the evidence that decided each one.

## If it doesn't work

Deduplication removes real incidents — your window is too wide; a repeated login failure over hours is a different event from forty in ten seconds. Everything ranks as critical — the asset-criticality join failed and every alert inherited the default. Timestamps do not line up — sources are in different time zones; normalise to UTC before correlating.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
