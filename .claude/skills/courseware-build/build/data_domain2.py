"""
Topic 2 — AI-Powered Network Risk Assessment and Management Planning.
LO2 · K2 · A3, A4.  Labs 4-6.
"""

DOMAIN2 = [
    dict(
        num=4, topic=2,
        stages=[
            "Add business columns",
            "Classify the data",
            "Rate C / I / A impact",
            "Set asset criticality",
            "Add unseen assets",
        ],
        title="Build an Asset Register and Classify What Needs Protecting",
        objective="A3 · K1 — Determine which organisational assets require protection, and defend the classification with a business impact judgement rather than a gut feeling.",
        desc=("Risk management starts with an honest asset register. In this lab you take the network inventory from "
              "Lab 1 and turn it into an organisational asset register: you add the owner, the data the asset holds, "
              "the business function it serves, and a classification against confidentiality, integrity and availability. "
              "You then rank the assets by criticality and use an AI assistant to challenge your classification — "
              "because the asset you forgot is the one that gets you."),
        build="A classified asset register with an owner, data classification and C/I/A impact rating for every asset, ranked by criticality, plus the crown-jewel shortlist.",
        services="Lab 1 inventory, a spreadsheet, a generative AI assistant",
        steps=[
            ("Open the network inventory from Lab 1 and add the organisational columns: Asset Name, Owner, Business Function, Data Held, Data Classification, Confidentiality Impact, Integrity Impact, Availability Impact, Criticality.", ""),
            ("Classify the data each asset holds as Public, Internal, Confidential or Restricted. Write the reason in the row — an unjustified classification cannot be defended in a review.", ""),
            ("Rate the Confidentiality, Integrity and Availability impact of losing each asset as High, Medium or Low. Ask the business question, not the technical one: what would this cost the organisation?", ""),
            ("Set the asset Criticality to the highest of its three C/I/A ratings. An asset with High availability impact is critical even if its data is public — a payment gateway is the obvious case.", ""),
            ("Add the assets that a network scan can never see: the people, the paper processes, the third-party services, the backups and the domain registration. These are real assets with real impact.", ""),
            ("Sort by criticality and identify the crown jewels — the three to five assets whose loss would genuinely damage the organisation.", ""),
            ("Ask your AI assistant to review your register for gaps.",
             "Prompt: 'Here is an asset register for a small enterprise network. Identify asset categories I have likely missed, and challenge any criticality rating that looks inconsistent with the stated business function. Do not rewrite my register — list the gaps and the inconsistencies.'"),
            ("Act on the review: add every legitimate missing asset, and either correct or justify each rating the AI challenged. Record which challenges you accepted and which you rejected, with the reason.", ""),
            ("Confirm every asset has a named owner. An asset with no owner has no one to accept its risk, which makes the register decorative.", ""),
        ],
        test=("Every row has an owner, a data classification with a reason, three C/I/A ratings and a criticality. "
              "Your register includes at least two non-technical assets that no scanner would have found, and you "
              "can name your crown jewels and say what makes each one critical."),
        troubleshoot=("Everything is rated High — you are rating the technology, not the business impact; force a "
                      "ranking by asking which single asset you would restore first. Ownership is unclear — assign "
                      "the manager of the business function the asset serves, not the system administrator."),
    ),
    dict(
        num=5, topic=2,
        stages=[
            "Create the register",
            "Write each risk",
            "Score likelihood",
            "Score impact",
            "Compute inherent risk",
        ],
        title="AI-Assisted Risk Scoring and the Risk Register",
        objective="A2 · A4 · K4 — Combine the asset register and the vulnerability worklist into a scored risk register, using AI to sharpen the likelihood estimate.",
        desc=("A risk is not a vulnerability. A risk is a threat exploiting a vulnerability against an asset, with a "
              "likelihood and an impact. In this lab you join Lab 3's vulnerabilities to Lab 4's assets to produce a "
              "proper risk register, score each entry on a 5x5 likelihood-impact matrix, and use an AI assistant to "
              "pressure-test your likelihood estimates against current threat intelligence. You end with a heat map "
              "that shows management where the real exposure is."),
        build="A scored risk register with inherent risk, existing controls and residual risk for every entry, plus a 5x5 heat map showing the distribution.",
        services="Lab 3 worklist, Lab 4 asset register, a spreadsheet, a generative AI assistant",
        steps=[
            ("Create the risk register with the columns Risk ID, Asset, Threat, Vulnerability, Existing Controls, Likelihood (1-5), Impact (1-5), Inherent Risk, Treatment, Owner, Target Date, Residual Risk.", ""),
            ("Write each risk as a full sentence before you score it: 'A [threat actor] exploits [vulnerability] on [asset], resulting in [consequence].' A risk you cannot phrase this way is not yet a risk.", ""),
            ("Score Likelihood 1-5 using evidence — is the vulnerability on the CISA KEV list, is the asset internet-facing, is there a public exploit, does an existing control reduce the chance?", ""),
            ("Score Impact 1-5 from the asset's criticality in Lab 4, adjusted for what this specific threat would actually do to it.", ""),
            ("Compute Inherent Risk as Likelihood x Impact, and band it: 1-4 Low, 5-9 Medium, 10-14 High, 15-25 Critical.", "Inherent Risk = Likelihood × Impact"),
            ("Record the controls already in place for each risk, then re-score to get Residual Risk. The gap between inherent and residual is exactly what your existing controls are buying you.", ""),
            ("Ask your AI assistant to challenge your likelihood scores against current threat activity.",
             "Prompt: 'Here is a risk register with likelihood scores from 1 to 5. For each risk, state whether current threat intelligence suggests my likelihood is too high, too low or about right, and give the reason. Note where you are uncertain.'"),
            ("Adjust the scores you agree with and document the ones you rejected. A risk register that is never challenged is a risk register nobody believes.", ""),
            ("Build the 5x5 heat map — likelihood on one axis, impact on the other, each cell counting the risks that land in it — and identify which quadrant carries your exposure.", ""),
            ("Sort by residual risk and confirm the top five are the risks you would genuinely lose sleep over. If they are not, your scoring is wrong.", ""),
        ],
        test=("Every risk is written as a complete threat-vulnerability-asset-consequence sentence and carries both "
              "an inherent and a residual score. Your heat map shows a real spread rather than everything clustered "
              "in one cell, and you can justify your top five to a manager."),
        troubleshoot=("Inherent and residual are identical everywhere — you have not recorded the existing controls. "
                      "All risks land in the same band — your 1-5 scales are being used as 3-4; force the extremes. "
                      "The AI is confidently wrong about a threat — treat its output as a prompt to check the source, never as the source."),
    ),
    dict(
        num=6, topic=2,
        stages=[
            "Assign a treatment",
            "Name the accepting authority",
            "Name the control",
            "State the control type",
            "Add owner & criterion",
        ],
        title="Develop the Risk Management Plan",
        objective="A4 · K4 — Turn the scored register into a risk management plan with treatments, owners, dates and a monitoring cadence that survives contact with reality.",
        desc=("A register records risk; a plan does something about it. In this lab you assign each risk one of the "
              "four treatments — mitigate, transfer, avoid or accept — select the specific controls that implement "
              "the mitigation, name an owner and a target date for each, and map the whole plan onto the NIST "
              "Cybersecurity Framework functions so that the coverage gaps become visible. You then use AI to draft "
              "the management summary and you edit it into something you would actually sign."),
        build="A risk management plan: treatment decisions with named controls, owners, target dates and success criteria; a NIST CSF coverage map; and a one-page management summary.",
        services="Lab 5 risk register, NIST CSF 2.0, a spreadsheet, a generative AI assistant",
        steps=[
            ("Assign each risk in the register one of the four treatments — Mitigate, Transfer, Avoid or Accept. Every risk gets exactly one; nothing may be left blank.", ""),
            ("Every Accept decision needs a named accepting authority and a written rationale. An accepted risk with no name against it is an ignored risk.", ""),
            ("For each Mitigate decision, name the specific control that will reduce the risk — not 'improve security', but 'disable Telnet on the three switches and enforce SSHv2 with key authentication'.", ""),
            ("State the control type for each: preventive, detective or corrective. A plan made only of detective controls will find every breach and stop none of them.", ""),
            ("Add an owner, a target date and a success criterion to every treatment. The success criterion must be testable — 'no Telnet listener on any managed switch, verified by Nmap' is testable; 'switches hardened' is not.", ""),
            ("Map every planned control onto the NIST CSF 2.0 functions — Govern, Identify, Protect, Detect, Respond, Recover — and count the controls in each. The thin function is your real gap.",
             "https://www.nist.gov/cyberframework"),
            ("Fill the thinnest function with at least one concrete control. Most first-draft plans are heavy on Protect and empty on Recover.", ""),
            ("Set the monitoring cadence: which risks are reviewed monthly, which quarterly, and what event forces an out-of-cycle review.", ""),
            ("Ask your AI assistant to draft a one-page management summary of the plan for a non-technical audience.",
             "Prompt: 'Summarise this risk management plan for a non-technical executive in under 400 words: the top three exposures in business terms, what we are doing about each, what it needs, and what happens if we do nothing. No jargon.'"),
            ("Edit the draft hard. Cut anything the register does not support, and add the one thing the AI could not know — what this actually costs and who has to approve it.", ""),
        ],
        test=("Every risk carries a treatment, and every Mitigate carries a named control, an owner, a date and a "
              "testable success criterion. Your NIST CSF map has at least one control under all six functions, and "
              "the management summary states the top three exposures in business language without jargon."),
        troubleshoot=("Everything is Mitigate — some risks are genuinely cheaper to accept or transfer; a plan that "
                      "mitigates everything will be funded for nothing. Success criteria are unverifiable — rewrite "
                      "each one as a test someone could run. Recover is empty — add backup restoration testing."),
    ),
]
