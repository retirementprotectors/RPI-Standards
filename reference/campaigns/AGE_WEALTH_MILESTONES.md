# AGE -- Wealth Milestone Engine

> Knowledge document for the AGE campaign engine. 9 age-triggered campaigns, all WEALTH division, PROSPER pillar.
> All content approved by JDM on 2026-02-16.

---

## Engine Overview

**AGE = Age-Triggered Wealth Milestones.** Campaigns that fire when a client reaches a specific age where a tax rule, regulatory threshold, or financial milestone unlocks. Unlike PSM (account-triggered) or T65 (birthday countdown), AGE fires at the exact age where the rules of the game change.

| Metric | Value |
|--------|-------|
| **Total Campaigns** | 9 |
| **Division** | WEALTH (all 9) |
| **Pillar** | PROSPER |
| **Trigger Type** | Age-based (client DOB + milestone age) |
| **Channels per campaign** | Email, Text/SMS, Voicemail Script, USPS Mailer |
| **Execution path** | C3 (campaign engine) --> PRODASH (delivery) --> 4 channels |

### Campaign Inventory

| # | Campaign ID | Name | Milestone Age | Trigger Type |
|---|-------------|------|---------------|--------------|
| 1 | AGE-50 | Catch-Up Contributions Begin | 50 | IRS contribution limit change |
| 2 | AGE-55 | Rule of 55 (Penalty-Free 401k) | 55 | Employer plan access rule |
| 3 | AGE-59 | 59 1/2 Penalty-Free IRA Access | 59 | Early withdrawal penalty elimination |
| 4 | AGE-62 | First Social Security Claim Year | 62 | SS eligibility |
| 5 | AGE-66 | Full Retirement Age (Born 1943-1954) | 66 | FRA milestone |
| 6 | AGE-67 | Full Retirement Age (Born 1960+) | 67 | FRA milestone |
| 7 | AGE-70 | Maximum Social Security Benefit | 70 | Delayed credits cap |
| 8 | AGE-73 | Required Minimum Distributions Begin | 73 | SECURE 2.0 RMD start |
| 9 | AGE-75 | SECURE 2.0 RMD (Born 1960+) | 75 | SECURE 2.0 RMD start |

---

## AGE Philosophy

**"We're Your People."** The AGE engine is how RPI proves that promise on the wealth side. Every campaign is anchored to a real moment where the tax code, Social Security rules, or retirement regulations change for the client -- and the client almost certainly does not know it happened. AGE campaigns make RPI the advisor who shows up before the milestone, explains what changed, and positions the client to take advantage.

### Core Principles

1. **Commission-based model.** RPI is compensated by carriers. The client never pays RPI for these services. Content must NEVER imply the client is paying for anything. Never use the word "free" -- that implies there could be a cost. There is not.

2. **Education-forward.** Every campaign leads with the rule -- what changed, why it matters, and what the client's options are. The client decides. RPI presents the facts and the math.

3. **Age-precise.** Each milestone fires at a specific age because that is when the IRS, SSA, or federal law says something changes. The campaigns are not arbitrary check-ins -- they are timed to the exact moment a rule unlocks or a penalty disappears.

4. **Proactive, not reactive.** RPI reaches out BEFORE the milestone hits, not after. The client should hear about catch-up contributions before they turn 50, not after they have missed a year. The tone is always "we're already on it" -- never "you should have called us."

5. **Full-picture advisory.** Every AGE milestone is a doorway to a broader Health + Wealth + Legacy conversation. Turning 62 is not just about Social Security -- it is about income planning, Medicare timing, life insurance review, and legacy positioning. AGE campaigns open the door; the agent walks the client through the whole house.

---

## Tone Rules

These rules apply to ALL 9 campaigns, ALL channels (email, text/SMS, VM, USPS).

| Rule | Detail |
|------|--------|
| **No "free" language** | Commission-based. There is no cost to imply the absence of. |
| **No urgency/sales mechanics** | No "15 minutes," "today only," "Reply YES," countdown timers. This is education, not sales. |
| **No technical jargon without explanation** | No "IRC Section 414(v)," "SECURE 2.0 Section 107." Cite the rule in plain language first, reference the legislation only in compliance notes. |
| **Commission transparency** | Never mention commission. Never imply RPI charges the client. The service just exists because "this is what we do." |
| **Always personalize** | Every client-facing touch must include `{FirstName}` and age-specific context at minimum. |
| **No sales language** | No "opportunity of a lifetime," "act now," "don't miss out." |
| **Agent as educator** | The agent is positioned as a knowledgeable advisor who explains rules and options, not a salesperson pushing products. |
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
| `{MilestoneAge}` | The age milestone being reached |
| `{MilestoneBirthday}` | The date the client hits the milestone age |
| `{Carrier}` | Insurance/annuity carrier (if applicable) |
| `{ProductName}` | Specific product (if applicable) |

---

## Cross-Campaign Flow

### Accumulation Phase (50-59)

```
AGE-50 (Catch-Up Contributions)
    IRS allows extra savings starting at 50.
    $7,500/yr to 401(k), $1,000/yr to IRA.
        |
        v
AGE-55 (Rule of 55)
    Separated from employer at 55+?
    Penalty-free access to THAT employer's 401(k).
    CRITICAL: Do NOT roll to IRA before understanding this rule.
        |
        v
AGE-59 (59 1/2 Penalty-Free Access)
    10% early withdrawal penalty eliminated on ALL retirement accounts.
    Full flexibility to reposition, consolidate, access.
```

