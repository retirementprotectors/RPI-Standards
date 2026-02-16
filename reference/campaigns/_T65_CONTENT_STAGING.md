# T65 Engine — Final Approved Content (15 Campaigns)
# Status: All approved by JDM on 2026-02-16
# Note: T65-00 corrected per JDM — generalized card types (no specific Supplement/MAPD card references)
# Merge field pattern: {Carrier} {PlanName} used where applicable (NOT in T65-00 birthday touch)

## PERSONALIZATION MERGE FIELDS
- {FirstName}, {LastName} — client name
- {AgentName} — assigned agent
- {BOBName} — Book of Business name
- {Phone} — agent phone
- {Email} — agent email
- {CalendarLink} — scheduling link
- {Carrier} — insurance carrier (e.g., Humana, Aetna, UnitedHealthcare)
- {ProductName} — specific product (e.g., Gold Plus, Plan G)
- {ProductType} — product category (e.g., Medicare Advantage, Medicare Supplement)
- {PlanName} — Medicare plan name (e.g., Humana Gold Plus)

## TONE RULES
- No "free" language for existing clients
- No urgency/sales mechanics (no "15 minutes", "today only", "Reply YES")
- Commission-based products: NEVER imply client pays RPI
- No EHR/technical jargon in client content — use "information from your providers about your healthcare trends"
- Energy: "we're your people, this is what we do, let's connect"
- T65-00 (birthday month): Keep card references general — works for both MedSupp+PDP and MAPD paths

## ENGINE CONTEXT
- T65 = Medicare Birthday Countdown engine
- 15 campaigns: T65-12 through T65-01, T65-00, T65+1, T65+2
- Countdown from 12 months before 65th birthday through 2 months after
- Phases: Education (12-7), Planning (6-4), Urgent (3-1), Action (00), Follow-up (+1, +2)
- IEP = Initial Enrollment Period (7-month window centered on 65th birthday month)

---

## T65-12 — 12 Months Out (EDUCATION)
**Trigger**: Client turns 64. Medicare is 12 months away.
**Division**: HEALTH

### Subject Line
You're Going to Hear a Lot About Medicare — Here's What Actually Matters

### Introduction
{FirstName}, in the next few months, you're going to start getting more information about Medicare than you could ever want or need — mailers, phone calls, TV ads, you name it. Before all of that noise starts, we want you to know one thing: we're here, and this is a huge part of what we do. Health, wealth, and legacy — Medicare is a full third of our practice, and we're going to be right here to walk you through it.

### Value Prop
Here's the good news: the sooner you understand what's ahead, the more confidently you can ignore everything else that's about to hit your mailbox. Depending on your situation — whether you're on an employer plan, a spouse's plan, or something else entirely — you may not even need to worry about this right now. That's one of the first things we'll help you figure out. And if you do need to make decisions, we'll educate you on what you have today, how it compares to what's available through Medicare, and what to expect in terms of premiums, copays, deductibles, and total costs. No pressure, no confusion — just clarity.

### Pain Point
The biggest mistake people make at this stage isn't choosing the wrong plan — it's not knowing whether they need to act at all. Some people stress about Medicare for a year when their employer coverage has them completely covered. Others assume everything is automatic and find out too late that they missed a window or owe a penalty. We sort all of that out so you know exactly where you stand — and whether this is something you need to worry about now, later, or not at all.

### Email CTA
This is what we're here for. Let's connect and figure out whether Medicare is something you need on your radar right now.

