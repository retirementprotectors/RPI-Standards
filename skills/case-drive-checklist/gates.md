# Case-Drive Checklist — Gates

> Hookify enforcement map for this skill. Rules are referenced BY NAME only —
> never duplicated here. Hookify (`_RPI_STANDARDS/hookify/`) is the SSOT for
> all literal patterns and enforcement logic.

## Gate #1 — Firestore True-Up (MEGAZORD lane)

**What the gate enforces:** Every carrier-confirmed correction must flow through
MEGAZORD's write path. Fields must be typed and schema-matched before any write.

**Enforcing hookify rules:**

| Rule | Why it applies |
|------|---------------|
| `block-untyped-firestore-fields` | Blocks Firestore set/update calls that write untyped fields — prevents schema drift when MEGAZORD corrects carrier-confirmed values (DOB, account balances, rider status, beneficiaries). |
| `block-direct-firestore-write` | Enforces that Firestore writes go through the sanctioned write path, not ad-hoc `db.collection().set()` calls — prevents VOLTRON from bypassing MEGAZORD's lane at the code level. |

## Gate #2 — ACF True-Up (Document file)

**What the gate enforces:** Client case documents (carrier statements, illustrations,
signed forms, beneficiary forms) must NEVER be committed to the toMachina repo.
They live in the inbox/funnel only.

**Enforcing hookify rules:**

| Rule | Why it applies |
|------|---------------|
| `block-case-roadmap-in-repo` | Blocks any client case file (HTML/PDF) written under `docs/cases/` in the toMachina repo — prevents PHI exposure via GitHub Pages (the incident that triggered this rule on 2026-06-12: 28 client case files were briefly public). ACF documents are filed to the inbox/funnel, never the repo. |

---

> **To add a new enforcing rule:** author it in `_RPI_STANDARDS/hookify/` per the
> hookify process (requires SHINOB1 review), then add a row to the relevant gate
> table above. Never define rule patterns here.
