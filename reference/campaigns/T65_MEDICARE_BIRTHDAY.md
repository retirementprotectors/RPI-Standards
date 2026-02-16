# T65 -- Medicare Birthday Countdown

> Knowledge document for the T65 campaign engine. 15 campaigns across 4 phases of the Medicare Initial Enrollment Period journey.
> All content approved by JDM on 2026-02-16.

---

## Engine Overview

**T65 = Medicare Birthday Countdown.** A 15-month journey that begins 12 months before a client's 65th birthday and runs through 2 months after. The engine guides prospective Medicare enrollees from initial education through enrollment and verification, using a reassurance-first approach that respects two distinct paths: enroll now or defer.

| Metric | Value |
|--------|-------|
| **Total Campaigns** | 15 |
| **Phase 1: Education** | 6 campaigns (T65-12 to T65-07) |
| **Phase 2: Planning** | 3 campaigns (T65-06 to T65-04) |
| **Phase 3: Urgent** | 3 campaigns (T65-03 to T65-01) |
| **Phase 4: Action/Follow-up** | 3 campaigns (T65-00 to T65+2) |
| **Channels per campaign** | Email, Text/SMS, Voicemail Script, USPS Mailer |
| **Execution path** | C3 (campaign engine) --> PRODASH (delivery) --> 4 channels |

### Campaign Inventory

| # | Campaign ID | Name | Phase | Months to 65 |
|---|-------------|------|-------|---------------|
| 1 | T65-12 | First Introduction | Education | 12 months before |
| 2 | T65-11 | Medicare Basics | Education | 11 months before |
| 3 | T65-10 | Two Paths | Education | 10 months before |
| 4 | T65-09 | Authorization Introduction | Education | 9 months before |
| 5 | T65-08 | Data Gathering Begins | Education | 8 months before |
| 6 | T65-07 | Situation Assessment | Education | 7 months before |
| 7 | T65-06 | IEP Window Preview | Planning | 6 months before |
| 8 | T65-05 | Plan Comparison Prep | Planning | 5 months before |
| 9 | T65-04 | Recommendation Build | Planning | 4 months before |
| 10 | T65-03 | IEP Window Opens | Urgent | 3 months before |
| 11 | T65-02 | Enrollment Push | Urgent | 2 months before |
| 12 | T65-01 | Final Pre-Birthday | Urgent | 1 month before |
| 13 | T65-00 | Birthday Month | Action/Follow-up | Birthday month |
| 14 | T65+1 | Post-Enrollment Check | Action/Follow-up | 1 month after |
| 15 | T65+2 | Coverage Verification | Action/Follow-up | 2 months after |

---

## T65 Philosophy

**"You might not even need to worry about it."** The T65 engine is anti-fear, anti-confusion, anti-pressure. Turning 65 is one of the most over-marketed, over-complicated events in American life. Every mailer, every ad, every "Medicare seminar" screams urgency and complexity. RPI does the opposite.

### Core Principles

1. **Reassurance-first.** The opening message is not "Medicare is coming and you need to act." It is "Hey, your birthday is coming up. You might not even need to worry about this. Let's find out." Most people approaching 65 are anxious because they have been bombarded with confusing information. RPI cuts through the noise.

2. **Two paths, both valid.** Every client turning 65 falls into one of two situations:
   - **Path 1: Stay on employer plan.** If the client (or their spouse) has employer coverage through a company with 20+ employees, they can defer Part B and Part D without penalty. RPI monitors the situation and is ready when the time comes.
   - **Path 2: Enroll in Medicare.** If the client does not have qualifying employer coverage, they need to enroll. RPI handles everything -- Part A, Part B, Part D or MAPD, Medigap if appropriate.

   Neither path is "better." The right path depends on the client's situation, and RPI figures that out early.

3. **Authorization model.** Before RPI can do meaningful work, the client needs to authorize data access. Two types:
   - **Third-party authorization from current health insurer** (FHIR format) -- gives RPI visibility into current coverage, claims, and utilization patterns.
   - **EHR from providers** -- healthcare trend information from the client's doctors.

   Authorization is introduced early (T65-09) but not pushed aggressively. It is framed as the thing that makes the analysis real instead of theoretical.

4. **Progressive education.** The 15-month journey follows a deliberate arc:
   ```
   Basics --> Situation Assessment --> Data Gathering --> Comparison --> Recommendation --> Enrollment --> Verification
   ```
   Each campaign builds on the last. By the time the IEP window opens, the client is educated, their data is in hand, and the decision is straightforward.

5. **"Hey, you're my people, what do you need me to do?"** That is the ideal client response. The entire T65 engine is designed to build enough trust and clarity that the client simply says "handle it." Not because they are passive, but because they are confident RPI has already done the work.

6. **Commission-based model.** Same as PSM. RPI is compensated by carriers. The client never pays RPI. Never use the word "free." There is no cost to imply the absence of.

---

## IEP Rules Reference

**Initial Enrollment Period (IEP) -- the rules that govern every T65 campaign.**

