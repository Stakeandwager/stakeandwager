# The Stakeandwager Protocol

**Version 1.0 — September 2026**

A protocol for turning claims into commitments, commitments into work, and work
into evidence somebody can stand behind.

---

## 0. What this is

Most systems that gather human opinion measure the cheapest possible signal: a
like, a vote, a comment, a survey answer. None of these cost anything, so none of
them tell you what a person would actually do.

This protocol measures the opposite. It records what people put behind an idea
before anyone knows whether the idea works, and what reality says about it on a
date fixed in advance.

It holds no money and settles no bets. **No money changes hands on outcomes.**

Anyone may operate a table under this protocol. It does not require permission
from Stakeandwager LLC, and it does not require Stakeandwager to be involved.

---

## 1. The core rule

> **No claim without a stake.
> No stake without a proposition.
> No proposition without a falsifiable outcome.**

Everything below follows from those three clauses.

---

## 2. The table

A **table** is the unit of this protocol. It is a claim somebody has put
something behind, opened for others to put something behind too, and settled on
a stated date.

A table has nine parts. All nine are set before it opens.

| | Part | Requirement |
|---|---|---|
| 1 | **Creator** | Who is making the claim, and what standing they have to make it. |
| 2 | **Stake** | What the creator has *already* spent. Not what they intend to spend. |
| 3 | **Proposition** | What is being attempted, and for whom. |
| 4 | **Falsifiable outcome** | The specific result that would prove the claim right or wrong. |
| 5 | **Deadline** | The date the table settles. |
| 6 | **Ask** | What is requested of others. Bounded, and no larger than the stake. |
| 7 | **Verification** | Who establishes whether the outcome happened, chosen now. |
| 8 | **Terms** | What a contributor receives if their contribution matters. |
| 9 | **Follows** | The prior table this one succeeds, or nothing. |

### 2.1 The non-empty rule

**A table cannot be opened empty.** The creator must have something down before
anyone else is asked for anything.

This is the asymmetry the protocol exists to create. A request with nothing
behind it costs nothing to make, so it carries no information. A request with a
cost behind it is a signal.

The stake is measured against the ask, not against other creators. Five hours
staked against a thirty-minute ask satisfies the rule as completely as five
hundred hours against fifty. **Proportion, not size.**

### 2.2 Falsifiability

An outcome qualifies only if a reasonable person could look at the world on the
deadline and say **no**.

Qualifies: *twenty invoices processed at ninety percent field accuracy* ·
*six of eleven farmers commit two hours each* · *the module ships and runs in
production*

Does not qualify: *the product is better* · *the business is healthier* ·
*people are more engaged* · *significant progress is made*

If it cannot come out false, it is not a proposition. It is a wish.

### 2.3 The state lock

**When a table opens, its nine parts are fixed.** No part may be edited,
clarified, softened or reinterpreted afterwards.

This is the single most important rule in the protocol, because every other
guarantee depends on it. A creator who can adjust the criteria after seeing the
result has not been tested by anything.

A table that turns out to be badly specified is not repaired. It resolves against
what it said, and a successor may say it better.

---

## 3. What can be staked

Valid: **measurable effort** — hours, work already completed · **tangible
assets** — equipment, land, materials, access under the staker's control ·
**public reputation** — a claim made under a real and traceable identity.

Not valid: **vague promises** — "I'll try to help", "I'll see what I can do" ·
**third-party actions** — anything depending on someone who has not themselves
staked it · **unverifiable claims** — specific but impossible to check ·
**unregulated cash** — money placed on an outcome. This protocol does not settle
in money.

---

## 4. The four states

These are distinct and must never be collapsed into one another.

**Interest** — somebody read it and reacted. Costs nothing. Evidence of nothing.

**Commitment** — somebody agreed to put a specific, bounded thing behind it.

**Completion** — the committed thing was actually delivered.

**Escalation** — a contributor voluntarily increased their commitment **without
being asked**. A commitment produced by a request, reminder or incentive is
solicited, and must be recorded as such.

> interest ≠ commitment ≠ completion ≠ escalation ≠ success

Every record must distinguish **solicited** from **organic**. A system that
cannot tell the difference between people responding to a mechanism and people
responding to a person is measuring the operator, not the protocol.

---

## 5. Contribution classes

**Advice** — voluntary, no ownership implied, no obligation either way. The
creator may use it freely. Suitable for small bounded asks.

**Contribution** — a defined deliverable, with terms agreed *before work begins*.

**Co-build** — a sustained role, with terms agreed *before work begins*.

Above the advice class, terms are not optional. A contribution that matters and
was made under no stated terms becomes a dispute the moment it succeeds. An
explicit *nothing* is acceptable. Silence is not.

---

## 6. Verification

Chosen when the table opens. Never after.

**Tier 1 — Creator attestation.** The creator reports the result. The record
states plainly that this is not independent. Adequate for small asks where the
stakes do not justify the cost of verifying.

**Tier 2 — Public trace.** A record a third party already produces: a filing, a
commit, a shipment, a weighbridge slip, a live URL.

