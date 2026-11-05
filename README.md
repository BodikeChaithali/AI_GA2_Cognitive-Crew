# AI_GA2 — Cognitive Crew

Group assignment (GA2) for Artificial Intelligence. The repository has three problems:

| Folder | Problem | Topic | Tools |
|--------|---------|-------|-------|
| [`PS1/`](PS1) | Problem 1 | Smart-home energy **Bayesian Network**: inference, conditional independence, synthetic data, parameter learning | Python, NumPy, pandas, Matplotlib, seaborn, NetworkX |
| [`PS2/`](PS2) | Problem 2 | **Mars Rover** sample collection planning in **PDDL** | PDDL, Python (custom planner), C++ |
| [`PS3/`](PS3) | Problem 3 | **Royal Archive** access verification by **resolution refutation** | SWI-Prolog |

## Team

| Name | Roll No. |
|------|----------|
| Bodike Chaithali | B24CS013 |
| Kotapati Sai Mounika | B24CS019 |
| Bailapudi Kusuma Teja | B24CS011 |
| Lanka Devi Satwika | B24DS013 |
| Boorada Jayasurya | B24MT010 |

## Repository structure

```
AI_GA2_Cognitive-Crew/
├── PS1/
│   ├── PS1.ipynb
│   └── Screenshots/            (8 output screenshots)
├── PS2/
│   ├── Q2_Mars_Rover.ipynb
│   ├── Domain.pddl
│   ├── Problem.pddl
│   ├── Problem_extended.pddl
│   ├── bfs_proof.cpp
│   ├── Report.txt
│   ├── planner_output.txt
│   ├── plan_scenario1_gbfs.txt / _astar.txt / _bfs.txt
│   ├── plan_scenario2_gbfs.txt / _astar.txt
│   └── Screenshots/            (validation, scenario, comparison and analysis outputs)
└── PS3/
    ├── royal_archive_access.pl
    └── Screenshots/Output.png
```

---

## PS1 — Bayesian Network for Smart-Home Energy

Everything is in `PS1/PS1.ipynb`, in five parts. Inference is implemented from scratch (enumeration over the joint distribution), without a Bayesian-network library.

**Network (6 variables, 6 edges)**

- Variables and states: `Weather` (Hot/Mild/Cold), `DayType` (Weekday/Weekend), `Occupancy` (High/Low), `AC` (On/Off), `ApplianceLoad` (Heavy/Light), `EnergyConsumption` (High/Low).
- Edges: `DayType → Occupancy`, `Weather → AC`, `Occupancy → AC`, `Occupancy → ApplianceLoad`, `AC → EnergyConsumption`, `ApplianceLoad → EnergyConsumption`.
- All expert CPTs are stored in the notebook and checked to sum to 1.

**Part A — Expert network.** The inference function computes the seven queries below. Q1 is also worked out by hand (law of total probability) and matches the code. Q6 vs Q7 is discussed as *explaining away*.

| Query | Meaning | Result |
|-------|---------|--------|
| Q1 | P(Energy=High) | 0.580631 |
| Q2 | P(Energy=High \| Weather=Hot) | 0.706266 |
| Q3 | P(Energy=High \| DayType=Weekend) | 0.640199 |
| Q4 | P(Energy=High \| Weather=Cold, Occupancy=High) | 0.484250 |
| Q5 | P(Weather=Hot \| Energy=High) | 0.608188 |
| Q6 | P(AC=On \| Energy=High) | 0.692867 |
| Q7 | P(AC=On \| Energy=High, ApplianceLoad=Heavy) | 0.649899 |

**Part B — Conditional independence** (d-separation, checked numerically):

- Weather ⊥ DayType — holds (0.5 vs 0.5).
- Weather ⊥ DayType | EnergyConsumption — does **not** hold (0.608188 vs 0.599751), because conditioning on a collider (or its descendant) opens a path.
- Weather ⊥ ApplianceLoad | Occupancy — holds (0.5 vs 0.5).

**Part C — Synthetic data.** Ancestral sampling in topological order, with datasets of 500, 5,000 and 20,000 rows (seed `42 + size`). The notebook reports empirical Weather frequencies and Weather–Occupancy combination counts for each size, with plots.

**Part D — Learning from data.** CPTs are re-estimated from each dataset with:

- **MLE** (observed conditional frequencies)
- **Bayesian / BDeu** (equivalent sample size 10)

Q1–Q7 are then re-run on every learned model.

**Part E — Comparative analysis.** Mean absolute error (MAE) against the expert answers, over Q1–Q7:

| Dataset size | MAE (MLE) | MAE (BDeu) | Lower |
|--------------|-----------|------------|-------|
| 500 | 0.015592 | 0.014685 | BDeu |
| 5,000 | 0.011020 | 0.010672 | BDeu |
| 20,000 | 0.007043 | 0.007122 | MLE |

At 500 samples the largest error is Q5 (MLE 0.040610, BDeu 0.032588). The notebook notes that Q5's evidence (Energy=High) appears in 289/500 samples, so rare evidence alone does not explain the error.

---

## PS2 — Mars Rover Sample Collection Planning (PDDL)

**Model** (`Domain.pddl`, requirements `:strips` and `:typing` only)

