---
title: Feature requirements for a worldly India AI Safety Institute
subtitle: Designing the IndiaAI Safety Institute from the evidence of ten peers
track: Track B, Investment (safety institutes)
---

## Summary

India is about to decide how it will test the most capable AI models before they reach a billion users. In October 2026 the government said a consultation paper on AI regulation would follow within weeks [S:in_mn_consult], and officials described pre-release evaluations and sandbox testing for the most capable models as options, without naming who would do the testing [S:in_elets]. India already has a body built for that job, the IndiaAI Safety Institute, announced in January 2025 [S:in_pib_aisi]. On paper it is the "main body" for safe and trusted AI [S:in_guidelines]. In practice this analysis finds that it has no published budget, no appointed accountable head position, and blurry hierarchical responsibilities across new apex governance bodies [S:in_dic], [S:in_pib_aigeg].

We compared how ten peers place, fund, steer and empower their institutes: the US and UK, seven middle powers and the EU AI Office. From that comparison we separate two things:

- **A baseline set of AISI features India should replicate now:** These are features most peers share and India lacks, like a named AI safety leader/ director, a defined regulatory/ non-regulatory role, governance shared across bodies, and membership of the international network.
- **A safety uplift set of AISI features India would do well to replicate over time:** These are features only one to four peers have that give the most safety coverage: pre-deployment access, a legal hook linking evaluation to duties, independence safeguards, reserved compute, published results and an incident reporting function.

| Key Takeaway | Analysis Confidence | Support |
|---|---|---|
| India's institute exists in name, but its money, leadership and powers are not yet defined | High | Official releases, vacancy notice for AISI director, parliamentary documentation) |
| Peers converge on a small, housed, non-statutory evaluator | High | Ten-jurisdiction comparison |
| Peers have real safety leverage, especially when it comes from a legal hook, compelled or contracted access, and AISI independence rules | Medium | Korea, EU statutes; UK practice  |
| Naming the institute as the evaluator in the coming law is the single highest-value decision | Medium | Judgement based on analysis |
| An Australia-level budget would cost about 10 times the current Safe & Trusted pillar within the current mandate, roughly 2% of the IndiaAI Mission over five years | Medium | Budget analysis across peers |

## 1. Why India, and why now

**India is the largest deployment-side test of AI governance:** India ranks first in the world for AI skill penetration and second for AI researchers and inventors, while also recording the largest net outflow of AI talent [S:in_aiindex]. GitHub counts about 32 million Indian developers, second only to the US and growing faster [S:in_octoverse]. India hosted the AI Impact Summit in February 2026, where 89 countries and the EU endorsed the New Delhi Declaration [S:in_delhi_decl] - the first convergence on AI related governance and regulation. Schwab and colleagues define middle powers as jurisdictions that host no frontier developer but shape deployment, procurement and regulation, and find that their duties fall on deployers and purchasers [S:schwab]. India fits that description at the largest scale.

**The risks are no longer hypothetical for deployers:** In April 2026 the UK AI Security Institute published an evaluation in which a frontier model completed a 32-step simulated corporate network attack in 3 of 10 attempts [S:uk_mythos]. In October 2026 Australia's government responded to OpenAI agents gaining unauthorised access to government websites, including a Medicare statistics portal, during testing [S:au_abc_charlton]. India runs the world's largest scaled national digital public infrastructure. It has the most to lose from agentic systems that incorrectly overreach. MeitY (Ministry of Electronics and Information Technology) - affiliated researchers have already built a DPI safety benchmark into an open India evaluation suite [S:in_inspect].

**The window is open now:** The minister has said AI risks have reached a threshold that calls for regulation. He compared the global coordination needed to nuclear governance most recently in October, and asked for human control and "a way to halt systems that go out of control" [S:in_mn_vaishnaw]. A consultation paper is due in November [S:in_mn_consult]. Whatever it proposes for pre-release testing needs an evaluator. Until the institute is formalized with responsibility and accountability structures, any at attempt at safety and governance will either default to developers' self-assessments or to a new body built from scratch.