### Social Security Decision Sequence (62-70)

```
AGE-62 (First SS Claim Year)
    Eligible to file -- permanently reduced benefit (~25-30% less than FRA).
    Most consequential financial decision most clients make.
        |
        +---> AGE-66 (FRA for born 1943-1954)
        |       100% benefit. Earnings test eliminated.
        |       8%/year delayed credits available (up to 32% boost).
        |
        +---> AGE-67 (FRA for born 1960+)
        |       100% benefit. Earnings test eliminated.
        |       8%/year delayed credits available (up to 24% boost).
        |
        v
AGE-70 (Maximum SS Benefit)
    Delayed credits stop. No benefit to waiting past 70.
    124-132% of FRA amount depending on birth year.
    File immediately. Coordinate income plan.
```

### Distribution Phase (73-75)

```
AGE-73 (RMD Begins -- SECURE 2.0)
    Mandatory distributions from traditional IRA, 401(k), 403(b).
    25% penalty on missed amounts. First-year double-RMD trap.
    Strategic sequencing: which accounts, what order, tax bracket management.
        |
        v
AGE-75 (RMD Begins -- Born 1960+)
    SECURE 2.0 pushes RMD start to 75 for this cohort.
    Two extra years of tax-deferred growth.
    Larger balances = larger mandatory distributions = bigger tax hit.
    Roth conversion window BEFORE RMDs start is critical.
```

### Key Flow Rules

- **AGE-50 through AGE-59 are accumulation/access milestones.** Each one unlocks a new capability the client did not have before. The campaigns build on each other.
- **AGE-62 through AGE-70 are a single decision sequence.** Filing for Social Security at 62 vs. 67 vs. 70 is one interconnected decision with hundreds of thousands of dollars at stake. The campaigns should reference each other.
- **AGE-73 and AGE-75 are mutually exclusive** based on birth year. A client gets one or the other, never both.
- **Every AGE campaign is a full Health + Wealth + Legacy touchpoint.** The age milestone is the door-opener; the conversation covers everything.
- **AGE-62 triggers the Medicare clock.** The T65 engine picks up at 64 with the Medicare birthday countdown. AGE-62 is where the first mention of Medicare timing belongs.

---

## Campaign Details

---

### 1. AGE-50 -- Catch-Up Contributions Begin

**Trigger:** Client approaching or turning 50. IRS allows additional retirement contributions starting at age 50.

**Division:** WEALTH

**Client Profile:** Working client with access to a 401(k), 403(b), or IRA. May or may not be maximizing current contributions. Likely in peak earning years. May have children approaching or in college. Retirement feels distant but the math is starting to matter.

**Psychology:** Most people do not know the IRS contribution limits change at 50. They have been saving the same amounts for years and assume the rules are the same. The core insight: the government just gave you a raise on your retirement savings capacity, and most people never use it. Over 15 years (50 to 65), catch-up contributions alone can add $125,000+ in additional tax-advantaged savings.

**Key Message:** "You just turned 50, and the IRS just changed the rules in your favor. Starting now, you can put an extra $7,500 per year into your 401(k) and an extra $1,000 per year into your IRA. Over the next 15 years, that is over $125,000 in additional tax-advantaged savings. Most people have no idea this exists."

**Risk/Urgency:** Every year the client does not use catch-up contributions is a year of lost tax-advantaged savings capacity that cannot be recovered. The contribution window is annual -- once a calendar year passes, that year's catch-up allowance is gone. There is no backfill. The math compounds: starting at 50 vs. 55 is a $37,500+ difference in contribution capacity alone, before any growth.

**Agent Coaching:**
- Lead with the rule change, not the product. "The IRS changed the rules for you at 50."
- Make the math tangible: "$7,500 extra per year for 15 years is $112,500 in 401(k) alone. Add IRA catch-ups and you're over $125,000 -- before any growth."
- Ask about current contributions: "Are you maxing out your 401(k)? If not, let's start there."
- If the client is not contributing at all, catch-up contributions are secondary -- start with base contribution strategy.
- Connect to the bigger picture: "This is the start of the 15-year runway to retirement. The decisions you make now set the trajectory."
- Do not overwhelm with tax code details. Keep it simple: "You can save more now. Let's figure out how much."

**Compliance Notes:**
- IRS catch-up contribution limits are subject to annual adjustment. Cite current-year limits accurately.
- Catch-up contributions apply to 401(k), 403(b), SIMPLE IRA, and traditional/Roth IRA with different limits for each. Be specific to the client's account types.
- Tax implications vary by account type (pre-tax vs. Roth). Always refer to client's tax advisor for specific tax advice.
- RPI does not manage 401(k) plans directly. Advisory only on contribution strategy.

**Cross-Sell Opportunities:**
- **Annuity products:** If the client has maximized tax-advantaged accounts, excess savings can go into fixed index annuities or MYGAs for tax-deferred growth.
- **Life insurance review:** Age 50 is a natural checkpoint for life insurance adequacy. Premiums increase with age -- locking in coverage now is strategic.
- **Full financial review:** "Now that the savings rules have changed, let's make sure your whole picture is aligned -- retirement accounts, insurance, legacy planning."

---

### 2. AGE-55 -- Rule of 55 (Penalty-Free 401k Access)

