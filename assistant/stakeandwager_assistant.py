"""
StakeandWager — Bounded Assistant
A desktop tool that enforces the StakeandWager governing principle.

    No claim without a stake.
    No stake without a proposition.
    No proposition without a falsifiable outcome.

The principle is enforced as refusals, not advice. A record that does not
satisfy it cannot be locked.

Copyright (c) 2026 Stakeandwager LLC. All rights reserved.
Authored by John Obidinma Okoli.  sw@stakeandwager.com
"""

import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

APP_TITLE = "StakeandWager — Bounded Assistant"
VERSION = "1.2"

EVIDENCE_STATES = ["UNKNOWN", "UNVERIFIED", "UNCHECKED", "INSUFFICIENT EVIDENCE",
                   "INFERRED", "REPORTED", "OBSERVED"]
HELD_STATES = {"UNKNOWN", "UNVERIFIED", "UNCHECKED", "INSUFFICIENT EVIDENCE", "INFERRED"}
NEEDS_SOURCE = {"OBSERVED", "REPORTED"}

TIERS = [
    ("self",     "Tier 1 — I report it myself",
     "Recorded as self-reported and uncorroborated. The record says so."),
    ("trace",    "Tier 2 — A public trace proves it",
     "A filing, a commit, a shipment, a live URL. Something anyone can check."),
    ("attested", "Tier 3 — A third party attests",
     "An auditor, registry or custodian. Paid for by the creator. The record shows who and when."),
]

PALETTE = {
    "paper":  "#E7E9E6",
    "raised": "#F4F5F3",
    "ink":    "#12201C",
    "muted":  "#576461",
    "rule":   "#B3BCB8",
    "bronze": "#8C6B33",
    "warn":   "#8A5A12",
}

PROTOCOL_TEXT = """STAKEANDWAGER — OFFICIAL CORE GOVERNING PRINCIPLE
Version 1.1

    NO CLAIM WITHOUT A STAKE.
    NO STAKE WITHOUT A PROPOSITION.
    NO PROPOSITION WITHOUT A FALSIFIABLE OUTCOME.

THE FALSIFIABILITY RULE
An outcome qualifies only if a reasonable person could look at the world on the
deadline and say NO.

  Qualifies:      twenty invoices at ninety percent field accuracy
                  six of eleven farmers commit two hours each
                  the module ships and runs in production

  Does not:       the product is better
                  the business is healthier
                  significant progress is made

If it cannot come out false, it is not a proposition. It is a wish.

THE EVIDENCE RULE
An assertion about an external state must not be presented as established fact
unless the evidence has actually been observed or supplied. Where evidence is
absent, stale, ambiguous or not independently verifiable, state the limitation.

  UNKNOWN / UNCHECKED / INSUFFICIENT EVIDENCE / UNVERIFIED are valid outcomes.

Do not substitute memory, probability, expectation, precedent, pattern matching,
assumption or narrative for missing evidence.

THE STATE LOCK
When a record is locked, its fields are fixed. No field may be edited, clarified,
softened or reinterpreted afterwards. A record that turns out to be badly
specified is not repaired. It resolves against what it said.

THE BOUNDED OBSERVER
This tool inspects, structures, challenges, classifies and records.
It is not the final judge of reality. Assistance is not independent
verification merely because the output sounds certain.

EMERGENCIES
An emergency is not whatever feels urgent.

  THIS TOOL IS NOT AN EMERGENCY SERVICE.
  If life, safety or property is at immediate risk, contact the emergency
  services in your country first. Do not fill in a form.

Where an evidenced high-consequence matter needs a stronger table, route the
proposition, stake, deadline, evidence, uncertainty, required action and
verified contact to the table that can actually act. Do not invent authority,
contact details, verification or urgency.

FAILURE
  ERROR DETECTED -> WITHDRAW -> CORRECT -> RECORD
An error is not defended merely because it was previously stated.

WHAT THIS TOOL WILL NOT DO
It will not score people. It will not label redemption. It will not convert
interpretation into fact. It will not summarise a chain.

    Show the sequence. Refuse to summarise the person.
"""


# ----------------------------------------------------------------------------
# The gates. These are the whole point: they refuse.
# ----------------------------------------------------------------------------

VAGUE_TERMS = [
    "better", "improve", "improved", "improving", "improvement",
    "successful", "success", "good", "great", "healthier", "healthy",
    "grow", "growth", "more", "less", "popular", "traction", "viable",
    "progress", "significant", "meaningful", "effective", "efficient",
    "optimise", "optimize", "enhance", "strengthen", "robust", "quality",
]

# Verbs and states that settle to yes or no on a date. Stems are matched, so
# "ship" also covers ships / shipped / shipping.
CONCRETE_STEMS = [
    "ship", "publish", "launch", "deliver", "merge", "release", "file",
    "register", "complete", "pass", "approve", "reject", "hire", "sign",
    "pay", "submit", "close", "open", "arrive", "resolve", "certif",
]
CONCRETE_WORDS = ["yes", "no", "live", "in production", "failed", "sold"]


