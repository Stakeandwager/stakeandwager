# Stakeandwager

**A protocol for turning claims into commitments, commitments into work, and
work into evidence somebody can stand behind.**

    No claim without a stake.
    No stake without a proposition.
    No proposition without a falsifiable outcome.

Most systems that gather human opinion measure the cheapest possible signal — a
like, a vote, a comment. None of them cost anything, so none of them tell you
what a person would actually do.

This records what people put behind an idea before anyone knows whether it
works, and what reality says about it on a date fixed in advance.

**No money changes hands on outcomes.** This holds no funds, operates no
escrow, and settles nothing in cash.

---

## What's here

| | |
|---|---|
| [`PROTOCOL.md`](PROTOCOL.md) | The governing principle. Version 1.1. What a table is, what can be staked, the four states, verification tiers, resolution, succession, and what this will not do. |
| [`OPERATING-GUIDE.md`](OPERATING-GUIDE.md) | How to actually run a table. Writing an outcome that can come out false, finding people, recording what happens, resolving on the date. |
| [`PARTICIPATION-POLICY.md`](PARTICIPATION-POLICY.md) | Who may sit at a table and what will never be asked of them. Adults only. Nothing collected beyond a handle and an email. |
| [`BRIEFING-NOTE.md`](BRIEFING-NOTE.md) | For anyone — or anything — asked to build under this principle. |
| [`assistant/`](assistant/) | A desktop tool that enforces the protocol as refusals. Python, no dependencies, builds to a single executable. |
| `index.html` | The site. [stakeandwager.com](https://stakeandwager.com) |

---

## The assistant

The documents ask people to behave a certain way. Prose can only request. The
assistant is the same rules expressed as conditions of proceeding.

    python assistant/stakeandwager_assistant.py

It refuses a stake that hasn't been spent — *"I will put in 200 hours"* is
rejected, *"40 hours and a working prototype"* passes. It refuses an outcome
that cannot come out false — *"make the harvest better"* is rejected, *"20
invoices at 90% field accuracy"* passes. It requires a deadline, and a
verification tier chosen before the deadline rather than after.

Records are written to an append-only event log. Opening, evidence and
resolution are each a separate line, and state is rebuilt by replaying them —
so there is no code path that rewrites a record after it is locked. The state
lock is a property of the storage, not a rule the interface is asked to respect.

`assistant/build.bat` produces a Windows executable. `build.sh` does the same on
macOS and Linux.

---

## Using this protocol

You do not need permission.

Open a table under the rules in the protocol. Set your stake, your proposition,
your falsifiable outcome, your deadline and your verification tier before you
invite anyone. Publish the result on the date, whichever way it goes. Keep the
record where others can check it.

To have a table sit in this record, send it to **sw@stakeandwager.com**.

---

## Limits, stated plainly

A project that hides its own weaknesses cannot ask anyone else for rigour.

**The lock in the browser is a claim, not a fact.** Until records are held
server-side, a table published on the site is enforced by the interface rather
than by the storage. The assistant's event log is stronger; the site's is not.

**Tier 1 is self-reported.** It says so, and a reader should weight it
accordingly. The protocol records who attested. It does not establish their
independence.

**Registry canonicity is unsolved.** There is currently one submission route
and one person at the end of it. The protocol claims anyone may implement it,
and that is true — but appearing in *this* record still passes through a single
point. Registered as an open gap, not closed.

**Nothing here is immutable.** Records are appended, dated and not revised. That
is a discipline, not a cryptographic guarantee.

**No table has resolved yet.** As of this version, this is a specification, not
a finding.

---

    Show the sequence. Refuse to summarise the person.

---

Copyright © 2026 Stakeandwager LLC. All rights reserved.
Authored by John Obidinma Okoli. See [`LICENSE`](LICENSE).

The protocol may be implemented by anyone. Stakeandwager™ is a trademark of
Stakeandwager LLC.

[stakeandwager.com](https://stakeandwager.com) · sw@stakeandwager.com