**Trigger:** Client approaching or turning 55. The "Rule of 55" allows penalty-free access to an employer 401(k) if the client has separated from that employer at age 55 or older.

**Division:** WEALTH

**Client Profile:** Client at or near 55 who may be considering early retirement, career change, or has already separated from an employer. May have multiple retirement accounts across various former employers. Likely does not know the Rule of 55 exists.

**Psychology:** The default assumption is that retirement money is locked until 59 1/2. Period. Most financial advisors do not mention the Rule of 55 because it only applies to the specific employer plan where the separation occurred. The client needs to know: if you leave your job at 55 or later, you can access THAT employer's 401(k) without the 10% penalty. This is not general knowledge. And the biggest mistake people make is rolling that 401(k) into an IRA before they understand this rule -- because once it is in the IRA, the penalty-free access disappears until 59 1/2.

**Key Message:** "There is a rule most people never hear about called the Rule of 55. If you separate from your employer at age 55 or older, you can access that employer's 401(k) without the 10% early withdrawal penalty. But there is a catch -- it only applies to the plan with that specific employer. And if you roll it into an IRA before you know this, you lose the penalty-free access until 59 1/2."

**Risk/Urgency:** The risk is not the rule itself -- it is what the client does before they know the rule exists. Rolling a 401(k) into an IRA is standard advice, and in most cases it is correct. But for a client who separated from an employer at 55+, rolling that specific 401(k) into an IRA locks out penalty-free access for up to 4 1/2 years. Once the rollover is done, it cannot be undone. This is a one-way door. The client needs to understand the rule BEFORE making the rollover decision.

**Agent Coaching:**
- This is one of the most valuable pieces of information RPI can deliver. Most advisors miss it or do not mention it.
- Lead with the rule: "Did you know that if you leave your employer at 55 or older, you can access that 401(k) without penalty?"
- Immediately clarify the limitation: "It only applies to the plan with the employer you separated from. Not IRAs, not other 401(k)s."
- Warn about the rollover trap: "If someone tells you to roll it into an IRA, make sure you understand what you're giving up first."
- Ask about employment status: "Are you still with your current employer? Thinking about a change?"
- If the client already rolled: do not panic them. "That's already done. The good news is 59 1/2 is not far away, and we can plan around it."
- Position RPI as the advisor who knows the rules others miss.

**Compliance Notes:**
- Rule of 55 applies to qualified employer plans (401(k), 403(b)) where separation occurred in or after the year the participant turns 55.
- Does NOT apply to IRAs. Does NOT apply to plans from previous employers (only the employer from which the client separated).
- Some plans have specific distribution rules. Client should verify with their plan administrator.
- Tax implications: distributions are still subject to ordinary income tax. Refer to client's tax advisor.
- SECURE 2.0 extended a similar rule to age 50 for certain public safety workers. Note if applicable.

**Cross-Sell Opportunities:**
- **Annuity repositioning:** If the client accesses 401(k) funds, a portion may be appropriate for a fixed index annuity or MYGA for guaranteed income or growth.
- **Income planning:** Early access to retirement funds demands an income strategy. "Now that you can access this money, let's make sure you don't outlive it."
- **Life insurance review:** Career transition is a natural moment to review life insurance needs. Employer-provided coverage may be ending.
- **Medicare planning:** If the client is retiring early, health insurance becomes a critical gap. Bridge the conversation to health coverage options.

---

### 3. AGE-59 -- 59 1/2 Penalty-Free IRA Access

**Trigger:** Client approaching or turning 59 1/2. The 10% early withdrawal penalty on ALL retirement accounts (IRA, 401(k), 403(b)) is eliminated.

**Division:** WEALTH

**Client Profile:** Client at or near 59 1/2 with retirement accounts that have been accumulating for years or decades. May have accounts scattered across multiple custodians, former employer plans, and IRAs. Allocations may be stale -- set once and never revisited. The client now has complete flexibility but may not realize the penalty is gone or what that means for their options.

**Psychology:** For 30+ years, the client has been told "don't touch your retirement money or you'll get hit with a penalty." At 59 1/2, that penalty disappears. The mental model shifts from "locked up" to "accessible." But the risk is inertia -- the client has been in "don't touch" mode for so long that they keep doing nothing even when the rules have changed. Accounts stay scattered. Allocations stay stale. Opportunities to consolidate, reposition, and optimize go unused.

**Key Message:** "You just hit 59 1/2, and the 10% early withdrawal penalty is officially behind you on ALL of your retirement accounts -- IRAs, 401(k)s, everything. You now have complete flexibility to consolidate, reposition, or access your money without penalties. The question is: are your accounts positioned the way they should be, or are they still set up the way you left them years ago?"

**Risk/Urgency:** The penalty being gone is not the event -- the event is what the client does with the flexibility. Accounts that have been scattered and unmanaged for years may have outdated allocations, redundant holdings, unnecessary fees, or suboptimal structures. In-service withdrawals from employer plans may now be available. The client's proximity to retirement makes every year of optimization matter more. The risk is continued inertia -- doing nothing when the rules have finally changed in the client's favor.

**Agent Coaching:**
- Frame 59 1/2 as a milestone, not just a birthday. "This is a real turning point. The penalty that has been hanging over your retirement accounts for 30 years is gone."
- Ask about account inventory: "How many retirement accounts do you have? When's the last time you looked at all of them together?"
- Suggest consolidation: "Most people have accounts scattered across three or four places. Now that there's no penalty, we can bring everything together and make sure it's all working toward the same goal."
- Check for in-service withdrawal eligibility: "If you're still working, your employer plan may now allow you to move money out while you're still employed."
- Connect to the 5-year runway to Social Security: "You're 8 years from 67 and 11 years from 70. The decisions you make now with these accounts directly impact your income in retirement."
- Do not push withdrawals. The message is optimization, not access for the sake of access.

