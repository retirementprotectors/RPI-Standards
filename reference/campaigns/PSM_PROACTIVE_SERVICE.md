# PSM -- Proactive Service Model

> Knowledge document for the PSM campaign engine. 15 account-triggered campaigns across HEALTH, LEGACY, and WEALTH.
> All content approved by JDM on 2026-02-16.

---

## Engine Overview

**PSM = Proactive Service Model.** Account-triggered campaigns that fire for existing RPI clients based on real data events -- plan changes, policy anniversaries, surrender charge milestones, CMS star ratings, FEMA declarations, and authorization gaps.

| Metric | Value |
|--------|-------|
| **Total Campaigns** | 15 |
| **HEALTH** | 10 campaigns (+ NO-CORE cross-sell into HEALTH = 11 total HEALTH-touching) |
| **LEGACY** | 1 campaign |
| **WEALTH** | 3 campaigns (all annuity) |
| **Channels per campaign** | Email, Text/SMS, Voicemail Script, USPS Mailer |
| **Execution path** | C3 (campaign engine) --> PRODASH (delivery) --> 4 channels |

### Campaign Inventory

| # | Campaign ID | Name | Division | Trigger Type |
|---|-------------|------|----------|--------------|
| 1 | PSM-SEP-PREP | AEP SEP Prep | HEALTH | Calendar + data gap |
| 2 | PSM-AEP-REV | AEP Review | HEALTH | Calendar (annual cycle) |
| 3 | PSM-AEP-MOVE | AEP Move | HEALTH | Review outcome |
| 4 | PSM-AEP-G2G | AEP Good to Go | HEALTH | Review outcome |
| 5 | PSM-AEP-STAY | AEP Stay | HEALTH | Review outcome |
| 6 | PSM-AEP-$0 | AEP Move ($0!) | HEALTH | Review outcome |
| 7 | PSM-SEP-5 | SEP 5-Star | HEALTH | CMS data event |
| 8 | PSM-SEP-3 | SEP Below 3-Star | HEALTH | CMS data event |
| 9 | PSM-SEP-FEMA | SEP FEMA | HEALTH | External event (FEMA) |
| 10 | PSM-OEP | OEP Benefit Check | HEALTH | Calendar (Jan-Mar) |
| 11 | PSM-NO-CORE | No-Core Cross-Sell | HEALTH | Account gap detection |
| 12 | PSM-LIFE | Life Statement Review | LEGACY | Policy anniversary |
| 13 | PSM-ANN-SUR | Annuity Surrender <10% | WEALTH | Surrender schedule threshold |
| 14 | PSM-ANN-ALLOC | Annuity Allocation Review | WEALTH | Policy anniversary |
| 15 | PSM-ANN-LIQ | Annuity Fully Liquid | WEALTH | Surrender schedule milestone |

---

## PSM Philosophy

**"We're Your People."** The PSM is the operational backbone of that promise. Every campaign reinforces one message: we are proactively managing your accounts, you do not have to ask, and you do not have to worry.

### Core Principles

1. **Commission-based model.** RPI is compensated by carriers. The client never pays RPI for these services. Content must NEVER imply the client is paying for anything. Never use the word "free" -- that implies there could be a cost. There is not.

2. **Data-driven.** Every recommendation is backed by P3 data (prescriptions, providers, pharmacies), healthcare consumption history (claims, diagnoses, procedures via Blue Button / Carrier Connect / provider data sharing), and product-specific account data (surrender schedules, allocation performance, in-force illustrations). The language reflects this: "based on your data," "your actual usage," "we ran the numbers."

3. **Authorization-first.** Before RPI can pull meaningful healthcare data, the client must authorize access. Three authorization types:
   - **CMS Blue Button** -- Original Medicare claims history
   - **Carrier Connect** -- Medicare Advantage plan-specific data
   - **Provider data sharing** -- Healthcare trend information from providers

   PSM-SEP-PREP exists specifically to close authorization gaps before AEP review season.

4. **Proactive, not reactive.** Campaigns fire based on account triggers and data events. RPI does not wait for the client to call. The tone is always "we're already on it" -- never "you should call us."

5. **Education, not pressure.** Every campaign educates the client on what changed, why it matters, and what the options are. The client decides. RPI presents data.

---

## Tone Rules

These rules apply to ALL 15 campaigns, ALL channels (email, text/SMS, VM, USPS).

| Rule | Detail |
|------|--------|
| **No "free" language** | Commission-based. There is no cost to imply the absence of. |
| **No urgency/sales mechanics** | No "15 minutes," "today only," "Reply YES," countdown timers. This is service, not sales. |
| **No technical jargon** | No "EHR," "Blue Button," "formulary tier structure," "actuarial." Use plain language: "information from your providers about your healthcare trends." |
| **Commission transparency** | Never mention commission. Never imply RPI charges the client. The service just exists because "this is what we do." |
| **Always personalize** | Every client-facing touch must include `{Carrier}` and `{ProductName}` or `{PlanName}` at minimum in the introduction, text/SMS, and voicemail. |
| **No sales language** | No "opportunity of a lifetime," "act now," "don't miss out." |
| **Agent as advisor** | The agent is positioned as a knowledgeable advisor who has already done the work, not a salesperson pitching. |
| **Energy** | Warm, confident, competent. "We're your people, this is what we do, let's connect." |

### Personalization Merge Fields

| Field | Source |
|-------|--------|
| `{FirstName}`, `{LastName}` | Client record |
| `{AgentName}` | Assigned agent |
| `{BOBName}` | Book of Business name |
| `{Phone}` | Agent phone |
| `{Email}` | Agent email |
| `{CalendarLink}` | Scheduling link |
| `{Carrier}` | Insurance carrier (e.g., Humana, North American, Kansas City Life) |
| `{ProductName}` | Specific product (e.g., Gold Plus, Versachoice 10, Supernova) |
| `{ProductType}` | Product category (e.g., Medicare Advantage, fixed index annuity, universal life) |
| `{PlanName}` | Medicare plan name (e.g., Humana Gold Plus) |

