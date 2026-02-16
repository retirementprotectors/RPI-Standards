# PSM Engine — Final Approved Content (15 Campaigns)
# Status: All approved by JDM on 2026-02-16
# Merge field pattern: {Carrier} {ProductName} {ProductType} in intro, text, VM, mailer minimum

## PERSONALIZATION MERGE FIELDS
- {FirstName}, {LastName} — client name
- {AgentName} — assigned agent
- {BOBName} — Book of Business name
- {Phone} — agent phone
- {Email} — agent email
- {CalendarLink} — scheduling link
- {Carrier} — insurance carrier (e.g., Humana, North American, Kansas City Life)
- {ProductName} — specific product (e.g., Gold Plus, Versachoice 10, Supernova)
- {ProductType} — product category (e.g., Medicare Advantage, fixed index annuity, universal life)
- {PlanName} — Medicare plan name (e.g., Humana Gold Plus)

## TONE RULES
- No "free" language for existing clients
- No urgency/sales mechanics (no "15 minutes", "today only", "Reply YES")
- Commission-based products: NEVER imply client pays RPI
- No EHR/technical jargon in client content — use "information from your providers about your healthcare trends"
- Energy: "we're your people, this is what we do, let's connect"

---

## PSM-AEP-REV — [CY] AEP Review
**Trigger**: Annual plan review time (Sep-Oct before AEP opens Oct 15)
**Division**: HEALTH

### Subject Line
Happy With Your Plan? It Just Changed.

### Introduction
{FirstName}, we hope you're loving your current {Carrier} {PlanName} — that's always the goal. But every year, your plan changes. Deductibles shift, copayments adjust, provider networks move, and formularies update. These changes happen at the carrier level whether you're paying attention or not. That's why we review every client's plan before AEP closes — so you're never caught off guard.

### Value Prop
Here's what we do that nobody else will: we pull your prescriptions, providers, pharmacies, and claims history — then we run a full cost projection for next year. Not a guess. A real, data-driven comparison that shows you what your current plan will actually cost you based on YOUR usage, and whether there's a better-aligned option in the marketplace. Apples to apples. No surprises.

### Pain Point
Here's what happens if we don't check: come January, you walk into the pharmacy or your doctor's office and discover your prescriptions aren't covered the same way, your provider left the network, or your copays doubled. By then, enrollment is closed and you're stuck for the entire year. The plan you loved last year may not love you back this year — and the only way to know is to review it now, while you can still make a change.

### Email CTA
We're already on it — just pick a time and we'll walk you through everything.

