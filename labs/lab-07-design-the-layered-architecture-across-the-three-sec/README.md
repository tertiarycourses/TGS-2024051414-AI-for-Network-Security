# Lab 7 — Design the Layered Architecture Across the Three Security Phases

**Topic 03 — Designing and Implementing AI-Enhanced Network Security Measures**  ·  LO3  ·  knowledge K3  ·  abilities A5, A6, A7

## Maps to

A5 · K3 — Define the planning, building and management phases for a network security design, and express the design as layered defence-in-depth controls.

## Goal

Security design is a phased engineering activity, not a shopping list. In this lab you take the risk management plan from Lab 6 and produce an actual design: you write the requirements and constraints in the planning phase, draw a segmented target architecture with the controls placed at each layer, and define the management phase that keeps the design honest after go-live. You use an AI assistant as a design reviewer and then defend the design against its objections.

## What you'll produce

A three-phase security design: a planning-phase requirements table, a segmented target architecture diagram with controls at every layer, and a management-phase operating model.

**Tools:** Lab 6 plan, a diagramming tool (draw.io or paper), a generative AI assistant

## Step-by-step

1. Planning phase — write the security requirements the design must satisfy, each traced back to a specific risk ID from Lab 5. A requirement with no risk behind it is a preference.
2. Planning phase — record the constraints: budget, existing equipment, skills available, downtime tolerance and any regulatory obligation. Constraints are what make a design real.
3. Planning phase — define the trust zones: Internet, DMZ, internal user network, server network, management network and any OT or guest segment. State what each zone is allowed to reach.
4. Building phase — draw the target architecture with the zones as segments and place the controls at each layer: perimeter firewall, DMZ, internal segmentation, host controls and data controls.
5. Building phase — write the zone-to-zone access matrix. Rows are source zones, columns are destination zones, cells hold the permitted protocols. Default deny: every empty cell is blocked.
6. Building phase — classify every control you have placed as physical, technical or administrative, and confirm you have all three. A design with no administrative controls has no way to stay correct.
7. Management phase — define what happens after go-live: who monitors what, the review cadence, the change-control path, and the trigger that forces a redesign.
8. Ask your AI assistant to review the design as an attacker would.

   ```bash
   Prompt: 'Here is a segmented network security design with a zone access matrix. Acting as an attacker, describe three paths you would take through this architecture and name the control that would have to fail at each step. Then identify the weakest zone boundary.'
   ```

9. Answer each attack path in writing: either add a control that closes it, or record why the residual risk is acceptable and who accepts it.
10. Trace every High and Critical risk from Lab 5 to at least one control in the design. Any risk with no control is either untreated or was accepted — and it must say which.

## Test it

Every security requirement traces to a risk ID, the access matrix is default-deny with justified exceptions, all three control categories are present, and every High or Critical risk maps to a control or a documented acceptance. You can answer all three of the AI's attack paths.

## If it doesn't work

The matrix has more allow cells than deny — you are documenting today's flat network rather than designing a segmented one. No management phase — a design with no operating model degrades within a quarter. The AI's attack paths seem unrealistic — say why in writing; that reasoning is the deliverable.

---

Part of **AI for Network Security** (TGS-2024051414), conducted by Tertiary Infotech Academy Pte Ltd.  
Full detail is in the Learner Guide: `courseware/LG-AI-for-Network-Security.docx`.