---

## Seasonal Calendar

| Month(s) | Campaigns Active | Notes |
|----------|-----------------|-------|
| **Jan -- Mar** | PSM-OEP, LIFE*, ANN-ALLOC*, ANN-SUR*, ANN-LIQ*, NO-CORE | OEP runs Jan 1 - Mar 31. *Anniversary/threshold-based, year-round. |
| **Apr -- Aug** | LIFE*, ANN-ALLOC*, ANN-SUR*, ANN-LIQ*, NO-CORE, SEP-5, SEP-3, SEP-FEMA | SEP campaigns fire on trigger, any time of year. |
| **Sep** | **PSM-SEP-PREP** (primary), PSM-AEP-REV (begins), LIFE*, ANN-ALLOC*, ANN-SUR*, ANN-LIQ*, NO-CORE | Authorization gathering before AEP. Reviews start. |
| **Oct** | **PSM-AEP-REV** (AEP opens Oct 15), SEP-PREP (stragglers) | **AEP BLACKOUT begins: NO-CORE paused Oct-Dec.** |
| **Nov** | PSM-AEP-MOVE, PSM-AEP-G2G, PSM-AEP-STAY, PSM-AEP-$0 | Post-review outcome campaigns fire based on results. |
| **Dec** | PSM-AEP-MOVE, PSM-AEP-G2G, PSM-AEP-STAY, PSM-AEP-$0 | AEP closes Dec 7. Final enrollment window. |
| **Year-round** | PSM-SEP-5, PSM-SEP-3, PSM-SEP-FEMA | Special Enrollment Period campaigns fire on trigger. |
| **Year-round** | PSM-LIFE, PSM-ANN-SUR, PSM-ANN-ALLOC, PSM-ANN-LIQ | Anniversary/threshold-based, per individual client schedule. |

### AEP Blackout (Oct -- Dec)

During AEP (October 15 -- December 7), **PSM-NO-CORE is paused**. Cross-sell Medicare outreach during AEP creates regulatory risk and message confusion. The team is focused exclusively on Medicare plan reviews and enrollments. All non-HEALTH campaigns (LIFE, ANN-SUR, ANN-ALLOC, ANN-LIQ) continue year-round on their own trigger schedules.

---

## Cross-Campaign Flow

### AEP Flow (Primary Annual Cycle)

```
PSM-SEP-PREP (Sep)
    Authorization gathering -- get data connected before AEP
        |
        v
PSM-AEP-REV (Sep-Oct)
    Full plan review using P3 + healthcare consumption data
        |
        +---> PSM-AEP-MOVE (Nov-Dec)
        |       Review found a better plan. Client switches.
        |
        +---> PSM-AEP-G2G (Nov-Dec)
        |       Plan confirmed best. No change. Peace of mind.
        |
        +---> PSM-AEP-STAY (Nov-Dec)
        |       Plan is best but has notable changes. Educate.
        |
        +---> PSM-AEP-$0 (Nov-Dec)
                $0-premium plan found. Strong switch candidate.
```

Every client who receives AEP-REV gets exactly ONE of the four outcome campaigns (MOVE, G2G, STAY, $0) based on the review result.

### Post-AEP Safety Net

```
AEP closes Dec 7
        |
        v
PSM-OEP (Jan 1 - Mar 31)
    Benefit check for all MA members.
    Catches misalignments that slipped through AEP.
    Last window before annual lock-in.
```

### SEP Flow (Trigger-Based, Year-Round)

```
PSM-SEP-5  -----> 5-star plan identified in client area (year-round SEP)
PSM-SEP-3  -----> Client plan drops below 3-star CMS rating (SEP triggered)
PSM-SEP-FEMA --> Client in FEMA-declared disaster area (2-month SEP window)
```

### Cross-Vertical Flow

```
PSM-NO-CORE (Jan-Sep)
    Client has WEALTH or LEGACY but no HEALTH (MedSupp/MAPD).
    Cross-sell into HEALTH vertical.
        |
        v
    If client engages --> enters AEP flow (SEP-PREP --> AEP-REV --> ...)
```

### WEALTH Internal Flow

```
PSM-ANN-ALLOC (Anniversary-based)
    Annual allocation review at policy anniversary.

PSM-ANN-SUR (Threshold-based)
    Surrender charges drop below 10%. Early signal.
        |
        v
PSM-ANN-LIQ (Milestone-based)
    Surrender charges reach 0%. Full repositioning opportunity.
```

### Key Flow Rules

- **SEP-PREP feeds AEP-REV.** Authorizations gathered in September enable the data-driven review that fires in September/October.
- **AEP-REV branches to exactly one outcome.** G2G, MOVE, STAY, or $0. Never more than one.
- **OEP catches misalignment.** If a client enrolled during AEP and something is wrong in January, OEP provides the safety net window through March 31.
- **ANN-SUR is the early signal, ANN-LIQ is the full open.** As surrender charges decline, SUR fires first (<10%). When they hit zero, LIQ fires with the full repositioning message.

---

## Campaign Details

---

### 1. PSM-SEP-PREP -- AEP SEP Prep (Authorization Gathering)

**Trigger:** September. Client authorizations are missing or more than 12 months old. Data gathering must happen before AEP opens October 15.

**Division:** HEALTH

**Client Profile:** Existing Medicare client (MAPD or MedSupp). May have been enrolled for one or more years. Authorization either never completed, expired, or was only partial (e.g., Blue Button done but no Carrier Connect or provider data sharing).