**Compliance Notes:**
- 59 1/2 is the IRS age at which the 10% additional tax on early distributions no longer applies to most retirement accounts.
- Distributions are still subject to ordinary income tax. Refer to client's tax advisor.
- Roth IRA earnings are tax-free only if the account has been open for at least 5 years AND the owner is 59 1/2 or older (the "5-year rule").
- In-service withdrawal eligibility varies by employer plan. Client should verify with their plan administrator.
- Any repositioning recommendation requires suitability analysis. 1035 exchange rules apply to insurance products.

**Cross-Sell Opportunities:**
- **Annuity products:** Consolidation conversation naturally leads to annuity options -- FIA for growth with downside protection, MYGA for guaranteed rates, income riders for retirement income planning.
- **Life insurance review:** "While we're consolidating your retirement accounts, let's make sure your life insurance is still sized correctly for where you are now."
- **Roth conversion strategy:** The window between 59 1/2 and RMD age is prime for Roth conversions. "We should talk about converting some of these funds to Roth before RMDs force your hand."
- **Income planning:** "You're in the home stretch. Let's build a plan for how these accounts turn into income."

---

### 4. AGE-62 -- First Social Security Claim Year

**Trigger:** Client approaching or turning 62. First year of eligibility to file for Social Security retirement benefits.

**Division:** WEALTH

**Client Profile:** Client at or near 62. May still be working, may be retired, may be planning retirement. Has been paying into Social Security for decades and is now eligible to start collecting. May have a spouse with their own SS benefit or who is dependent on the client's record. This is likely the single most consequential financial decision the client will make -- and most people make it without understanding the full picture.

**Psychology:** The pull to file at 62 is enormous. "I've been paying in for 40 years -- I want my money." The problem: filing at 62 means a permanently reduced benefit -- roughly 25-30% less than the Full Retirement Age amount, depending on birth year. And "permanently" means permanently. It does not go back up later. The decision cannot be undone after the first 12 months. Most clients do not understand that waiting to 67 or 70 could mean hundreds of thousands of dollars more over their lifetime. Filing at 62 vs. 70 is not an 8-year difference -- it is a lifetime income difference that can exceed $200,000+.

**Key Message:** "You're about to become eligible for Social Security, and this may be the single most important financial decision you'll make. Filing at 62 means a permanently reduced benefit -- roughly 25-30% less than your full amount. Filing at 67 gets you 100%. Waiting to 70 gets you 124-132%. We're talking about hundreds of thousands of dollars over your lifetime. Let's run the numbers before you decide."

**Risk/Urgency:** Filing early is irreversible after 12 months. Once the decision is made, the client lives with that benefit amount for life (adjusted only by COLA). If the client files at 62 without understanding the trade-off, they may lock in a benefit that is $500-$1,000+ per month less than what they could have received. For a couple, the spousal coordination implications multiply the impact. This is not a "we can fix it later" situation. The urgency is education BEFORE the client files -- not pressure to file or not file.

**Agent Coaching:**
- This is the most important conversation in the AGE engine. Prepare thoroughly.
- Lead with the magnitude: "This decision is worth more than most people's entire retirement savings."
- Show the three scenarios: 62 vs. FRA (66 or 67) vs. 70. Use actual projected dollar amounts from the client's SSA statement if available.
- Explain permanence: "Whatever you choose is your number for life. It doesn't go back up."
- Address the "I want my money" impulse directly: "I understand that feeling. But let's look at the math first so you're making this decision with full information."
- Spousal coordination: "If you're married, this decision affects both of you. Your filing age impacts your spouse's survivor benefit."
- Ask about other income sources: "Do you have enough income from other sources to delay? If so, waiting may be significantly more valuable."
- If the client needs the money at 62, that is a valid decision. Help them understand what they are trading and plan accordingly.
- RPI does not file Social Security claims. Refer to SSA for the actual filing.

**Compliance Notes:**
- RPI does not file Social Security claims -- this is advisory only. Client must contact the Social Security Administration directly to file.
- Benefit reduction percentages are based on birth year and filing age. Use SSA's published reduction factors.
- The 12-month withdrawal rule: a client can withdraw their SS application within 12 months of filing and repay all benefits received. After 12 months, the decision is permanent.
- Spousal benefits are based on the higher earner's record. Coordination strategies vary by situation.
- Tax implications of SS benefits depend on total income. Refer to client's tax advisor.
- Never guarantee specific benefit amounts -- direct the client to their SSA statement (my Social Security account at ssa.gov).

**Cross-Sell Opportunities:**
- **Medicare planning (T65 handoff):** "Turning 62 means Medicare is just around the corner. The T65 engine will pick you up at 64, but we should start the conversation now."
- **Income planning:** If the client delays SS, they need income from other sources to bridge the gap. Annuity income riders, systematic withdrawals, and Roth conversions become relevant.
- **Life insurance review:** "If you're approaching retirement, let's make sure your life insurance is still doing what you need it to do."
- **Annuity repositioning:** "While we're planning your Social Security strategy, let's look at how your other retirement accounts fit into the income picture."
- **Legacy planning:** "Social Security is one piece. Let's make sure your full plan -- income, insurance, legacy -- is working together."