| Rule | Detail |
|------|--------|
| **Window** | 7 months: 3 months before 65th birthday, birthday month, 3 months after |
| **Months 1-3 enrollment** | Part B starts the 1st of the birthday month (no coverage gap) |
| **Month 4 (birthday month)** | Part B starts the 1st of the month after enrollment |
| **Month 5** | Part B starts 2 months after enrollment |
| **Month 6** | Part B starts 3 months after enrollment |
| **Month 7** | Part B starts 3 months after enrollment |
| **Part B late penalty** | 10% increase per 12-month period without coverage. **PERMANENT. LIFETIME.** Added to the premium forever. |
| **Part D late penalty** | 1% of national base premium per month without creditable coverage. **PERMANENT. LIFETIME.** |
| **Medigap guaranteed issue** | 6 months from Part B effective date. During this window, no medical underwriting -- guaranteed acceptance. Miss it and the client may face medical underwriting **possibly forever.** |
| **Auto-enrollment** | If already receiving Social Security benefits, Part A (and sometimes Part B) may be auto-enrolled. Client still needs to make coverage decisions. |
| **Employer coverage (20+ employees)** | Can delay Part B and Part D enrollment without penalty for as long as employer coverage continues. |
| **COBRA / Retiree plans** | Do NOT protect from late enrollment penalties. COBRA and retiree coverage are NOT creditable for penalty avoidance. This is the single most common and costly mistake. |
| **General Enrollment Period** | If the IEP is missed entirely: Jan 1 - Mar 31 each year. Coverage does not start until July 1. Plus permanent late penalties. |

### Penalty Math Examples

**Part B:** Client delays 2 years without qualifying coverage. Penalty = 20% (10% x 2). If the standard premium is $185/month, they pay $222/month. Forever.

**Part D:** Client delays 14 months without creditable coverage. Penalty = 14% of the national base beneficiary premium. If NBBP is $36.78, penalty = $5.15/month. Added to every Part D premium. Forever.

**Medigap:** Client waits 7 months after Part B effective date to apply. Guaranteed issue period has closed. Carrier can medically underwrite. Client with pre-existing conditions may be denied or rated up. No federal protection outside the guaranteed issue window.

---

## Tone Rules

These rules apply to ALL 15 campaigns, ALL channels (email, text/SMS, VM, USPS).

| Rule | Detail |
|------|--------|
| **No "free" language** | Commission-based. There is no cost to imply the absence of. |
| **No urgency/sales mechanics** | No "15 minutes," "today only," "Reply YES," countdown timers. This is education and service, not sales. |
| **No technical jargon** | No "IEP," "creditable coverage," "IRMAA," "Part B penalty" in client-facing content. Use plain language: "your enrollment window," "coverage that counts," "your monthly premium." |
| **Anti-urgency framing** | "You might not even need to worry about this." The first message is calming, not alarming. |
| **Commission transparency** | Never mention commission. Never imply RPI charges the client. The service just exists because "this is what we do." |
| **Always personalize** | Every client-facing touch must include `{FirstName}` and `{AgentName}` at minimum. |
| **No sales language** | No "opportunity of a lifetime," "act now," "don't miss out." |
| **Agent as guide** | The agent is positioned as a knowledgeable guide who has been through this hundreds of times, not a salesperson pitching. |
| **Energy** | Warm, calm, competent. "We've done this a thousand times. Let's figure out what makes sense for you." |

### Personalization Merge Fields

| Field | Source |
|-------|--------|
| `{FirstName}`, `{LastName}` | Client/prospect record |
| `{AgentName}` | Assigned agent |
| `{BOBName}` | Book of Business name |
| `{Phone}` | Agent phone |
| `{Email}` | Agent email |
| `{CalendarLink}` | Scheduling link |
| `{BirthdayMonth}` | Client's 65th birthday month |
| `{IEPStart}` | IEP window open date (3 months before birthday) |
| `{IEPEnd}` | IEP window close date (3 months after birthday) |
| `{MedigapDeadline}` | 6 months from Part B effective date |

---

## Phase Overview

### Phase 1: Education (T65-12 to T65-07)

**Purpose:** Build the relationship, establish RPI as the guide, assess the client's situation, and begin data gathering. No decisions are made in this phase. The client should leave this phase understanding what Medicare is, which of the two paths applies to them, and why data authorization matters.

### Phase 2: Planning (T65-06 to T65-04)

**Purpose:** Translate education into action. The IEP window is visible on the horizon. Data is being gathered and analyzed. Plan comparisons are being built. The client transitions from "learning about Medicare" to "here are my specific options."

### Phase 3: Urgent (T65-03 to T65-01)

**Purpose:** The IEP window is open. Decisions need to be made. This phase is where enrollment happens for clients on Path 2. For Path 1 clients, this phase confirms their deferral strategy and documents it. "Urgent" does not mean "pushy" -- it means the window is real and the consequences of missing it are permanent.

### Phase 4: Action/Follow-up (T65-00 to T65+2)

**Purpose:** Birthday month enrollment execution, post-enrollment verification, and handoff to ongoing PSM service model. The client transitions from T65 prospect to PSM-managed client.

---

## Campaign Details

---

### 1. T65-12 -- First Introduction

**Trigger:** 12 months before 65th birthday. First touch in the T65 journey.

**Phase:** Education