**Psychology:** Most clients do not understand what authorizations do or why they matter. They need to hear the concrete difference between "with data" and "without data" -- the difference between a real analysis and a guess. Frame authorization as the thing that makes their review worth doing.

**Key Message:** "We're getting ready to run your annual plan review, but we need your authorizations updated first. It takes a couple minutes and it's what lets us give you real numbers instead of guesswork."

**Risk/Urgency:** Without authorization data, RPI can only check P3 network status (providers, pharmacies, formulary). Cannot project actual costs based on healthcare consumption. If the client had four EKGs, fifty physical therapy visits, or a surgery last year, RPI has no way to know that without the data. The review becomes speculation instead of science. AEP opens October 15 -- data must be in hand before reviews begin.

**Agent Coaching:**
- Lead with the value of the data, not the authorization itself. Clients do not care about "authorizations" -- they care about getting an accurate review.
- Explain the three authorization types simply: CMS Blue Button (Original Medicare claims), Carrier Connect (plan-specific data), and provider data sharing (healthcare trends from your doctors).
- Emphasize speed: "It takes a couple of minutes."
- Walk the client through the authorization process on the call.
- If the client pushes back: "Without this, we can tell you if your doctors and meds are in network, but we're guessing on what it's actually going to cost you. And guessing is not how we do this."
- Never use the term "EHR" with the client.

**Compliance Notes:**
- Authorization language must not imply medical records access. Use "information from your providers about your healthcare trends."
- Never reference EHR, electronic health records, or clinical data in client-facing content.
- Client must actively consent. Document the authorization and date.
- All authorization data and PHI obtained must be stored in Google Workspace (Drive/Sheets). Never Slack, text, or personal email.

**Cross-Sell Opportunities:** None. This is a data-gathering campaign. Do not cross-sell during authorization outreach -- it muddies the message and reduces completion rates. However, the conversation naturally reveals what other products the client has, which can be noted for future outreach.

---

### 2. PSM-AEP-REV -- Annual Enrollment Period Review

**Trigger:** Annual plan review time, September through October before AEP opens October 15. Fires for all Medicare clients with active coverage.

**Division:** HEALTH

**Client Profile:** Any client with MAPD or MedSupp coverage through RPI. Year-one or multi-year client. May or may not have completed authorizations (SEP-PREP should have caught gaps, but not all clients complete them).

**Psychology:** Clients assume their plan is fine because they have not heard otherwise. The core insight: your plan changed whether you noticed or not. Every year, carriers adjust deductibles, copays, networks, and formularies at the carrier level. The only way to know the impact is to check.

**Key Message:** "Happy with your plan? It just changed. Every year it does. We review every client's plan before AEP closes so you're never caught off guard."

**Risk/Urgency:** If the client does not engage before December 7, they are locked into whatever their plan became for the entire next year. Pharmacy surprises, network drops, and copay changes all hit in January with no recourse.

**Agent Coaching:**
- Do not lead with "your plan might be worse." Lead with "your plan changed -- let's see what that means for you."
- Position the review as something RPI is already doing: "We're already on it -- just need to connect with you to walk through everything."
- Use data language: "We pull your prescriptions, providers, pharmacies, and claims history -- then we run a full cost projection for next year."
- If the client says "I'm happy with my plan," respond: "That's great -- this review might confirm that. But we need to check, because the plan you loved last year may have changed in ways you haven't seen yet."
- Have the cost projection built before the call when possible.

**Compliance Notes:**
- AEP runs October 15 through December 7. Do not reference enrollment dates outside this window.
- All plan comparison data must come from verified CMS/carrier sources.
- Never guarantee savings or better coverage before the review is completed.
- Do not reference specific plan changes until the comparison is built from actual client data.

**Cross-Sell Opportunities:**
- If the review reveals the client has no WEALTH or LEGACY products, the review appointment is a natural point to mention: "While we're reviewing your Medicare, we should also take a look at your overall picture."
- Do NOT cross-sell in the initial outreach. Only during the live review conversation.

---

### 3. PSM-AEP-MOVE -- AEP Move (Switch Plans)

**Trigger:** Plan review complete. Analysis found a better plan. Client needs to switch before AEP closes December 7.

**Division:** HEALTH

**Client Profile:** Existing Medicare client whose current plan no longer aligns with their P3 and healthcare consumption data. The plan's network, formulary, or cost structure shifted in a way that creates a measurable disadvantage compared to available alternatives.

**Psychology:** Clients are attached to their current plan. "I've had Humana for years." The message is not "your plan is bad" -- it is "your plan changed, and based on your data, there's something that fits you better now." Let the data do the persuading.

**Key Message:** "We've finished your full plan analysis. Based on your prescriptions, providers, pharmacies, and your diagnosis and condition history, there are options that could be a substantial improvement over your current plan."

**Risk/Urgency:** AEP closes December 7. If the client does not act within this window, they remain on the misaligned plan for the entire next year. January pharmacy and doctor visit surprises are the consequence. The message: "Just because your plan changes its networks or formularies doesn't mean you have to conform to those changes."

**Agent Coaching:**
- Lead with the data, not the recommendation. "Here's what we found" before "here's what we think you should do."
- Use side-by-side comparison language: "We put together a comparison using your actual healthcare consumption over the last few years."
- Acknowledge the attachment: "Just because your plan changed doesn't mean you have to conform. We find the plan that fits YOU."
- Never pressure. Present data, answer questions, let the client decide.
- Have the full comparison report ready before outreach.

**Compliance Notes:**
- Scope of Appointment (SOA) must be completed before discussing specific plan alternatives in detail.
- All plan comparisons must use verified CMS data.
- Do not disparage the current carrier -- focus on data alignment, not carrier quality.
- All comparisons must use actual client data, not hypotheticals.

