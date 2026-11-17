# Before and after

Worked examples for the rules in [ANTI-SLOP.md](../ANTI-SLOP.md). Each pair shows a pattern and a rewrite. Load this file with the rules: a model follows an example more reliably than an instruction.

Two things to know when reading the pairs:

- Where a rewrite contains a detail the original lacks, assume the detail was in the source material. Never invent one. When no fact is available, the right rewrite is a simpler sentence or a deletion, and several pairs below show that.
- The rewrites are not the only correct answers. They show the direction: say the thing, name the actor, end on a fact.

Every rewrite on this page passes `tools/slopcheck.py`.

## Strong tells

### Contrast that adds weight and no claim

**Before**

> The layoffs aren't about cutting costs. They're about survival.

**After**

The company has enough cash to cover four more months of payroll, and the layoffs extend that to nine.

**Before**

> This isn't just a software update. It's a statement about where the industry is headed.

**After**

The update removes the headphone setting that 40 percent of users had turned on.

**Before**

> The mayor did not lose because voters disliked her. She lost because turnout collapsed.

**After**

Turnout fell from 41 percent to 23 percent, and the mayor lost by 900 votes.

### Negative listing

**Before**

> Not a merger. Not a partnership. A takeover.

**After**

The deal is a takeover. The buyer gets seven of the nine board seats.

### Closers that repeat the point

**Before**

> The agency approved the drug in six months, half the usual time. Let that sink in.

**After**

The agency approved the drug in six months, half the usual time.

**Before**

> Rents in the city rose 18 percent in a year while wages rose 3 percent. That is the real story of this economy.

**After**

Rents in the city rose 18 percent in a year while wages rose 3 percent. A tenant earning the median wage now spends 44 percent of it on rent.

**Before**

> Whether the new rules will work remains to be seen.

**After**

The rules take effect on March 1, and the first compliance reports are due in June.

### Dramatic fragments

**Before**

> No warning. No hearing. No appeal. The permits were simply gone.

**After**

The county revoked the permits without a hearing, and the ordinance gives owners no right to appeal.

**Before**

> One email. That's it. That's all it took.

**After**

A single email to the wrong address exposed the records of 12,000 patients.

### Sayings that sound deep

**Before**

> At its core, the dispute is about trust. Data is the currency of the modern economy.

**After**

The retailer sold location data from its loyalty app to a broker, and members found out from a news report.

**Before**

> The real question is whether the school board is ready for change.

**After**

Four of the seven board members have said they will vote against the new schedule.

### Run-ups before the point

**Before**

> Here's the thing about the new stadium deal. Let's break it down.

**After**

The stadium deal commits the city to $300 million in bonds and gives the team all parking revenue for 30 years.

**Before**

> The uncomfortable truth is that most startups fail. What nobody tells you is why.

**After**

About two in three funded startups return less than investors put in. The most common cause founders report is running out of cash before finding customers.

### Colon reveals

**Before**

> The catch: none of it is refundable.

**After**

None of the fees are refundable.

**Before**

> The best part: taxpayers are covering the bill.

**After**

Taxpayers are covering the $4 million bill.

### Arguing with no one

**Before**

> To be clear, this is not to say that remote work is perfect. But the data points one way.

**After**

In the company's own survey, remote teams shipped as many releases as office teams and quit at half the rate.

**Before**

> Some might say the fine is too small to matter.

**After**

The fine equals about three hours of the company's revenue.

### Questions answered at once

**Before**

> The result? Chaos.

**After**

Two hundred flights were canceled before noon.

**Before**

> So why does this matter? Because your password is probably in the leak.

**After**

The leak includes 180 million passwords, and anyone who reused one on another site should change it there.

### Chat and model residue

**Before**

> Great question! Here is a summary of the hearing. I hope this helps.

**After**

The committee heard five hours of testimony and postponed its vote to next week.

**Before**

> While specific details are limited, the founder likely grew up in the Midwest.

**After**

(Cut the sentence. The sources say nothing about where the founder grew up.)

## Inflation and borrowed authority

### Importance claims

**Before**