**The gap is concrete:** The whole "Safe & Trusted AI pillar" of the IndiaAI Mission is ₹20.46 crore over five years, or 0.2% of the ₹10,371.92 crore AI Mission in general [S:in_mn_alloc]. The UK plans £60 million a year for its institute alone [S:uk_rd2930]. India's director post is planned as single contractual role[S:in_dic]. The apex AI Governance and Economic Group and its expert committee were set up in April 2026, and neither notice mentions the formal constitution of the institute [S:in_pib_aigeg], [S:in_tpec]. One analyst calls the result "institutions in name but not function" [S:in_eaf].

## 2. Theory of change

The claim here is narrow. Frontier models are built elsewhere but used in India at scale. India reduces risk most by knowing the depths of a model's capabilities before it is widely deployed, and by having a lawful way to act on what the country finds.

1. **Inputs:** A dedicated budget, a director with tenure, evaluators empanelled from India's partner-cell network, leveraging the deep talent pool, reserved compute from the IndiaAI Mission, and access agreements with developers.
2. **Activities:** Pre-deployment evaluation of the most capable models for India-relevant risks (cyber, DPI, multilingual misuse, agentic behaviour), incident intake, and publication of results with methods.
3. **Outputs:** Evaluation reports to MeitY and the apex AI governance bodies, published summaries, India-specific benchmarks, and inputs to the national incidents database.
4. **Outcomes:** Deployment decisions and safeguards informed by evidence rather than sensationalism. The coming law can turn "should be tested" into "is tested by the safety institute". India also formalizes a seat in the international evaluation network.
5. **Impact:** Fewer severe incidents from frontier models deployed in India, and earlier warning for everyone else.

**Where this can fail:** Developers may refuse access based on technical capabilities. Our idea is to initially pair voluntary agreements with a legal hook, as Korea and the EU do. Evaluations may produce findings no one acts on, which is the "measure but cannot act" problem Schwab et al. identify [S:schwab]. Our suggestion is to tie findings to named decision-makers. The institute may be captured by politics or industry. Our position is to model independence rules along the India's best regulator examples, in its central bank and federal financial markets authority, as well as the EU Scientific Panel [S:eu_act68], with precedence in AI-related governance. It may also be under-resourced into comparative irrelevance; the US centre is funded at $10 million a year [S:us_fedscoop], and the OSTP Director told Congress it "can certainly benefit from more resources". Our response is a protected multi-year budget line to kick start the functionality for the initial few years.

## 3. What ten peers show

The full evidence is in the comparison workbook: 17 features and a RACI matrix compare US, 8 middle powers, EU and India and outline RACI, budgetary and legislative factors.

**Pattern 1: nearly every institute is housed, small and non-statutory. All ten sit inside an existing body:**
- **Ministries:** DSIT in the UK [S:uk_about], ISED in Canada [S:ca_launch], DISR in Australia  [S:au_foi]
- **Laboratories:** NIST in the US [S:us_commerce], ETRI in Korea [S:kr_launch], IPA in Japan [S:jp_aisi]
- **A university:** NTU in Singapore [S:sg_about]
- **The Commission:** the EU AI Office
- **A federation of agencies:** INESIA in France [S:fr_create]

Among the institutes whose legal basis we could verify, only Korea [S:kr_act] and the EU [S:eu_decision] have a binding one. Australia's own documents say its institute "has no statutory powers" [S:au_foi]. Germany's government says its institute cannot demand model access [S:de_hib]. India's hub-and-spoke model inside the IndiaAI Mission is therefore normal given comparisons.

**Pattern 2: Funding and accountability is usually under the same ministry. Delivery is often shared:** Canada has the clearest split: ISED is accountable. CIFAR runs investigator-led research under a contribution agreement, and the National Research Council runs government-directed projects under an MOU [S:ca_launch]. Japan has the strongest cross-government steering: A council led by the Cabinet Office sits over the institute, twelve ministries and agencies take part, and four national laboratories work with it under a partnership agreement [S:jp_aisi]. France shows the cost of spread-ownership: A July 2026 parliamentary mission found INESIA has no legal personality and no budget of its own, and recommended a single supervising body [S:fr_paoli].

**Pattern 3: money is thin everywhere except the UK.** Converted at the exchange rates stated in the workbook:

| Institute | Annual budget | Basis |
|---|---|---|
| UK AI Security Institute | about $78M (£60M) | DSIT plan to 2029/30 [S:uk_rd2930] |
| US CAISI | $10M | FY2026 appropriation [S:us_fedscoop] |
| Canada CAISI | about $7.2M (C$10M) | C$50M over five years [S:ca_launch] |
| Australia AISI | about $4.8M (A$7.45M) | A$29.8M over four years [S:au_foi] |
| India | about $0.47M (₹4.1 crore) | ₹20.46 crore over five years [S:in_mn_alloc] |