**Cross-Sell Opportunities:**
- LIFE: "Since we're making a change on the health side, this is a good time to check in on your life insurance too."
- ANN-ALLOC: If annuity anniversary is near, bundle the conversations.
- During the switch conversation, natural opening to discuss whether other accounts are being proactively managed.

---

### 4. PSM-AEP-G2G -- AEP Good to Go

**Trigger:** Plan review complete. Current plan is still the best option. No change needed.

**Division:** HEALTH

**Client Profile:** Client whose plan survived the annual review. P3 data, healthcare consumption, and cost projections all confirm the current plan is the best available option in the marketplace.

**Psychology:** This is a retention and trust-building touchpoint. The client needs to hear that their plan was checked, it passed, and they can relax. The subtle but important message: "The reason your plan still works is because we checked, not because nothing changed."

**Key Message:** "Great news -- your plan still checks every box. We ran your data against everything available and your plan came out on top. That's exactly what we like to see, and it's exactly why we check every year."

**Risk/Urgency:** None for the client. They are in great shape. The only risk is failing to communicate the result and losing the trust-building opportunity. Clients who hear "you're good" from RPI every year become deeply loyal. This is one of the highest-value touches in the entire PSM.

**Agent Coaching:**
- This is the easiest call to make. Lead with good news.
- Still reference the work: "We ran your data against every available plan in your area -- premiums, copays, formulary coverage, provider networks, the whole picture."
- Mention minor changes that were caught: "We did see a few small plan changes, but none of them impact you."
- Reinforce the relationship: "This is exactly why we check every year."
- Do not rush this call. The client is relaxed and open.

**Compliance Notes:**
- No SOA required since no plan change is being discussed.
- Document the review and the G2G outcome in the client record for audit trail.
- Do not overstate the significance of changes that were reviewed.

**Cross-Sell Opportunities:**
- **Highest cross-sell conversion rate of any HEALTH campaign.** Client is relaxed, trusting, and open.
- LIFE: "Your health side is great. When's the last time we looked at your life insurance?"
- ANN-ALLOC: "Your Medicare is set. Let's make sure your retirement accounts are positioned just as well."
- NO-CORE reverse: If client only has HEALTH, introduce WEALTH/LEGACY services.

---

### 5. PSM-AEP-STAY -- AEP Stay (Stay with Changes)

**Trigger:** Plan review complete. Current plan is still the best option, but there are notable changes the client should know about before January.

**Division:** HEALTH

**Client Profile:** Client whose plan is still the best fit but has meaningful adjustments -- formulary changes, copay shifts, network updates -- that will be noticeable. Not bad enough to warrant switching, but significant enough to warrant a heads-up.

**Psychology:** This is a "no surprises" touchpoint. The client needs to know what is different so they are not blindsided at the pharmacy or doctor's office in January. The message: "You're staying, and that's the right call -- but here's what to expect."

**Key Message:** "Your plan is still the right fit, but there are a few changes this year we want to make sure you're aware of before January. None of it is big enough to justify switching, but it IS the kind of thing that surprises people in January when they weren't expecting it."

**Risk/Urgency:** If the client is not informed, they discover changes in January at the pharmacy counter or at a doctor visit. That creates frustration, erodes trust, and generates inbound service calls that could have been prevented. Proactive communication eliminates all of this.

**Agent Coaching:**
- Frame changes as manageable: "Nothing major, but we want you to know."
- Be specific about what changed without overwhelming: formulary adjustments, copay differences at certain visit types, minor network updates.
- Reinforce the decision: "We checked everything against the full marketplace -- staying put is the right call."
- Have the updated plan summary ready before the call.
- End with availability: "If you have questions about any of the changes, we're here."

**Compliance Notes:**
- No SOA required since no plan change is being discussed.
- Document the specific changes communicated in the client record.
- Accurately represent the nature and magnitude of changes. Do not minimize or exaggerate.

**Cross-Sell Opportunities:**
- Moderate. Client may be slightly anxious about changes, so cross-sell should be gentle.
- LIFE: "By the way, your policy anniversary is coming up -- we should check on that too."
- Best approached after the STAY conversation wraps, not during.

---

### 6. PSM-AEP-$0 -- AEP Move ($0 Premium)

**Trigger:** Plan review found a $0-premium plan that aligns with the client's P3 and healthcare consumption data. Represents a significant cost improvement.

**Division:** HEALTH

**Client Profile:** Client currently paying a monthly premium on their MAPD plan. A $0-premium alternative exists in their service area that covers their doctors, medications, and pharmacy at the same or better level, with lower projected costs.

**Psychology:** "$0 premium" is a powerful hook, but it must be grounded in data, not hype. The message is not "look how cheap this is" -- it is "we ran your numbers, and this plan covers everything you need with zero monthly premium. The data backs it up."

**Key Message:** "There's a $0-premium plan available that aligns with your prescriptions, providers, and pharmacies -- and based on your claims history, it projects to save you real money. We don't get excited about a plan unless the data backs it up."

**Risk/Urgency:** Client is currently paying a premium for coverage that is not outperforming a $0 option based on their actual situation. Every month that premium is paid is money that could stay in their pocket. $0-premium plans are not guaranteed to return year to year -- this is the window.

**Agent Coaching:**
- Lead with the data, not the $0. "We ran the full comparison... and it happens to be a $0-premium option."
- Emphasize alignment: "Same doctors, same medications, same pharmacy, lower cost structure."
- Address skepticism head-on: "We don't get excited about a plan unless the data backs it up."
- Let the client ask about the catch. If there are trade-offs (higher specialist copay, different pharmacy tier), be transparent.
- Have the full side-by-side comparison ready.

**Compliance Notes:**
- SOA required before discussing specific plan details.
- Never position $0 premium as "free healthcare" or "free insurance."
- All cost projections must be based on verified data, not estimates.
- Cannot guarantee the $0 plan will be available next year.