[Let's Connect]

### Text/SMS CTA
{FirstName}, it's that time — your {Carrier} {PlanName} has changes coming for next year. We're on it, just need to connect with you to make sure everything's still lined up. Call or text us back at {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. It's that time of year — your {Carrier} {PlanName} has some changes coming and I want to make sure your prescriptions, doctors, and pharmacy are still lined up the way they should be. We're already looking into it, just need to connect with you to walk through everything. Give me a call at {Phone} whenever you get a chance. Talk soon.

### USPS Piece
Dear {FirstName},

We hope your {Carrier} {PlanName} has been working well for you this year — that's always our goal when we help you choose coverage.

However, we want you to know that your plan has changes coming for next year. Every year, carriers adjust deductibles, copayments, provider networks, and prescription formularies. The plan that was perfect for you this year may look very different come January.

That's why we proactively review every client's plan during the Annual Enrollment Period. Here's what we do:

- Pull your current prescriptions, providers, and pharmacy preferences
- Analyze your claims history and project your costs for next year
- Compare your current plan against every available option in your area
- Deliver a clear, side-by-side report showing you exactly where you stand

If your plan is still the best fit — great, we'll confirm that and you'll have peace of mind. If there's a better option with lower costs or better alignment with your doctors and medications, we'll show you exactly what it looks like and help you make the switch before the December 7th deadline.

Don't wait until January to find out something changed. This is exactly why you have us — let's get ahead of it now.

Call us at {Phone} or visit {CalendarLink} to schedule your annual review. We'll pull your numbers, run the comparison, and make sure you're set for next year.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-AEP-MOVE — 26.AEP Move
**Trigger**: Review complete — found a better plan. Client needs to switch.
**Division**: HEALTH

### Subject Line
We Found a Better Plan for You — Let's Talk

### Introduction
{FirstName}, we've finished running your full plan analysis and wanted to share what we found. As you know, every year we review your prescriptions, providers, pharmacies, and claims history against everything available in the marketplace — and this year, the numbers are telling us something worth your attention.

### Value Prop
Based on your prescriptions, providers, pharmacies, and your diagnosis and condition history, it looks like there are a couple of options out there that could be a substantial improvement over your current {Carrier} {PlanName}. We've put together a side-by-side comparison using your actual healthcare consumption over the last few years so you can see exactly what to expect — from your current plan and from the alternatives. No guesswork, just your numbers.

### Pain Point
Here's the thing — just because your plan changes its networks, formularies, or preferred pharmacies doesn't mean you have to conform to those changes. You shouldn't have to scramble for a new doctor or switch pharmacies because your carrier made a business decision. That's not how it's supposed to work. We take your situation — your doctors, your medications, your conditions — and we find the plan that fits you. That's why you have us.

### Email CTA
We've got your comparison ready. Pick a time and we'll walk you through everything.

[Let's Connect]

### Text/SMS CTA
{FirstName}, we finished your plan analysis and it looks like there's a solid option that could be a real improvement over your {Carrier} {PlanName}. We've got your comparison ready — call or text us at {Phone} and we'll walk you through it.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. We just wrapped up your plan analysis and I wanted to let you know — it does look like there's a pretty significant advantage for you with a couple of options out there compared to your {Carrier} {PlanName}. We've got your full comparison based on your prescriptions, doctors, and your claims history. We just want to educate you on what's out there and help you make the right call. Give me a ring at {Phone} and we'll get it squared away.

### USPS Piece
Dear {FirstName},

We've completed your annual plan analysis, and we want to make sure you see what we found.

Based on your prescriptions, providers, pharmacies, and your diagnosis and condition history over the last few years, it looks like there are options available that could be a substantial improvement over your current {Carrier} {PlanName} for the upcoming year.

We've prepared a side-by-side comparison for you that shows:

- What to expect from your current plan based on your actual healthcare usage
- How a couple of alternative plans stack up using the same data
- Where you'll see the biggest differences in cost and coverage alignment

Just because your current plan changed its networks or formularies doesn't mean you have to conform to those changes. You shouldn't have to find a new doctor or switch pharmacies because your carrier made a business decision. That's not how it's supposed to work — we find the plan that fits your situation, not the other way around.

The good news is you have a window right now to make a change if the numbers make sense. We just need to connect with you to walk through everything.

Call us at {Phone} or visit {CalendarLink} to set up a time. We've got your report ready to go.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-AEP-G2G — [CY] AEP Good to Go
**Trigger**: Review complete — plan is still the best option. No change needed.
**Division**: HEALTH

### Subject Line
Great News — Your Plan Still Checks Every Box

### Introduction
{FirstName}, we just finished your annual plan review and we've got good news — your {Carrier} {PlanName} is still the best fit for you heading into next year. Your prescriptions, providers, and pharmacies are all aligned, and the cost projections look solid based on your claims history.

### Value Prop
We ran your data against every available plan in your area — premiums, copays, formulary coverage, provider networks, the whole picture. Your current plan came out on top. That's exactly what we like to see, and it's exactly why we check every year.

### Pain Point
Even though you're in great shape this year, it's worth knowing that we caught a few minor plan changes that won't impact you but are good to be aware of. Networks and formularies shift every year — the reason your plan still works is because we checked, not because nothing changed.

### Email CTA
Your plan's in great shape. If you have any questions about the changes we reviewed, we're here.

[View My Plan Summary]

### Text/SMS CTA
{FirstName}, good news — we reviewed your {Carrier} {PlanName} and you're all set for next year. Everything's aligned. If you want to go over the details, give us a call at {Phone}. We're here.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Good news — I just finished reviewing your {Carrier} {PlanName} for next year and everything looks great. Your doctors, prescriptions, and pharmacy are all still in network and your costs are looking solid. You're good to go. If you have any questions or just want to see the full breakdown, give me a call at {Phone}. Talk soon.

### USPS Piece
Dear {FirstName},

We've completed your annual Medicare plan review, and we're happy to report that your {Carrier} {PlanName} remains the best option for you heading into next year.

We compared your plan against every available option in your area using your prescriptions, providers, pharmacies, and your claims and condition history. Here's what we found:

- Your providers are in network
- Your prescriptions are covered at the same or better tier
- Your projected out-of-pocket costs are competitive with everything else available

While there were some changes to your plan this year — there always are — none of them impact your coverage in a meaningful way. The reason everything still lines up is because we check every year, not because nothing changed.

No action needed on your end. If you'd like to review the full breakdown, call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-AEP-STAY — 26.AEP Stay
**Trigger**: Review complete — staying on current plan, but acknowledging some changes.
**Division**: HEALTH

### Subject Line
Your Plan Has Some Changes — Here's What You Need to Know

### Introduction
{FirstName}, we wrapped up your annual plan review and here's where you stand: your {Carrier} {PlanName} is still the right fit, but there are a few changes this year we want to make sure you're aware of before January.

### Value Prop
We've gone through the updated formulary, provider network, and cost structure for your plan and compared it against your prescriptions, providers, and pharmacies. Even with the changes, your plan is still the best alignment for your situation — but we want you to know exactly what shifted so nothing catches you off guard.

### Pain Point
Some of the adjustments might mean a small change in what you pay at the pharmacy or a copay difference at certain visit types. None of it is big enough to justify switching plans, but it IS the kind of thing that surprises people in January when they weren't expecting it. That's why we're getting ahead of it now.

### Email CTA
We've got your updated plan summary ready. Let's connect so we can walk you through the changes.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your {Carrier} {PlanName} has a few changes for next year — nothing major, but we want to walk you through what to expect. You're staying put, just want to make sure you're informed. Call or text {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Finished your plan review — good news is you're in solid shape and sticking with your {Carrier} {PlanName} makes sense. There are a few changes I want to walk you through so nothing surprises you in January. Give me a call at {Phone} whenever you get a chance.

### USPS Piece
Dear {FirstName},

We've completed your annual plan review and your {Carrier} {PlanName} remains the best fit for your situation. You don't need to switch plans this year.

That said, there are some changes to your plan that take effect in January, and we want to make sure you know what to expect:

- Some formulary adjustments that may affect your prescription costs
- Minor network updates that could change copay amounts for certain visit types
- Updated cost-sharing details for specific services

None of these changes are significant enough to warrant moving to a different plan — we checked everything against the full marketplace to confirm. But knowing about them now means you won't be caught off guard at the pharmacy counter or the doctor's office.

If you'd like to go over the specifics, call us at {Phone} or visit {CalendarLink}. We've got your full comparison ready.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-AEP-$0 — 26.AEP Move ($0!)
**Trigger**: Review found a $0-premium plan that's a perfect fit.
**Division**: HEALTH

### Subject Line
$0 Premium. Better Coverage. Let's Talk.

### Introduction
{FirstName}, we just finished your plan analysis and found something we're excited to show you. There's a $0-premium plan available in your area that aligns with your prescriptions, providers, and pharmacies — and based on your claims history, it projects to save you real money compared to your current {Carrier} {PlanName}.

### Value Prop
We ran the full comparison — your {Carrier} {PlanName} side-by-side with this $0-premium option — using your actual prescriptions, providers, pharmacies, and healthcare usage. The numbers speak for themselves: same doctors, same medications, same pharmacy, lower cost structure, and zero monthly premium. We don't get excited about a plan unless the data backs it up.

### Pain Point
You're currently paying a monthly premium for coverage that, based on your situation, isn't outperforming what's available to you at $0. Every month that premium comes out is money that could stay in your pocket — with the same or better coverage. Plans like this don't always stick around year to year, so this is the window to take advantage of it.

### Email CTA
We've got your side-by-side comparison ready. Let's connect and walk through the numbers.

[Let's Connect]

### Text/SMS CTA
{FirstName}, we found a $0-premium plan that covers your doctors, meds, and pharmacy — and the numbers look great compared to your {Carrier} {PlanName}. We've got your comparison ready, call or text {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. I just finished your plan analysis and I'm pretty excited about what I found. There's a $0-premium plan in your area that covers all your doctors, all your prescriptions, same pharmacy — and based on your history, it's going to save you money compared to your {Carrier} {PlanName}. We've got the full comparison ready for you. Give me a call at {Phone} and we'll go over the numbers.

### USPS Piece
Dear {FirstName},

We've completed your annual plan analysis, and we want to make sure you see this.

There is a $0-premium Medicare Advantage plan available in your area that aligns with your current prescriptions, providers, and pharmacy. We ran a full comparison against your {Carrier} {PlanName} using your actual claims and condition history, and the results are compelling:

- $0 monthly premium (you're currently paying a monthly premium)
- Your doctors and specialists remain in network
- Your prescriptions are covered at the same or better tier
- Projected out-of-pocket costs are lower based on your usage history

We don't recommend a change unless the data makes it clear. In this case, it does. You'd be getting the same or better coverage and keeping more money in your pocket every month.

This plan is available right now, but options like this can change from year to year. Call us at {Phone} or visit {CalendarLink} to go over your comparison and make the right decision while the window is open.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-SEP-PREP — 26.AEP SEP Prep
**Trigger**: September — authorizations missing or >12 months old. Data gathering before AEP.
**Division**: HEALTH

### Subject Line
It's Time to Get Your Data Connected for This Year's Review

### Introduction
{FirstName}, AEP is right around the corner, which means it's time for us to start pulling your plan data so we can run your annual review. Before we can do that, we need to get your authorizations updated so we can access the information that makes your review actually meaningful.

### Value Prop
Here's why this matters: with your authorizations, we can pull your actual healthcare consumption — every doctor visit, every prescription fill, every procedure — from the last one to three years. That's what lets us build a real cost projection and a real plan comparison, not a guess. We can tell you exactly what your current plan is going to cost you next year AND how it stacks up against every other option — apples to apples, based on YOUR data. Without it, we're just speculating.

### Pain Point
Without your authorization data, we can check whether your prescriptions, providers, and pharmacies are in network — but that's where it stops. We can't tell you what your actual costs are going to be. If you had four EKGs last year, or 50 physical therapy visits, or a surgery — we have no way to know that without the data. And if we don't know your healthcare hotspots, it's nearly impossible to build a plan comparison that means anything. We'd be guessing, and guessing is not how we do this.

### Email CTA
It only takes a couple minutes to get your authorizations set up, and it makes all the difference in your review. Let's get it done.

[Let's Connect]

### Text/SMS CTA
{FirstName}, we're gearing up for your annual plan review but need to get your authorizations updated first. It takes a couple minutes and makes the whole review better. Call or text {Phone} and we'll walk you through it.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. AEP is coming up and we're getting ready to run your annual plan review. Before we can pull your data and build your comparison, we need to get your authorizations updated — it only takes a couple minutes and it's what lets us give you real numbers instead of guesswork. Give me a call at {Phone} and we'll knock it out real quick.

### USPS Piece
Dear {FirstName},

The Annual Enrollment Period is approaching, and we're preparing to run your plan review. Before we can pull your data and build a meaningful comparison, we need your help with one thing: updating your authorizations.

Depending on your current coverage, here's what we need:

- If you're on Original Medicare (Part A & B): We need your CMS Blue Button authorization so we can access your claims and healthcare history
- If you're on a Medicare Advantage plan: We need your Carrier Connect authorization so we can pull your plan-specific data
- Either way: We need your approval to get information from your providers about your healthcare trends, so we can give you an accurate projection of what your expenses will be

Here's why this matters: with this data, we can see your actual healthcare consumption — every visit, every prescription, every procedure — and build a real cost projection for next year. Without it, we can check whether your doctors and medications are in network, but we're just guessing on what your actual costs will be. And guessing is not how we do this.

It only takes a couple of minutes. Call us at {Phone} or visit {CalendarLink} and we'll walk you through it. The sooner we get your authorizations in, the better your review will be.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-SEP-5 — 25.SEP 5-Star
**Trigger**: 5-star plan identified in client's area that aligns with their data. Year-round SEP available.
**Division**: HEALTH

### Subject Line
There's a 5-Star Plan in Your Area — And It Looks Like a Fit

### Introduction
{FirstName}, we've identified a 5-star rated Medicare Advantage plan available in your area, and based on your data, it looks like it could be a real improvement over your {Carrier} {PlanName}. A 5-star rating is the highest CMS gives — and it comes with a benefit most people don't know about: a year-round Special Enrollment Period, which means you don't have to wait for AEP to make a change.

### Value Prop
We ran the numbers using your prescriptions, providers, pharmacies, and your healthcare consumption history, and this 5-star plan is showing as a strong fit for your situation. We've built a comparison that shows you side by side — what you have now versus what this plan offers — so you can see exactly where the differences are and what the projected costs look like based on your actual usage.

### Pain Point
Most people don't realize that a 5-star plan opens up a Special Enrollment Period that's available all year long. That means if there's an opportunity sitting in your area right now, you don't have to wait until October to take advantage of it. The question isn't whether you're eligible to switch — you are. The question is whether the numbers make sense, and based on what we're seeing, they do.

### Email CTA
We've got your comparison ready. Let's connect and walk through what this 5-star plan looks like for your situation.

[Let's Connect]

### Text/SMS CTA
{FirstName}, there's a 5-star Medicare plan in your area and based on your data, it looks like a real improvement over your {Carrier} {PlanName}. You don't have to wait for AEP — you're eligible to switch now. Call or text {Phone} and we'll walk you through the comparison.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. I wanted to reach out because we've identified a 5-star Medicare Advantage plan in your area, and based on your prescriptions, providers, and claims history, it's looking like a solid improvement over your {Carrier} {PlanName}. The good news is you don't have to wait for AEP — 5-star plans have a year-round Special Enrollment Period. We've got the full comparison built for you. Give me a call at {Phone} and we'll go through it.

### USPS Piece
Dear {FirstName},

We've identified a 5-star rated Medicare Advantage plan available in your area, and based on your data, we believe it's worth your attention.

A 5-star rating is the highest quality rating the Centers for Medicare & Medicaid Services awards. Fewer than 5% of plans nationwide earn it. What most people don't realize is that when a 5-star plan is available in your area, you have access to a year-round Special Enrollment Period — meaning you don't have to wait until the Annual Enrollment Period to make a change.

We ran a full comparison using your prescriptions, providers, pharmacies, and your healthcare consumption history against your current {Carrier} {PlanName}. Here's what we found:

- Your providers and pharmacy align with this plan's network
- Your prescriptions are covered at competitive or better tiers
- Based on your actual usage, projected costs show a meaningful improvement

We've put together a detailed side-by-side report so you can see exactly how this plan compares to what you have now. If the numbers make sense — and based on what we're seeing, they do — we can help you take advantage of this opportunity right now.

Call us at {Phone} or visit {CalendarLink} to go over your report.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-SEP-3 — 25.SEP <3-Star
**Trigger**: Client's plan dropped below 3-star CMS rating. Eligible for Special Enrollment Period.
**Division**: HEALTH

### Subject Line
Your Plan's Ratings Are In — We Should Talk

### Introduction
{FirstName}, CMS recently released their annual plan ratings, and we want to make sure you're aware of where your {Carrier} {PlanName} stands. Your plan received a rating below 3 stars this year, which puts it in the lower tier of plan performance based on a number of different factors — customer service, preventive care, member outcomes, and more.

### Value Prop
Here's what this means for you: because your plan rated below 3 stars, Medicare has opened a Special Enrollment Period that gives you the option to look at other plans that may be a better fit. We've already started pulling your data — prescriptions, providers, pharmacies, and your healthcare consumption — so we can run a full comparison and show you whether there's a plan out there that's better aligned with your situation. If your current plan still checks the boxes for you, we'll tell you that too.

### Pain Point
A low star rating doesn't mean your plan is going to stop working tomorrow — but it does reflect how the plan has performed over the last year across the metrics that matter. Customer service, getting members the preventive care they need, claims processing, overall quality of care. That track record generally isn't a great indicator of what's coming. The good news is you have a window right now to explore your options, and we've got the data to help you make the right call.

### Email CTA
We've got your data and we're ready to run the comparison. Let's connect and go over your options.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your {Carrier} {PlanName} star ratings came in below 3 stars. You've got a special window to look at other options. We've got your data — call or text {Phone} and we'll walk you through it.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. I'm reaching out because your {Carrier} {PlanName} ratings just came in and it's sitting below 3 stars this year. That opens up a Special Enrollment Period for you, which means you've got the option to look at other plans right now. We've already started pulling your information so we can run a comparison and see if there's something better aligned with your doctors, prescriptions, and pharmacy. Give me a call at {Phone} and we'll go over everything.

### USPS Piece
Dear {FirstName},

CMS has released their annual plan quality ratings, and we want to make sure you know where your {Carrier} {PlanName} stands. Your plan received a rating below 3 stars this year.

Star ratings are based on a composite of performance factors including:

- Quality of care and member health outcomes
- Customer service responsiveness
- Preventive care and wellness measures
- Claims processing and member satisfaction

A below-3-star rating reflects how your plan performed over the past year across these areas. While it doesn't mean your coverage stops working, it's generally not a strong indicator for what's ahead.

The good news: because your plan rated below 3 stars, Medicare has opened a Special Enrollment Period that allows you to explore other options right now. We've already started pulling your prescriptions, providers, pharmacies, and healthcare history so we can run a full comparison and show you whether there's a plan that's a better fit for your situation.

If your current plan is still the best option for you, we'll tell you. If there's something better, you'll see exactly why.

Call us at {Phone} or visit {CalendarLink} to go over your comparison.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-SEP-FEMA — 25.SEP FEMA
**Trigger**: Client in FEMA-declared disaster area. Special Enrollment Period available (2 months).
**Division**: HEALTH

### Subject Line
You Have a Special Enrollment Window — Here's What It Means

### Introduction
{FirstName}, due to the recent FEMA-declared emergency in your area, you've been granted a Special Enrollment Period for your Medicare coverage. You have 2 months from the end of the declared emergency period to make changes to your plan — whether that's switching to a different Medicare Advantage plan, adjusting your coverage, or exploring what else is available.

### Value Prop
Whether your needs have changed since you enrolled, you're looking at different providers, you've got new prescriptions, or you're just not thrilled with your current plan — this is a unique opportunity to take a fresh look at what's available. We can run a full comparison using your prescriptions, providers, pharmacies, and your actual healthcare usage to make sure that if there is a better option, you're educated on it and in a position to take advantage of this window.

### Pain Point
Special Enrollment Periods like this don't come around often outside of AEP. If there's been any change in your situation — new medications, different doctors, a pharmacy that's more convenient — or if your plan just hasn't been the right fit, this is your chance to make a move without waiting until October. The window is 2 months, so if there's something worth looking at, we want to get your data pulled and your comparison built while there's still time.

### Email CTA
If your needs have changed or you want to see what else is out there, let's connect while this window is open.

[Let's Connect]

### Text/SMS CTA
{FirstName}, you have a Special Enrollment Period right now due to the recent FEMA-declared emergency in your area. If anything has changed with your healthcare needs, this is a good window to look at your options. Call or text {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Just reaching out because you've got a Special Enrollment Period available right now due to the recent emergency declaration in your area. If anything has changed with your doctors, prescriptions, or if you've been wanting to look at other plan options — this is a good window to do it. We can pull your data and run a comparison to see if there's something better out there for you. Give me a call at {Phone} and we'll take a look.

### USPS Piece
Dear {FirstName},

Due to the recent FEMA-declared emergency in your area, you have been granted a Special Enrollment Period for your Medicare coverage. This gives you 2 months from the end of the declared emergency period to make changes to your plan.

This is good news if any of the following apply to you:

- Your healthcare needs have changed since you last enrolled
- You're seeing different providers or have new prescriptions
- You've been considering a different pharmacy
- You're not completely satisfied with your current plan

We can run a full analysis using your prescriptions, providers, pharmacies, and your healthcare history to determine whether there's a plan that's a better fit for your situation. If there is, we'll show you exactly how it compares — and help you make the switch while this window is open.

If your current plan is still the best fit, we'll confirm that too. Either way, this is a good opportunity to make sure everything is lined up.

Call us at {Phone} or visit {CalendarLink} to get started.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-OEP — 26.OEP Beni Check
**Trigger**: January-March — Open Enrollment Period benefit check for MA members.
**Division**: HEALTH

### Subject Line
New Year, New Plan Details — Let's Make Sure You're Set

### Introduction
{FirstName}, happy new year. Your {Carrier} {PlanName} has officially rolled over into the new plan year, which means all those changes we talked about during AEP are now in effect. We're doing a quick benefit check for all our clients to make sure everything is running smoothly now that the new plan details are live.

### Value Prop
This is the time of year where the rubber meets the road — your updated formulary, copays, and network are all active now. We want to make sure your first few doctor visits and pharmacy trips go exactly the way you expect. If anything feels off — a copay that's higher than expected, a prescription that's processing differently, a provider showing as out of network — this is exactly what we're here for.

### Pain Point
If there's a misalignment that slipped through, you still have the Medicare Advantage Open Enrollment Period through March 31st to make a switch. This is your safety net. After March 31st, you're locked in for the rest of the year. If something isn't right, now is the time to flag it — not in April when the window is closed.

### Email CTA
If anything feels different with your coverage this year, we need to know now while there's still time to adjust. Let's connect.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your {Carrier} {PlanName} just rolled into the new year. If anything feels off with your coverage — prescriptions, doctors, copays — let us know now. We've got until March 31 to fix it. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Happy new year. Just checking in — your {Carrier} {PlanName} rolled into the new plan year and all those updates are live now. If anything feels different at the pharmacy or the doctor's office, we need to know about it now while we still have the open enrollment window to make adjustments. Give me a call at {Phone} and we'll make sure everything's running right.

### USPS Piece
Dear {FirstName},

Happy new year. Your {Carrier} {PlanName} has officially rolled over into the new plan year, and all updated benefits, formulary changes, and network adjustments are now in effect.

We're reaching out to all our clients for a quick benefit check to make sure everything is running smoothly:

- Are your prescriptions processing the same way at the pharmacy?
- Are your copays at the doctor's office what you expected?
- Is your provider still showing as in network?

If anything feels different or unexpected, now is the time to let us know. You have until March 31st during the Medicare Advantage Open Enrollment Period to make a plan change if needed. After that, you're locked in for the year.

This is exactly what we're here for. Call us at {Phone} or visit {CalendarLink} if anything needs attention.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-NO-CORE — No-Core Cross-Sell
**Trigger**: Active client with life/annuity/other but NO MedSupp or MAPD through RPI. Jan-Sep only.
**Division**: HEALTH

### Subject Line
We've Got Your Account — But Not Your Medicare

### Introduction
{FirstName}, we were going through your account and noticed something: you've got your {Carrier} {ProductName} with us, but we don't currently have your Medicare coverage on file. Health, wealth, and legacy are all interconnected — and Medicare is one of the core services we provide for our clients. For whatever reason, whether the timing wasn't right, you already had it handled elsewhere, or it just never came up — we want to make sure you know this is a huge part of what we do.

### Value Prop
Since you've been a client, we've invested heavily in our technology and our team to deliver a Proactive Service Model for Medicare that goes well beyond just picking a plan. We pull your prescriptions, providers, pharmacies, and healthcare data. We run cost projections. We monitor your plan year-round and proactively review it every AEP to make sure you're always on the best option for your situation. It's the same level of attention we give your other accounts — applied to your health insurance.

### Pain Point
If your Medicare coverage isn't being actively managed the same way your other accounts are, there's a good chance you're leaving value on the table. Plans change every year — networks shift, formularies update, costs adjust — and without someone running the numbers on your behalf, it's easy to end up on a plan that's out of alignment with your current situation. This is exactly what we're built for, and we'd love the opportunity to be a resource for you here.

### Email CTA
Let's connect and see if we can bring the same value to your Medicare that we bring to everything else.

[Let's Connect]

### Text/SMS CTA
{FirstName}, we handle your {Carrier} {ProductName} but noticed we're not managing your Medicare coverage. That's one of the biggest things we do. Let's connect and see if we can add some value there. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. I was looking at your account and realized we've got your {Carrier} {ProductName} but we're not handling your Medicare coverage. That's actually one of the core things we do for our clients — we run full plan reviews, monitor your coverage year-round, and make sure you're always on the best option for your situation. Whether we just never got the chance to talk about it or the timing wasn't right before, we'd love the opportunity to be a resource for you there. Give me a call at {Phone}.

### USPS Piece
Dear {FirstName},

We appreciate your trust in us with your {Carrier} {ProductName} {ProductType}, and we wanted to reach out about something we noticed: we don't currently have your Medicare coverage on file.

Health, wealth, and legacy are all interconnected — and Medicare is one of the core services we provide for our clients. Whether the timing wasn't right before, you already had it handled elsewhere, or it simply never came up, we want you to know what we bring to the table.

Here's what our Proactive Service Model for Medicare includes:

- Full analysis of your prescriptions, providers, and pharmacies
- Data-driven cost projections based on your actual healthcare usage
- Annual plan reviews every AEP with side-by-side comparisons
- Year-round monitoring so you're never caught off guard by plan changes

It's the same level of attention and care we give your other accounts — applied to your health insurance. We've made significant investments in our technology and team since you became a client, and we'd love the opportunity to show you what that looks like.

Call us at {Phone} or visit {CalendarLink}. We'd love to be a resource for you here.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-LIFE — Life Statement Review
**Trigger**: ~30 days after policy anniversary, when annual statement arrives.
**Division**: LEGACY

### Subject Line
Your Life Insurance Statement Is In — Here's What to Look For

### Introduction
{FirstName}, your annual statement on your {Carrier} {ProductName} should be arriving right around now, and we want to make sure you know what to look for. Your statement is a snapshot of the last 12 months — it shows your premiums, policy fees, cost of insurance, rider charges, and any interest or index credits that were applied. That's the rearview mirror. What it doesn't show you is the part that actually matters.

### Value Prop
What your statement can't tell you is how your policy is going to perform over the next 10, 15, or 20 years based on current conditions. That's what an in-force illustration does — and that's what we want to order for you. An in-force illustration takes your current policy values, the current cost of insurance, fees, and interest crediting rates, and projects forward to show you whether your policy is on track to do what you need it to do. Is it going to last as long as you are? If it is, great — you'll have peace of mind. If it's not, we need to know now while we still have options.

### Pain Point
Here's what keeps people up at night: they assume their life insurance is fine because they've been paying the premium. But costs of insurance increase as you age, and if interest rates or index credits haven't kept pace, your policy could be quietly falling behind. The worst time to find that out is when it's too late to fix. If your policy needs attention — whether that means adjusting your premium, modifying the benefit, or looking at other options — we can figure that out now and build a plan to get it back on track.

### Email CTA
We want to order an in-force illustration on your policy to make sure it's on track. Let's connect and get it started.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your {Carrier} {ProductName} statement should be hitting your mailbox soon. We want to order an in-force illustration to make sure your policy is going to last as long as you are. Call or text {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Your annual statement on your {Carrier} {ProductName} should be arriving soon, and I want to make sure you don't just file it away. Your statement shows what happened last year, but what really matters is how your policy is going to perform going forward. We want to order an in-force illustration to make sure everything is on track. Give me a call at {Phone} and we'll get that ordered for you.

### USPS Piece
Dear {FirstName},

Your annual statement on your {Carrier} {ProductName} {ProductType} should be arriving right about now. Before you file it away, we'd like to help you understand what it's telling you — and more importantly, what it's not.

Your statement is a look in the rearview mirror. It shows you:

- Premiums paid and policy fees deducted
- Cost of insurance and rider charges
- Interest rates and any index credits applied
- Your current cash value and death benefit

What your statement doesn't show you is the most important thing: is your policy going to last as long as you are?

That's what an in-force illustration tells us. It takes your current policy values, today's cost of insurance, current fees, and crediting rates, and projects them forward 10, 15, and 20+ years. If your policy is on track — great, you'll have that peace of mind in writing. If it needs attention — more premium, a benefit adjustment, or a different strategy — we want to catch that now while there are still options.

The worst time to find out your policy is falling behind is when it's too late to fix. Let us order that in-force illustration and make sure you're in good shape.

Call us at {Phone} or visit {CalendarLink} to get started.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-ANN-SUR — ANN <10% Surrender
**Trigger**: Annuity surrender charge below 10%. Repositioning window opening.
**Division**: WEALTH

### Subject Line
Your Annuity May Have an Opportunity — Let's Take a Look

### Introduction
{FirstName}, based on the information we have on file for your {Carrier} {ProductName}, it looks like your surrender charges have come down to a point where it may be worth taking a fresh look at your options. This doesn't mean anything is wrong with what you have — it means the window is opening for us to evaluate whether there's an opportunity to improve your situation without a net loss to your account value.

### Value Prop
Depending on when you got your annuity, how interest rates have moved, and how these products are priced today, there may be options available that could improve your position — whether your goal is guaranteed income now, guaranteed income later, access to your capital for a long-term care need, or protection in the event of a terminal illness. We want to run a comparison that shows you the features and benefits of your current account side by side with what's available in the marketplace. If you're already in the best spot, we'll tell you. If there's an improvement, we'll have something to talk about.

### Pain Point
Your current annuity is doing its job, and that's a good thing. But our role is to make sure that if there is an opportunity to improve what you have — either with your current company or with another option — you're educated on it. Interest rates change, product designs evolve, and what was the best fit five or ten years ago may not be the best fit today. With your surrender charges where they are, you're approaching the point where a move could be made without a net negative to your account. That's an opportunity worth exploring.

### Email CTA
Let us run a comparison report on your current account versus what's available today. If there's an improvement, we'll walk you through it.

[Let's Connect]

### Text/SMS CTA
{FirstName}, surrender charges on your {Carrier} {ProductName} are getting low enough that it might be time to look at your options. We can run a comparison — call or text {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. I'm reaching out because based on the information we have on your {Carrier} {ProductName}, it looks like your surrender charges have come down to a point where there may be an opportunity to improve your situation. Give me a call at {Phone} and we'll run a comparison.

### USPS Piece
Dear {FirstName},

Based on the information we have on file, the surrender charges on your {Carrier} {ProductName} {ProductType} have come down to a level where it may be worth taking a fresh look at your options.

This doesn't mean anything is wrong with your current account. It means the timing may be right to evaluate whether there's an opportunity to improve your position — potentially without any net loss to your account value.

Depending on your goals, there may be options that offer:

- Higher guaranteed income — now or in the future
- Better access to your capital if needed
- Enhanced protection for long-term care or terminal illness
- Improved crediting strategies based on today's interest rate environment

We want to run a side-by-side comparison of your current account versus what's available in the marketplace today. If you're in the best spot already, we'll confirm that. If there's a meaningful improvement, we'll show you exactly what it looks like and you can decide if it makes sense.

Call us at {Phone} or visit {CalendarLink} to get your comparison started.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-ANN-ALLOC — ANN Allocation Review
**Trigger**: Policy anniversary — annual allocation/strategy review.
**Division**: WEALTH

### Subject Line
Your Annuity Anniversary Is Coming Up — Let's Review Your Strategy

### Introduction
{FirstName}, your {Carrier} {ProductName} is approaching its policy anniversary, and this is the time of year we take a fresh look at your allocation strategy. How your money is distributed across your available options — fixed accounts, index strategies, crediting methods — has a direct impact on how your annuity performs over the next 12 months. We want to make sure you're positioned for what's ahead, not just riding on last year's selections.

### Value Prop
Every year, the available index options and cap rates can change, and the interest rate environment may look very different than when you first set your allocations. We'll pull your current account details, review how each strategy performed over the last year, and compare that against what's available for the next contract year. If your current allocations still make sense for your goals, we'll confirm that. If there's a better positioning, we'll show you exactly what it looks like.

### Pain Point
Most people set their allocation when they first fund their annuity and never touch it again. That means they could be sitting in a strategy that made sense three or five years ago but doesn't reflect today's rate environment or their current objectives. Your anniversary is the one time each year you can make changes — once it passes, you're locked into those allocations for another 12 months.

### Email CTA
Your anniversary window is coming up. Let's connect and make sure your allocations are positioned for the year ahead.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your {Carrier} {ProductName} anniversary is coming up — that's your window to review and adjust your allocations. Let's make sure you're positioned right. Call or text {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Your {Carrier} {ProductName} anniversary is coming up, and this is the time we review your allocation strategy for the next year. Cap rates and index options can shift, and we want to make sure you're positioned for what's ahead. Give me a call at {Phone} and we'll go over your options.

### USPS Piece
Dear {FirstName},

Your {Carrier} {ProductName} {ProductType} is approaching its policy anniversary, and we want to make sure you're positioned for the year ahead.

Your anniversary is the one time each year you can review and adjust how your money is allocated across your available options — fixed accounts, index strategies, and crediting methods. How you're positioned has a direct impact on how your annuity performs over the next 12 months.

Here's what we'll review together:

- How each of your current allocations performed over the last year
- What cap rates and index options are available for the next contract year
- Whether the current interest rate environment creates any new opportunities
- How your allocations align with your current financial goals

If your current strategy still makes sense, we'll confirm it. If there's a better positioning available, we'll show you exactly what it looks like — and help you make the adjustment before your anniversary window closes.

Call us at {Phone} or visit {CalendarLink} to schedule your allocation review.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## PSM-ANN-LIQ — ANN Liquid
**Trigger**: Annuity fully liquid — zero surrender charges. Full repositioning opportunity.
**Division**: WEALTH

### Subject Line
Your Annuity Is Fully Liquid — Here's What That Means

### Introduction
{FirstName}, your {Carrier} {ProductName} has reached the point where your surrender charges are completely behind you. Your money is fully liquid, which means you have complete flexibility to keep it where it is, reposition it, or explore other options — with no penalties and no fees for moving.

### Value Prop
This is the widest your window has ever been. We want to run a comprehensive review of your current account — how it's credited, what guarantees it offers, how it compares against what's available in today's marketplace — and show you a side-by-side comparison. Whether your goal is guaranteed income, growth potential, long-term care protection, or simply the best rate available, we can evaluate every option on the table and help you make the right decision for where you are right now. If your current account is still the best fit, we'll tell you. If the market has something materially better, you'll see exactly why.

### Pain Point
Just because your annuity is fully liquid doesn't mean it's performing at its best. The product landscape changes — new crediting strategies, better income riders, improved guarantees — and what was competitive when you first funded your account may not be competitive today. The risk of doing nothing isn't that you lose money; it's that you leave opportunity on the table. Your money is free to move, and this is the best time to make sure it's working as hard as it can for you.

### Email CTA
Your money is fully liquid and the market has options. Let's connect and run your comparison.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your {Carrier} {ProductName} is fully liquid — no surrender charges left. Good time to see if the market has something better for you. Call or text {Phone} and we'll run a comparison.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. I wanted to reach out because your {Carrier} {ProductName} is now fully liquid — your surrender charges are completely behind you. That means if there's a better option out there for your situation, this is the time to look at it. We want to run a comparison against what's available in the marketplace and make sure your money is working as hard as it can for you. Give me a call at {Phone}.

### USPS Piece
Dear {FirstName},

Your {Carrier} {ProductName} {ProductType} has reached an important milestone: your surrender charges are completely behind you. Your account is fully liquid.

This means you have complete flexibility — no penalties, no fees — to evaluate your options and decide what's best for your situation going forward.

We'd like to run a comprehensive comparison for you that includes:

- How your current account is performing — crediting rates, guarantees, and features
- What's available in today's marketplace for your goals
- Side-by-side analysis of income potential, growth, and protection features
- A clear recommendation based on your specific objectives

If your current account is still the best fit, we'll confirm that. If the market has moved and there's a meaningful improvement available, you'll see exactly what it looks like.

The product landscape evolves — new crediting strategies, better income riders, improved guarantees — and what was competitive when you first funded your account may not be competitive today. With your money fully liquid, this is the ideal time to make sure it's positioned where it should be.

Call us at {Phone} or visit {CalendarLink} to get your comparison started.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}