def check_falsifiable(text):
    """Can this outcome come out false?

    Returns (ok: bool, reason: str).
    Structural check only. It never judges whether a milestone is
    worthwhile, difficult or significant - that is explicitly prohibited.
    """
    t = (text or "").strip()
    if len(t) < 3:
        return False, "No outcome supplied."

    low = t.lower()
    has_number = bool(re.search(r"\d", low))
    has_marker = (any(re.search(r"\b%s\w*\b" % re.escape(w), low) for w in CONCRETE_STEMS)
                  or any(re.search(r"\b%s\b" % re.escape(w), low) for w in CONCRETE_WORDS))
    vague_hits = [w for w in VAGUE_TERMS if re.search(r"\b%s\b" % re.escape(w), low)]

    if has_number or has_marker:
        if vague_hits and not has_number:
            return False, (
                "Contains %s, which cannot come out false. Give the number or the "
                "plain yes-or-no that settles it." % ", ".join('"%s"' % w for w in vague_hits[:3])
            )
        return True, "Contains a condition that could come out false."

    if vague_hits:
        return False, (
            "%s cannot come out false. Put a number or a plain yes-or-no in it."
            % ", ".join('"%s"' % w for w in vague_hits[:3]).capitalize()
        )

    return False, (
        "No measurable condition found. A reasonable person must be able to look "
        "at this on the deadline and say no."
    )


def check_stake(text):
    """A stake must be what has already been spent, and it must be countable."""
    t = (text or "").strip()
    if len(t) < 3:
        return False, "No stake supplied. A record cannot open empty."
    if re.search(r"\b(will|intend|plan|going to|hope to|aim to|would)\b", t, re.I):
        return False, ("This describes what you intend to spend. A stake is what has "
                       "already been spent.")
    if not re.search(r"\d", t):
        return False, ("No countable amount. Hours, money, or a thing that exists - "
                       "not a description of effort.")
    return True, "Countable and already spent."


def classify_claim(text):
    """Classify a claim by how it is written.

    Hedged language is checked FIRST: an inferential sentence almost always
    also contains a copula, so testing for assertions first would swallow it.
    """
    t = (text or "").strip()
    if not t:
        return "UNKNOWN", ["No claim supplied."]

    if re.search(r"\b(i think|i believe|i suspect|seems?|appears?|probably|likely|"
                 r"maybe|perhaps|might|could be|presumably|apparently|reportedly)\b", t, re.I):
        return "INFERRED", ["Hedged or probabilistic language. This is an inference, "
                            "not an observation, and must not be recorded as one."]

    if re.search(r"\b(definitely|certainly|obviously|clearly|proves?|proved|proven|"
                 r"undoubtedly|without doubt|guaranteed)\b", t, re.I):
        return "UNVERIFIED", ["Emphatic certainty without a stated source. Strong "
                              "wording is not evidence. Supply what was observed."]

    if re.search(r"\b(is|are|was|were|has|have|had|will|does|did|cannot|can)\b", t, re.I):
        return "UNVERIFIED", ["An assertion about an external state. It cannot be "
                              "presented as established fact until the evidence is supplied."]

    return "REPORTED", ["No independent observation source available here, so this is "
                        "recorded as reported rather than observed."]


def validate_record(rec):
    """Every refusal the governing principle requires."""
    errors = []

    if not rec.get("claim", "").strip():
        errors.append("Claim is missing.")

    ok, why = check_stake(rec.get("stake", ""))
    if not ok:
        errors.append("Stake: " + why)

    if not rec.get("proposition", "").strip():
        errors.append("Proposition is missing. No stake without a proposition.")

    ok, why = check_falsifiable(rec.get("outcome", ""))
    if not ok:
        errors.append("Falsifiable outcome: " + why)

    if not rec.get("deadline", "").strip():
        errors.append("Deadline is missing. An outcome with no date never resolves.")

    if not rec.get("tier"):
        errors.append("Verification tier not chosen. Deciding after the deadline how "
                      "something will be verified is moving the goalposts.")

    status = rec.get("evidence_status")
    if status in NEEDS_SOURCE and not rec.get("evidence", "").strip():
        errors.append("Evidence state is %s but no source was supplied." % status)

    return errors