**Cross-Sell Opportunities:**
- Strong. Client is about to save money on premiums. Natural pivot: "Since you'll be saving on your monthly premium, this is a great time to think about where that money could be working for you."
- ANN-ALLOC or ANN-SUR if client has existing annuity products.
- Income planning if client is nearing or in retirement.

---

### 7. PSM-SEP-5 -- SEP 5-Star Plan Available

**Trigger:** A 5-star CMS-rated Medicare Advantage plan is identified in the client's service area that aligns with their P3 and healthcare consumption data. Can fire year-round because 5-star plans carry a year-round Special Enrollment Period.

**Division:** HEALTH

**Client Profile:** Existing Medicare client (MAPD) whose current plan is not 5-star rated. A 5-star alternative exists in their county that the data indicates would be a better fit.

**Psychology:** Most clients do not know what star ratings mean, and they definitely do not know that 5-star plans unlock year-round enrollment. The message: "There's a top-rated plan available, your data shows it's a fit, and you don't have to wait for October."

**Key Message:** "We've identified a 5-star rated Medicare Advantage plan in your area. A 5-star rating is the highest CMS gives -- fewer than 5% of plans nationwide earn it. Based on your data, it looks like a real improvement, and you don't have to wait for AEP to make a change."

**Risk/Urgency:** The 5-star SEP is available year-round, so there is no artificial time pressure. However, the plan itself may not return next year with the same rating or benefits. The opportunity is current. The data supports the move now.

**Agent Coaching:**
- Educate on what 5-star means: "The highest quality rating CMS gives. Fewer than 5% of plans nationwide earn it."
- Explain the SEP: "5-star plans have a year-round Special Enrollment Period, so you can switch any time."
- Let the comparison do the work: "We ran the numbers using your prescriptions, providers, pharmacies, and healthcare consumption."
- Do not rush. The year-round window removes time pressure. Focus on the data and let the client decide.

**Compliance Notes:**
- SOA required before discussing specific plan details.
- CMS star ratings must be current-year ratings. Cite the source.
- Do not guarantee the plan will maintain its 5-star rating in future years.
- 5-star SEP eligibility is a CMS rule. Accurately represent what it means.

**Cross-Sell Opportunities:**
- Moderate. If the client switches and saves money, the follow-up appointment is a natural place to discuss LIFE or WEALTH.
- Since this is a mid-year event: "While we're at it, let's make sure everything else is squared away."

---

### 8. PSM-SEP-3 -- SEP Below 3-Star Rating

**Trigger:** Client's current Medicare Advantage plan received a CMS rating below 3 stars. This opens a Special Enrollment Period, giving the client the option to switch.

**Division:** HEALTH

**Client Profile:** Client on a low-performing plan. May or may not be experiencing issues directly, but the plan's quality metrics are below average across customer service, preventive care, member outcomes, and claims processing.

**Psychology:** This is sensitive. The client may be perfectly happy with their plan despite the low rating. The message is not "your plan is bad" -- it is "the ratings are in, your plan is below average on quality metrics, and you have a window to look at alternatives if you want to."

**Key Message:** "CMS released their annual plan ratings. Your plan received a rating below 3 stars. That puts it in the lower tier of plan performance. You have a Special Enrollment Period to explore other options -- we've already started pulling your data."

**Risk/Urgency:** A low star rating does not mean the plan stops working tomorrow, but it reflects the plan's track record across quality metrics -- customer service, preventive care, member outcomes, claims processing. That track record is generally not a great indicator of what is coming. The SEP window is time-limited.

**Agent Coaching:**
- Be factual, not alarmist. "Your plan rated below 3 stars -- here's what that means."
- Explain what star ratings measure: customer service, preventive care, member outcomes, claims processing.
- Offer choice, not direction: "We've already started pulling your data so we can show you your options. If your plan is still the best fit despite the rating, we'll tell you."
- If the client says "I'm fine with my plan," respect it: "That's completely okay. We just wanted to make sure you knew about the window."
- Do not editorialize beyond what the data shows.

**Compliance Notes:**
- SOA required before discussing specific alternatives.
- Star rating data must come from official CMS sources.
- Do not predict future plan performance based on current star rating.
- Document the client's decision whether or not they choose to review alternatives.

**Cross-Sell Opportunities:**
- Low. This is a potentially anxious conversation. Focus on the HEALTH matter at hand.
- Cross-sell only if the client initiates a broader conversation about their accounts.

---

### 9. PSM-SEP-FEMA -- SEP FEMA Disaster Declaration

**Trigger:** Client resides in a FEMA-declared disaster area. A Special Enrollment Period of 2 months from the end of the declared emergency period is available.

**Division:** HEALTH

**Client Profile:** Client whose address falls within a FEMA-declared disaster area. Their healthcare situation may or may not have changed as a result of the emergency, but the SEP window gives them the option to revisit coverage regardless.

**Psychology:** This is a service touchpoint during a stressful time. The client needs to know about the window without feeling pressured. The message: "You have an option available to you. If your needs have changed, we're here."

**Key Message:** "Due to the recent FEMA-declared emergency in your area, you have a Special Enrollment Period. You have 2 months from the end of the declared emergency to make changes. If anything has changed with your healthcare needs, this is a good window to look at your options."

**Risk/Urgency:** FEMA SEPs do not come around often outside of AEP. The 2-month window is finite. If the client's situation has changed (new doctors, new prescriptions, pharmacy access disrupted), they need to act within this window or wait until the next AEP.