---

### 5. AGE-66 -- Full Retirement Age (Born 1943-1954)

**Trigger:** Client approaching or turning 66. Full Retirement Age (FRA) for individuals born between 1943 and 1954. Social Security benefit reaches 100% of the Primary Insurance Amount.

**Division:** WEALTH

**Client Profile:** Client born 1943-1954 reaching FRA. May have already filed for Social Security (reduced benefit at 62-65), may be filing now at FRA, or may be considering delaying to 70. If already collecting, the earnings test is about to be eliminated. If not yet collecting, the delayed credit calculation becomes the key decision.

**Psychology:** For clients who have been waiting, FRA feels like the finish line. "I made it -- time to file." For clients already collecting, FRA means the earnings test goes away and they can work without benefit reduction. The key insight for those who have not yet filed: FRA is not the finish line -- it is a choice point. Every year of delay from 66 to 70 adds 8% to the benefit. That is a 32% increase over 4 years, guaranteed by the federal government. No investment on earth offers a guaranteed 8% annual return. The question: can the client afford to wait?

**Key Message:** "You've reached your Full Retirement Age. Your Social Security benefit is now at 100%. But here's what most people don't realize: for every year you wait past 66, your benefit goes up 8%. Wait until 70 and your benefit is 132% of what it is today. That's a guaranteed increase backed by the federal government. The question is whether you can afford to wait -- and that's what we're here to help you figure out."

**Risk/Urgency:** For clients who have not yet filed, the decision is whether to take 100% now or earn 8% per year in delayed credits up to 70. This is not a "right or wrong" decision -- it depends on the client's health, other income sources, spousal situation, and financial needs. But the client must understand the trade-off to make an informed choice. For clients already collecting, FRA eliminates the earnings test -- they can now earn any amount without benefit reduction. This may change their work/retirement calculus.

**Agent Coaching:**
- If the client has not yet filed: "You're at 100% right now. The question is whether you can get more."
- Explain delayed credits simply: "8% per year. 32% total if you wait to 70. That's a government-guaranteed raise."
- Run the break-even analysis: "If you wait to 70, it takes about 12-13 years to recoup the payments you skipped. After that, you're ahead every month for life."
- Ask about health: "How's your health? If you're in good shape, waiting often wins the math."
- Ask about other income: "Can you cover expenses from other sources for the next 4 years? If so, the math strongly favors waiting."
- Spousal coordination: "Your filing decision affects your spouse's survivor benefit. If something happens to you, your spouse gets YOUR benefit amount. A higher benefit protects them."
- If the client wants to file now at FRA, that is a perfectly valid decision. Confirm they understand the trade-off and support the choice.
- For clients already collecting: "Good news -- the earnings test is gone. You can work as much as you want without any reduction in your Social Security benefit."

**Compliance Notes:**
- FRA of 66 applies to individuals born 1943-1954. Verify the client's birth year.
- Delayed retirement credits are 8% per year (2/3 of 1% per month) from FRA to age 70.
- The earnings test applies before FRA. At FRA, it is eliminated. In the year of FRA, a higher earnings limit applies for months before the birthday month.
- Spousal benefit coordination: the lower-earning spouse can claim up to 50% of the higher earner's FRA benefit. Survivor benefit equals the deceased spouse's actual benefit amount (including delayed credits if applicable).
- Tax implications of SS benefits depend on total income. Refer to client's tax advisor.
- RPI does not file SS claims. Advisory only. Refer to SSA.

**Cross-Sell Opportunities:**
- **Income planning:** If the client delays to 70, they need bridge income. Annuity income riders and systematic withdrawals from retirement accounts are directly relevant.
- **Annuity repositioning:** FRA is a natural moment to review all retirement assets. "Your Social Security decision affects how you should structure everything else."
- **Life insurance review:** "Your survivor benefit decision matters. Let's also make sure your life insurance is aligned."
- **Roth conversions:** The years between FRA and 70 (if delaying) can be prime Roth conversion years before RMDs start. "While your SS benefit is growing, we can use this window to convert some IRA funds to Roth."

---

### 6. AGE-67 -- Full Retirement Age (Born 1960+)

**Trigger:** Client approaching or turning 67. Full Retirement Age (FRA) for individuals born 1960 or later. Social Security benefit reaches 100% of the Primary Insurance Amount.

**Division:** WEALTH

**Client Profile:** Client born 1960 or later reaching FRA at 67. Same decision framework as AGE-66 but with one fewer year of delayed credits available (3 years to 70 instead of 4). May have already filed at 62-66 (reduced), may be filing now at FRA, or may be considering delay to 70.

**Psychology:** Identical to AGE-66 with one key difference: the delayed credit window is 3 years instead of 4. The 8% per year is the same, but the maximum boost is 24% instead of 32%. The message is the same -- "FRA is a choice point, not a finish line" -- but the math shifts slightly. Every year matters more when there are only 3 of them.

**Key Message:** "You've reached your Full Retirement Age. Your Social Security benefit is now at 100%. For every year you wait past 67, your benefit goes up 8%. Wait until 70 and your benefit is 124% of what it is today. Three years, 24% more income for life. That's the decision in front of you -- and we're here to help you make it with full information."