[Let's Connect]

### Text/SMS CTA
{FirstName}, you're about a year out from Medicare and the noise is about to start. Before it does — we're your people and this is what we do. Let's connect and figure out if this is even something you need to worry about. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. You're coming up on 65, and I wanted to reach out before all the Medicare mailers and phone calls start hitting. This is a huge part of what we do, and we're going to be right here to walk you through everything. Depending on your situation, you may not even need to worry about it — and that's one of the first things we'll help you figure out. Give me a call at {Phone} whenever you get a chance. We're your people on this.

### USPS Piece
Dear {FirstName},

You're approaching a milestone — and with it comes a flood of information about Medicare that's about to start showing up in your mailbox, your phone, and your inbox. Before all of that noise begins, we want you to know: we're here, and this is what we do.

Health, wealth, and legacy are the three pillars of our practice. Medicare is a full third of what we do every day, and we're going to walk you through every step of this.

Here's what we want you to know right now:

- Depending on your situation, you may not even need to worry about Medicare yet — if you're on an employer plan, a spouse's plan, or have other creditable coverage, there may be nothing you need to do right now
- If you DO need to make decisions, we'll educate you on what you have today, how it compares to what's available through Medicare, and what to expect
- The sooner you understand what's ahead, the more confidently you can ignore the noise that's coming

No pressure, no deadlines — just an early conversation to make sure you know where you stand and whether this is something you need on your radar.

Call us at {Phone} or visit {CalendarLink}. We're your people on this.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-11 — 11 Months Out (EDUCATION)
**Trigger**: Education phase. Gentle follow-up to first touch. What IS Medicare?
**Division**: HEALTH

### Subject Line
Medicare 101 — What It Actually Is (and Isn't)

### Introduction
{FirstName}, last month we reached out to let you know we're here as your resource on Medicare. This month, we want to give you a quick overview of what Medicare actually is — because there's a lot of misinformation out there and the sooner you understand the basics, the less stressful this whole process becomes.

### Value Prop
Medicare has four parts — Part A covers hospital stays, Part B covers doctor visits and outpatient services, Part C (Medicare Advantage) is an alternative way to get A and B plus extras through a private plan, and Part D covers prescription drugs. How these pieces fit together depends on your situation, and there are multiple paths you can take. Our job is to figure out which path makes sense for YOU based on your doctors, your prescriptions, and how you use healthcare. That's it. No one-size-fits-all answer.

### Pain Point
The biggest misconception we see: people assume Medicare covers everything automatically, or that there's only one option. There are real decisions to make, and the right answer is different for everyone. The good news is you've got time, and you've got us. We'll walk you through all of it.

### Email CTA
Have questions about how Medicare works? We're here.

[Let's Connect]

### Text/SMS CTA
{FirstName}, quick Medicare primer: there are 4 parts and multiple paths. Which one's right for you depends on your situation. We'll figure it out together when the time comes. Questions? {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Just a quick follow-up — wanted to give you a heads-up that Medicare has a few different parts and multiple paths you can take, and the right one depends on your situation. We'll walk you through all of it when the time comes. If you have any questions in the meantime, give me a call at {Phone}.

### USPS Piece
Dear {FirstName},

Last month we reached out to let you know we're here for your Medicare journey. This month, a quick primer on what Medicare actually is:

- **Part A** — Hospital coverage (most people get this at no premium)
- **Part B** — Doctor visits, outpatient services, preventive care
- **Part C (Medicare Advantage)** — A private plan option that bundles A, B, and usually D together, often with additional benefits
- **Part D** — Prescription drug coverage

How these pieces fit together — and which path makes sense for you — depends on your doctors, your prescriptions, your pharmacy, and how you use healthcare. There's no one-size-fits-all answer, and that's exactly why you have us.

No decisions to make yet. Just wanted you to have the basics. We'll be in touch.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-10 — 10 Months Out (EDUCATION)
**Trigger**: Education phase. Let's figure out YOUR situation.
**Division**: HEALTH

### Subject Line
Do You Even Need to Worry About Medicare? Let's Find Out

### Introduction
{FirstName}, we've been sharing some Medicare basics with you, and now it's time to zero in on your situation. Depending on what coverage you have today — employer plan, spouse's plan, retirement benefits, or something else — you may not need to do anything when you turn 65. Or you may have some important decisions ahead. Either way, we need to figure that out now, not three months from now.

### Value Prop
Here's what we'll determine together: are you on a qualifying employer plan that lets you defer Medicare without penalty? Do you have creditable drug coverage? Is your current situation better than what Medicare offers, or is there a real opportunity to improve? These are the questions that matter, and the answers are specific to you. Once we know where you stand, we can either put this on the back burner or start building your comparison.

### Pain Point
The worst spot to be in is six months from now, scrambling because you assumed your employer plan handled everything — only to find out it doesn't qualify, or that you missed a window. A quick conversation now saves a lot of stress later.

### Email CTA
Let's figure out your situation. A quick conversation now saves stress later.

[Let's Connect]

### Text/SMS CTA
{FirstName}, depending on your current coverage, you may not need to worry about Medicare at all. But we need to figure that out. Quick call — {Phone}.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Quick question for you — do you even need to worry about Medicare when you turn 65? Depending on your current coverage, the answer might be no. But we need to look at your situation to know for sure. Give me a call at {Phone} and we'll figure it out in a few minutes.

### USPS Piece
Dear {FirstName},

Here's the question that matters most right now: do you even need to worry about Medicare?

Depending on your current situation, the answer might be no:

- If you're on a qualifying employer plan (20+ employees), you may be able to defer Part B and Part D with no penalty
- If your spouse's employer plan covers you, same thing
- If you have creditable drug coverage, your Part D window stays protected

Or the answer might be yes — and if it is, we need to start building your comparison soon.

Either way, a quick conversation now tells us which path you're on and saves you from scrambling later. Let us take a look at your situation and give you a clear answer.

Call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-09 — 9 Months Out (EDUCATION)
**Trigger**: Education phase. Time to get your data connected.
**Division**: HEALTH

### Subject Line
Let's Get Your Data Connected — Your Medicare Review Starts Here

### Introduction
{FirstName}, we're 9 months out from your 65th birthday, and if Medicare is something you'll need to act on, now is the time to get your data connected so we can start building your picture. The more information we have, the better your comparison will be when the time comes to make a decision.

### Value Prop
Here's what we need: your authorization to pull information from your current health insurance carrier — your prescriptions, providers, pharmacies, diagnoses, and claims history. It's a simple electronic authorization, similar to how banks share data between institutions. Once we have it, your information flows into our system automatically and we don't need to ask you about anything — we'll have your full healthcare picture without you having to remember every doctor visit or prescription.

### Pain Point
Without this data, we're guessing. We can tell you what plans are available in your area, but we can't tell you which one is actually the best fit for YOUR situation. With it, we can build a real cost projection based on how you actually use healthcare — not a generic estimate. The earlier we get this connected, the more complete your comparison will be when decisions need to be made.

### Email CTA
It takes a couple minutes to get your authorization set up. Let's get it done.

[Let's Connect]

### Text/SMS CTA
{FirstName}, 9 months from Medicare. We need to get your data connected so we can build your comparison. Quick authorization — takes a couple minutes. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. We're about 9 months out from your 65th birthday, and I want to get your healthcare data connected to our system so we can start building your Medicare comparison. It's a quick authorization — takes a couple minutes — and it lets us pull your prescriptions, providers, and claims history automatically so we have everything we need when decision time comes. Give me a call at {Phone} and we'll knock it out.

### USPS Piece
Dear {FirstName},

We're 9 months from your 65th birthday, and it's time to get your data connected.

In order to build a meaningful Medicare comparison for you, we need your authorization to access your current healthcare information — prescriptions, providers, pharmacies, diagnoses, and claims history. It's a simple electronic authorization that allows your data to flow into our system securely.

Here's why this matters:

- With your data, we build a real cost projection based on how YOU actually use healthcare
- Without it, we're guessing — and guessing is not how we do this
- The earlier we connect your data, the more complete your comparison will be when decision time comes

It takes a couple of minutes. Once it's done, we don't need to ask you about every doctor visit or prescription — we'll have everything automatically.

Call us at {Phone} or visit {CalendarLink} to get your authorization set up.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-08 — 8 Months Out (EDUCATION)
**Trigger**: Education phase. We're building your picture.
**Division**: HEALTH

### Subject Line
We're Building Your Medicare Picture — Here's Where We Are

### Introduction
{FirstName}, we're 8 months out from 65, and if you've connected your data with us, we're already starting to build your Medicare picture. Your prescriptions, providers, pharmacy preferences, and healthcare history are coming together, and we're beginning to map out what your options will look like.

### Value Prop
Over the next few months, we'll be refining your comparison as plan details for the upcoming year start to become available. Right now, we're establishing your baseline — what you currently have, how you use healthcare, and what matters most to you. By the time your enrollment window opens, we'll have a clear, data-driven recommendation ready for you. No scrambling, no guessing, no last-minute decisions.

### Pain Point
If you haven't connected with us yet, there's still time — but the earlier we get your data, the better your comparison will be. We'd rather have months of healthcare history to work with than weeks.

### Email CTA
Your picture is coming together. If you haven't connected your data yet, let's get it done.

[Let's Connect]

### Text/SMS CTA
{FirstName}, 8 months to 65. If you've connected your data, we're building your comparison. If not — let's get it set up. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Quick update — we're 8 months out and if you've connected your data with us, your Medicare picture is starting to come together. By the time your enrollment window opens, we'll have a recommendation ready for you. If you haven't gotten your data connected yet, give me a call at {Phone} and we'll get it done. Still plenty of time.

### USPS Piece
Dear {FirstName},

Quick update: we're 8 months from your 65th birthday, and your Medicare picture is starting to take shape.

If you've already connected your data with us, we're building your baseline — mapping your prescriptions, providers, pharmacy, and healthcare usage against what will be available through Medicare. By the time your enrollment window opens, we'll have a clear recommendation ready for you.

If you haven't connected with us yet, there's still time. But the sooner we have your data, the more complete your comparison will be. We'd rather have months of healthcare history to work with than weeks.

Call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-07 — 7 Months Out (PLANNING)
**Trigger**: One month before IEP opens. Transition to planning phase.
**Division**: HEALTH

### Subject Line
One Month Until Your Medicare Enrollment Window Opens

### Introduction
{FirstName}, your Initial Enrollment Period opens next month. That's the 7-month window where you can enroll in Medicare — and the earlier you act within that window, the sooner your coverage starts. If this is something you need to act on, the planning phase starts now.

### Value Prop
If we've been working together, your comparison is nearly ready. We've got your prescriptions, providers, pharmacies, and healthcare data, and we're matching it against the options available for your situation. When your window opens next month, we'll be ready to walk you through your recommendation so you can enroll early and get the earliest possible coverage start date.

### Pain Point
If you haven't connected with us yet — this is the nudge. Your enrollment window opens in about 30 days, and once it does, the clock starts. Enrolling in the first 3 months of your IEP gets your coverage started on your birthday month. Wait past that and your start date gets delayed. We still have time to pull your data and build a comparison, but the window is narrowing. Let's connect.

### Email CTA
Your enrollment window opens next month. Let's make sure you're ready.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your Medicare enrollment window opens next month. If we haven't connected yet, now's the time. Let's make sure you're ready. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Your Medicare enrollment window opens next month, and I want to make sure you're in good shape. If we've been working together, your comparison is nearly ready. If we haven't connected yet, now's the time — let's get your data pulled and your options laid out before the window opens. Call me at {Phone}.

### USPS Piece
Dear {FirstName},

Your Medicare Initial Enrollment Period opens next month. Here's where you should be:

**If we've been working together:** Your comparison is nearly ready. When your window opens, we'll walk you through your recommendation and get you enrolled early for the earliest possible coverage start date.

**If we haven't connected yet:** This is the time. Your enrollment window opens in about 30 days, and enrolling in the first 3 months gives you the best coverage start date. We can still pull your data and build your comparison, but the window is narrowing.

Either way, call us at {Phone} or visit {CalendarLink}. Let's make sure you're ready.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-06 — 6 Months Out / IEP Opens (PLANNING)
**Trigger**: Client is 64 1/2. IEP opens in 3 months.
**Division**: HEALTH

### Subject Line
Medicare Is 6 Months Away — Time to Figure Out Your Plan

### Introduction
{FirstName}, we've reached out before, and whether you've had a chance to connect with us yet or not, now's the time to start thinking about this. You're 6 months out from 65, your Initial Enrollment Period opens in about 3 months, and we need to figure out together whether this is something you need to act on — or whether you're all set where you are.

### Value Prop
Here's how this works: we look at your current situation — what coverage you have, your prescriptions, your providers, your pharmacy, and how you've been using your healthcare — and we determine which path makes sense for you. Path one: you're on a qualifying employer plan, everything's covered, and you don't need to worry about it. You'll get Part A automatically, defer Part B and Part D, and we stay on top of it for when your situation changes down the road. Path two: you do need to make a decision, and we build out your full comparison of what's available through Medicare versus what you have now so you can see exactly what to expect. Either way, you'll know where you stand.

### Pain Point
The window for making the right move on Medicare has real deadlines with real consequences. If you need to enroll and you wait too long, Part B penalties are permanent — 10% added to your premium for every 12 months you could've had coverage but didn't. Part D penalties work the same way. And the guaranteed-issue window for a Medicare Supplement — where no insurance company can turn you down or charge you more for health reasons — only lasts 6 months from when your Part B starts. Miss that window and you may face medical underwriting for the rest of your life. None of this is designed to scare you. It's designed to make sure you talk to us now so we can sort it out while every option is still on the table.

### Email CTA
Let's figure out which path you're on. Pick a time and we'll walk through everything.

[Let's Connect]

### Text/SMS CTA
{FirstName}, you're 6 months from 65 and it's time to figure out your Medicare situation. You might not even need to worry about it — but we need to find out. Call or text {Phone}. We're your people on this.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. You're about 6 months out from 65 and your Medicare enrollment window opens in about 3 months. I want to connect with you and figure out whether this is something you even need to worry about. If you're on an employer plan and everything's covered, you may not need to do a thing. If you do need to make a decision, now's the time to start building your comparison. Either way, let's get it figured out. Give me a call at {Phone}.

### USPS Piece
Dear {FirstName},

You're 6 months away from turning 65, and your Medicare Initial Enrollment Period opens in about 3 months. Whether we've had a chance to connect yet or not, now is the time to figure out your plan.

Here's what we need to determine together:

**Path 1 — You may not need to worry about it:**
If you're on a qualifying employer plan (yours or a spouse's), you may be able to defer Part B and Part D without any penalty. You'll get Part A automatically, and we'll stay on top of your situation so that when things change down the road, we're ready to move.

**Path 2 — You need to make a decision:**
If you do need to enroll in Medicare, we'll pull your prescriptions, providers, pharmacy data, and your healthcare claims history. We'll build a full comparison of what's available through Medicare versus what you have now — premiums, copays, deductibles, total projected costs — so you can make the right decision with real numbers.

Here's why timing matters:
- Part B late enrollment penalties are permanent — 10% per year of delay, for life
- Part D late penalties are also permanent — 1% per month without creditable coverage
- Your Medicare Supplement guaranteed-issue window lasts only 6 months from when Part B starts — miss it and you may face medical underwriting forever

This isn't about pressure — it's about making sure every option is still available to you when the time comes. Let's figure out which path you're on.

Call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-05 — 5 Months Out / IEP Month 2 (PLANNING)
**Trigger**: IEP is open, month 2. Deepening the conversation.
**Division**: HEALTH

### Subject Line
Your Options Are on the Table — Let's Walk Through Them

### Introduction
{FirstName}, you're in month 2 of your enrollment window and your options are on the table. If we've been building your comparison, it's time to walk through the details and start narrowing down which path makes the most sense for your situation.

### Value Prop
We've looked at everything — your prescriptions, your providers, your pharmacy, your healthcare consumption — and matched it against what's available. You'll see exactly what each path costs, what's covered, and how it compares to what you have today. Original Medicare with a Supplement and a drug plan versus Medicare Advantage — we'll show you the numbers for both so you can make an informed decision, not a guess.

### Pain Point
Every month you wait within your IEP pushes things back. Enrolling now means your Part B starts on your birthday month. Waiting until your birthday month or later starts delaying your coverage. Let's get your decision locked in while the timing is optimal.

### Email CTA
Your comparison is ready. Let's walk through your options.

[Let's Connect]

### Text/SMS CTA
{FirstName}, month 2 of your enrollment window. Your comparison is ready — let's walk through your options and get your decision locked in. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. You're in month 2 of your Medicare enrollment window and your comparison is built. I want to walk you through your options so you can see exactly what each path looks like with your numbers. Give me a call at {Phone} and we'll go through it.

### USPS Piece
Dear {FirstName},

You're in month 2 of your Medicare enrollment window, and your options are on the table.

We've built your comparison using your prescriptions, providers, pharmacy, and healthcare history. You'll see:

- What Original Medicare with a Supplement and drug plan looks like for your situation
- What Medicare Advantage options are available and how they compare
- Projected costs for each path based on your actual healthcare usage
- Which path gives you the best alignment with your doctors and medications

Enrolling now means your Part B starts on your birthday month with no gap. Let's walk through the numbers and get your decision locked in.

Call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-04 — 4 Months Out / IEP Month 3 (PLANNING)
**Trigger**: Last month for optimal enrollment timing.
**Division**: HEALTH

### Subject Line
Last Month for the Best Start Date — Let's Finalize Your Plan

### Introduction
{FirstName}, this is month 3 of your enrollment window — the last month where enrolling gets your Part B coverage started on your birthday month with no gap. After this month, your coverage start date starts getting pushed back. If we've been working together and you've seen your comparison, now is the time to finalize your decision and get enrolled.

### Value Prop
Your recommendation is ready. We've shown you the numbers — what each path costs, what's covered, how it aligns with your doctors and prescriptions. Now it's about locking it in. We'll handle the enrollment, make sure everything is filed correctly, and make sure your coverage starts on time. One conversation and you're set.

### Pain Point
After this month, every month you wait adds a month of delay to your coverage start. There's no reason to wait if your decision is made. Let's get it done.

### Email CTA
This is the last month for the best start date. Let's finalize and get you enrolled.

[Let's Connect]

### Text/SMS CTA
{FirstName}, month 3 of your Medicare window — last month for your Part B to start on your birthday. Let's finalize your plan. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Quick heads-up — you're in month 3 of your Medicare enrollment window, which is the last month for your coverage to start right on your birthday with no delay. If you've seen your comparison and you're ready, let's get you enrolled. One conversation and you're done. Call me at {Phone}.

### USPS Piece
Dear {FirstName},

This is month 3 of your Initial Enrollment Period — the final month for enrolling and getting your Part B started on your birthday month with no gap.

If you've already reviewed your comparison with us, now is the time to finalize your decision and get enrolled. We'll handle everything — enrollment paperwork, plan selection, and making sure your coverage starts on time.

After this month, every month you wait pushes your coverage start date back. If your decision is made, there's no reason to wait.

Call us at {Phone} or visit {CalendarLink}. One conversation and you're set.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-03 — 3 Months Out / IEP Opens (URGENT)
**Trigger**: IEP officially opens. Months 1-3 = Part B starts birthday month (no gap).
**Division**: HEALTH

### Subject Line
Your Medicare Enrollment Window Is Open

### Introduction
{FirstName}, your Initial Enrollment Period for Medicare is officially open. This is the 7-month window where you can enroll in Medicare without penalties, and the earlier you act within this window, the sooner your coverage starts. If you enroll in the first 3 months — which is right now — your Part B coverage starts on your birthday month with no gap. If you wait past your birthday month, your start date gets pushed back and you could have a period without coverage.

### Value Prop
If you've already connected with us, we've got your data and we're running your comparison right now. What we're looking at today is what we're going to recommend for you — this isn't speculative anymore. We've got your prescriptions, providers, pharmacies, and your healthcare history, and we're matching that against every option available for your situation. Whether it's Original Medicare with a Supplement and a standalone drug plan, or a Medicare Advantage plan that bundles everything together, we'll show you exactly what each path looks like with your numbers. And if your situation means you should defer — employer coverage, spouse's plan — we'll confirm that too.

### Pain Point
If you haven't connected with us yet, now is the time. You're probably getting hit with Medicare information from every direction right now and it can feel overwhelming. Here's what you need to know: you might not even need to worry about this. But we won't know that until we look at your situation. The one thing you don't want to do is let this window pass without knowing where you stand. Connect with us — tell us "you're my people, what do I need to do?" — and we'll tell you. That's the easiest thing in the world.

### Email CTA
Your enrollment window is open. Let's connect and get this figured out.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your Medicare enrollment window is officially open. If we haven't connected yet — now's the time. You might not even need to worry about it, but let's find out. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Your Medicare enrollment window just opened, and I want to make sure we're connected. If you enroll in the next few months, your coverage starts right on your birthday with no gap. If we've already been working together, your comparison is ready and we've got a recommendation for you. If we haven't connected yet, give me a call — you might not even need to worry about this, but we need to figure that out now while every option is on the table. {Phone}. Talk soon.

### USPS Piece
Dear {FirstName},

Your Medicare Initial Enrollment Period is officially open. This is your 7-month window to enroll in Medicare — and the earlier you act, the better your position.

**Why now matters:**
If you enroll in the first 3 months of your IEP (which is right now), your Part B coverage starts on your birthday month — no gap, no delay. If you wait past your birthday month, your coverage start date gets pushed back, and you could have a period without coverage.

**If we've already connected:**
Your comparison is built. We've got your prescriptions, providers, pharmacies, and healthcare history matched against every available option. We're ready to walk you through our recommendation and get you enrolled.

**If we haven't connected yet:**
Now is the time. You might not even need to worry about this — if you have qualifying employer coverage, you may be able to defer without penalty. But we need to look at your situation to know for sure. The one thing you don't want to do is let this window pass without knowing where you stand.

Here's what we need from you: connect with us, tell us what you need, and we'll handle the rest. That's the easiest thing in the world.

Call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-02 — 2 Months Out / IEP Month 5 (URGENT)
**Trigger**: Post-birthday, coverage delayed if not yet enrolled.
**Division**: HEALTH

### Subject Line
You're 2 Months Past 65 — Let's Get This Handled

### Introduction
{FirstName}, you're now 2 months past your 65th birthday, and if you haven't enrolled in Medicare yet, your enrollment window is narrowing. You have 2 months left in your Initial Enrollment Period, and every month you wait delays when your coverage can start.

### Value Prop
It's not too late. We can still pull your data, build your comparison, and get you enrolled. But we need to move on this — once your IEP closes, the next opportunity to enroll is the General Enrollment Period in January, and your coverage wouldn't start until July of the following year. Plus, you'd face permanent penalties on your Part B premium. Let's avoid all of that by getting this handled now.

### Pain Point
We know life gets busy. Maybe the timing wasn't right, maybe you were waiting on employer coverage to change, maybe it just fell off the radar. Whatever the reason, we're here and we can still get this done. But the window is closing.

### Email CTA
Two months left in your enrollment window. Let's get this done.

[Let's Connect]

### Text/SMS CTA
{FirstName}, 2 months left in your Medicare enrollment window. We can still get you set up — but we need to connect soon. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. You're about 2 months past your 65th birthday and I want to make sure your Medicare situation is handled. If you're enrolled, great — ignore this. If you're not, you've got 2 months left in your enrollment window and we need to connect before it closes. We can still get everything set up. Call me at {Phone}.

### USPS Piece
Dear {FirstName},

You're now 2 months past your 65th birthday, and we want to make sure your Medicare coverage is in order.

If you're already enrolled — great, you're all set. If you're not, your Initial Enrollment Period closes in 2 months, and we need to act.

Here's what's at stake if the window closes:
- Next enrollment opportunity: General Enrollment Period (January - March)
- Coverage wouldn't start until July
- Permanent Part B late penalty: 10% per year of delay, for life
- Permanent Part D late penalty: 1% per month without creditable coverage, for life

We can still get you enrolled, build your plan comparison, and get you on the right coverage. But we need to connect soon.

Call us at {Phone} or visit {CalendarLink}.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-01 — 1 Month Out / IEP Month 6 (URGENT)
**Trigger**: Second-to-last month of IEP.
**Division**: HEALTH

### Subject Line
Your Medicare Enrollment Window Closes Next Month

### Introduction
{FirstName}, your Initial Enrollment Period closes next month. If you haven't enrolled in Medicare yet, this is the final stretch. We need to hear from you.

### Value Prop
We can still get you set up. Even at this stage, we can pull your data, review your options, and get you enrolled before the window closes. But we need to connect now — not next week, not next month. The process is straightforward and we handle the heavy lifting. One call and we'll get it moving.

### Pain Point
Once your IEP closes, the consequences are real: you'll wait until the General Enrollment Period in January, your coverage won't start until July, and you'll pay permanent penalties on your Part B premium — 10% per year for every year you could've been enrolled. That penalty never goes away. Please call us.

### Email CTA
One month left. Let's get this handled right now.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your Medicare enrollment window closes next month. We need to hear from you. Call or text {Phone} — we'll get it handled.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. This is important — your Medicare enrollment window closes next month. If you haven't enrolled yet, we really need to connect. I can get everything set up for you, but we're running out of time. Call me at {Phone} as soon as you can.

### USPS Piece
Dear {FirstName},

Your Medicare Initial Enrollment Period closes next month. If you have not yet enrolled, we need to hear from you immediately.

We can still get you set up — one call and we'll handle the enrollment, the plan comparison, everything. But we need to do it now.

If your IEP closes without enrollment:
- You'll wait until January for the next enrollment opportunity
- Coverage won't start until July
- You'll face permanent Part B penalties — 10% per year of delay, for life
- You'll face permanent Part D penalties — 1% per month, for life

Please call us at {Phone} or visit {CalendarLink}. We're here and we'll get this done.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65-00 — Birthday Month! (ACTION)
**Trigger**: Client turns 65. Part B should be active if enrolled on time. Medigap OEP clock running.
**Division**: HEALTH
**NOTE**: Content generalized — no specific card types (works for both MedSupp+PDP and MAPD paths)

### Subject Line
Happy 65th — Welcome to Medicare

### Introduction
{FirstName}, happy birthday! Your Medicare coverage should be active and your cards should be arriving any day. This is it — you're officially on Medicare, and we want to make sure your first month goes smoothly.

### Value Prop
Here's what to do: get your new cards to your doctor's office, your pharmacy, and keep a copy for yourself. When you go to your first appointment or pick up your first prescription, everything should process under your new coverage. If anything feels off — a copay that doesn't look right, a prescription that processes differently, or a provider that doesn't recognize your new plan — call us immediately. That's what we're here for. We'll get it sorted out.

### Pain Point
If you haven't enrolled yet, here's where you stand: you're now in month 4 of your Initial Enrollment Period, which means you have 3 months left to enroll before the window closes entirely. If you miss the IEP, the next opportunity is the General Enrollment Period (January through March), and your coverage won't start until July — plus you'll face permanent penalties on your Part B premium for every year you delayed. We don't work for CMS and we don't work for Medicare — we can't enroll you in Part B for you. But we can help you get it done right now, and once it's in place, we'll handle the rest. Give us a call right away so we can get this squared away while the window is still open.

### Email CTA
Welcome to Medicare. If you need help with anything during your first month, or if you still need to get enrolled, we're here.

[Let's Connect]

### Text/SMS CTA
{FirstName}, happy 65th! Your Medicare coverage should be active and cards on the way. If anything comes up or you still need to get enrolled — call or text {Phone}. We're here.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Happy birthday! Just wanted to check in — your Medicare coverage should be active and your cards should be arriving soon. Get them to your doctor and your pharmacy, and if anything feels off during your first visits, give us a call. If you still haven't gotten enrolled yet, we really need to connect — you've got a few months left in your enrollment window and we want to get this taken care of before it closes. Call me at {Phone}. Happy 65th!

### USPS Piece
Dear {FirstName},

Happy 65th birthday — and welcome to Medicare!

If you've been working with us, your coverage is active and your cards should be arriving shortly. Here's what to do:

- **Get your cards to your providers:** Bring your new cards to your doctor's office, your pharmacy, and keep a copy for yourself
- **Use your new coverage:** Your first doctor visit and pharmacy trip should process under your new plan. Everything should be seamless.
- **Reach out if anything feels off:** If a copay seems wrong, a prescription processes differently, or a provider doesn't recognize your new coverage, call us immediately. That's what we're here for.

**If you haven't enrolled yet:**
You're now in month 4 of your Initial Enrollment Period, with 3 months remaining before the window closes. If you miss it, the next chance to enroll is the General Enrollment Period (January - March) with coverage not starting until July — and you'll face permanent penalties on your Part B premium. Please call us right away at {Phone} so we can help you get this handled.

We're here for you — this month and every month that follows.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65+1 — 1 Month After Birthday (FOLLOW-UP)
**Trigger**: First month on Medicare — how's it going?
**Division**: HEALTH

### Subject Line
Your First Month on Medicare — How's Everything Going?

### Introduction
{FirstName}, you've been on Medicare for about a month now, and we're checking in to make sure everything is working the way it should. Your first few doctor visits and pharmacy trips should have gone smoothly — but if anything felt off, we want to know about it.

### Value Prop
This is the part most agencies skip. We don't just help you pick a plan and disappear — we make sure it's actually working. If your prescriptions are processing correctly, your doctors are recognizing your new coverage, and your copays are what we projected, you're in great shape. If anything is off, we'll get it fixed.

### Pain Point
Small issues in the first month can turn into bigger problems if they're not caught early — a pharmacy that doesn't have your new plan on file, a provider billing under your old coverage, a copay that doesn't match what it should be. These are all fixable, but only if we know about them.

### Email CTA
How's your first month? If anything feels off, let us know.

[Let's Connect]

### Text/SMS CTA
{FirstName}, one month into Medicare. How's everything going? If anything feels off with your coverage, let us know. {Phone}

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. Just checking in — you've been on Medicare for about a month now. How's everything going? If your doctor visits and pharmacy trips went smoothly, great. If anything felt off, give me a call at {Phone} and we'll get it sorted out. That's what we're here for.

### USPS Piece
Dear {FirstName},

You've been on Medicare for about a month, and we're checking in to make sure everything is running smoothly.

A few things to look for:
- Are your prescriptions processing correctly at the pharmacy?
- Are your copays at the doctor what you expected?
- Is your provider recognizing your new coverage?

If everything is working perfectly — great, no action needed. If anything feels off, let us know right away so we can get it fixed while it's still a small issue.

Call us at {Phone} or visit {CalendarLink}. We're here.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}

---

## T65+2 — 2 Months After Birthday / IEP Final Month (FOLLOW-UP)
**Trigger**: IEP closing. Last chance for anyone who hasn't acted.
**Division**: HEALTH

### Subject Line
Your Enrollment Window Closes This Month — Final Check

### Introduction
{FirstName}, if you're already enrolled and settled into your Medicare coverage, this is just a check-in — you're all set and we're here if you need anything.

If you have NOT yet enrolled in Medicare, this is your last month. Your Initial Enrollment Period closes at the end of this month, and once it does, the consequences are significant.

### Value Prop
For those already enrolled: we're monitoring your coverage and we'll be in touch when it's time for your first annual review. You don't need to do anything.

For those who still need to enroll: we can still get this done. Call us today. We'll walk you through the enrollment, help you select the right plan, and get everything filed before the deadline. One call is all it takes.

### Pain Point
If your IEP closes without enrollment, here's what happens: you wait until the General Enrollment Period in January. Coverage doesn't start until July. And you'll face permanent penalties — 10% per year on Part B, 1% per month on Part D — that you'll pay for the rest of your life. Plus, you'll miss your guaranteed-issue window for a Medicare Supplement, meaning you could be denied coverage or charged higher rates based on your health. This is the last call.

### Email CTA
If you're enrolled, you're set. If you're not — this is it. Call us today.

[Let's Connect]

### Text/SMS CTA
{FirstName}, your Medicare enrollment window closes this month. If you're enrolled, you're good. If not — call us today. {Phone}. This is the last window.

### VM Script
Hey {FirstName}, this is {AgentName} with {BOBName}. If you're already on Medicare, you're all set — just checking in. If you haven't enrolled yet, I need to hear from you. Your enrollment window closes at the end of this month and after that, the penalties are permanent and you won't be able to enroll until January. Please call me at {Phone} today.

### USPS Piece
Dear {FirstName},

**If you're already enrolled in Medicare:** You're all set. We're here if you need anything, and we'll be in touch when it's time for your first annual review.

**If you have NOT enrolled in Medicare:** Your Initial Enrollment Period closes at the end of this month. This is your final opportunity to enroll without penalty.

After this month:
- Next enrollment: General Enrollment Period (January - March)
- Coverage starts: July (6+ month gap)
- Part B penalty: 10% per year of delay — permanent, for life
- Part D penalty: 1% per month — permanent, for life
- Medigap guaranteed-issue window: missed — you may face medical underwriting or denial

We can still get you enrolled today. One call. We handle everything.

Call us at {Phone} or visit {CalendarLink}. Please don't wait.

We're Your People.™

{AgentName}
{BOBName}
{Phone} | {Email}
