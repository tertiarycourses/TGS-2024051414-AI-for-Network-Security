# Lab 4 — Build an Asset Register and Classify What Needs Protecting

**Topic 02 — AI-Powered Network Risk Assessment and Management Planning**  ·  LO2  ·  knowledge K2  ·  abilities A3, A4

## Maps to

A3 · K1 — Determine which organisational assets require protection, and defend the classification with a business impact judgement rather than a gut feeling.

## Goal

Risk management starts with an honest asset register. In this lab you take the network inventory from Lab 1 and turn it into an organisational asset register: you add the owner, the data the asset holds, the business function it serves, and a classification against confidentiality, integrity and availability. You then rank the assets by criticality and use an AI assistant to challenge your classification — because the asset you forgot is the one that gets you.

## What you'll produce

A classified asset register with an owner, data classification and C/I/A impact rating for every asset, ranked by criticality, plus the crown-jewel shortlist.

**Tools:** Lab 1 inventory, a spreadsheet, a generative AI assistant

## Step-by-step

1. Open the network inventory from Lab 1 and add the organisational columns: Asset Name, Owner, Business Function, Data Held, Data Classification, Confidentiality Impact, Integrity Impact, Availability Impact, Criticality.
2. Classify the data each asset holds as Public, Internal, Confidential or Restricted. Write the reason in the row — an unjustified classification cannot be defended in a review.
3. Rate the Confidentiality, Integrity and Availability impact of losing each asset as High, Medium or Low. Ask the business question, not the technical one: what would this cost the organisation?
4. Set the asset Criticality to the highest of its three C/I/A ratings. An asset with High availability impact is critical even if its data is public — a payment gateway is the obvious case.
5. Add the assets that a network scan can never see: the people, the paper processes, the third-party services, the backups and the domain registration. These are real assets with real impact.
6. Sort by criticality and identify the crown jewels — the three to five assets whose loss would genuinely damage the organisation.
7. Ask your AI assistant to review your register for gaps.

   ```bash
   Prompt: 'Here is an asset register for a small enterprise network. Identify asset categories I have likely missed, and challenge any criticality rating that looks inconsistent with the stated business function. Do not rewrite my register — list the gaps and the inconsistencies.'
   ```

8. Act on the review: add every legitimate missing asset, and either correct or justify each rating the AI challenged. Record which challenges you accepted and which you rejected, with the reason.
9. Confirm every asset has a named owner. An asset with no owner has no one to accept its risk, which makes the register decorative.

## Test it

Every row has an owner, a data classification with a reason, three C/I/A ratings and a criticality. Your register includes at least two non-technical assets that no scanner would have found, and you can name your crown jewels and say what makes each one critical.

## If it doesn't work

Everything is rated High — you are rating the technology, not the business impact; force a ranking by asking which single asset you would restore first. Ownership is unclear — assign the manager of the business function the asset serves, not the system administrator.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
