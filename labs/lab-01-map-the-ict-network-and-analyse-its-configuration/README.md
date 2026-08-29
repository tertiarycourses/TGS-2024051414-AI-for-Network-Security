# Lab 1 — Map the ICT Network and Analyse Its Configuration

**Topic 01 — AI-Assisted Network Threat and Vulnerability Analysis**  ·  LO1  ·  knowledge K1  ·  abilities A1, A2

## Maps to

K1 · A1 — Establish what the network actually is before judging whether it is safe: discover live hosts, open ports and services, and read the configuration for weaknesses.

## Goal

You are handed an unfamiliar subnet and asked the question every security review starts with: what is on this network, and what is it running? You use Nmap to discover live hosts and their open ports and service versions, record the result as a structured inventory, and then read the configuration evidence for the weaknesses that matter — management ports exposed, unencrypted protocols in use, out-of-date service versions and default configurations left in place.

## What you'll produce

A network configuration inventory (host, IP, OS guess, open ports, service versions) plus a written list of the configuration weaknesses you found and why each one matters.

**Tools:** Nmap, Zenmap, the IP Calculator (alfredang.github.io/ipcalculator), a spreadsheet, a generative AI assistant

## Step-by-step

1. Confirm you are scanning only the lab network you have been authorised to scan. Never scan a network you do not own or have written permission to test.
2. Before you scan anything, work out exactly what 192.168.56.0/24 covers so your scan scope is defensible. Open the IP Calculator, enter the CIDR, and record the network address, the broadcast address, the usable host range and the host count.

   → <https://alfredang.github.io/ipcalculator/>

3. Discover which hosts are alive on the lab subnet with a ping sweep. Note how many hosts answer, and compare that against the usable host count you just calculated.

   ```bash
   nmap -sn 192.168.56.0/24
   ```

4. Run a service and version scan against the live hosts to learn what each one is actually running.

   ```bash
   nmap -sV -O -T4 192.168.56.0/24 -oN inventory.txt
   ```

5. Scan the full TCP port range on the one host that looks most interesting, so nothing above port 1024 is missed.

   ```bash
   nmap -sV -p- -T4 192.168.56.101 -oN host101-full.txt
   ```

6. Export the scan to a machine-readable form so it can be loaded into a spreadsheet or a script.

   ```bash
   nmap -sV 192.168.56.0/24 -oX inventory.xml
   ```

7. Build the inventory table in a spreadsheet with the columns Host, IP, OS, Open Ports, Services, Versions, Owner, Business Function.
8. Read the inventory for configuration weaknesses. Flag every unencrypted management protocol (Telnet 23, FTP 21, HTTP 80 on an admin interface), every service version that is behind, and every port that has no business being open.
9. Paste the sanitised Nmap output into your AI assistant and ask it to identify the configuration weaknesses and explain the risk of each. Compare its list against yours.

   ```bash
   Prompt: 'Here is Nmap output from a network I am authorised to assess. Identify configuration weaknesses, name the affected protocol or service, and explain the risk of each in one sentence.'
   ```

10. Reconcile the two lists. Record anything the AI found that you missed, and anything it claimed that the evidence does not support — the second list is the more important one.

## Test it

Your inventory names every live host with its open ports and service versions, and your weakness list contains at least five configuration weaknesses, each tied to specific evidence in the scan output. You can state, for each AI-suggested finding, whether the scan evidence actually supports it.

## If it doesn't work

No hosts answer the ping sweep — the lab hosts may block ICMP; re-run with `nmap -Pn`. The version scan is slow — narrow the port range with `-p 1-1024` or raise the timing to `-T4`. `-O` reports 'too many fingerprints' — OS detection needs at least one open and one closed port; it is a hint, not evidence.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