**Client Profile:** Person approaching 65. May be an existing RPI client (WEALTH or LEGACY) or a new prospect. Has likely been receiving Medicare mailers from every carrier and agency in their ZIP code for months. Confused, possibly anxious, definitely over-marketed-to.

**Psychology:** The client has been bombarded. Every piece of mail says "URGENT" or "DON'T MISS YOUR WINDOW." RPI's first touch needs to be the opposite -- calm, reassuring, and honest. "You might not even need to worry about this" is disarming because nobody else is saying it. It immediately positions RPI as different.

**Key Message:** "Your 65th birthday is about a year away. You've probably been getting a lot of mail about Medicare. Here's the truth: you might not even need to worry about it right now. We're going to help you figure out what actually applies to your situation -- no pressure, no sales pitch, just clarity."

**Risk/Urgency:** None at this stage. The IEP window does not open for 9 more months. The only risk is the client ignoring all outreach (including RPI's) and not engaging until it is too late. This touch begins the relationship early enough to prevent that.

**Agent Coaching:**
- This is an introduction, not a consultation. Keep it light.
- The goal is a response -- any response. "Got it, thanks" is a win.
- Do NOT launch into Medicare education on the first touch. Save that for T65-11.
- If the client responds with questions, answer them warmly but steer toward scheduling a proper conversation at T65-10 or later.
- If the client says "I have employer coverage": "Perfect -- that changes the picture entirely. We'll walk through what that means for you in our next touch."
- If the client is an existing RPI client: reference their existing relationship. "We've got your {Carrier} {ProductName} -- now we want to make sure your Medicare is just as well-handled."

**Compliance Notes:**
- No plan-specific information at this stage.
- No enrollment discussions.
- This is purely introductory. No SOA required.
- Do not promise specific outcomes or savings.

---

### 2. T65-11 -- Medicare Basics

**Trigger:** 11 months before 65th birthday. Second touch.

**Phase:** Education

**Client Profile:** Same as T65-12 but has now received the first introduction. May or may not have responded. Regardless, the education continues.

**Psychology:** Now that the ice is broken, the client needs a simple foundation. "What is Medicare, actually?" Most people approaching 65 have heard the terms -- Part A, Part B, Part D -- but have no idea what they mean or how they fit together. This touch provides the basics without overwhelming.

**Key Message:** "Medicare has a few parts, and they're simpler than the mail makes them look. Part A covers hospital stays -- most people get it automatically. Part B covers doctors and outpatient care -- there's a monthly premium. Part D covers prescriptions. That's the foundation. Everything else builds on top of it."

**Risk/Urgency:** None. Pure education. The only risk is information overload, which is why this touch stays at the 30,000-foot level.

**Agent Coaching:**
- Keep it simple. Part A = hospitals. Part B = doctors. Part D = drugs. That is all the client needs right now.
- Do NOT introduce Medicare Advantage, Medigap, or supplemental coverage yet. That comes later.
- Do NOT discuss costs, penalties, or enrollment windows. Too early.
- If the client asks about Medicare Advantage or supplements: "Great question -- we'll get into that. Right now we're just laying the foundation so the rest makes sense."
- Use analogies if they help: "Think of Part A and Part B as the base layer. Everything else is built on top."

**Compliance Notes:**
- No plan-specific information.
- No carrier names or product references.
- Educational content only.
- Ensure all descriptions of Medicare Parts are factually accurate per CMS definitions.

---

### 3. T65-10 -- Two Paths

**Trigger:** 10 months before 65th birthday.

**Phase:** Education

**Client Profile:** Client now has the basics. This touch introduces the critical fork: are they staying on employer coverage, or do they need to enroll?

**Psychology:** This is the most important early touchpoint. The client needs to understand that their situation determines their path, and that both paths are completely fine. The anxiety most people feel comes from not knowing which path they are on. This touch resolves that ambiguity.

**Key Message:** "Here's the big question: do you (or your spouse) have health insurance through an employer with 20 or more employees? If yes, you might be able to delay Medicare enrollment with no penalty -- and we'll keep an eye on things until you're ready. If no, we'll start building your Medicare plan now. Either way, we've got you."

**Risk/Urgency:** Getting the path wrong has permanent consequences. Enrolling in Part B unnecessarily costs money. Failing to enroll when required triggers lifetime penalties. This touch is about accurately assessing the situation, not about urgency.

**Agent Coaching:**
- The 20-employee threshold is critical. Ask specifically: "Is the company 20 or more employees?" Do not assume based on company name.
- COBRA does NOT count. Retiree coverage does NOT count. If the client mentions either: "That's good coverage to have right now, but it doesn't protect you from Medicare late enrollment penalties the way active employer coverage does. This is exactly why we check."
- If the client is on Path 1 (employer coverage): "You're in great shape. We'll document your employer coverage and monitor things. When you do transition to Medicare, we'll be ready."
- If the client is on Path 2 (needs to enroll): "No problem at all. We've got plenty of time and we're going to walk you through every step."
- Document the client's path in their record. This drives the entire remaining campaign sequence.

**Compliance Notes:**
- Employer coverage determination must be based on the client's actual situation, not assumptions.
- COBRA and retiree coverage exceptions must be communicated clearly. This is a high-liability area.
- Document the employer coverage status and date of assessment.
- If the client is uncertain about their employer's size, advise them to confirm with HR before making any decisions.

---

### 4. T65-09 -- Authorization Introduction

**Trigger:** 9 months before 65th birthday.

**Phase:** Education

**Client Profile:** Path is determined. For Path 2 clients, data gathering needs to begin. For Path 1 clients, authorization still provides value for future planning.

**Psychology:** "Authorization" sounds bureaucratic. The client needs to understand what it does in plain terms: it lets RPI see actual healthcare data instead of guessing. Frame it as the difference between a real analysis and a shot in the dark.

**Key Message:** "To give you real numbers instead of guesswork, we need to connect to your healthcare information. That means two things: a quick authorization with your current health insurer so we can see your coverage history, and a connection to your healthcare providers so we can understand your healthcare trends. It takes a few minutes and it's what makes our analysis worth doing."

**Risk/Urgency:** Without authorization data, any plan comparison is theoretical. RPI can check if doctors and medications are in network, but cannot project actual costs based on real utilization. The sooner authorization is in place, the more time RPI has to build a thorough analysis.

**Agent Coaching:**
- Do not use the term "EHR" or "electronic health records" with the client.
- Frame it as: "information from your health insurer about your coverage" and "information from your doctors about your healthcare trends."
- Emphasize speed: "It takes a few minutes."
- Walk the client through the process on the call if possible.
- For Path 1 clients: "Even though you're staying on employer coverage for now, this data helps us understand your healthcare picture so we're ready when you do transition."
- If the client hesitates: "This is the same kind of information sharing that happens when you see a new doctor. We just need your okay to access it."

**Compliance Notes:**
- Authorization language must not imply access to full medical records. Use "healthcare trends" and "coverage history."
- Client must actively consent. Document the authorization type and date.
- All data obtained must be stored in Google Workspace (Drive/Sheets). Never Slack, text, or personal email.
- FHIR-format authorization from current insurer must comply with carrier-specific consent requirements.

---

### 5. T65-08 -- Data Gathering Begins

**Trigger:** 8 months before 65th birthday.

**Phase:** Education

**Client Profile:** Authorization is (ideally) in place. RPI begins pulling and analyzing the client's healthcare data -- prescriptions, providers, pharmacies, utilization history.

**Psychology:** The client should feel that things are moving. Not rushed, but progressing. "We're doing the work" is the message. The client does not have to do anything except confirm their information is current.

**Key Message:** "We're pulling your data now -- prescriptions, providers, pharmacies, and your healthcare trends. Once we have the full picture, we'll be able to show you exactly what your options look like. Quick question: has anything changed with your medications, doctors, or pharmacy in the last few months?"

**Risk/Urgency:** Stale data leads to bad recommendations. A medication change, a new specialist, or a pharmacy switch can materially change the plan comparison. This touch ensures the data is current.

**Agent Coaching:**
- Ask specifically about changes: new medications, new doctors, dropped doctors, pharmacy changes.
- If authorization is not yet complete: "We're still waiting on your authorization -- can we get that done today so we can start pulling your data?"
- For Path 1 clients: data gathering still applies. "Even while you're on employer coverage, understanding your healthcare picture helps us plan for when you do transition."
- Confirm the P3 (prescriptions, providers, pharmacies) is accurate. This is the foundation of every plan comparison.

**Compliance Notes:**
- All healthcare data must be handled per PHI rules. Google Workspace only.
- Do not share specific healthcare data (medications, diagnoses) via unencrypted channels.
- If the client provides updated medication or provider information, update the record immediately.

---

### 6. T65-07 -- Situation Assessment

**Trigger:** 7 months before 65th birthday. End of Education phase.

**Phase:** Education

**Client Profile:** Data is in hand (or as much as the client has authorized). RPI now has a clear picture of the client's healthcare situation, current coverage, and which path they are on.

**Psychology:** This is the "here's where you stand" touchpoint. The client has been learning for 5 months. Now they get a personalized summary. "Based on everything we've gathered, here's your situation." This is satisfying -- it shows the education was leading somewhere.

**Key Message:** "We've put together a clear picture of your situation. Here's what we know: your current coverage, your prescriptions, your providers, your pharmacy, and your healthcare patterns. In the next few months, we're going to use all of this to build your specific Medicare options. You're in great shape."

**Risk/Urgency:** None directly. This is a status report. The indirect risk is losing the client's attention before the Planning phase begins. The situation assessment keeps them engaged by showing tangible progress.

**Agent Coaching:**
- Present a summary, not a data dump. "Here's what we know about your situation" -- not a spreadsheet.
- For Path 1 clients: "Your employer coverage is solid. We've documented everything and we'll be ready when the time comes. In the meantime, here's what your healthcare picture looks like."
- For Path 2 clients: "We've got everything we need to start building your options. Your IEP window opens in 4 months -- we'll have a full comparison ready well before then."
- Confirm the client's path has not changed (e.g., job change, spouse coverage change).
- This is a good time to schedule the T65-06 or T65-05 planning conversation.

**Compliance Notes:**
- Do not present specific plan options yet. This is a situation summary, not a recommendation.
- All data presented must be verified against current records.
- Document any changes to the client's situation (path change, coverage change, P3 update).

---

### 7. T65-06 -- IEP Window Preview

**Trigger:** 6 months before 65th birthday. Planning phase begins.

**Phase:** Planning

**Client Profile:** Educated client who understands their path, has authorized data access, and has a documented healthcare profile. The IEP window is now on the near horizon.

**Psychology:** The shift from education to planning. The client needs to understand what the IEP window is in practical terms: when it opens, when it closes, and what happens inside it. No jargon -- just the timeline.

**Key Message:** "Your enrollment window opens in 3 months. It runs for 7 months total -- 3 months before your birthday, your birthday month, and 3 months after. The earlier you enroll within that window, the sooner your coverage kicks in. We're going to have everything ready so you can make your decision with confidence."

**Risk/Urgency:** The IEP window is approaching. While not yet urgent, the client needs to understand the timeline so they are not caught off guard. The key rule: enrolling in the first 3 months means coverage starts the birthday month with no gap. Waiting past the birthday month means delayed coverage.

**Agent Coaching:**
- Explain the 7-month window simply. Draw the timeline if on a call.
- Emphasize that early enrollment within the window = no coverage gap.
- For Path 1 clients: "This window is yours if you need it. Since you have employer coverage, you can let it pass without penalty. But if anything changes with your employment between now and then, we need to know immediately."
- For Path 2 clients: "We want to be ready to enroll you in the first 3 months of your window. That means the work we do over the next few months is critical."
- Introduce the Medigap guaranteed issue window: "There's a separate window for supplemental coverage that we need to be aware of too -- 6 months from when your Part B starts."

**Compliance Notes:**
- IEP dates must be calculated accurately based on the client's actual birth date.
- Do not overstate consequences of waiting within the window. Be factual: later enrollment = later coverage start.
- Medigap guaranteed issue must be explained accurately. 6 months from Part B effective date, not from enrollment date.

---

### 8. T65-05 -- Plan Comparison Prep

**Trigger:** 5 months before 65th birthday.

**Phase:** Planning

**Client Profile:** Client is aware of the timeline. Data is in hand. RPI is now actively building the plan comparison.

**Psychology:** The client needs to know the analysis is happening. "We're building your comparison" creates anticipation and reinforces that RPI is doing the work proactively. The client should feel like the heavy lifting is being handled.

**Key Message:** "We're building your personalized plan comparison right now. We're running your prescriptions, providers, pharmacies, and healthcare history against every available plan in your area. When we're done, you'll see exactly what each option looks like for YOUR situation -- not generic brochures, your actual numbers."

**Risk/Urgency:** The comparison needs to be complete before the IEP window opens (3 months before birthday). Building it now ensures there is time for questions, revisions, and confident decision-making.

**Agent Coaching:**
- Reinforce the data-driven approach: "This isn't a brochure comparison. This is YOUR data against every plan available."
- Set expectations for the next touch: "We'll have your full comparison ready to walk through at our next conversation."
- If any data gaps remain (authorization not complete, P3 outdated), escalate now: "We're missing [X] -- can we get that filled in so the comparison is complete?"
- For Path 1 clients: "We're still building your comparison even though you're deferring. That way, if anything changes with your employment, we can move immediately."

**Compliance Notes:**
- Plan comparisons must use current CMS and carrier data for the upcoming plan year.
- Do not share preliminary or incomplete comparisons. Wait until the analysis is thorough.
- All comparison data must be sourced from verified systems.

---

### 9. T65-04 -- Recommendation Build

**Trigger:** 4 months before 65th birthday.

**Phase:** Planning

**Client Profile:** Comparison is built. RPI is preparing the recommendation. This is the last Planning phase touch before the Urgent phase begins.

**Psychology:** The client is about to receive a recommendation. This touch prepares them for that conversation. "We've done the analysis. Here's what we're going to walk you through." Building anticipation for the decision, not the sale.

**Key Message:** "Your comparison is complete. We've analyzed every available option against your actual healthcare data. At our next conversation, we're going to walk you through the top options and our recommendation. No surprises -- just clear data and a straightforward recommendation."

**Risk/Urgency:** The IEP window opens next month. The recommendation needs to be delivered and discussed before the window opens so the client can enroll in the first month if they choose. This is the "get ready" touch.

**Agent Coaching:**
- Schedule the T65-03 conversation (IEP window opens). This is the decision meeting.
- Confirm the client's situation has not changed since T65-07 situation assessment.
- For Path 2 clients: "Your window opens next month. We'll be ready."
- For Path 1 clients: "Your comparison is ready if you need it. If your employment situation stays the same, you're all set to defer. But we have a plan either way."
- Prepare the full recommendation package: top 2-3 options, cost projections, network analysis, formulary coverage.

**Compliance Notes:**
- Recommendation must be documented with supporting data rationale.
- If recommending MAPD: SOA timing must be planned for the T65-03 conversation.
- Do not deliver the recommendation via text or email. This should be a live conversation.

---

### 10. T65-03 -- IEP Window Opens

**Trigger:** 3 months before 65th birthday. The IEP window is officially open. Enrollment can begin.

**Phase:** Urgent

**Client Profile:** Educated, data-complete client whose IEP window has just opened. If enrolled this month, Part B coverage begins the 1st of the birthday month with no gap.

**Psychology:** The window is open. The tone shifts from "we're getting ready" to "we're ready -- let's do this." Still calm, still confident, but with a clear acknowledgment that the window is real. "This is the window. Here's the recommendation. Let's make your decision."

**Key Message:** "Your enrollment window is open. We've done the work -- your data is analyzed, your options are clear, and we have a recommendation. Let's connect and make your decision so your coverage starts the day it needs to."

**Risk/Urgency:** Enrolling in the first 3 months of the IEP ensures Part B starts the birthday month with no gap. Waiting past the birthday month delays coverage start and can create a gap. The Medigap guaranteed issue clock starts ticking from Part B effective date. Early enrollment maximizes flexibility.

**Agent Coaching:**
- This is the decision meeting. Come prepared with the full recommendation.
- Walk through the top 2-3 options. Explain why the recommendation is the recommendation.
- Let the client decide. Present data, answer questions, do not pressure.
- If the client wants to enroll today: execute. Handle Part B enrollment, plan selection, and any supplemental coverage.
- If the client wants more time: "Your window is open for 7 months, but enrolling in the first 3 months means your coverage starts on your birthday month with no gap. Take the time you need -- we're here."
- For Path 1 clients: confirm deferral is still appropriate. If employment has changed, pivot to enrollment immediately.
- SOA must be completed before discussing specific plan details.

**Compliance Notes:**
- SOA required before discussing specific Medicare Advantage or Part D plans.
- Enrollment must be submitted through proper carrier channels.
- Document the recommendation, the client's decision, and the enrollment date.
- If the client defers (Path 1), document the employer coverage verification and deferral decision.

---

### 11. T65-02 -- Enrollment Push

**Trigger:** 2 months before 65th birthday. Second month of the IEP window.

**Phase:** Urgent

**Client Profile:** Client who has not yet enrolled despite the window being open. May have been busy, uncertain, or simply procrastinating. Still in the optimal enrollment window (coverage starts birthday month if enrolled this month).

**Psychology:** Gentle persistence. The client is not being pressured -- they are being reminded that the window is open and that enrolling now means seamless coverage. "We're still here. Your window is still open. Let's get this done."

**Key Message:** "Just checking in -- your enrollment window is open and everything is ready on our end. Enrolling this month means your coverage starts right on time with no gap. Whenever you're ready, we can have this done in one conversation."

**Risk/Urgency:** This is the second of three optimal enrollment months. Enrolling this month still guarantees Part B starts the birthday month. Waiting past this month increases the risk of a coverage gap. The message is factual, not alarmist.

**Agent Coaching:**
- If the client is stalling due to confusion: "What questions do you have? Let's clear them up."
- If the client is stalling due to busyness: "This takes one conversation. We've done all the prep work -- you just need to make the decision and we handle the rest."
- If the client is stalling due to uncertainty about the recommendation: "Let's revisit the comparison. I want you to feel 100% confident."
- Do not nag. Two touches (T65-03 and T65-02) is enough if the client is unresponsive. They know the window is open.
- For Path 1 clients who may have had an employment change: "Quick check -- anything changed with your work situation?"

**Compliance Notes:**
- Same as T65-03. SOA required if not already completed.
- Do not overstate consequences of waiting one more month. Be factual.
- Document all outreach attempts and client responses.

---

### 12. T65-01 -- Final Pre-Birthday

**Trigger:** 1 month before 65th birthday. Last month of the optimal enrollment window.

**Phase:** Urgent

**Client Profile:** Client who has still not enrolled. This is the last month where enrollment guarantees Part B starts the birthday month. After this, coverage is delayed.

**Psychology:** This is the firmest touch in the sequence -- but still not aggressive. The message: "This is the last month to enroll and have coverage start on time. After this, there's a delay. We want to make sure you're not caught in a gap."

**Key Message:** "Your birthday is next month. If we get your enrollment done this month, your coverage starts right on your birthday with no gap. After this month, there's a delay before coverage kicks in. We don't want you caught without coverage -- let's get this wrapped up."

**Risk/Urgency:** Real and immediate. Enrolling during the birthday month or later results in delayed Part B coverage. The client could have a period with no Medicare coverage. Additionally, the Medigap guaranteed issue period is tied to Part B effective date -- a delayed Part B means a delayed (and shorter effective) Medigap window.

**Agent Coaching:**
- Be direct but not pushy: "This is the last month for on-time coverage. I want to make sure you know that."
- If the client is ready: enroll immediately.
- If the client is still hesitating: "What's holding you back? Let's talk through it."
- If the client has decided to defer (Path 1 confirmed): "Perfect. You're all set. We've documented your employer coverage and we'll be here when you're ready."
- If the client is simply unresponsive: document the outreach. The IEP window remains open for 3 more months after the birthday, but with delayed coverage.

**Compliance Notes:**
- Accurately represent the coverage delay for post-birthday enrollment.
- Do not overstate the delay -- it is real but varies by enrollment month.
- Document all attempts to contact the client.
- If the client is unresponsive and has no employer coverage, note the case for escalation.

---

### 13. T65-00 -- Birthday Month

**Trigger:** The client's 65th birthday month.

**Phase:** Action/Follow-up

**Client Profile:** Two populations: (1) Clients who enrolled in months 1-3 -- their Part B is now active, coverage is live, celebrate. (2) Clients who have not yet enrolled -- still within the IEP window but coverage will be delayed.

**Psychology:** For enrolled clients: "Happy birthday -- you're covered." For non-enrolled clients: "Happy birthday -- your window is still open, but coverage will be delayed. Let's get this done."

**Key Message (enrolled):** "Happy birthday! Your Medicare coverage is active. Everything is set up and working. We're going to check in over the next couple months to make sure everything is running smoothly. Welcome to the team."

**Key Message (not enrolled):** "Happy birthday! Your enrollment window is still open for 3 more months, but the sooner we get this done, the sooner your coverage starts. Let's connect and get you set up."

**Risk/Urgency:** For enrolled clients: none. For non-enrolled Path 2 clients: every month of delay is a month of delayed coverage start. The permanent late penalties have not kicked in yet (still within IEP), but the coverage gap widens.

**Agent Coaching:**
- For enrolled clients: this is a celebration and a transition touch. "You're covered. We're going to be managing your plan going forward -- annual reviews, benefit checks, the whole program."
- For non-enrolled clients: be warm but clear about the delay. "You're still in your window -- but coverage won't start the day you enroll. The sooner we do this, the shorter the gap."
- For Path 1 (deferred) clients: "Happy birthday! Your employer coverage has you covered. We've got everything documented and we're here when you're ready to transition."
- Begin transitioning the client mindset from "T65 prospect" to "PSM-managed client."

**Compliance Notes:**
- Enrolled clients: verify enrollment confirmation from carrier.
- Non-enrolled clients: document continued outreach.
- Do not imply that missing the optimal window is catastrophic -- the IEP extends 3 more months. Be factual about the delay.

---

### 14. T65+1 -- Post-Enrollment Check

**Trigger:** 1 month after 65th birthday.

**Phase:** Action/Follow-up

**Client Profile:** Newly enrolled Medicare client in their first month of coverage (or second month if they enrolled early). Experiencing Medicare for the first time -- pharmacy visits, doctor visits, understanding their benefits.

**Psychology:** New Medicare enrollees are anxious. They are using a new system for the first time. "Is my doctor really in network? Will my medications really be covered? What do I do at the pharmacy?" This touch catches problems early and builds confidence.

**Key Message:** "It's been about a month since your Medicare coverage kicked in. How's it going? Any surprises at the pharmacy or the doctor's office? If anything feels off, we want to know now while we can fix it."

**Risk/Urgency:** First-month issues -- pharmacy rejections, prior authorization requirements, network confusion -- are common and fixable if caught early. If the client is enrolled in MAPD and something is materially wrong, the OEP window (Jan-Mar) may be available for adjustment. For Medigap enrollees, the guaranteed issue window is ticking.

**Agent Coaching:**
- Ask specific questions: "How was your first pharmacy visit? Any copay surprises? Is your primary doctor showing in network?"
- If issues are found: act immediately. Contact the carrier, resolve the issue, report back to the client.
- If everything is smooth: "Great -- that's exactly what we like to hear. We'll check in once more next month and then you're fully in our ongoing service program."
- Remind the client about the Medigap guaranteed issue window if applicable: "You have 6 months from your Part B effective date to enroll in supplemental coverage with guaranteed acceptance."
- Begin documenting the client for PSM onboarding.

**Compliance Notes:**
- Document any issues reported and their resolution.
- If the client needs a plan change, verify eligibility (SEP, OEP, or other qualifying event).
- Medigap guaranteed issue dates must be accurately tracked and communicated.

---

### 15. T65+2 -- Coverage Verification

**Trigger:** 2 months after 65th birthday. Final T65 campaign touch.

**Phase:** Action/Follow-up

**Client Profile:** Client who has been on Medicare coverage for approximately 2-3 months. Should be settled into their plan. This is the formal handoff from the T65 engine to the ongoing PSM service model.

**Psychology:** Closure and transition. The 15-month journey is complete. The client needs to feel that the process had a beginning, a middle, and an end -- and that the end is not RPI walking away. It is RPI shifting into ongoing management mode.

**Key Message:** "You're officially settled in. Your coverage is verified, your providers and prescriptions are confirmed, and everything is running the way it should. From here, we shift into our ongoing service program -- annual plan reviews, benefit checks, and proactive monitoring. You don't have to think about this. We're on it."

**Risk/Urgency:** The Medigap guaranteed issue window is still open (6 months from Part B effective date). If the client has not enrolled in Medigap and should, this is a critical reminder. Otherwise, no urgency -- this is a wrap-up touch.

**Agent Coaching:**
- Confirm everything is working: prescriptions, providers, pharmacy, copays, benefits.
- If Medigap is relevant and not yet in place: "You have [X] months left in your guaranteed acceptance window for supplemental coverage. Let's talk about whether that makes sense for you."
- Introduce the PSM model: "From here, you're in our ongoing service program. We review your plan every year before AEP, monitor for any changes that affect you, and proactively reach out if something needs attention. You don't have to remember to call us -- we call you."
- Thank the client for trusting RPI with the process.
- Formally transition the client record from T65 pipeline to PSM management.

**Compliance Notes:**
- Verify all enrollment records are complete and accurate.
- Confirm Medigap guaranteed issue deadline is documented if applicable.
- Document the transition from T65 to PSM in the client record.
- If the client did not enroll (Path 1 deferral), document the deferral status and set a monitoring trigger for employment status changes.

---

## Cross-Campaign Flow

### T65 Journey Arc

```
T65-12 (First Introduction)
    "You might not even need to worry about it"
        |
T65-11 (Medicare Basics)
    Part A, Part B, Part D -- the foundation
        |
T65-10 (Two Paths)
    Employer coverage? --> Path 1 (defer) or Path 2 (enroll)
        |
T65-09 (Authorization Introduction)
    Connect your healthcare data
        |
T65-08 (Data Gathering Begins)
    Pulling prescriptions, providers, pharmacies, utilization
        |
T65-07 (Situation Assessment)
    "Here's where you stand"
        |
T65-06 (IEP Window Preview)
    The timeline: 7-month window, when and how it works
        |
T65-05 (Plan Comparison Prep)
    "We're building your comparison right now"
        |
T65-04 (Recommendation Build)
    Comparison complete, recommendation ready
        |
T65-03 (IEP Window Opens)
    "Let's do this" -- enrollment begins
        |
T65-02 (Enrollment Push)
    Gentle persistence for non-enrolled
        |
T65-01 (Final Pre-Birthday)
    Last optimal enrollment month
        |
T65-00 (Birthday Month)
    Celebrate enrolled / Urgency for non-enrolled
        |
T65+1 (Post-Enrollment Check)
    First-month experience check
        |
T65+2 (Coverage Verification)
    Final check, transition to PSM
```

### Path Branching

```
T65-10 determines the path:

Path 1 (Employer Coverage):
    T65-09 through T65-07: data gathering continues (for future readiness)
    T65-06 through T65-01: monitoring, confirm deferral each month
    T65-00: Happy birthday, deferral confirmed
    T65+1, T65+2: Set monitoring trigger for employment change
    --> Exits T65 engine, enters monitoring mode
    --> Re-enters at T65-03 equivalent when employment status changes

Path 2 (Needs Medicare):
    Full 15-campaign sequence as documented above
    --> Exits T65 engine at T65+2, enters PSM service model
```

### T65 to PSM Handoff

```
T65+2 (Coverage Verification)
        |
        v
PSM-AEP-REV (first AEP cycle after enrollment)
    Client is now a PSM-managed Medicare client.
    Annual reviews, benefit checks, SEP monitoring.
```

### Key Flow Rules

- **T65-10 determines the path.** Every subsequent campaign adapts based on whether the client is Path 1 (defer) or Path 2 (enroll).
- **Authorization starts at T65-09.** Earlier is better, but do not push before the client understands why it matters.
- **IEP month 1-3 enrollment is the target.** Coverage starts birthday month with no gap. Everything in the Planning phase works toward this.
- **T65+2 is the formal handoff.** The client exits the T65 engine and enters PSM management. No gap in service.
- **Path 1 clients re-enter.** When employer coverage ends, the client re-enters the T65-equivalent flow at the urgency level appropriate to their timeline (SEP for loss of employer coverage).

---

## Quick Reference Matrix

| # | Campaign ID | Phase | Months to 65 | Path 1 (Defer) | Path 2 (Enroll) | Key Action |
|---|-------------|-------|---------------|-----------------|------------------|------------|
| 1 | T65-12 | Education | -12 | Yes | Yes | Introduce RPI, set tone |
| 2 | T65-11 | Education | -11 | Yes | Yes | Medicare basics |
| 3 | T65-10 | Education | -10 | **Determines path** | **Determines path** | Employer coverage assessment |
| 4 | T65-09 | Education | -9 | Yes | Yes | Authorization introduction |
| 5 | T65-08 | Education | -8 | Yes | Yes | Data gathering |
| 6 | T65-07 | Education | -7 | Yes | Yes | Situation assessment |
| 7 | T65-06 | Planning | -6 | Monitor | IEP window preview |
| 8 | T65-05 | Planning | -5 | Monitor | Plan comparison prep |
| 9 | T65-04 | Planning | -4 | Monitor | Recommendation delivery |
| 10 | T65-03 | Urgent | -3 | Confirm deferral | **IEP opens -- enroll** |
| 11 | T65-02 | Urgent | -2 | Confirm deferral | Enrollment push |
| 12 | T65-01 | Urgent | -1 | Confirm deferral | Final optimal month |
| 13 | T65-00 | Action | 0 | Happy birthday (deferred) | Birthday month enrollment |
| 14 | T65+1 | Follow-up | +1 | Set monitoring trigger | Post-enrollment check |
| 15 | T65+2 | Follow-up | +2 | Exit to monitoring | Exit to PSM |

---

*We're Your People.(TM)*