**Pattern 4: real safety leverage within an AI Safety Institute is rare:** Only a few peers have it, and each has a different piece:
- **Access and publication (UK):** Pre-deployment access through MoUs, priority access to over £1.5 billion of compute [S:uk_about] , and published evaluations with methods [S:uk_mythos].
- **Legal hook (Korea):** The statute names a safety institute and ties it to a duty on operators of systems above a training-compute threshold [S:kr_act]. A draft notice sets that threshold at generally 10^26 FLOPs [S:kr_mondaq].
- **Compelled access and independence (EU):** The AI Office can compel access to general-purpose models by API or source code. Its scientific panel experts must be independent of providers and declare their interests [S:eu_act92], [S:eu_act68].
- **Incidents (Japan):** The draft revised plan gives the institute an incident-sharing role and asks for mechanisms that link evaluation results to ministries' decisions [S:jp_plan_draft].

No middle-power peer combines these pieces, which this document looks at as an opportunity.

## 4. Recommendations

Each recommendation lists what it does for safety, what it costs, and the stakeholder who must agree. The baseline items are low-cost and can be decided inside MeitY. The uplift items carry the largest safety impacts.

### Baseline features: replicate now (0 to 6 months)

**B1. Appoint a director with a fixed term:** Five of the ten peers have a named head in post in the sources we read, and India's single contractual post is unfilled [S:in_dic]. A fixed term of at least three years, with defined removal governance, is a cheap independence safeguard to start with, that also shows seriousness across other stakeholders.
- **Who must agree:** MeitY and within it, the IndiaAI Mission
- **Cost:** one senior salary

**B2. Give the institute a defined seat in the new apex structure:** Make it the technical secretariat for AI risk to the apex AI governance body, AIGEG and a standing invitee to the other AI governance body, TPEC. The original Guidelines already assign it support to these bodies [S:in_guidelines], but the April 2026 notices do not [S:in_pib_aigeg].
- **Who must agree:** The chair of the AIGEG should agree and own the integration
- **Cost:** none

**B3. State its role in formalized mandates:** It evaluates and advises; it does not regulate. Five peers say this explicitly, and it reduces industry resistance [S:uk_intro],  [S:kr_launch], [S:au_foi]. The founding charter (a sample charter that formalizes these recommendations) in Annex A does this.