**Risk/Urgency:** Same as AGE-66. The decision is whether to take 100% now or earn delayed credits. The shorter window (3 years vs. 4) means the total potential increase is smaller, but 8% per year is still unmatched by any guaranteed investment. The break-even calculation shifts slightly earlier. Client's health, income needs, and spousal situation remain the key variables.

**Agent Coaching:**
- Same framework as AGE-66, adjusted for the 3-year window.
- Emphasize the per-year value: "8% per year for 3 years. 24% total. Still the best guaranteed return you'll find anywhere."
- Run the break-even: "Slightly shorter payback period than the 4-year window. If you're in good health, the math typically favors waiting."
- Spousal coordination remains critical. Same messaging as AGE-66.
- Earnings test elimination messaging is the same.
- If the client filed early (62-66), the benefit is permanently reduced. Acknowledge it and focus on optimizing everything else: "That decision is made. Let's make sure the rest of your plan is working as hard as possible."

**Compliance Notes:**
- FRA of 67 applies to individuals born 1960 or later. For birth years 1955-1959, FRA is between 66 and 67 (graduated by birth year). Verify the client's specific FRA.
- Delayed retirement credits are 8% per year from FRA to age 70 regardless of FRA.
- All other SS compliance notes from AGE-66 apply.
- RPI does not file SS claims. Advisory only. Refer to SSA.

**Cross-Sell Opportunities:**
- Same as AGE-66. Income planning, annuity repositioning, life insurance review, Roth conversions.
- The 3-year delay window may make bridge income planning slightly simpler -- smaller gap to fill.

---

### 7. AGE-70 -- Maximum Social Security Benefit

**Trigger:** Client approaching or turning 70. Delayed retirement credits stop accruing. No financial benefit to waiting past 70 to file for Social Security.

**Division:** WEALTH

**Client Profile:** Client who has delayed filing for Social Security, either intentionally or through inertia. Benefit has reached its maximum -- 124% (FRA=67) to 132% (FRA=66) of the Primary Insurance Amount. The only action is to file. Some clients may have forgotten or not realized they should file at 70. Others have been strategically waiting and this is the planned filing date.

**Psychology:** Two profiles: (1) The strategic delayer who planned this and is ready to file. Simple -- confirm the plan, execute the filing, and optimize the income structure. (2) The client who forgot, did not realize, or kept putting it off. For this client, every month past 70 is a month of benefits they have earned but are not collecting. There is no additional benefit to waiting. The message for both: "It's time. Your benefit is at its maximum. Let's file and build the income plan."

**Key Message:** "Your Social Security benefit has reached its maximum. Delayed credits stop at 70 -- there is no additional benefit to waiting even one more month. Your benefit is now 124-132% of your Full Retirement Age amount. It's time to file and make sure this income is coordinated with everything else in your financial picture."

**Risk/Urgency:** The risk is delay past 70. Every month the client waits past 70, they forfeit benefits they have earned. Social Security will pay up to 6 months of retroactive benefits for late filers over 70, but anything beyond that is lost permanently. The urgency is real and specific: file now. Additionally, the income from Social Security changes the client's tax picture, RMD strategy, and overall income plan. All of these need to be coordinated.

**Agent Coaching:**
- For the strategic delayer: "Congratulations -- you played the long game and it paid off. Let's get you filed and get your income flowing."
- For the late filer: "Let's get this filed right away. Social Security can pay up to 6 months retroactively, but beyond that, those benefits are gone."
- Focus shifts to income coordination: "Now that Social Security is starting, we need to make sure your other income sources -- retirement accounts, annuities, any pensions -- are working together and not pushing you into a higher tax bracket."
- Spousal implications: "Your filing now affects your spouse's survivor benefit. Let's make sure the coordination is right."
- RMD planning: "If you're approaching 73 (or 75), the combination of Social Security income and required minimum distributions needs to be managed carefully for taxes."
- The conversation is no longer about IF or WHEN. It is about HOW -- how to integrate SS income into the total financial plan.

**Compliance Notes:**
- Delayed retirement credits do not accrue past age 70. There is no benefit to delaying beyond 70.
- Social Security Administration will pay retroactive benefits for up to 6 months for filers over 70.
- The client must file with SSA directly. RPI does not file SS claims. Advisory only.
- SS income is taxable depending on total income (up to 85% of benefits may be taxable). Refer to client's tax advisor.
- Survivor benefit: the surviving spouse receives the higher of their own benefit or the deceased spouse's benefit (including delayed credits). This makes the age-70 filing amount the survivor benefit floor.

**Cross-Sell Opportunities:**
- **Income planning:** Filing at 70 triggers a full income plan review. How do SS, retirement accounts, annuities, and any other income sources work together?
- **Annuity repositioning:** Now that guaranteed SS income is flowing, the role of annuity products in the portfolio may shift. Income riders vs. growth strategies.
- **Tax planning:** SS income + RMDs can create tax bracket surprises. Roth conversions (if not already done) and income sequencing become critical.
- **Life insurance review:** "Your survivor benefit is now locked in at the highest possible amount. Let's make sure your life insurance complements that, not duplicates it."
- **Legacy planning:** "With your income secured, this is a great time to think about legacy -- what you want to pass on and how."

---

### 8. AGE-73 -- Required Minimum Distributions Begin

**Trigger:** Client approaching or turning 73. SECURE 2.0 Act requires mandatory distributions from traditional IRA, 401(k), 403(b), and other tax-deferred retirement accounts beginning at age 73.

**Division:** WEALTH