def fingerprint(rec):
    """A hash of the locked fields.

    States plainly what it is: it detects later alteration of this file.
    It does not make the record immutable and must never be described as
    though it does.
    """
    payload = json.dumps({k: rec.get(k) for k in
                          ("claim", "stake", "proposition", "outcome",
                           "deadline", "tier", "evidence", "evidence_status",
                           "locked_at", "follows", "succession_type")},
                         sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def store_path():
    base = Path.home() / ".stakeandwager"
    base.mkdir(parents=True, exist_ok=True)
    return base / "record.jsonl"


def append_event(event):
    """The only write this program performs.

    The file is an event log. A line is appended and never altered. State is
    derived by replaying the log, so there is no code path that can rewrite
    a record after it is locked - the state lock is a property of the
    storage, not a rule the interface is asked to respect.
    """
    with store_path().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_events():
    p = store_path()
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def replay(events=None):
    """Rebuild every record from the log. Later events add; none overwrite."""
    events = read_events() if events is None else events
    records = {}
    for ev in events:
        kind = ev.get("event")
        rid = ev.get("id")

        if kind == "OPENED" or (kind is None and ev.get("claim")):
            rec = dict(ev)
            rec.setdefault("id", rid or ev.get("locked_at", ""))
            rec["evidence_log"] = []
            rec["state"] = "OPEN"
            rec["resolution"] = None
            rec["narrative"] = None
            records[rec["id"]] = rec

        elif kind == "EVIDENCE" and rid in records:
            records[rid]["evidence_log"].append({
                "at": ev.get("at"), "action": ev.get("action"),
                "evidence": ev.get("evidence"), "classification": ev.get("classification"),
            })

        elif kind == "RESOLVED" and rid in records:
            r = records[rid]
            if r["state"] == "OPEN":          # a resolution cannot be revised
                r["state"] = "CLOSED"
                r["resolution"] = ev.get("resolution")
                r["resolved_at"] = ev.get("at")
                r["resolved_early"] = ev.get("early", False)
                r["evidence_log"].append({
                    "at": ev.get("at"), "action": "Resolved " + str(ev.get("resolution")),
                    "evidence": ev.get("basis", ""), "classification": "OBSERVED"})

        elif kind == "NARRATIVE" and rid in records:
            r = records[rid]
            if not r.get("narrative"):        # an account cannot be rewritten
                r["narrative"] = {"at": ev.get("at"), "text": ev.get("text")}

    return list(records.values())


def next_id(records):
    nums = [int(r["id"].split("-")[1]) for r in records
            if isinstance(r.get("id"), str) and r["id"].startswith("SW-")
            and r["id"].split("-")[1].isdigit()]
    return "SW-%03d" % ((max(nums) + 1) if nums else 1)


RESOLUTIONS = ["ACHIEVED", "FAILED", "PARTIAL", "DISPUTED", "EXPIRED"]


def now_utc():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


# ----------------------------------------------------------------------------
# Interface
# ----------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1080x820")
        self.minsize(920, 680)
        self.configure(bg=PALETTE["paper"])
        self.records = replay()
        self.tier_var = tk.StringVar(value="")
        self._style()
        self._build()
        self._refresh_records()
        self._refresh_pickers()
        self._refresh_pickers()

    # -- chrome ------------------------------------------------------------
    def _style(self):
        s = ttk.Style(self)
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        p = PALETTE
        s.configure("TNotebook", background=p["paper"], borderwidth=0)
        s.configure("TNotebook.Tab", padding=(16, 9), font=("Segoe UI", 10))
        s.configure("TFrame", background=p["paper"])
        s.configure("TLabel", background=p["paper"], foreground=p["ink"], font=("Segoe UI", 10))
        s.configure("Header.TLabel", font=("Georgia", 19))
        s.configure("Sub.TLabel", foreground=p["muted"], font=("Segoe UI", 9))
        s.configure("Field.TLabel", font=("Segoe UI", 10, "bold"))
        s.configure("Hint.TLabel", foreground=p["muted"], font=("Segoe UI", 8))
        s.configure("TButton", font=("Segoe UI", 10), padding=(14, 8))
        s.configure("Go.TButton", font=("Segoe UI", 10, "bold"), padding=(16, 9))
        s.configure("TRadiobutton", background=p["paper"], font=("Segoe UI", 10))

    def _build(self):
        top = ttk.Frame(self, padding=(20, 15, 20, 8))
        top.pack(fill="x")
        ttk.Label(top, text="Stakeandwager", style="Header.TLabel").pack(side="left")
        ttk.Label(top, text="Bounded Assistant  ·  constitutional v%s" % VERSION,
                  style="Sub.TLabel").pack(side="left", padx=14)
        ttk.Button(top, text="The principle", command=self.show_protocol).pack(side="right")

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        self._tab_gate()
        self._tab_evidence()
        self._tab_resolve()
        self._tab_emergency()
        self._tab_record()

        foot = ttk.Frame(self, padding=(20, 0, 20, 12))
        foot.pack(fill="x")
        ttk.Label(foot, text="No money changes hands on outcomes.  ·  "
                             "© 2026 Stakeandwager LLC", style="Sub.TLabel").pack(side="left")

    def _text(self, parent, height=4):
        t = tk.Text(parent, height=height, wrap="word", font=("Segoe UI", 10),
                    bg=PALETTE["raised"], fg=PALETTE["ink"], relief="solid", bd=1,
                    padx=9, pady=8, insertbackground=PALETTE["ink"])
        t.pack(fill="x")
        return t

    def _field(self, parent, label, hint=None):
        ttk.Label(parent, text=label, style="Field.TLabel").pack(anchor="w", pady=(11, 1))
        if hint:
            ttk.Label(parent, text=hint, style="Hint.TLabel").pack(anchor="w", pady=(0, 4))

    # -- the gate ----------------------------------------------------------
    def _tab_gate(self):
        outer = ttk.Frame(self.nb)
        self.nb.add(outer, text="  Open a record  ")

        canvas = tk.Canvas(outer, bg=PALETTE["paper"], highlightthickness=0)
        scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        tab = ttk.Frame(canvas, padding=18)
        tab.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=tab, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

        ttk.Label(tab, text="Turn a claim into something that can come out false.",
                  style="Header.TLabel").pack(anchor="w")
        ttk.Label(tab, text="Every field below is a refusal. A record that does not "
                            "satisfy the principle cannot be locked.",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 6))

        self._field(tab, "The claim", "What are you asserting?")
        self.f_claim = self._text(tab, 3)

        self._field(tab, "The stake",
                    "What you have ALREADY spent. Hours, money, work finished. Not what you intend to spend.")
        self.f_stake = self._text(tab, 2)

        self._field(tab, "The proposition", "What is being attempted, and for whom. One sentence.")
        self.f_prop = self._text(tab, 2)

        self._field(tab, "The falsifiable outcome",
                    "What result would prove you wrong? Numbers, not adjectives.")
        self.f_outcome = self._text(tab, 3)

        self._field(tab, "The deadline", "The date it settles.")
        self.f_deadline = tk.StringVar()
        ttk.Entry(tab, textvariable=self.f_deadline, font=("Segoe UI", 10)).pack(fill="x")

        self._field(tab, "Who says whether it happened?", "Chosen now. Never after.")
        for key, title, note in TIERS:
            row = ttk.Frame(tab)
            row.pack(fill="x", pady=1)
            ttk.Radiobutton(row, text=title, value=key,
                            variable=self.tier_var).pack(anchor="w")
            ttk.Label(row, text="        " + note, style="Hint.TLabel").pack(anchor="w")

        self._field(tab, "Evidence / source", "What was actually observed, and where it came from.")
        self.f_evidence = self._text(tab, 2)

        row = ttk.Frame(tab)
        row.pack(fill="x", pady=(12, 0))
        ttk.Label(row, text="Evidence state:", style="Field.TLabel").pack(side="left")
        self.f_status = tk.StringVar(value="UNKNOWN")
        ttk.Combobox(row, textvariable=self.f_status, values=EVIDENCE_STATES,
                     state="readonly", width=22).pack(side="left", padx=8)
        ttk.Button(row, text="RUN THE GATE", style="Go.TButton",
                   command=self.run_gate).pack(side="right")
        self.btn_lock = ttk.Button(row, text="Lock the record", state="disabled",
                                   command=self.lock_record)
        self.btn_lock.pack(side="right", padx=8)

        self.out_gate = tk.Text(tab, height=12, wrap="word", font=("Consolas", 10),
                                bg=PALETTE["ink"], fg="#F4F5F3", relief="flat",
                                padx=12, pady=11)
        self.out_gate.pack(fill="both", expand=True, pady=(12, 4))
        self._pending = None

    def run_gate(self):
        rec = {
            "checked_at": now_utc(),
            "claim": self.f_claim.get("1.0", "end").strip(),
            "stake": self.f_stake.get("1.0", "end").strip(),
            "proposition": self.f_prop.get("1.0", "end").strip(),
            "outcome": self.f_outcome.get("1.0", "end").strip(),
            "deadline": self.f_deadline.get().strip(),
            "tier": self.tier_var.get(),
            "evidence": self.f_evidence.get("1.0", "end").strip(),
            "evidence_status": self.f_status.get(),
            "follows": None,
            "succession_type": None,
        }

        errors = validate_record(rec)
        status, notes = classify_claim(rec["claim"])

        lines = ["THE GATE", "=" * 56, "Checked: %s" % rec["checked_at"],
                 "Claim reads as: %s" % status, ""]

        if errors:
            lines.append("REFUSED")
            lines.append("")
            for e in errors:
                lines.append("  · " + e)
            lines += ["", "Nothing is locked and no resolution is authorised while the",
                      "principle is unsatisfied."]
            self.btn_lock.configure(state="disabled")
            self._pending = None
        elif rec["evidence_status"] in HELD_STATES:
            lines.append("HELD")
            lines.append("")
            lines.append("  Structurally sound. Evidence state is %s." % rec["evidence_status"])
            lines.append("  This may be locked as a record, but the claim must not be")
            lines.append("  presented as established fact.")
            self.btn_lock.configure(state="normal")
            self._pending = rec
        else:
            lines.append("STRUCTURED")
            lines.append("")
            lines.append("  The proposition can come out false, the stake is already spent,")
            lines.append("  and the verification tier was chosen before the deadline.")
            if rec["tier"] == "self":
                lines.append("")
                lines.append("  Tier 1: self-reported and uncorroborated. The record says so.")
            self.btn_lock.configure(state="normal")
            self._pending = rec

        lines += ["", "Observer notes:"]
        lines += ["  · " + n for n in notes]
        lines += ["", "This tool is a bounded observer. It is not the final judge of reality."]

        self.out_gate.delete("1.0", "end")
        self.out_gate.insert("1.0", "\n".join(lines))

    def lock_record(self):
        if not self._pending:
            return
        if not messagebox.askyesno(
                "Lock the record",
                "Once locked, no field can be edited, clarified or reinterpreted.\n\n"
                "A record that turns out to be badly specified is not repaired. It "
                "resolves against what it said.\n\nLock it?"):
            return

        rec = dict(self._pending)
        rec["event"] = "OPENED"
        rec["id"] = next_id(self.records)
        rec["locked_at"] = now_utc()
        rec["fingerprint"] = fingerprint(rec)
        append_event(rec)
        self.records = replay()
        self._refresh_records()
        self.btn_lock.configure(state="disabled")
        self._pending = None

        self.out_gate.insert("end",
                             "\n\nLOCKED %s\nFingerprint %s\nNothing above can be changed "
                             "from here.\n" % (rec["locked_at"], rec["fingerprint"][:16]))
        messagebox.showinfo("Locked", "%s recorded and appended.\n\nFingerprint: %s"
                            % (rec["id"], rec["fingerprint"][:16]))


    # -- evidence ----------------------------------------------------------
    def _tab_evidence(self):
        tab = ttk.Frame(self.nb, padding=18)
        self.nb.add(tab, text="  Evidence  ")
        ttk.Label(tab, text="Add evidence to an open record", style="Header.TLabel").pack(anchor="w")
        ttk.Label(tab, text="Entries are appended and dated. Nothing already written is "
                            "altered. A record that has closed can no longer receive evidence.",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 10))

        row = ttk.Frame(tab); row.pack(fill="x")
        ttk.Label(row, text="Record:", style="Field.TLabel").pack(side="left")
        self.ev_pick = ttk.Combobox(row, state="readonly", width=72)
        self.ev_pick.pack(side="left", padx=8)
        ttk.Button(row, text="Refresh", command=self._refresh_pickers).pack(side="left")

        self._field(tab, "What was done?")
        self.ev_action = self._text(tab, 2)
        self._field(tab, "Evidence", "A link, a file, a reference. What someone else could check.")
        self.ev_evidence = self._text(tab, 2)

        row2 = ttk.Frame(tab); row2.pack(fill="x", pady=(11, 0))
        ttk.Label(row2, text="Classification:", style="Field.TLabel").pack(side="left")
        self.ev_class = tk.StringVar(value="OBSERVED")
        ttk.Combobox(row2, textvariable=self.ev_class, state="readonly", width=22,
                     values=["OBSERVED", "REPORTED", "INFERRED", "UNVERIFIED", "UNKNOWN"]
                     ).pack(side="left", padx=8)
        ttk.Button(row2, text="APPEND", style="Go.TButton",
                   command=self.add_evidence).pack(side="right")

        self.out_ev = tk.Text(tab, height=14, wrap="word", font=("Consolas", 10),
                              bg=PALETTE["raised"], fg=PALETTE["ink"], relief="solid",
                              bd=1, padx=11, pady=10)
        self.out_ev.pack(fill="both", expand=True, pady=(12, 0))

    def add_evidence(self):
        rec = self._picked(self.ev_pick)
        if not rec:
            messagebox.showwarning("No record", "Choose an open record first.")
            return
        if rec["state"] != "OPEN":
            messagebox.showwarning("Closed", "%s has resolved. Evidence cannot be added "
                                             "to a closed record." % rec["id"])
            return
        action = self.ev_action.get("1.0", "end").strip()
        ev = self.ev_evidence.get("1.0", "end").strip()
        cls = self.ev_class.get()
        if not action:
            messagebox.showwarning("Missing", "State what was done.")
            return
        if cls in NEEDS_SOURCE and not ev:
            messagebox.showwarning(
                "Missing evidence",
                "Classification is %s but no source was supplied.\n\n"
                "Either supply what was observed, or classify this as INFERRED "
                "or UNVERIFIED." % cls)
            return

        append_event({"event": "EVIDENCE", "id": rec["id"], "at": now_utc(),
                      "action": action, "evidence": ev, "classification": cls})
        self.records = replay()
        self._refresh_records(); self._refresh_pickers()
        self.ev_action.delete("1.0", "end"); self.ev_evidence.delete("1.0", "end")
        self._show_log(rec["id"])

    def _show_log(self, rid):
        rec = next((r for r in self.records if r["id"] == rid), None)
        if not rec:
            return
        lines = ["%s  [%s]" % (rec["id"], rec["state"]), "=" * 56,
                 rec.get("proposition", ""), "",
                 "Resolves yes if: " + rec.get("outcome", ""),
                 "Settles on:      " + rec.get("deadline", ""), "", "LOG", "-" * 56]
        for e in rec.get("evidence_log", []):
            lines.append("[%s] %-11s %s" % ((e.get("at") or "")[:10],
                                            e.get("classification", ""), e.get("action", "")))
            if e.get("evidence"):
                lines.append("             %s" % e["evidence"])
        self.out_ev.delete("1.0", "end"); self.out_ev.insert("1.0", "\n".join(lines))

    # -- resolution --------------------------------------------------------
    def _tab_resolve(self):
        tab = ttk.Frame(self.nb, padding=18)
        self.nb.add(tab, text="  Resolve  ")
        ttk.Label(tab, text="Resolve a record", style="Header.TLabel").pack(anchor="w")
        ttk.Label(tab, text="A resolution is published whichever way it goes and cannot "
                            "be revised. The outcome is judged against what the record "
                            "said, not against what would be convenient now.",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 10))

        row = ttk.Frame(tab); row.pack(fill="x")
        ttk.Label(row, text="Record:", style="Field.TLabel").pack(side="left")
        self.rs_pick = ttk.Combobox(row, state="readonly", width=72)
        self.rs_pick.pack(side="left", padx=8)
        self.rs_pick.bind("<<ComboboxSelected>>", self._show_criteria)
        ttk.Button(row, text="Refresh", command=self._refresh_pickers).pack(side="left")

        self.rs_view = tk.Text(tab, height=9, wrap="word", font=("Consolas", 10),
                               bg=PALETTE["raised"], fg=PALETTE["ink"], relief="solid",
                               bd=1, padx=11, pady=10)
        self.rs_view.pack(fill="x", pady=(11, 0))

        self._field(tab, "The basis", "What establishes the outcome, at the tier chosen when it opened.")
        self.rs_basis = self._text(tab, 2)

        row2 = ttk.Frame(tab); row2.pack(fill="x", pady=(11, 0))
        ttk.Label(row2, text="Resolution:", style="Field.TLabel").pack(side="left")
        self.rs_value = tk.StringVar(value="")
        ttk.Combobox(row2, textvariable=self.rs_value, state="readonly", width=22,
                     values=RESOLUTIONS).pack(side="left", padx=8)
        ttk.Button(row2, text="RESOLVE", style="Go.TButton",
                   command=self.do_resolve).pack(side="right")

        ttk.Label(tab, text="Afterwards, an account of what happened may be attached. It "
                            "is kept, dated and attributed, and it is never evidence. If "
                            "you believe it, put it on the next record and let reality answer.",
                  style="Hint.TLabel", wraplength=940).pack(anchor="w", pady=(14, 2))
        self.rs_narr = self._text(tab, 2)
        ttk.Button(tab, text="Attach the account", command=self.add_narrative).pack(anchor="e", pady=6)

    def _show_criteria(self, _e=None):
        rec = self._picked(self.rs_pick)
        if not rec:
            return
        early = ""
        try:
            if datetime.now(timezone.utc).date() < datetime.strptime(
                    rec.get("deadline", ""), "%Y-%m-%d").date():
                early = "\n\nNOTE: today is before the deadline. Resolving now is " \
                        "recorded as an early resolution."
        except (ValueError, TypeError):
            early = "\n\nNOTE: the deadline is not a plain date, so it cannot be checked."
        self.rs_view.delete("1.0", "end")
        self.rs_view.insert("1.0",
            "%s  [%s]\n%s\n\nResolves yes if:\n  %s\n\nSettles on: %s\nVerified by: %s\n"
            "Evidence entries: %d%s" % (
                rec["id"], rec["state"], rec.get("proposition", ""),
                rec.get("outcome", ""), rec.get("deadline", ""), rec.get("tier", ""),
                len(rec.get("evidence_log", [])), early))

    def do_resolve(self):
        rec = self._picked(self.rs_pick)
        if not rec:
            messagebox.showwarning("No record", "Choose a record first.")
            return
        if rec["state"] != "OPEN":
            messagebox.showwarning("Already resolved",
                                   "%s resolved %s. A resolution cannot be revised."
                                   % (rec["id"], rec.get("resolution")))
            return
        value = self.rs_value.get()
        basis = self.rs_basis.get("1.0", "end").strip()
        if not value:
            messagebox.showwarning("Missing", "Choose a resolution.")
            return
        if not basis:
            messagebox.showwarning("Missing", "State what establishes the outcome.")
            return

        early = False
        try:
            early = datetime.now(timezone.utc).date() < datetime.strptime(
                rec.get("deadline", ""), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            pass

        if not messagebox.askyesno(
                "Resolve %s" % rec["id"],
                "Resolve as %s.\n\nThis is published whichever way it goes and cannot be "
                "revised. No further evidence can be added.\n\nProceed?" % value):
            return

        append_event({"event": "RESOLVED", "id": rec["id"], "at": now_utc(),
                      "resolution": value, "basis": basis, "early": early})
        self.records = replay()
        self._refresh_records(); self._refresh_pickers()
        self.rs_basis.delete("1.0", "end")
        self._show_criteria()
        messagebox.showinfo("Resolved", "%s resolved %s.%s" % (
            rec["id"], value, "\n\nRecorded as an early resolution." if early else ""))

    def add_narrative(self):
        rec = self._picked(self.rs_pick)
        if not rec:
            return
        if rec["state"] != "CLOSED":
            messagebox.showwarning("Not resolved", "An account is attached after the "
                                                   "record resolves, not before.")
            return
        if rec.get("narrative"):
            messagebox.showwarning("Already attached",
                                   "An account is already attached. It cannot be rewritten - "
                                   "an explanation edited afterwards is a prediction "
                                   "written backwards.")
            return
        text = self.rs_narr.get("1.0", "end").strip()
        if not text:
            return
        append_event({"event": "NARRATIVE", "id": rec["id"], "at": now_utc(), "text": text})
        self.records = replay(); self._refresh_records()
        self.rs_narr.delete("1.0", "end")
        messagebox.showinfo("Attached", "Kept, dated and attributed. It is not evidence.")

    # -- shared ------------------------------------------------------------
    def _picked(self, box):
        label = box.get()
        if not label:
            return None
        rid = label.split(" ")[0]
        return next((r for r in self.records if r["id"] == rid), None)

    def _refresh_pickers(self):
        opts = ["%s  [%s]  %s" % (r["id"], r["state"], (r.get("proposition") or "")[:60])
                for r in self.records]
        for box in (self.ev_pick, self.rs_pick):
            box["values"] = opts

    # -- emergencies -------------------------------------------------------
    def _tab_emergency(self):
        tab = ttk.Frame(self.nb, padding=18)
        self.nb.add(tab, text="  Routing  ")

        warn = tk.Frame(tab, bg="#F6EBD6", highlightbackground=PALETTE["warn"],
                        highlightthickness=1)
        warn.pack(fill="x", pady=(0, 14))
        tk.Label(warn, bg="#F6EBD6", fg=PALETTE["warn"], justify="left",
                 font=("Segoe UI", 10, "bold"),
                 text="  This is not an emergency service.").pack(anchor="w", padx=10, pady=(9, 0))
        tk.Label(warn, bg="#F6EBD6", fg=PALETTE["warn"], justify="left",
                 font=("Segoe UI", 9), wraplength=940,
                 text="  If life, safety or property is at immediate risk, contact the "
                      "emergency services in your country now. Do not fill in this form. "
                      "This tool structures a high-consequence matter for delivery to a "
                      "table that can act. It does not deliver it, and it cannot respond."
                 ).pack(anchor="w", padx=10, pady=(2, 10))

        ttk.Label(tab, text="Route a high-consequence matter", style="Header.TLabel").pack(anchor="w")
        ttk.Label(tab, text="Urgency must be evidenced. Nothing is routed on a feeling, "
                            "and no authority or contact is ever invented.",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 4))

        self._field(tab, "What is happening?")
        self.e_claim = self._text(tab, 2)
        self._field(tab, "Why is delay consequential?")
        self.e_basis = self._text(tab, 2)
        self._field(tab, "Stake / consequence")
        self.e_stake = self._text(tab, 2)
        self._field(tab, "Deadline")
        self.e_deadline = tk.StringVar()
        ttk.Entry(tab, textvariable=self.e_deadline, font=("Segoe UI", 10)).pack(fill="x")
        self._field(tab, "Evidence currently available")
        self.e_evidence = self._text(tab, 2)
        self._field(tab, "Verified contact or decision-maker",
                    "Someone you have actually confirmed. Not a guess, not a title.")
        self.e_contact = self._text(tab, 2)

        ttk.Button(tab, text="ASSESS", style="Go.TButton",
                   command=self.assess).pack(anchor="e", pady=11)
        self.out_em = tk.Text(tab, height=12, wrap="word", font=("Consolas", 10),
                              bg=PALETTE["raised"], fg=PALETTE["ink"], relief="solid",
                              bd=1, padx=11, pady=10)
        self.out_em.pack(fill="both", expand=True)

    def assess(self):
        vals = {
            "What is happening": self.e_claim.get("1.0", "end").strip(),
            "Why delay is consequential": self.e_basis.get("1.0", "end").strip(),
            "Stake / consequence": self.e_stake.get("1.0", "end").strip(),
            "Deadline": self.e_deadline.get().strip(),
            "Evidence": self.e_evidence.get("1.0", "end").strip(),
            "Verified contact": self.e_contact.get("1.0", "end").strip(),
        }
        missing = [k for k, v in vals.items() if not v]

        if missing:
            out = ["EMERGENCY STATUS: UNVERIFIED", "",
                   "Routing is blocked until the gap is made explicit:", ""]
            out += ["  · %s — UNKNOWN" % m for m in missing]
            out += ["", "Do not invent urgency, authority, contact details or a",
                    "destination table to fill these in."]
        else:
            out = ["EMERGENCY STATUS: CANDIDATE — evidence supplied", "",
                   "ROUTING PACKET", "-" * 56]
            out += ["%-28s %s" % (k + ":", v) for k, v in vals.items()]
            out += ["", "Prepared: " + now_utc(), "",
                    "Deliver this to the verified table yourself.",
                    "This tool has not sent anything and cannot.",
                    "Do not treat the matter as resolved because it has been routed."]

        self.out_em.delete("1.0", "end")
        self.out_em.insert("1.0", "\n".join(out))

    # -- the record --------------------------------------------------------
    def _tab_record(self):
        tab = ttk.Frame(self.nb, padding=18)
        self.nb.add(tab, text="  The record  ")
        ttk.Label(tab, text="The record", style="Header.TLabel").pack(anchor="w")
        ttk.Label(tab, text="Append-only. Locked records are never rewritten, and no "
                            "score is calculated from them. The sequence is shown; the "
                            "person is not summarised.",
                  style="Sub.TLabel").pack(anchor="w", pady=(3, 10))

        cols = ("id", "locked", "state", "result", "tier", "proposition")
        self.tree = ttk.Treeview(tab, columns=cols, show="headings", height=15)
        for c, w in zip(cols, (70, 160, 80, 90, 80, 420)):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._show_detail)

        self.detail = tk.Text(tab, height=9, wrap="word", font=("Consolas", 9),
                              bg=PALETTE["raised"], fg=PALETTE["ink"], relief="solid",
                              bd=1, padx=10, pady=9)
        self.detail.pack(fill="x", pady=(10, 0))

        row = ttk.Frame(tab)
        row.pack(fill="x", pady=10)
        ttk.Label(row, text="Stored at %s" % store_path(),
                  style="Sub.TLabel").pack(side="left")
        ttk.Button(row, text="Export the record", command=self.export).pack(side="right")

    def _refresh_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for n, r in enumerate(self.records):
            self.tree.insert("", "end", iid=str(n), values=(
                r.get("locked_at", "—"), r.get("state", "—"),
                r.get("tier", "—"), (r.get("proposition", "") or "")[:90]))

    def _show_detail(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        r = self.records[int(sel[0])]
        lines = []
        for k in ("locked_at", "state", "claim", "stake", "proposition", "outcome",
                  "deadline", "tier", "evidence", "evidence_status",
                  "follows", "succession_type", "fingerprint"):
            if r.get(k) not in (None, ""):
                lines.append("%-17s %s" % (k + ":", r.get(k)))
        intact = fingerprint(r) == r.get("fingerprint")
        lines.append("")
        lines.append("Fingerprint %s" % ("matches — this line has not been altered since "
                                         "it was written." if intact else
                                         "DOES NOT MATCH — this line has been altered."))
        self.detail.delete("1.0", "end")
        self.detail.insert("1.0", "\n".join(lines))

    def export(self):
        if not self.records:
            messagebox.showinfo("Export", "Nothing recorded yet.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")],
            initialfile="stakeandwager_record.json")
        if not path:
            return
        Path(path).write_text(json.dumps(self.records, indent=2, ensure_ascii=False),
                              encoding="utf-8")
        messagebox.showinfo("Exported", "Written to:\n%s" % path)

    def show_protocol(self):
        win = tk.Toplevel(self)
        win.title("The governing principle")
        win.geometry("860x700")
        win.configure(bg=PALETTE["paper"])
        t = tk.Text(win, wrap="word", font=("Consolas", 10), bg=PALETTE["raised"],
                    fg=PALETTE["ink"], padx=16, pady=15, relief="flat")
        t.pack(fill="both", expand=True, padx=14, pady=14)
        t.insert("1.0", PROTOCOL_TEXT)
        t.configure(state="disabled")


def main():
    App().mainloop()


if __name__ == "__main__":
    main()