**Tier 3 — Independent attestation.** A named third party — auditor, registry,
custodian — attests, paid for directly by the creator. The record shows who
attested and when.

Deciding *after* the deadline how something will be verified is another way of
moving the goalposts, and the protocol treats it as such.

**Verification is not custody.** An attestation establishes that something was
true on a date. It does not lock the asset, and it must never be described as
though it does.

---

## 7. Resolution

On the deadline the table resolves and closes. One of:

**ACHIEVED** · **FAILED** · **PARTIAL** · **DISPUTED** · **EXPIRED**

**Every result is published, whichever way it goes.** A registry that publishes
only its successes is an advertisement.

The result is published together with the stake, the ask, the outcome as
originally written, and the verification tier — so a reader can judge for
themselves what the result was worth.

Closed tables are not revised. Any correction appears as a new, dated entry
alongside the original, never as an edit of it.

---

## 8. Succession

A closed table may be followed. The original stays closed and unchanged.

A successor is a **new table** and must satisfy every requirement in §2 on its
own — its own creator, stake, proposition, falsifiable outcome and deadline.

Two kinds, and they must never be conflated:

**Self-succession** — the original creator returns to their own outcome.

**Independent succession** — a different creator takes up the problem. Recorded
as independent. It is not the first creator's continuation and must never be
displayed as though it were.

A successor may follow any resolution, not only a failure. Restricting succession
to failure would frame it as a redemption mechanism, which this protocol
explicitly refuses to be.

---

## 9. Narrative

A creator may attach an account of what they think happened.

It is **preserved, timestamped, attributed, and visibly separated from the
record**. It is never evidence, never part of the resolution, and never alters
what was recorded.

It also cannot be revised once attached. An explanation edited after the fact is
a prediction written backwards.

> **Don't explain the past into submission. Put the explanation back on the
> table.**

If a creator believes their account, the protocol offers a way to find out: make
it the proposition of the next table, put something behind it, and let reality
answer. That converts an unfalsifiable story into a testable claim, which is the
whole method applied to itself.

---

## 10. What this protocol will not do

**It will not score people.** No reputation number, no rating, no trust
percentage. A score compresses away the stakes, the sizes, the dates and the
reasons, and then readers trust the number instead of looking.

**It will not label redemption.** The record can show *they failed, then came
back and put something else down*. Whether that constitutes redemption is the
reader's judgment, not the institution's.

**It will not convert interpretation into fact.** Participants may interpret.
The institution records.

**It will not summarise a chain.** Where a summary is tempting, the sequence is
shown instead — every table, its stake, its outcome, in order.

> **Show the sequence. Refuse to summarise the person.**

---

## 11. Anti-gaming

**Retreat is visible.** A chain reading 500 hours failed → 20 hours → 15 minutes
tells the reader everything without anyone judging it. Because stakes are always
shown at actual size, a chain cannot be inflated without actually staking more.

**Succession cannot be inherited.** Only the original creator may open a
self-succession. Anyone else's is independent, and labelled so.

**Narrative cannot become evidence.** It is free to write, so it counts for
nothing.

**Founder influence is disclosed.** Where the operator personally solicited a
commitment, the record says so.

**Falsifiability is enforced at entry**, not argued about at resolution.

---

## 12. Disputes

A result may be marked **DISPUTED**. That is a state, not a verdict, and it does
not reopen the table.

The protocol does not adjudicate. Whoever disputes may state their position, and
it is recorded as narrative under §9. The stronger remedy is the one the protocol
is built for: open a successor and settle it with evidence.

---

## 13. Stop conditions

Any operator running this protocol as an experiment states, **before beginning**,
what result would make them stop.

For the first implementation: two cohorts maximum. If the first produces no
unprompted escalation, one further cohort with a materially different framing. If
that also produces none, stop.

A stop condition written after the results are in is not a stop condition.

---

## 14. Limits of this version

Stated plainly, because a protocol that hides its own weaknesses cannot ask
anyone else for rigour.

**The lock is enforced in the interface, not on a server.** Until records are
held server-side, a published table is a claim rather than an enforced fact.

**Tier 1 is self-reported.** It says so, but a reader should weight it
accordingly.

**Public-trace verification excludes the undocumented.** Informal businesses,
unregistered land, cash economies — real problems that leave no public trace.
Any archive built on this protocol will over-represent the formal economy until
that is solved.

**No implementation has yet resolved a table.** As of this version, the protocol
is a specification, not a finding.

---

## 15. Using this protocol

You do not need permission.

Open a table under the rules in §2. Set your stake, your proposition, your
falsifiable outcome, your deadline and your verification tier before you invite
anyone. Publish the result on the date, whichever way it goes. Keep the record
where others can check it.

If you want your table to sit in the same record as others, and to be available
for succession by people you have never met, send it to
**sw@stakeandwager.com**.

---

*Stakeandwager Protocol v1.0 — September 2026*
*Authored by John Obidinma Okoli · Stakeandwager LLC · stakeandwager.com*

*This document may be quoted and referred to freely. The protocol may be
implemented by anyone. Stakeandwager(TM) is a trademark of Stakeandwager LLC.*