> The ruling marks a pivotal moment for tenants and sends a clear message to landlords.

**After**

The ruling bars landlords in the state from charging application fees above $50.

**Before**

> The stakes are high for the region's farmers.

**After**

The region's farmers grow a third of the country's almonds, and the canal that waters them is at 20 percent of capacity.

### Bolted-on -ing clauses

**Before**

> The airline cut 30 routes, highlighting the pressures facing the industry.

**After**

The airline cut 30 routes after fuel costs rose 22 percent in a quarter.

**Before**

> Three directors resigned, raising questions about the company's future.

**After**

Three directors resigned in a week. The board now lacks the five members its bylaws require to approve a sale.

### Unnamed authority

**Before**

> Experts say the bridge is unsafe.

**After**

The state's chief bridge engineer, Dana Ruiz, told the committee that two support cables have corroded through.

**Before**

> Critics argue the plan favors developers.

**After**

(Cut the sentence. The sources name no critic and quote no argument.)

### Vague connection

**Before**

> The senator is linked to the lobbying firm.

**After**

The senator's brother founded the lobbying firm, and the senator held shares in it until 2022.

### Dodging is, are, and has

**Before**

> The warehouse serves as a hub for the company's regional operations and boasts 400 loading bays.

**After**

The warehouse is the company's regional hub and has 400 loading bays.

### False agency

**Before**

> The decision to close the plant emerged after months of review.

**After**

The chief executive decided to close the plant after the board reviewed its losses for six months.

**Before**

> The market punished the stock.

**After**

Investors sold, and the stock fell 14 percent by the close.

### Sweeping claims

**Before**

> Everyone knows the subway is unreliable.

**After**

One subway train in five ran late last year, by the transit agency's count.

### Synonym cycling

**Before**

> The automaker recalled 90,000 trucks. The Detroit giant said the vehicles had faulty brakes. The car company will notify owners by mail.

**After**

The automaker recalled 90,000 trucks with faulty brakes and will notify owners by mail.

## Whole paragraphs

### A news item

**Before**

> In a move that underscores the shifting landscape of urban transit, the city council voted Tuesday to end free bus service — a decision that has sparked fierce debate. This isn't just about fares. It's about who the city is for. Critics argue the change will hit low-income riders hardest, while supporters say the system simply cannot survive without revenue. The stakes are high. Only time will tell whether the gamble pays off.

**After**

The city council voted 6 to 3 on Tuesday to end free bus service and bring back a $1.50 fare on July 1. The transit agency told the council it faces a $14 million shortfall next year and that fares would cover about half of it. Council member Lee Park, who voted no, said riders in her district earn a median of $31,000 and take the bus twice as often as riders elsewhere in the city. The agency will report ridership to the council in October.

What changed: the opening clause and the dash went, and the vote count and the fare took their place. The contrast, the unnamed critics and supporters, the stakes line, and the closer were replaced by the shortfall, a named council member, and a date.

### A product announcement

**Before**

> We're thrilled to unveil a game-changing update that empowers teams to streamline their workflows. Here's the thing: collaboration is hard. That's why we've reimagined search from the ground up, leveraging cutting-edge technology to deliver a seamless, intuitive experience. Faster. Smarter. Better.

**After**

Search now covers comments and attachments as well as document titles. Results appear as you type, and in our tests the median query returned in 80 milliseconds, down from 600. Press the slash key on any page to try it.

What changed: every claim about feelings and quality went. What the feature does, one measured number, and how to use it remain.

### A personal essay

**Before**

> I'll be honest: leaving my job was the hardest decision I've ever made. It wasn't about the money. It was about meaning. What most people miss is that burnout doesn't arrive all at once. It creeps in. Slowly. Quietly. And then one day you realize you're not the same person anymore. That realization changed everything.

**After**

I quit in March, eleven years in, with no job waiting. The money was fine. What I could not stand was the Sunday feeling, which had started arriving on Saturday morning. I noticed it the day my daughter asked why I was already sad and it was only breakfast.

What changed: the staged candor, the contrast, the lone-expert setup, and the fragments went. The writer's own details carry the feeling, and the last line is something that happened.