**Agent Coaching:**
- Lead with empathy. Do not lead with the enrollment opportunity.
- Keep it simple: "You have a window. If anything has changed, we can help."
- List potential changes that would warrant a review: new providers, new prescriptions, pharmacy access changes, dissatisfaction with current plan.
- If the client's situation has not changed: "If everything is still working for you, no action needed. We just wanted to make sure you knew the window was open."
- Let the client drive the conversation.

**Compliance Notes:**
- FEMA SEP eligibility is tied to the official disaster declaration. Confirm the client's ZIP is within the declared area before outreach.
- The 2-month window starts at the END of the declared emergency period, not the start.
- Document the FEMA declaration number and dates in the outreach record.
- Be sensitive to the emergency context. No sales language whatsoever.

**Cross-Sell Opportunities:**
- None during the initial FEMA outreach. This is purely a service touchpoint.
- Disaster situations can prompt life insurance and financial planning conversations, but only if the client initiates. Let the client drive.

---

### 10. PSM-OEP -- Open Enrollment Period Benefit Check

**Trigger:** January through March. The Medicare Advantage Open Enrollment Period. All MA members' plans have rolled into the new plan year. Benefit check to confirm everything is working as expected.

**Division:** HEALTH

**Client Profile:** Any client on a Medicare Advantage plan. Plan benefits, formulary, copays, and network have all updated as of January 1. May or may not have gone through an AEP review.

**Psychology:** "Rubber meets the road." The client is now living with whatever their plan became. If something is wrong -- pharmacy surprise, copay increase, provider network issue -- this is the safety net. The message: "If anything feels off, tell us now while we can still fix it."

**Key Message:** "Your plan has officially rolled over into the new year. We're doing a benefit check to make sure everything is running smoothly. If anything feels different -- prescriptions, doctors, copays -- we need to know before March 31st."

**Risk/Urgency:** March 31 is a hard deadline. After that, the client is locked in for the rest of the year. Any misalignment not caught and addressed during OEP becomes a full-year problem with no recourse until the next AEP.

**Agent Coaching:**
- Frame as a check-in, not a sales call: "Happy new year. Just making sure everything's running right."
- Ask specific questions: "How was your first pharmacy visit? Any copay surprises? Is your doctor still showing as in network?"
- If something is wrong, act immediately: "Good thing you told us -- we have until March 31 to fix this."
- If everything is fine: "Great -- you're all set for the year."
- This is where AEP misalignments get caught. Take it seriously.

**Compliance Notes:**
- OEP allows ONE plan switch during Jan 1 - Mar 31 for MA members (MA to MA, or MA to Original Medicare + standalone PDP). Not multiple switches.
- Document the benefit check conversation and outcome in the client record.

**Cross-Sell Opportunities:**
- Moderate. "New year, fresh start" energy. If the client is happy and the benefit check is clean:
- LIFE: "Your health coverage is great. Want us to take a quick look at your life insurance too?"
- ANN-ALLOC: If annuity anniversary is in Q1, combine the conversations.
- Best timed after the benefit check confirms everything is smooth.

---

### 11. PSM-NO-CORE -- No-Core Cross-Sell

**Trigger:** Active RPI client who has life insurance, annuity, or other products through RPI but does NOT have MedSupp or MAPD through RPI. Runs January through September only (paused Oct-Dec for AEP blackout).

**Division:** HEALTH

**Client Profile:** WEALTH or LEGACY client who, for whatever reason, does not have their Medicare coverage managed by RPI. May have it through another agent/agency, may be on Original Medicare without supplemental coverage, or may have enrolled directly through a carrier.

**Psychology:** The client already trusts RPI with other products. The message: "We noticed we're not handling your Medicare. Health, wealth, and legacy are interconnected. Let us show you what our Proactive Service Model looks like for Medicare -- it's the same level of attention we give your other accounts."

**Key Message:** "We've got your {Carrier} {ProductName}, but we don't have your Medicare coverage on file. Medicare is one of the core services we provide. We'd love the opportunity to be a resource for you here."

**Risk/Urgency:** If Medicare coverage is not being actively managed with the same data-driven approach RPI uses for other products, the client is likely leaving value on the table. Plans change every year. Without someone running the numbers, misalignment compounds over time.

**Agent Coaching:**
- Do not criticize their current agent or coverage. "For whatever reason -- timing wasn't right, you already had it handled, it never came up -- we just want you to know this is a huge part of what we do."
- Sell the PSM model, not a specific plan: "We pull your prescriptions, providers, pharmacies, and healthcare data. We run cost projections. We monitor your plan year-round and proactively review it every AEP."
- Connect the verticals: "It's the same level of attention we give your other accounts -- applied to your health insurance."
- If they are happy with their current setup: "No pressure at all. Just want you to know the door is open."

**Compliance Notes:**
- Cannot run during AEP blackout (Oct-Dec). Cross-sell Medicare outreach during AEP creates regulatory risk and message confusion.
- SOA will be required if the client engages and wants to discuss specific plan options.
- Ensure the client is Medicare-eligible before outreach. If under 65, note for future outreach at eligibility.
- Never disparage the client's current agent or agency.

**Cross-Sell Opportunities:**
- This IS the cross-sell campaign. If the client engages, they enter the HEALTH flow: SEP-PREP (if authorizations needed), then AEP-REV at the next AEP cycle.
- During the conversation, also confirm satisfaction with existing WEALTH/LEGACY products. This is a full-relationship touchpoint.

---

### 12. PSM-LIFE -- Life Insurance Statement Review

**Trigger:** Approximately 30 days after the policy anniversary, timed to when the annual statement arrives in the client's mailbox.

**Division:** LEGACY

**Client Profile:** Client with a permanent life insurance policy (universal life, indexed universal life, whole life, variable universal life) through RPI. The annual statement is a summary of the last 12 months of policy activity.