**Client Profile:** Client with traditional (pre-tax) retirement accounts who is approaching or has reached 73. May have substantial balances that have been growing tax-deferred for decades. May not know that mandatory distributions exist, or may not understand the penalties for missing them. The client's tax situation is about to change significantly whether they need the money or not.

**Psychology:** For decades, the client has been told to save, save, save in tax-deferred accounts. At 73, the IRS says "time to pay up." The client must take distributions whether they need the income or not. The government is not giving the client money -- it is forcing the client to move money from tax-deferred to taxable so it can collect income tax. For clients with large balances, RMDs can push them into higher tax brackets, increase Medicare premiums (IRMAA), and trigger taxes on Social Security benefits. The message: "The government is about to start telling you how much money to take out of your retirement accounts. Let's make sure you are ready."

**Key Message:** "Starting at 73, the IRS requires you to take minimum distributions from your retirement accounts every year -- whether you need the money or not. Miss it, and the penalty is 25% of the amount you should have taken. We need to make sure you know exactly what's required, when, and from which accounts -- and that we're managing the tax impact."

**Risk/Urgency:**
- **Penalty:** 25% of the missed RMD amount. Reduced to 10% if corrected within 2 years under SECURE 2.0.
- **First-year trap:** The first RMD can be delayed until April 1 of the year after turning 73. But this means TWO RMDs in the same tax year (the delayed first-year RMD + the second-year RMD by December 31). Double distributions = potential tax bracket spike.
- **Tax cascade:** RMD income can push the client into higher tax brackets, trigger IRMAA surcharges on Medicare premiums, and increase taxation of Social Security benefits. The impact is not just the tax on the RMD itself -- it is the ripple effect across the entire tax picture.
- **Roth conversion window closing:** Once RMDs start, the client cannot convert RMD amounts to Roth. The best time for Roth conversions is BEFORE RMDs begin. If the client has not already explored this, the window is closing.

**Agent Coaching:**
- Start with the basics: "Do you know what a Required Minimum Distribution is? Starting at 73, the IRS requires you to take a certain amount out of your retirement accounts every year."
- Explain the penalty clearly: "If you miss it, the penalty is 25% of what you should have taken. That's one of the harshest penalties in the tax code."
- Warn about the first-year trap: "You can delay your first RMD to April 1 of the next year, but then you'll have two RMDs in the same year. That could push you into a higher tax bracket. Let's plan around this."
- Ask about account inventory: "Which accounts are subject to RMDs? Traditional IRAs, 401(k)s, 403(b)s -- but not Roth IRAs. Let's make sure we have the full picture."
- Strategic sequencing: "The IRS says how much you have to take, but you get to choose WHICH accounts to take it from. That's where strategy comes in."
- Roth conversion: "Have you done any Roth conversions? If not, we should look at this before RMDs start. Once they start, the calculation changes."
- Tax coordination: "RMDs affect your tax bracket, your Medicare premiums, and how much of your Social Security is taxed. We need to look at all of this together."

**Compliance Notes:**
- SECURE 2.0 Act of 2022 moved the RMD start age from 72 to 73 for individuals turning 72 after December 31, 2022.
- RMDs are calculated based on the prior year-end account balance divided by the IRS life expectancy factor (Uniform Lifetime Table, or Joint and Last Survivor Table if sole beneficiary spouse is 10+ years younger).
- Penalty for missed RMDs: 25% excise tax on the undistributed amount. Reduced to 10% if corrected within a 2-year correction window (SECURE 2.0).
- First RMD deadline: April 1 of the year following the year the client turns 73. All subsequent RMDs are due by December 31.
- Roth IRAs are not subject to RMDs during the owner's lifetime.
- 401(k) participants who are still working for the plan sponsor may defer RMDs from that specific plan (the "still working" exception does not apply to IRAs or other plans).
- Tax implications are significant and complex. Always refer to client's tax advisor for specific tax advice.

**Cross-Sell Opportunities:**
- **Annuity income riders:** RMD amounts can be satisfied by annuity income rider payments in many cases. "Your annuity can generate RMD-satisfying income while keeping the balance growing."
- **Roth conversions:** "Before your RMDs start, let's look at converting some of your traditional IRA to Roth. It's taxable now, but it eliminates RMDs on those funds forever."
- **Legacy planning:** "RMDs force money out of tax-deferred accounts. If you don't need the income, let's talk about where that money goes -- and how to minimize the tax hit for your heirs."
- **Life insurance:** Premium financing using RMD income for a permanent life insurance policy can be a legacy strategy. "If you don't need your RMDs for living expenses, we can put that money to work for your family."
- **Medicare (IRMAA):** "Your RMDs can increase your Medicare premiums through IRMAA. Let's coordinate your distribution strategy with your Medicare costs."

---

### 9. AGE-75 -- SECURE 2.0 RMD (Born 1960+)

**Trigger:** Client approaching or turning 75. SECURE 2.0 Act pushes the RMD start age to 75 for individuals born in 1960 or later.

**Division:** WEALTH

**Client Profile:** Client born 1960 or later with traditional (pre-tax) retirement accounts approaching 75. Has had two additional years of tax-deferred growth compared to the AGE-73 cohort. Balances may be larger as a result. The same RMD rules, penalties, and strategies apply -- but the extended deferral window amplifies both the opportunity and the risk.

