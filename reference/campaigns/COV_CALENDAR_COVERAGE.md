# COV -- Calendar Coverage Events

> Knowledge document for the COV campaign engine. 7 awareness-month-triggered campaigns for existing clients with a product gap.
> All content approved by JDM on 2026-02-16.

---

## Engine Overview

**COV = Calendar Coverage Events.** Awareness-month-triggered campaigns that fire for existing RPI clients who have a gap in their coverage portfolio. Each campaign uses a national awareness month or seasonal event as a natural conversation opener, combined with the PSM-NO-CORE positioning: "You're our client, but you don't have THIS."

| Metric | Value |
|--------|-------|
| **Total Campaigns** | 7 |
| **Campaign Type** | Cross-sell / gap detection |
| **Target** | Existing RPI clients missing a specific product type |
| **Channels per campaign** | Email, Text/SMS, Voicemail Script, USPS Mailer |
| **Execution path** | C3 (campaign engine) --> PRODASH (delivery) --> 4 channels |
| **Formula** | NO-CORE positioning + PSM product education + awareness month timing |

### Campaign Inventory

| # | Campaign ID | Name | Timing | Product Gap |
|---|-------------|------|--------|-------------|
| 1 | COV-PREAEP | Pre-AEP Medicare Gap | Jul-Sep | Medicare (MAPD/MedSupp) |
| 2 | COV-LTC | Long-Term Care Awareness | November | LTC / Hybrid LTC |
| 3 | COV-LIAM | Life Insurance Awareness | September | Life Insurance |
| 4 | COV-DI | Disability Insurance Awareness | May | Disability Income |
| 5 | COV-LOVE | Love & Protection Month | February | Life Insurance (Valentine's framing) |
| 6 | COV-ANN | Annuity Awareness | June | Annuity / Retirement Income |
| 7 | COV-TAX | Tax Season Coverage Review | Feb-Apr | Annuity / IRA / Retirement Vehicles |

---

## COV Philosophy

**"We're Your People -- for everything."** The COV engine extends the PSM-NO-CORE concept beyond Medicare. Every existing RPI client has a relationship built on trust. The COV campaigns identify product gaps and use awareness month timing as a natural, non-pushy conversation starter.

### Core Principles

1. **Not selling a product -- educating on a gap.** The client already trusts RPI with one or more products. The COV campaign does not pitch a new product. It says: "You're our client. We noticed you don't have [X]. Given what [awareness month] is about, this is a good time to talk about whether that matters for your situation."

2. **Awareness months are the opener, not the reason.** The timing creates a natural entry point. "It's Life Insurance Awareness Month" is a reason to bring it up, not a reason to buy. The reason to buy (or not) comes from the client's actual situation.

3. **Same tone as PSM.** Commission-based, no "free" language, no urgency mechanics, no sales pressure. The agent is an advisor presenting information. The client decides.

4. **Personalized with existing relationship.** Every COV touch references what the client DOES have with RPI: `{Carrier} {ProductName}`. This reinforces the relationship before introducing the gap. "We've got your Humana Gold Plus and your North American Versachoice 10 -- but we don't have anything in place for [gap]."

5. **One gap per campaign.** Each COV campaign addresses exactly one product gap. No multi-product pitches. If the client has multiple gaps, they receive multiple campaigns at different times throughout the year, each tied to the appropriate awareness month.

6. **Commission-based model.** Same as PSM. RPI is compensated by carriers. The client never pays RPI. Never use "free." There is no cost to imply the absence of.

---

## Tone Rules

These rules apply to ALL 7 campaigns, ALL channels (email, text/SMS, VM, USPS).

| Rule | Detail |
|------|--------|
| **No "free" language** | Commission-based. There is no cost to imply the absence of. |
| **No urgency/sales mechanics** | No "15 minutes," "today only," "Reply YES," countdown timers. This is education, not sales. |
| **No technical jargon** | No "asset allocation," "elimination period," "benefit trigger," "non-forfeiture." Use plain language. |
| **Commission transparency** | Never mention commission. Never imply RPI charges the client. |
| **Always personalize** | Every touch references the client's existing products: `{Carrier}` and `{ProductName}`. |
| **No sales language** | No "opportunity of a lifetime," "act now," "don't miss out." |
| **Agent as advisor** | The agent has already identified the gap and is offering to be a resource. Not selling. |
| **Awareness month as context** | Reference the awareness month naturally, not as a gimmick. |
| **Energy** | Warm, consultative, low-pressure. "We noticed this gap -- want us to take a look?" |

### Personalization Merge Fields

| Field | Source |
|-------|--------|
| `{FirstName}`, `{LastName}` | Client record |
| `{AgentName}` | Assigned agent |
| `{BOBName}` | Book of Business name |
| `{Phone}` | Agent phone |
| `{Email}` | Agent email |
| `{CalendarLink}` | Scheduling link |
| `{Carrier}` | Existing carrier (e.g., Humana, North American, Kansas City Life) |
| `{ProductName}` | Existing product (e.g., Gold Plus, Versachoice 10, Supernova) |
| `{ProductType}` | Existing product category (e.g., Medicare Advantage, fixed index annuity) |

---

## Seasonal Calendar

| Month(s) | Campaign | Awareness Month / Event |
|----------|----------|------------------------|
| **February** | COV-LOVE | Valentine's Day / "Love & Protection" |
| **Feb -- Apr** | COV-TAX | Tax season |
| **May** | COV-DI | Disability Insurance Awareness Month |
| **June** | COV-ANN | Annuity Awareness Month |
| **Jul -- Sep** | COV-PREAEP | Pre-AEP Medicare preparation |
| **September** | COV-LIAM | Life Insurance Awareness Month |
| **November** | COV-LTC | Long-Term Care Awareness Month |

### AEP Blackout (Oct -- Dec)

COV-PREAEP wraps before AEP opens October 15. No COV campaigns run during AEP blackout (Oct-Dec) that involve Medicare products. Non-Medicare COV campaigns (LTC, LIAM, DI, LOVE, ANN, TAX) can run during their scheduled months regardless of AEP status, as they do not involve Medicare.

---

## Campaign Details

---

### 1. COV-PREAEP -- Pre-AEP Medicare Gap

**Trigger:** July through September. Client has WEALTH or LEGACY products through RPI but does NOT have Medicare coverage (MAPD or MedSupp) managed by RPI. Client is Medicare-eligible (65+).

**Timing:** July, August, September. Timed to plant the seed before AEP opens October 15. If the client engages, they enter the PSM-SEP-PREP flow in September and the full AEP review cycle in October.

**Client Profile:** Existing RPI client with annuity, life insurance, or other non-Medicare products. Medicare coverage is either managed by another agent, enrolled directly through a carrier, or possibly absent. The client is 65+ and Medicare-eligible.

**Psychology:** The client trusts RPI with their money or their legacy planning but not their health insurance. The question is not "why not?" -- it is "did you know we do this too?" Many clients compartmentalize their financial relationships. RPI's value proposition is the integrated approach: Health + Wealth + Legacy under one roof, one team, one proactive service model.

**Key Message:** "We've got your {Carrier} {ProductName}, and we're making sure that's in great shape. But we noticed we're not handling your Medicare coverage. AEP is coming up in October -- that's the annual window to review and adjust your Medicare plan. The same data-driven, proactive approach we use for your other accounts applies to Medicare too. Want us to take a look?"

**Risk/Urgency:** AEP is a fixed calendar event (Oct 15 - Dec 7). If the client's current Medicare plan is misaligned with their healthcare needs, the next window to change is AEP. Without a proactive review, the client stays on whatever they have -- whether it still fits or not. Reaching out July-September ensures there is time to gather authorizations and build a comparison before AEP opens.

**Agent Coaching:**
- Lead with the existing relationship: "We've got your [product] -- now let's talk about your Medicare."
- Do not criticize their current Medicare setup. "For whatever reason, we're not handling this side yet -- and we'd love the chance to show you what our approach looks like."
- Sell the PSM model, not a specific plan: "We pull your prescriptions, providers, pharmacies, and healthcare data. We run the numbers. We check every year."
- If the client is happy with their current agent: "No pressure at all. Just want you to know we do this, and the same team managing your [product] could be managing your Medicare too."
- If the client engages: start authorization (PSM-SEP-PREP equivalent) immediately.
- This is functionally PSM-NO-CORE but timed specifically to the pre-AEP window for maximum relevance.

**Compliance Notes:**
- Cannot continue Medicare cross-sell outreach into AEP blackout (Oct-Dec). July-September only.
- SOA required if the client engages and wants to discuss specific Medicare plan options.
- Verify the client is Medicare-eligible (65+) before outreach.
- Never disparage the client's current agent or agency.
- If the client is under 65, flag for T65 pipeline instead.

**Cross-Sell:** This IS the cross-sell. If the client engages, they enter PSM-SEP-PREP --> AEP-REV --> full AEP cycle.

---

### 2. COV-LTC -- Long-Term Care Awareness

**Trigger:** November. Client has HEALTH and/or WEALTH products through RPI but does NOT have long-term care coverage (standalone LTC, hybrid life/LTC, or annuity with LTC rider).

**Timing:** November. Long-Term Care Awareness Month. Timed after AEP closes (Dec 7 is AEP end, but LTC conversations are non-Medicare and can start in November). Natural timing as families gather for Thanksgiving and discuss aging, caregiving, and future planning.

**Client Profile:** Existing RPI client, typically 50-75, with Medicare and/or retirement products but no long-term care protection. May have aging parents and direct experience with caregiving costs. May have dismissed LTC in the past due to cost or "it won't happen to me" thinking.

**Psychology:** Long-term care is the product nobody wants to think about. The Thanksgiving timing is powerful because it is often when adult children see aging parents and the reality of caregiving hits home. The message is not "you're going to need a nursing home" -- it is "70% of people turning 65 will need some form of long-term care. The question is how it gets paid for."

**Key Message:** "November is Long-Term Care Awareness Month. We've got your {Carrier} {ProductName} and your health coverage is in great shape. But we noticed there's nothing in place for long-term care. The reality is that most people will need some form of care as they age -- and the cost can be significant. We don't want that to catch you or your family off guard. Want us to run some numbers?"

**Risk/Urgency:** LTC costs are significant and rising. The average cost of a private room in a nursing facility exceeds $100,000/year in most states. Home health aide costs are approaching $60,000/year. Medicare covers very limited skilled nursing (up to 100 days with conditions). Without a plan, the cost falls on savings, family, or Medicaid (which requires spending down assets). The younger and healthier the client is when they apply, the more options and better rates they have.

**Agent Coaching:**
- Do not lead with fear. Lead with facts: "70% of people turning 65 will need some form of long-term care."
- Present the three funding options: self-insure (pay out of pocket), Medicaid (spend down assets), or insurance (LTC, hybrid, or rider). RPI helps with option 3.
- Hybrid products (life/LTC combos) are often easier to discuss: "If you never need care, your family gets the death benefit. If you do need care, the policy covers it."
- Annuity-based LTC riders are another option: "Your existing annuity may be able to add LTC protection."
- If the client has aging parents: "What you're seeing with your parents is exactly what this protects against for your family."
- If the client pushes back on cost: "Let's at least see what the numbers look like. You might be surprised."
- November is also a good time because AEP is wrapping up and agents have bandwidth for LEGACY conversations.

**Compliance Notes:**
- LTC product discussions require appropriate state licensing.
- Accurate representation of LTC costs must be sourced from current data (Genworth Cost of Care Survey or equivalent).
- Do not guarantee future LTC costs or insurance availability.
- If discussing hybrid products, clearly explain the trade-offs between death benefit and care benefit.
- Partnership/state-specific LTC programs may affect planning -- verify state rules.

**Cross-Sell:**
- LIFE: If the LTC conversation reveals no life insurance, natural bridge to life coverage discussion.
- ANN-ALLOC/ANN-SUR: If the client has an existing annuity, explore whether an LTC rider can be added or whether repositioning to a product with an LTC rider makes sense.
- Estate/Legacy planning: LTC is inherently a legacy conversation. Protecting assets from care costs is protecting the family's inheritance.

---

### 3. COV-LIAM -- Life Insurance Awareness Month

**Trigger:** September. Client has HEALTH and/or WEALTH products through RPI but does NOT have life insurance through RPI.

**Timing:** September. Life Insurance Awareness Month (LIAM). Industry-wide awareness campaign that creates a natural conversation starter. Also strategically timed -- September is pre-AEP, and the HEALTH team is focused on SEP-PREP and AEP-REV. LIAM conversations are handled by the LEGACY division, keeping both divisions productive simultaneously.

**Client Profile:** Existing RPI client with Medicare, annuity, or both, but no life insurance through RPI. May have group life through an employer, an old term policy, or no coverage at all. May assume their needs are met or may not have revisited life insurance in years.

**Psychology:** Life insurance is the product people "mean to get to." They know they should have it (or review it), but it never feels urgent -- until it is too late. LIAM creates a moment of relevance. The message is not "you could die tomorrow" -- it is "you've got your health and wealth covered. Let's make sure your family is protected too."

**Key Message:** "September is Life Insurance Awareness Month. We've got your {Carrier} {ProductName} and your Medicare is handled. But we noticed there's no life insurance in your file. Whether it's protecting your family's income, covering final expenses, or leaving a legacy, life insurance is one of those things that's easy to put off. Want us to take a look at your situation?"

**Risk/Urgency:** Life insurance is health-dependent. The younger and healthier the client is, the more options and better rates available. Waiting does not make it cheaper or easier -- it makes it more expensive, and at some point, it becomes unavailable. There is no urgency gimmick here -- just the biological reality.

**Agent Coaching:**
- Lead with the gap, not the product: "We noticed there's nothing in place for life insurance."
- Ask about their current situation: "Do you have any coverage through work? An old policy somewhere? Or is this something you've been meaning to look into?"
- Position life insurance by purpose, not by product: income replacement, final expense, legacy, estate planning, charitable giving. Different purposes lead to different products.
- If the client has group life: "Group life is great while you're working, but it usually ends when you leave or retire. And the amount is typically 1-2x salary -- is that enough?"
- If the client has an old term policy: "When does your term expire? If it's approaching the end, now's the time to look at options before it goes away."
- If the client says "I don't need life insurance": respect it. "Fair enough. If that changes, you know where to find us."
- September timing means AEP is on the horizon. Do not let the LIAM conversation bleed into Medicare topics -- keep it focused.

**Compliance Notes:**
- Life insurance recommendations require appropriate state licensing.
- Needs analysis should be documented before making product recommendations.
- Do not use scare tactics or overstate mortality risk.
- If discussing replacement of an existing policy, a full suitability analysis and replacement form (where required by state) is mandatory.
- Group life limitations should be stated factually, not as a criticism of the employer benefit.

**Cross-Sell:**
- LTC: "While we're looking at life insurance, have you thought about long-term care protection? There are hybrid products that combine both."
- Estate planning: If the client has significant assets, life insurance as an estate planning tool (ILIT, estate equalization, charitable remainder).
- ANN-LIQ: If an annuity is fully liquid, 1035 exchange into a life product with LTC rider may be appropriate.

---

### 4. COV-DI -- Disability Insurance Awareness

**Trigger:** May. Client is under 65, still working, has other RPI products, but does NOT have disability income insurance.

**Timing:** May. Disability Insurance Awareness Month. Targets working-age clients (typically under 65) who are still earning income and would be financially devastated by an inability to work.

**Client Profile:** Existing RPI client, under 65, actively employed. May have life insurance, annuity, or early Medicare planning through RPI. Does not have individual disability income insurance. May have short-term disability through employer but likely does not have long-term coverage.

**Psychology:** Disability insurance is the most under-owned insurance product in America. People insure their cars, their homes, even their phones -- but not their income. The message: "Your ability to earn income is your most valuable asset. Everything else depends on it."

**Key Message:** "May is Disability Insurance Awareness Month. We've got your {Carrier} {ProductName} in great shape. But here's something most people don't think about: if you couldn't work for 6 months or a year due to illness or injury, how would your bills get paid? Your ability to earn is what funds everything else. Want us to take a look at your options?"

**Risk/Urgency:** The statistics are compelling: 1 in 4 workers will experience a disability lasting more than 90 days during their career. Social Security Disability is difficult to qualify for and covers only a fraction of income. Employer short-term disability typically covers 60% of salary for 3-6 months. After that, there is often nothing. The younger the client, the longer the potential exposure and the lower the premiums.

**Agent Coaching:**
- Lead with the income question, not the product: "If you couldn't work for a year, what happens to your mortgage, your car payment, your family's lifestyle?"
- Ask about employer coverage: "Do you have any disability coverage through work? Short-term? Long-term?" Most people have short-term and assume it is enough.
- Explain the gap: "Short-term disability from your employer typically covers about 60% of your pay for 3-6 months. If your disability lasts longer, the coverage usually ends."
- Position DI as income protection, not insurance: "This isn't about being disabled -- it's about protecting your paycheck."
- If the client is healthy and active: "That's exactly why now is the time. DI is health-dependent -- the healthier you are when you apply, the better the terms."
- If the client says "it won't happen to me": "Nobody thinks it will. That's what makes it the most under-insured risk in America."
- Note: this campaign targets clients UNDER 65. If the client has retired, DI is no longer relevant.

**Compliance Notes:**
- DI product recommendations require appropriate state licensing.
- Accurately represent disability statistics from reputable sources (Council for Disability Awareness or equivalent).
- Do not overstate Social Security Disability limitations but do represent the qualification difficulty accurately.
- If the client has employer group DI, do not disparage it -- supplement it.
- Needs analysis should document income, existing coverage, monthly obligations.

**Cross-Sell:**
- LIFE: "While we're talking about protecting your income, is your life insurance up to date too?"
- ANN: "If you're thinking about protecting your financial future, have you considered starting to build guaranteed retirement income?"
- HEALTH: If the client is approaching 65, bridge to T65 pipeline: "Your 65th birthday is coming up -- we should start thinking about Medicare too."

---

### 5. COV-LOVE -- Love & Protection Month

**Trigger:** February. Client has HEALTH and/or WEALTH products through RPI but does NOT have life insurance through RPI. Valentine's Day framing.

**Timing:** February. Valentine's Day creates a natural emotional context for conversations about protecting the people you love. Not cheesy -- genuine. "February is about the people who matter most. Let's make sure they're protected."

**Client Profile:** Existing RPI client without life insurance through RPI. Broad targeting -- any client with a spouse, partner, children, or dependents who would be financially impacted by the client's death. This is the emotional complement to COV-LIAM's rational September touch.

**Psychology:** February and Valentine's Day put love and family at the center of the cultural conversation. Life insurance is fundamentally an act of love -- it protects the people who depend on you. The message is not morbid or fear-based. It is affirmative: "You take care of the people you love. Life insurance is one of the ways you do that even when you can't be there."

**Key Message:** "February is about the people who matter most. We've got your {Carrier} {ProductName} and we're making sure you're taken care of. But we wanted to ask: if something happened to you, are the people you love financially protected? Life insurance is one of those things people mean to take care of but never quite get to. This is a good time to check."

**Risk/Urgency:** Same as COV-LIAM -- life insurance is health-dependent and age-dependent. Every year the client waits, premiums increase and health conditions may develop. The February timing adds emotional resonance without artificial urgency.

**Agent Coaching:**
- Keep the tone warm, not morbid. This is about love and protection, not death.
- Ask about dependents: "Who depends on you financially? A spouse? Kids? Aging parents?"
- Frame life insurance as a gift: "It's the one thing you do for the people you love that they'll never have to ask for."
- If the client has young children: "If something happened, would your family be able to stay in the house? Would college be funded?"
- If the client is a single income household: "Your income is what keeps everything running. Life insurance replaces that if you can't be there."
- If the client already has coverage through another source: "That's great. When's the last time it was reviewed? Life insurance needs change as your family grows."
- This campaign pairs well with a handwritten card or personal touch in the USPS mailer channel.

**Compliance Notes:**
- Same as COV-LIAM. Appropriate licensing, needs analysis, no scare tactics.
- Valentine's/love framing must be tasteful, not manipulative.
- Do not imply that not having life insurance means the client does not love their family.
- Emotional framing is appropriate; emotional manipulation is not.

**Cross-Sell:**
- LTC: "While we're thinking about protecting your family, have you considered what happens if you need long-term care? That can impact your family's finances too."
- Estate planning: If the client has assets, life insurance as an estate planning tool.
- ANN: If the client is thinking about retirement, guaranteed income products protect the surviving spouse's lifestyle.

---

### 6. COV-ANN -- Annuity Awareness Month

**Trigger:** June. Client has HEALTH and/or LEGACY products through RPI but does NOT have any annuity or retirement income product through RPI.

**Timing:** June. Annuity Awareness Month. Mid-year timing catches clients who are thinking about retirement planning after tax season but before the second-half-of-year financial push.

**Client Profile:** Existing RPI client with Medicare, life insurance, or both, but no annuity or retirement income product. May be pre-retirement (accumulation phase) or post-retirement (distribution phase) but without guaranteed income protection. May have 401(k), IRA, or other qualified money that could benefit from guaranteed income strategies.

**Psychology:** "Annuity" is one of the most misunderstood words in financial services. Most clients either think annuities are "too complicated" or "too expensive" or have heard a negative anecdote. The message is not about annuities as a product category -- it is about the problem they solve: "How do you make sure you don't run out of money in retirement?"

**Key Message:** "June is Annuity Awareness Month. We've got your {Carrier} {ProductName} and your health coverage is solid. But we wanted to ask: do you have a plan for guaranteed retirement income? Social Security covers part of it, but most people have a gap between what Social Security provides and what they actually need. That's what annuities are designed to solve. Want us to take a look?"

**Risk/Urgency:** Longevity risk is the quiet crisis. People are living longer, and their money needs to last. A 65-year-old couple has a 50% chance that one of them will live past 90. Social Security replaces approximately 40% of pre-retirement income for average earners. The gap between Social Security and actual living expenses is the problem annuities address. There is no urgency gimmick -- just math.

**Agent Coaching:**
- Do not lead with the word "annuity" if the client has preconceived notions. Lead with the problem: "How are you planning to make sure your money lasts as long as you do?"
- Explain the gap simply: "Social Security covers about 40% of what most people need. What covers the other 60%?"
- Position annuities by what they do, not what they are: "Guaranteed income you can't outlive."
- Different products for different situations: FIA for accumulation with downside protection, MYGA for guaranteed rates, income annuities for lifetime income. Match the product to the client's phase and goals.
- If the client has a 401(k) or IRA: "Have you considered rolling a portion into something that guarantees income? Your 401(k) grows, but it doesn't guarantee it'll last."
- If the client is already retired: "You're in distribution mode. The question is: do you have enough guaranteed income to cover your non-negotiable expenses -- housing, food, utilities, insurance?"
- If the client pushes back: "I get it -- annuities have a reputation. But the products available today are very different from what your parents might have heard about. Let us show you the numbers."

**Compliance Notes:**
- Annuity recommendations require appropriate state licensing and suitability analysis.
- Accurately represent Social Security replacement ratios (varies by income level).
- Do not guarantee future interest rates or index performance.
- If discussing rollovers from qualified plans (401k, IRA), tax implications must be addressed. Refer to tax advisor as appropriate.
- Do not disparage other retirement vehicles (401k, IRA, brokerage accounts). Position annuities as a complement, not a replacement.

**Cross-Sell:**
- LIFE: "Your retirement income is covered -- is your family protected if something happens before you get there?"
- LTC: "Guaranteed income protects against running out of money. LTC protection protects against care costs eating into that income."
- HEALTH: If Medicare is not managed by RPI, natural bridge: "Your financial side is coming together. Let's make sure your health insurance is just as well-positioned."

---

### 7. COV-TAX -- Tax Season Coverage Review

**Trigger:** February through April. Tax season. Client has HEALTH and/or LEGACY products through RPI but does NOT have an annuity, IRA, or other tax-advantaged retirement vehicle through RPI.

**Timing:** February, March, April. Tax season puts financial planning front-of-mind. Clients are looking at their tax returns, seeing what they owe, and thinking about how to reduce their tax burden. This is the most natural time of year for retirement savings conversations.

**Client Profile:** Existing RPI client without retirement savings or annuity products through RPI. May be working (and eligible for IRA contributions) or retired (and dealing with RMDs, tax bracket management). The tax return is the trigger -- it surfaces the financial picture and creates a planning moment.

**Psychology:** Nobody likes paying taxes. Tax season is when people are most receptive to strategies that reduce their tax burden. The message is not "buy an annuity to save on taxes" -- it is "your tax return just showed you something. Let's see if there's a smarter way to position your money for retirement and reduce your tax exposure."

**Key Message:** "Tax season is here, and it's the one time of year everyone's looking at their financial picture. We've got your {Carrier} {ProductName} in good shape. But looking at the bigger picture -- are you maximizing your retirement savings strategies? There may be tax-advantaged options that could reduce what you owe and grow your retirement income at the same time. Want us to take a look?"

**Risk/Urgency:** IRA contribution deadlines are tied to tax filing (April 15 for prior-year contributions). If the client has not maxed out their IRA contributions, the window is finite. For retired clients, RMD strategies and tax bracket management are ongoing concerns. The tax return provides concrete data for the conversation.

**Agent Coaching:**
- Lead with the tax return: "What did your tax situation look like this year? Anything surprise you?"
- For working clients: "Have you maxed out your IRA contributions? If not, you still have until April 15 to contribute for last year."
- For retired clients: "How are you managing your RMDs? There may be strategies to reduce the tax impact."
- Position tax-advantaged vehicles by their tax benefit, not their product features: "This grows tax-deferred, meaning you don't pay taxes on the gains until you take the money out."
- Annuities, traditional IRAs, Roth IRAs, and qualified plans all have different tax treatment. Match the strategy to the client's situation.
- If the client has a CPA or tax advisor: "We work alongside your tax advisor, not instead of them. We handle the financial products -- they handle the tax strategy. Together, we optimize."
- Do NOT provide tax advice. Provide tax-advantaged product information and recommend the client consult their tax advisor for specific tax decisions.

**Compliance Notes:**
- RPI agents are not tax advisors. All tax-related conversations must include the recommendation to consult a qualified tax professional.
- IRA contribution limits and deadlines must be stated accurately (current year limits).
- RMD rules must be represented accurately per current IRS regulations.
- Do not promise specific tax savings -- outcomes depend on individual circumstances.
- If discussing Roth conversions, the tax implications are complex. Always involve the client's tax advisor.
- Suitability analysis required for any product recommendation.

**Cross-Sell:**
- LIFE: "While we're looking at your financial picture, is your life insurance up to date?"
- HEALTH: If Medicare is not managed by RPI: "Your finances are coming together. Let's make sure your health insurance is just as optimized."
- LTC: If the client is in their 50s-60s and has assets: "Part of smart tax and retirement planning is protecting those assets from long-term care costs."

---

## Cross-Campaign Flow

### Annual COV Calendar

```
February:   COV-LOVE (Life Insurance -- Valentine's framing)
            COV-TAX begins (Tax Season -- retirement vehicles)

March:      COV-TAX continues

April:      COV-TAX ends (IRA contribution deadline April 15)

May:        COV-DI (Disability Insurance Awareness)

June:       COV-ANN (Annuity Awareness)

July:       COV-PREAEP begins (Pre-AEP Medicare Gap)

August:     COV-PREAEP continues

September:  COV-PREAEP ends + COV-LIAM (Life Insurance Awareness)

October:    [AEP Blackout begins -- no Medicare COV campaigns]

November:   COV-LTC (Long-Term Care Awareness)

December:   [AEP Blackout -- no Medicare COV campaigns]
```

### COV to PSM Handoff

```
COV-PREAEP (client engages)
        |
        v
PSM-SEP-PREP (September authorization gathering)
        |
        v
PSM-AEP-REV (October plan review)
        |
        v
PSM outcome campaigns (MOVE, G2G, STAY, $0)
```

When a COV campaign generates engagement, the client enters the appropriate PSM or T65 flow:
- **COV-PREAEP** --> PSM-SEP-PREP --> AEP cycle
- **COV-LIAM / COV-LOVE** --> PSM-LIFE (if they enroll, enters LIFE anniversary cycle)
- **COV-ANN / COV-TAX** --> PSM-ANN-ALLOC (if they fund an annuity, enters allocation review cycle)
- **COV-LTC** --> Standalone LTC management (no current PSM campaign, but policy anniversary reviews apply)
- **COV-DI** --> Standalone DI management (working-age clients, pre-retirement)

### Gap Detection Logic

```
Client has HEALTH only?
    --> COV-LIAM, COV-LOVE (life gap)
    --> COV-ANN, COV-TAX (retirement gap)
    --> COV-LTC (LTC gap)
    --> COV-DI (if under 65, DI gap)

Client has WEALTH only?
    --> COV-PREAEP (Medicare gap, if 65+)
    --> COV-LIAM, COV-LOVE (life gap)
    --> COV-LTC (LTC gap)
    --> COV-DI (if under 65, DI gap)

Client has LEGACY only?
    --> COV-PREAEP (Medicare gap, if 65+)
    --> COV-ANN, COV-TAX (retirement gap)
    --> COV-LTC (LTC gap)
    --> COV-DI (if under 65, DI gap)

Client has HEALTH + WEALTH?
    --> COV-LIAM, COV-LOVE (life gap)
    --> COV-LTC (LTC gap)

Client has HEALTH + LEGACY?
    --> COV-ANN, COV-TAX (retirement gap)
    --> COV-LTC (LTC gap)

Client has WEALTH + LEGACY?
    --> COV-PREAEP (Medicare gap, if 65+)
    --> COV-LTC (LTC gap)
```

A client receives ONLY the COV campaigns for products they do NOT have. Once a gap is filled, that COV campaign stops and the client enters the corresponding PSM service cycle.

---

## Quick Reference Matrix

| # | Campaign ID | Timing | Product Gap | Awareness Event | Target Age | Cross-Sell Strength |
|---|-------------|--------|-------------|-----------------|------------|---------------------|
| 1 | COV-PREAEP | Jul-Sep | Medicare (MAPD/MedSupp) | Pre-AEP season | 65+ | **Feeds PSM-AEP cycle** |
| 2 | COV-LTC | November | LTC / Hybrid LTC | LTC Awareness Month | 50-75 | Strong (LIFE, estate) |
| 3 | COV-LIAM | September | Life Insurance | LIAM | All ages | Strong (LTC, estate) |
| 4 | COV-DI | May | Disability Income | DI Awareness Month | Under 65 (working) | Moderate (LIFE, ANN) |
| 5 | COV-LOVE | February | Life Insurance | Valentine's Day | All ages | Strong (LTC, estate) |
| 6 | COV-ANN | June | Annuity / Retirement | Annuity Awareness Month | 50+ | Strong (LIFE, LTC) |
| 7 | COV-TAX | Feb-Apr | Annuity / IRA / Retirement | Tax Season | All ages | Strong (LIFE, HEALTH) |

---

*We're Your People.(TM)*