**Psychology:** Most clients receive their annual statement, glance at it (or don't), and file it. They assume their life insurance is fine because they have been paying the premium. The core message: "Your statement shows the rearview mirror. What matters is the windshield -- is your policy going to last as long as you are?"

**Key Message:** "Your annual statement is in. It shows what happened last year -- premiums, fees, cost of insurance, credits. What it can't tell you is how your policy is going to perform going forward. We want to order an in-force illustration to make sure it's on track."

**Risk/Urgency:** Cost of insurance increases with age. If interest rates or index credits have not kept pace, the policy could be quietly falling behind. The worst time to discover this is when it is too late to fix. An in-force illustration reveals the trajectory now, while there are still options -- adjust premium, modify the benefit, or look at other strategies.

**Agent Coaching:**
- Do not alarm the client. "We do this for every client every year."
- Explain the difference between statement and in-force illustration simply: "Your statement looks backward. An in-force illustration looks forward."
- Use the "peace of mind" frame for healthy policies: "If it's on track, great -- you'll have that in writing."
- Use the "options" frame for at-risk policies: "If it needs attention, we want to catch it now while we still have options."
- The ask is small: "Let us order an in-force illustration. You don't have to do anything except let us request it."
- If the policy shows lapse risk, escalate to the agent's COR/SPC for a formal review.

**Compliance Notes:**
- In-force illustrations must be requested from the carrier. RPI cannot generate them independently.
- Never guarantee policy performance based on the annual statement alone.
- If the in-force shows lapse risk, document the finding and the recommended course of action.
- Any 1035 exchange discussion requires full suitability analysis.
- Client must understand the difference between guaranteed and non-guaranteed columns in the illustration.

**Cross-Sell Opportunities:**
- HEALTH: "While we're looking at your life insurance, when's the last time we reviewed your Medicare?"
- ANN-ALLOC/ANN-SUR: "Your life policy anniversary just passed -- do any of your annuity anniversaries line up? Let's check those too."
- Estate/Legacy planning: If the in-force shows a healthy policy, natural door-opener for broader legacy conversations.
- If the policy is underperforming and a 1035 exchange is appropriate, WEALTH products (FIA, MYGA) may be relevant.

---

### 13. PSM-ANN-SUR -- Annuity Surrender Charge Below 10%

**Trigger:** Client's annuity surrender charge has declined below 10%. The repositioning window is opening.

**Division:** WEALTH

**Client Profile:** Client with a fixed index annuity, multi-year guaranteed annuity, or other deferred annuity that has been in force for several years. Surrender charges have eroded to the point where a 1035 exchange or repositioning could be executed with minimal or no net loss to account value.

**Psychology:** The client may not know what surrender charges are or that they have been declining. The message is not "your annuity is bad" -- it is "a window is opening. Let's see if the market has something better for your situation."

**Key Message:** "Your surrender charges have come down to a point where it may be worth taking a fresh look. If there's an opportunity to improve your position without a net loss to your account value, we want to show you."

**Risk/Urgency:** Not urgent in the "act now" sense. The surrender charges will continue to decline. But interest rates, product designs, and available features are market-dependent and change. The current environment may offer opportunities that were not available when the client originally funded their annuity. Worth exploring while conditions are favorable.

**Agent Coaching:**
- Be neutral. "This doesn't mean anything is wrong with what you have."
- Explain what surrender charges are simply: "When you first put money into your annuity, there was a period where moving it would cost you a percentage. That percentage has been going down every year, and it's getting to the point where it may not cost you anything."
- Frame the comparison as optional but valuable: "We want to run a comparison. If you're already in the best spot, we'll tell you."
- Ask about the client's current goals -- they may have shifted since the annuity was funded.
- Have carrier illustrations ready to compare: guaranteed income options, capital access features, LTC riders, terminal illness riders, crediting strategies.

**Compliance Notes:**
- Any 1035 exchange recommendation requires a full suitability analysis.
- Must disclose the new surrender charge period if the client repositions.
- Never characterize moving as "penalty-free" unless surrender charges are truly at 0%.
- Accurately represent current surrender charge percentage.
- Document the comparison and the client's decision in the account record.

**Cross-Sell Opportunities:**
- LIFE: If the client's life insurance is with the same carrier, natural time to review both.
- Income planning: If the client is approaching RMD age or retirement, the annuity conversation naturally extends to income strategy.
- HEALTH: "While we're looking at your financial picture, let's make sure your Medicare is just as optimized."

---

### 14. PSM-ANN-ALLOC -- Annuity Allocation Review

**Trigger:** Policy anniversary. The annual window when the client can adjust their allocation strategy (index options, fixed accounts, crediting methods) for the next contract year.

**Division:** WEALTH

**Client Profile:** Client with a fixed index annuity that allows annual allocation changes at the policy anniversary. May have set their allocation at funding and never revisited it.

**Psychology:** Most clients set their allocation once and forget it. The message: "Your anniversary is your one chance each year to make sure your money is positioned for what's ahead. Cap rates change, index options evolve, and what worked three years ago may not be optimal today."

**Key Message:** "Your annuity anniversary is coming up. This is your window to review and adjust your allocations for the next 12 months. Let's make sure you're positioned for what's ahead, not just riding on last year's selections."

**Risk/Urgency:** The anniversary window is typically short (30 days). Once it passes, the client is locked into their current allocations for another 12 months. If cap rates have shifted or new index options have been added, the client misses the opportunity to optimize. This is a calendar-driven hard deadline.

**Agent Coaching:**
- Educate on what the anniversary means: "This is the one time each year you can change how your money is allocated."
- Review performance: "Here's how each of your strategies performed over the last year."
- Show what is available: "Here are the cap rates and index options for the next contract year."
- Present the interest rate environment context: "Rates have [moved/held steady], which means [these strategies] look [more/less] attractive."
- If the current allocation still makes sense: "You're in good shape -- we'll confirm it."
- If adjustments are warranted: "Based on the new cap rates, here's what we'd recommend."
- Pull the current allocation detail and performance summary before the call.

**Compliance Notes:**
- Allocation changes are within the existing contract -- no suitability analysis required for internal reallocations.
- Accurately represent historical performance and do not guarantee future results based on past index performance.
- Document the review and the client's allocation decisions.
- If the conversation leads to a discussion about moving the annuity entirely, that becomes a PSM-ANN-SUR or PSM-ANN-LIQ conversation and requires suitability.

**Cross-Sell Opportunities:**
- LIFE: "Your annuity anniversary just passed. When's the last time we looked at your life insurance? The anniversary on that should be coming up too."
- HEALTH: "Your financial accounts are in great shape. Let's make sure your Medicare is just as well-positioned."
- Income planning: If the client is nearing retirement/RMD age, the allocation review naturally leads to income strategy discussions.

---

### 15. PSM-ANN-LIQ -- Annuity Fully Liquid

**Trigger:** Annuity surrender charges have reached zero. The account is fully liquid with complete flexibility to keep, reposition, or withdraw without penalties.

**Division:** WEALTH

**Client Profile:** Client whose annuity has completed its surrender charge period. May be 5-10+ years into the contract. The client may not realize they have reached this milestone.

**Psychology:** "Fully liquid" is a milestone most clients do not think about. The message: "Your money is completely free to move. The question is whether it's working as hard as it can for you where it is. This is the widest your window has ever been."

**Key Message:** "Your annuity is fully liquid -- zero surrender charges. Complete flexibility to keep it, reposition it, or explore other options. No penalties, no fees. Let's make sure your money is positioned where it should be."

**Risk/Urgency:** The risk is inaction. The product landscape evolves -- new crediting strategies, better income riders, improved guarantees. What was competitive when the client funded may not be competitive today. The client is not losing money, but they may be leaving opportunity on the table. This is the most important decision point in the annuity lifecycle.

**Agent Coaching:**
- Frame liquidity as a milestone: "Congratulations -- your surrender charges are completely behind you."
- Be clear about the options: "You can keep it where it is, reposition it for better terms, or access it. No penalties either way."
- Offer the comparison: "Let us run a side-by-side of what you have versus what's available today."
- If the current account is still competitive: "You're in a great spot. We'll confirm that."
- If there is a meaningful improvement: "The market has moved since you funded this. Here's what that looks like."
- Have the full comparison ready: current crediting rates, guarantees, rider values vs. marketplace alternatives.
- Present multiple options based on the client's goals: income, growth, LTC protection, legacy.
- Do not pressure. The client's money is free, and so is their decision.

**Compliance Notes:**
- Full suitability analysis required before recommending any 1035 exchange or repositioning.
- Must disclose new surrender charge period if the client moves to a new product.
- Accurately represent current account values and any guarantees that would be forfeited by moving. Client must understand what they keep vs. what they give up.
- If the client wants to withdraw, discuss tax implications and RMD considerations. Refer to tax advisor as appropriate.
- Document the review, the comparison, and all client decisions.

**Cross-Sell Opportunities:**
- **Strongest cross-sell opportunity in the WEALTH vertical.** Client has a liquid asset and is in a decision-making mindset.
- LIFE: If the client has excess funds, permanent life insurance as an estate planning tool.
- Income planning: If retirement is approaching, guaranteed income products.
- HEALTH: "Your financial side is optimized. Let's make sure your healthcare is too."
- Legacy planning: "Now that your annuity is liquid, this is a great time to revisit your overall legacy plan."
- This is the full Health + Wealth + Legacy conversation opportunity.

---

## Quick Reference Matrix

| # | Campaign ID | Division | Trigger | Timing | Enrollment Type | Cross-Sell Strength |
|---|-------------|----------|---------|--------|-----------------|---------------------|
| 1 | PSM-SEP-PREP | HEALTH | Missing/expired authorizations | Sep | Pre-AEP | None |
| 2 | PSM-AEP-REV | HEALTH | Annual plan review cycle | Sep-Oct | AEP | Low (initial outreach) |
| 3 | PSM-AEP-MOVE | HEALTH | Review found better plan | Nov-Dec | AEP | Moderate |
| 4 | PSM-AEP-G2G | HEALTH | Plan confirmed best | Nov-Dec | AEP | **Highest (HEALTH)** |
| 5 | PSM-AEP-STAY | HEALTH | Plan best, has changes | Nov-Dec | AEP | Moderate |
| 6 | PSM-AEP-$0 | HEALTH | $0-premium plan found | Nov-Dec | AEP | Strong |
| 7 | PSM-SEP-5 | HEALTH | 5-star plan in area | Year-round | SEP | Moderate |
| 8 | PSM-SEP-3 | HEALTH | Plan below 3 stars | Year-round | SEP | Low |
| 9 | PSM-SEP-FEMA | HEALTH | FEMA declaration | 2-month window | SEP | None |
| 10 | PSM-OEP | HEALTH | New year rollover | Jan-Mar | OEP | Moderate |
| 11 | PSM-NO-CORE | HEALTH | No Medicare through RPI | Jan-Sep | N/A | **IS the cross-sell** |
| 12 | PSM-LIFE | LEGACY | Policy anniversary +30d | Year-round | N/A | Moderate |
| 13 | PSM-ANN-SUR | WEALTH | Surrender charge <10% | Year-round | N/A | Moderate |
| 14 | PSM-ANN-ALLOC | WEALTH | Policy anniversary | Year-round | N/A | Moderate |
| 15 | PSM-ANN-LIQ | WEALTH | Surrender charges at 0% | Year-round | N/A | **Highest (WEALTH)** |

---

*We're Your People.(TM)*