**Psychology:** Two extra years of deferral sounds like good news -- and it is, if the client uses those years strategically. The risk is complacency. Larger balances mean larger mandatory distributions, which means a bigger tax hit when RMDs finally start. The client who thought "I have more time" may be hit harder than the client who started at 73 with a smaller balance. The message: "You got two extra years. The question is whether you used them wisely -- and what happens now."

**Key Message:** "Because of the SECURE 2.0 Act, your Required Minimum Distributions don't start until 75 -- two years later than the previous rule. That's two extra years of tax-deferred growth. But larger balances mean larger required distributions, which means a bigger tax impact when they start. Let's make sure we have a strategy in place so your RMDs work for you, not against you."

**Risk/Urgency:**
- **Same penalties as AGE-73:** 25% of missed amount (10% if corrected within 2 years).
- **Same first-year trap:** April 1 delay option creates double-RMD year.
- **Amplified tax impact:** Two additional years of growth = larger account balances = larger RMDs = higher tax bills. The deferred tax bill has been growing along with the account.
- **Roth conversion window:** The client has had two more years than the AGE-73 cohort to do Roth conversions. If they have not, the window is now closing. Larger balances make conversions more impactful but also more complex.
- **Complacency risk:** The client may have coasted through 73 and 74 thinking "I don't have to worry about RMDs yet." That is two years of tax planning that may have been missed.

**Agent Coaching:**
- Same foundational coaching as AGE-73, with the amplification angle.
- Acknowledge the benefit: "You got two extra years of tax-deferred growth. That's real money."
- Pivot to reality: "But those two extra years also mean your balances are larger, which means your required distributions will be larger, which means the tax hit will be bigger."
- Roth conversion urgency: "Have you done any Roth conversions in the last few years? If not, we've missed a window -- but we still have options."
- Strategic sequencing: "With larger balances, the order in which you take RMDs from different accounts matters even more. This is precision work."
- Tax cascade awareness: "RMDs at this level can affect your tax bracket, your Medicare premiums, and your Social Security taxation. Everything is connected."
- If the client has already been planning: "Great -- let's make sure the numbers are dialed in for year one."
- If the client has not been planning: "No panic. We have time to set this up right. But let's start now."

**Compliance Notes:**
- SECURE 2.0 Act, Section 107 establishes RMD age 75 for individuals born 1960 or later.
- For individuals born 1951-1959, the RMD start age is 73. For 1960+, it is 75. There is no "74" cohort.
- All other RMD compliance notes from AGE-73 apply: penalty structure, first-year trap, calculation methodology, still-working exception, Roth IRA exemption.
- Tax implications are more significant due to larger account balances. Always refer to client's tax advisor.
- Legislation could change. Cite SECURE 2.0 as enacted, but note that future legislation may modify these rules.

**Cross-Sell Opportunities:**
- Same as AGE-73, amplified by larger balances.
- **Annuity income riders:** Larger RMDs may make annuity income riders more attractive for RMD satisfaction.
- **Roth conversions:** Even at 75, partial Roth conversions can reduce future RMDs and create tax-free legacy assets.
- **Legacy planning:** Larger balances = larger estate planning opportunities. Life insurance, charitable strategies, trust structures.
- **IRMAA management:** "Your RMDs are large enough to potentially trigger Medicare premium surcharges. Let's coordinate."
- **Full Health + Wealth + Legacy review:** At 75, the entire financial picture should be reviewed together. This is a natural inflection point for comprehensive planning.

---

## Quick Reference Matrix

| # | Campaign ID | Milestone Age | Trigger | Key Rule/Event | Cross-Sell Strength |
|---|-------------|---------------|---------|----------------|---------------------|
| 1 | AGE-50 | 50 | IRS contribution limit change | Catch-up: +$7,500/yr (401k), +$1,000/yr (IRA) | Moderate |
| 2 | AGE-55 | 55 | Employer plan access rule | Rule of 55: penalty-free 401(k) if separated | Moderate |
| 3 | AGE-59 | 59 1/2 | Early withdrawal penalty elimination | 10% penalty gone on ALL retirement accounts | Strong |
| 4 | AGE-62 | 62 | SS eligibility | First SS claim year -- permanently reduced benefit | **Highest** |
| 5 | AGE-66 | 66 | FRA milestone (born 1943-1954) | 100% benefit. 8%/yr delayed credits to 70 (32%) | Strong |
| 6 | AGE-67 | 67 | FRA milestone (born 1960+) | 100% benefit. 8%/yr delayed credits to 70 (24%) | Strong |
| 7 | AGE-70 | 70 | Delayed credits cap | Maximum SS benefit. File immediately. | Strong |
| 8 | AGE-73 | 73 | SECURE 2.0 RMD start | Mandatory distributions begin. 25% penalty. | **Highest** |
| 9 | AGE-75 | 75 | SECURE 2.0 RMD start (born 1960+) | Same as 73, larger balances, bigger tax impact | **Highest** |

### Phase Summary

| Phase | Campaigns | Theme | Primary Action |
|-------|-----------|-------|----------------|
| **Accumulation** | AGE-50, AGE-55, AGE-59 | Save more, access unlocks | Maximize contributions, understand access rules |
| **Social Security** | AGE-62, AGE-66/67, AGE-70 | Filing decision sequence | Run the numbers, coordinate spousal strategy |
| **Distribution** | AGE-73, AGE-75 | Mandatory withdrawals | Tax management, income sequencing, legacy planning |

---

*We're Your People.(TM)*
