# Lab 2 — Baseline Normal Traffic and Detect an Anomaly with AI

**Topic 01 — AI-Assisted Network Threat and Vulnerability Analysis**  ·  LO1  ·  knowledge K1  ·  abilities A1, A2

## Maps to

K1 · K2 · A1 — Learn what 'normal' looks like on a network, then let a machine-learning model tell you when traffic stops being normal.

## Goal

Signature detection only finds what someone has already named. This lab builds the other half of the picture. You capture live traffic in Wireshark, turn it into per-connection features, train an unsupervised anomaly-detection model on the quiet 'pattern of life' period, and then score a period that contains a port scan and a data-staging burst. You see for yourself which events the model scores as anomalous and — just as importantly — which normal events it wrongly flags.

## What you'll produce

A labelled anomaly report: the connections your Isolation Forest model scored as anomalous, ranked by score, with your own verdict of true positive or false positive against the packet evidence.

**Tools:** Wireshark, tshark, the PCAP Analyzer (alfredang.github.io/pcapanalyzer), Python 3, pandas, scikit-learn, a generative AI assistant

## Step-by-step

1. Start a Wireshark capture on the lab interface and leave it running while you browse and use the lab services normally for five minutes. This is your baseline period.
2. While the capture runs, generate the anomalous period: run a port scan against a lab host and then copy a large file across the network.

   ```bash
   nmap -sS -p- 192.168.56.101
   ```

3. Stop the capture and save it as traffic.pcapng.
4. Before writing any code, get a fast read on what you captured. Drag traffic.pcapng into the PCAP Analyzer (it runs entirely in your browser — nothing is uploaded) and note the packet count, capture duration, protocol distribution, top talkers and top conversations.

   → <https://alfredang.github.io/pcapanalyzer/>

5. Write down which conversation you EXPECT the model to flag as anomalous, based on the top-talkers view alone. You will check that prediction against the model's output in step 10 — a human hypothesis first is what stops you rationalising whatever the model happens to say.
6. Export per-connection features from the capture with tshark — source, destination, port, packet count, byte count and duration.

   ```bash
   tshark -r traffic.pcapng -q -z conv,tcp > conversations.txt
   ```

7. Export the same data as CSV for the model to read.

   ```bash
   tshark -r traffic.pcapng -T fields -e ip.src -e ip.dst -e tcp.dstport -e frame.len -e frame.time_relative -E header=y -E separator=, > traffic.csv
   ```

8. Load traffic.csv into pandas and aggregate it per (source, destination, port) conversation: packet count, total bytes, mean packet size and duration.

   ```bash
   python3 baseline.py   # provided in labs/lab-02/
   ```

9. Fit an Isolation Forest on the baseline period only, with a contamination rate of 0.02, then score every conversation in the full capture.

   ```bash
   from sklearn.ensemble import IsolationForest
   model = IsolationForest(contamination=0.02, random_state=42).fit(X_baseline)
   df['score'] = model.decision_function(X_all)
   ```

10. Sort by score ascending and inspect the twenty most anomalous conversations. Open each one in Wireshark using a display filter and decide what it actually was.

   ```bash
   ip.addr == 192.168.56.101 && tcp.port == 445
   ```

11. Mark each of the twenty as a true positive or a false positive, and write one sentence saying what evidence decided it.
12. Ask your AI assistant to explain the anomalies and suggest which features would separate the scan from the file copy more cleanly. Test one of its suggestions and record whether it improved the result.

   ```bash
   Prompt: 'These network conversations were scored as anomalous by an Isolation Forest. Given packet count, byte count and duration, explain what behaviour each likely represents and suggest one additional feature that would separate port scanning from a legitimate large file transfer.'
   ```


## Test it

The port scan appears in your top-ranked anomalies — it shows as many short connections from one source to many destination ports. You can name at least one false positive and explain why the model flagged legitimate traffic, and you can state your model's precision on the twenty you reviewed.

## If it doesn't work

tshark is not found — it ships with Wireshark; on macOS add /Applications/Wireshark.app/Contents/MacOS to PATH. The capture is empty — you may be capturing on the wrong interface; list them with `tshark -D`. Everything scores as anomalous — your baseline period contained the attack traffic; re-cut the baseline to the quiet window only.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