**B4. Join the international network:** Nine of ten peers are members [S:net_mission], and the original Guidelines say the institute should represent India there [S:in_guidelines]. Membership brings shared methods, tools such as Inspect (which India's own evaluation suite already builds on [S:in_inspect]) and collaborative testing.
- **Who must agree:** MeitY and Ministry of External Affairs

### Uplift: features that provide the safety premium (6 to 36 months)

**U1. Name the institute as India's pre-deployment tester/ evaluator in the coming law:**
- **Safety impact:** highest; it turns pre-release testing from an option into an obligation for a formalized agency. This addresses the gap Schwab et al. find across middle powers, where evaluators measure but cannot act [S:schwab] as cleanly.
- **Model:** Korea's Article 12 and Article 32. The statute names the institute, defines its functions, and links it to safety duties for systems above a compute threshold [S:kr_act].
- **Who must agree:** MeitY drafts, the Union Cabinet approves, Parliament passes such mandates assigning formalized roles to the Institute
- **Cost:** eventual expert empanelment and logistics costs that the rest of the recommendations already cover

**U2. Contracted pre-deployment access now, before any law**
- **What it involves:** sign access agreements with developers whose models are deployed at scale in India, with a minimum evaluation window.
- **Model:** the UK's MoUs; the UK's experience shows windows can shrink to days [S:uk_ada], so a minimum window must be in the agreement.
- **Who must agree:** MeitY and each developer.
- **Feasibility:** medium; India's market size is the leverage

**U3. Reserve compute for evaluation:**
- **What it involves:** set aside a fixed share of IndiaAI Mission compute for the institute and empanelled evaluators. The IndiaAI Mission has sanctioned 9,300,000 GPU hours [S:in_pib_safe]. In comparison, the UK gives its institute priority access to its national compute [S:uk_about].
- **Annex:** our audit of 11 public compute programmes found no AI-safety condition or reserved evaluator share in any of them (see the companion workbook - which was pending verification at the time of submission of this work).
- **Who must agree:** the IndiaAI Mission governance chief
- **Cost:** opportunity cost of democratised compute

**U4. Independence and publication rules:**
- **Independence:** empanelled evaluators declare interests and take no instructions from political or industry influences, just as the EU Scientific Panel's members must and musn't [S:eu_act68].
- **Publication:** results are published with methods by default, with security redactions, following UK practices [S:uk_mythos].
- **Why it matters:** the US shows the risk of doing neither. Its centre's mission was redirected by a change of administration, and publication of its assessments was reportedly halted [S:us_commerce], [S:us_transformer].
- **Who must agree:** MeitY
- **Cost:** none

**U5. An evaluator empanelment route**
- **What it involves:** convert the AI Mission partner-cell EoI [S:in_eoi] into a standing panel of accredited evaluators, with conflict-of-interest screening.
- **Models:** the US consortium works through cooperative research agreements [S:us_aisic]. Philanthropy-funded fellowships place technical staff in US security offices with recusal rules [S:us_horizon].
- **Benefit:** this also addresses India's talent outflow, and eventually has the opportunity to reverse it [S:in_aiindex].
- **Who must agree:** MeitY and the IndiaAI Mission
- **Cost:** within U6 as outlined below

**U6. A protected, multi-year budget line:** An Australia-level institute, a lean in-house testing team, would cost about ₹42 crore a year. That is about ten times the current pillar's appropriated annual average, and about 2% of the IndiaAI Mission's appropriated budget over five years (workbook, "Budgets" sheet).
- **Who must agree:** the Ministry of Finance (Department of Expenditure) on MeitY's proposal
- **Feasibility:** medium; The India AI Mission's 2026-27 budget estimate is ₹1,000 crore, but releases have lagged allocations [S:in_mn_release].

**Also: an incident function:** Make the institute the technical analyst for the national AI incidents database the initial AI governance Guidelines propose [S:in_guidelines], with CERT-In for cyber incidents. Most recent incidents were communicated within hours of identification, which describes the capability's existence. Japan's draft plan gives its institute this role [S:jp_plan_draft].

## 5. Feasibility: who must agree, and in what order

| Step | Decision-maker | Instrument | Time |
|---|---|---|---|
| Director, charter, apex seat (B1 to B3) | MeitY Secretary, IndiaAI CEO | Office order; charter adopted by MeitY | 0 to 3 months |
| Network membership (B4) | MeitY with MEA | Communications with the network | 0 to 6 months |
| Access agreements (U2), compute share (U3), rules (U4, U5) | MeitY, IndiaAI Mission | MoUs; Mission guidelines | 3 to 12 months |
| Budget line (U6) | Ministry of Finance | Expenditure Finance Committee; Union Budget | Next budget cycle |
| Legal mandate (U1) | Cabinet, Parliament | Clauses in the forthcoming AI law | 12 to 36 months |

Most of this needs no new law and no new organisation, which answers the main objection Indian commentators regularly raise: that an institute would become another bureaucracy or a Western import [S:in_carnegie]. The design keeps India's hub-and-spoke model and adds a few hard edges given evidence that they together make up the minimum viable institute as features.

## 6. What could make these recommendations land imperfectly:

- **Budget comparisons depend on exchange rates and scope:** India's figure is that of the safety pillar within it's total guidelines, and not verifiably for an institute.
- **Single-source claims:** Some US and Australian details come from one outlet only. They are labelled in the workbook and are not load-bearing.
- **Access may not follow money:** Even a well-funded institute may be refused access. Our answer is the legal hook (U1) and leveraging India's market size.
- **The consultation paper may already assign testing elsewhere:** If so, the charter should be adapted so the institute serves that body as its technical arm.

**Method:** We searched each jurisdiction and read official pages, statutes, budget documents, parliamentary answers. We recorded 93 findings against 67 sources, each graded A (statute), B (official publication) or C (news or analysis). Features were coded from those findings. The coding, the thresholds and the exchange rates are all editable in the workbook, so readers can test our conclusions. Annex A is a draft founding charter. The companion workbooks hold the evidence.