- Types: `location, rover, bay, rock, drill`.
- Actions: `move`, `pick-drill`, `collect-soft`, `collect-hard` (needs the drill), `deposit`.
- Two storage bays, each holding one rock, so the rover carries at most two rocks.
- Hard and soft rocks are static facts. The drill is never dropped once picked up.
- `connected` is directional. The one-way slope is the single fact `(connected sitec sited)`.

**Problems**

- `Problem.pddl` — original scenario: 7 locations (Base, SiteA–SiteF), 5 rocks, 1 drill at SiteE.
- `Problem_extended.pddl` — dust-storm scenario: adds Rock6 (soft, SiteE) and Rock7 (hard, SiteF), closes Base↔SiteB in both directions, and requires Rock1–Rock7 at Base.

**Planner** (`Q2_Mars_Rover.ipynb`). The notebook writes the PDDL files, parses and grounds them to STRIPS (162 grounded actions for the original problem, 216 for the extended one), and searches with:

- Greedy Best-First Search with h_add (satisficing)
- A\* with LM-cut (optimal)
- Breadth-First Search (optimal cross-check, scenario 1)
- Weighted A\* (w=2, LM-cut) for scenario 2, where plain A\* did not finish within the 1,800 s limit

Every plan is validated by step-by-step simulation (all rocks at Base, both bays empty, rover at Base).

**Results**

| Scenario | Configuration | Plan length | States expanded | Time |
|----------|---------------|-------------|-----------------|------|
| 1 (original) | GBFS + h_add | 34 | 78 | 0.04 s |
| 1 (original) | A\* + LM-cut | 25 | 6,741 | 34.88 s |
| 1 (original) | BFS | 25 | 332,520 | 6.96 s |
| 2 (extended) | GBFS + h_add | 61 | 722 | 0.37 s |
| 2 (extended) | A\* + LM-cut | not finished in 1,800 s | 204,000 | — |
| 2 (extended) | Weighted A\* (w=2) | 40 | 2,425 | 23.32 s |

`bfs_proof.cpp` runs an exhaustive BFS over all 22,274,690 reachable states of the extended scenario. The goal is first reached at depth 40, so the 40-action plan is optimal.

**Analysis** (full text in `PS2/Report.txt`)

- **Plan length:** the greedy plan is 9 actions (36%) longer in scenario 1 and 21 actions (52%) longer in scenario 2. It carries one rock per trip, always in Bay1.
- **Bays and drill:** optimal plans use both bays together to save round trips. The drill is picked up before any hard rock is collected.
- **Dust storm:** SiteB can only be reached from SiteD, so the rover goes Base → SiteA → SiteC → SiteD (using the one-way slope in its allowed direction) → SiteB.

Output files: `planner_output.txt` (all search output) and `plan_scenario*_*.txt`. The `plan_scenario2_astar.txt` file holds the weighted A\* plan (cost 40). `PS2/Screenshots/` contains the validation, scenario, comparison and analysis outputs.

---

## PS3 — Royal Archive: Resolution Refutation

`PS3/royal_archive_access.pl` proves **`trusted(mira)`** from the knowledge base by resolution refutation, printing every stage.

**Knowledge base**

1. An archivist who verifies a record is trusted.
2. A trusted person with access to a sealed record is permitted to inspect it.
3. Anyone who inspects a record and finds a hidden mark in it verifies it.
4. Every stored record is sealed.
5. Facts: `stored(scroll_7)`, `has_access(mira, scroll_7)`, `inspects(mira, scroll_7) ∧ finds_mark(mira, scroll_7)`, `archivist(mira)`.

**Steps printed by the program**

1. Predicate-logic representation
2. Negation of the goal (`¬trusted(mira)`)
3. Implication removal
4. Moving negation inward (De Morgan)
5. Standardizing variables apart
6. Skolemization — none needed, there are no existential quantifiers
7. CNF clauses (the conjunctive fact splits into two unit clauses)
8. Resolution refutation, starting from the negated goal (set-of-support / linear resolution)

**Result:** the empty clause `[]` is derived in 5 resolution steps (using c1, c3, c7a, c7b and c8), so `trusted(mira)` follows from the KB. Clauses c2 and c4 are not needed. See `PS3/Screenshots/Output.png`.

---

## How to run

**PS1 and PS2 notebooks.** Python 3 with Jupyter. PS1 needs `numpy`, `pandas`, `matplotlib`, `seaborn` and `networkx`.

```bash
pip install numpy pandas matplotlib seaborn networkx jupyter
jupyter notebook PS1/PS1.ipynb
```

For PS2, open `Q2_Mars_Rover.ipynb` and run the cells in order. It writes the PDDL files, solves both scenarios, validates the plans and compiles `bfs_proof.cpp` (needs `g++`). Scenario 1 A\* takes about 35 s. The scenario-2 A\* run uses a 1,800 s limit.

**PS2 exhaustive BFS check (standalone)**

```bash
cd PS2
g++ -O2 -o bfs_proof bfs_proof.cpp && ./bfs_proof
```

**PS3 (SWI-Prolog)**

```bash
cd PS3
swipl -q -s royal_archive_access.pl -g main -t halt
```
