STAKEANDWAGER — BOUNDED ASSISTANT
Version 1.2

A desktop tool that enforces the StakeandWager governing principle.

    No claim without a stake.
    No stake without a proposition.
    No proposition without a falsifiable outcome.

The principle is enforced as refusals, not advice. A record that does not
satisfy it cannot be locked.


WHAT IT DOES

The whole cycle
    Open a record -> add evidence -> resolve -> the record stands.

Open a record
    Four gates that refuse:

      · The stake must be already spent and countable. "I will put in 200
        hours" is refused. "40 hours and a working prototype" passes.

      · The outcome must be able to come out false. "Make the harvest
        better" is refused. "20 invoices at 90% field accuracy" passes.

      · A deadline is required. An outcome with no date never resolves.

      · The verification tier is chosen now, never after the deadline.

    The claim is also classified — INFERRED, UNVERIFIED or REPORTED —
    by how it is written, so hedged language is never recorded as
    observation.

Evidence
    Append dated entries to an open record as work happens. Each entry is
    classified OBSERVED / REPORTED / INFERRED / UNVERIFIED / UNKNOWN, and an
    entry classified OBSERVED or REPORTED is refused without a source.

    Entries are appended, never altered. A closed record cannot receive them.

Resolve
    ACHIEVED / FAILED / PARTIAL / DISPUTED / EXPIRED, judged against what the
    record said rather than what would be convenient now. Resolving before the
    deadline is permitted and recorded as early.

    A resolution cannot be revised. Afterwards an account of what happened may
    be attached once - kept, dated, attributed, and never treated as evidence.

Routing
    Structures a high-consequence matter for delivery to a table that can
    act. It refuses to produce a packet until every field is supplied, and
    it never invents authority, contacts, verification or urgency.

    THIS IS NOT AN EMERGENCY SERVICE. If life, safety or property is at
    immediate risk, contact the emergency services in your country first.

The record
    Append-only. Locked records are never rewritten. No score is ever
    calculated. The sequence is shown; the person is not summarised.

    Each locked record carries a SHA-256 fingerprint. This detects later
    alteration of the file. It does not make the record immutable and is
    not described as though it does.


WHERE RECORDS ARE KEPT

    Windows   %USERPROFILE%\.stakeandwager\record.jsonl
    macOS     ~/.stakeandwager/record.jsonl
    Linux     ~/.stakeandwager/record.jsonl

One JSON object per line, appended, never rewritten. Plain text — readable
without this program, which is the point.


RUNNING FROM SOURCE

    python stakeandwager_assistant.py

Requires Python 3.10 or later. No third-party packages. Tkinter ships with
Python on Windows and macOS; on Debian or Ubuntu it may need:

    sudo apt install python3-tk


BUILDING THE EXECUTABLE

    Windows     build.bat
    macOS/Linux ./build.sh

Produces a single file in dist/ that needs no installation and no Python on
the machine it runs on.


WHAT THIS TOOL WILL NOT DO

    It will not score people.
    It will not label redemption.
    It will not convert interpretation into fact.
    It will not summarise a chain.

    Show the sequence. Refuse to summarise the person.


LIMITS, STATED PLAINLY

    The fingerprint detects alteration. It does not prevent it.
    Nothing here is immutable. It is appended, dated and not revised.
    Records are local. There is no server and nothing is transmitted.
    Tier 1 is self-reported and uncorroborated, and says so.
    This tool is a bounded observer, not the final judge of reality.


Copyright (c) 2026 Stakeandwager LLC. All rights reserved.
Authored by John Obidinma Okoli.
stakeandwager.com  ·  sw@stakeandwager.com