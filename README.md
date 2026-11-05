# AI_GA2 — Cognitive Crew

Group Assignment 2 (GA2) for Artificial Intelligence. This repository contains solutions to three problems covering probabilistic reasoning using Bayesian Networks, automated planning using PDDL, and logical inference using Resolution Refutation.

## Team Members

| Name | Roll No. |
|---|---|
| Bodike Chaithali | B24CS013 |
| Kotapati Sai Mounika | B24CS019 |
| Bailapudi Kusuma Teja | B24CS011 |
| Lanka Devi Satwika | B24DS013 |
| Boorada Jayasurya | B24MT010 |

## Team Contributions

| Problem | Contributors | Topic |
|---|---|---|
| PS1 | Kotapati Sai Mounika, Bailapudi Kusuma Teja | Smart-Home Energy Bayesian Network |
| PS2 | Bodike Chaithali | Mars Rover Sample Collection Planning using PDDL |
| PS3 | Lanka Devi Satwika, Boorada Jayasurya | Royal Archive Access Verification using Resolution Refutation |

---

## Repository Structure

```text
AI_GA2_Cognitive-Crew/
├── PS1/
│   ├── PS1.ipynb
│   └── Screenshots/            (8 output screenshots)
│
├── PS2/
│   ├── Q2_Mars_Rover.ipynb
│   ├── Domain.pddl
│   ├── Problem.pddl
│   ├── Problem_extended.pddl
│   ├── bfs_proof.cpp
│   ├── Report.txt
│   ├── planner_output.txt
│   ├── plan_scenario1_gbfs.txt
│   ├── plan_scenario1_astar.txt
│   ├── plan_scenario1_bfs.txt
│   ├── plan_scenario2_gbfs.txt
│   ├── plan_scenario2_astar.txt
│   └── Screenshots/
│
└── PS3/
    ├── royal_archive_access.pl
    └── Screenshots/
        └── Output.png
```

---

## PS1 — Bayesian Network for Smart-Home Energy

**Tools:** Python, NumPy, Pandas, Matplotlib, Seaborn, NetworkX

The complete implementation is available in `PS1/PS1.ipynb`, organized into five parts. Bayesian inference is implemented from scratch using enumeration over the joint distribution, without using an external Bayesian Network library.

**Network Structure (6 variables, 6 edges)**

Variables and their states:

- `Weather`: Hot / Mild / Cold
- `DayType`: Weekday / Weekend
- `Occupancy`: High / Low
- `AC`: On / Off
- `ApplianceLoad`: Heavy / Light
- `EnergyConsumption`: High / Low

Edges:

- DayType → Occupancy
- Weather → AC
- Occupancy → AC
- Occupancy → ApplianceLoad
- AC → EnergyConsumption
- ApplianceLoad → EnergyConsumption

All expert-defined CPTs are stored in the notebook and validated to ensure that their probabilities sum to 1.

### Part A — Expert Network and Inference

An inference function computes the following seven queries. Q1 is also derived manually using the Law of Total Probability and verified against the implementation.

| Query | Description | Result |
|---|---|---:|
| Q1 | P(Energy=High) | 0.580631 |
| Q2 | P(Energy=High \| Weather=Hot) | 0.706266 |
| Q3 | P(Energy=High \| DayType=Weekend) | 0.640199 |
| Q4 | P(Energy=High \| Weather=Cold, Occupancy=High) | 0.484250 |
| Q5 | P(Weather=Hot \| Energy=High) | 0.608188 |
| Q6 | P(AC=On \| Energy=High) | 0.692867 |
| Q7 | P(AC=On \| Energy=High, ApplianceLoad=Heavy) | 0.649899 |

Q6 and Q7 are compared to demonstrate the concept of *explaining away*.

### Part B — Conditional Independence

Conditional independence properties are examined using d-separation and verified numerically.

- Weather ⊥ DayType — holds (0.5 vs. 0.5).
- Weather ⊥ DayType | EnergyConsumption — does not hold (0.608188 vs. 0.599751), due to conditioning on a collider or its descendant.
- Weather ⊥ ApplianceLoad | Occupancy — holds (0.5 vs. 0.5).

### Part C — Synthetic Data Generation

Synthetic datasets are generated using ancestral sampling in topological order.

Dataset sizes:

- 500 samples
- 5,000 samples
- 20,000 samples

Random seeds are set to `42 + dataset_size` for reproducibility. The notebook reports empirical Weather frequencies and Weather–Occupancy combination counts for each dataset, along with corresponding visualizations.

### Part D — Parameter Learning

CPTs are re-estimated from each synthetic dataset using:

- **Maximum Likelihood Estimation (MLE):** Based on observed conditional frequencies.
- **Bayesian Estimation (BDeu):** Uses an equivalent sample size (ESS) of 10.

All seven inference queries (Q1–Q7) are evaluated again using each learned model.

### Part E — Comparative Analysis

The learned models are compared against the expert network using Mean Absolute Error (MAE) across Q1–Q7.

| Dataset Size | MAE (MLE) | MAE (BDeu) | Better Method |
|---|---:|---:|---|
| 500 | 0.015592 | 0.014685 | BDeu |
| 5,000 | 0.011020 | 0.010672 | BDeu |
| 20,000 | 0.007043 | 0.007122 | MLE |

**Observations:**

- Both methods generally improve as the dataset size increases.
- BDeu performs better for 500 and 5,000 samples, while MLE performs marginally better for 20,000 samples.
- For the 500-sample dataset, Q5 has the largest error (MLE: 0.040610, BDeu: 0.032588).
- The evidence `Energy=High` occurs in 289 out of 500 samples, indicating that rare evidence alone does not explain the estimation error.

---

## PS2 — Mars Rover Sample Collection Planning using PDDL

**Tools:** PDDL, Python (Custom Planner), C++

The implementation is available in `Q2_Mars_Rover.ipynb`, along with the domain, problem files, planner outputs, and supporting C++ implementation.

### Domain Model

`Domain.pddl` uses the `:strips` and `:typing` requirements.

**Types:** `location`, `rover`, `bay`, `rock`, `drill`.

**Actions:**

- `move`
- `pick-drill`
- `collect-soft`
- `collect-hard`
- `deposit`

The rover has two storage bays, each holding one rock. Hard and soft rock classifications are static facts, and the drill is never dropped once acquired.

Connectivity is directional, with the one-way slope represented by `(connected sitec sited)`.

### Problem Scenarios

- **Scenario 1 — `Problem.pddl`:** Contains seven locations (Base and SiteA–SiteF), five rocks, and one drill initially located at SiteE.
- **Scenario 2 — `Problem_extended.pddl`:** Introduces Rock6 (soft, SiteE) and Rock7 (hard, SiteF), blocks Base↔SiteB in both directions, and requires all seven rocks to be transported to the Base.

### Planner Implementation

The notebook generates the PDDL files, parses and grounds them into STRIPS representations, and executes the following search algorithms:

- Greedy Best-First Search (GBFS) with h_add — satisficing search.
- A* with LM-cut — optimal search.
- Breadth-First Search (BFS) — optimality cross-check for Scenario 1.
- Weighted A* (w=2) with LM-cut — used for Scenario 2 when standard A* did not finish within the 1,800-second limit.

Grounding produces:

- 162 actions for Scenario 1.
- 216 actions for Scenario 2.

Every generated plan is validated through step-by-step simulation. The final state must have all rocks at the Base, both bays empty, and the rover back at the Base.

### Experimental Results

| Scenario | Algorithm | Plan Length | States Expanded | Time |
|---|---|---:|---:|---:|
| 1 (Original) | GBFS + h_add | 34 | 78 | 0.04 s |
| 1 (Original) | A* + LM-cut | 25 | 6,741 | 34.88 s |
| 1 (Original) | BFS | 25 | 332,520 | 6.96 s |
| 2 (Extended) | GBFS + h_add | 61 | 722 | 0.37 s |
| 2 (Extended) | A* + LM-cut | Not completed | 204,000 | 1,800 s limit |
| 2 (Extended) | Weighted A* (w=2) | 40 | 2,425 | 23.32 s |

### Exhaustive BFS Verification

The standalone C++ implementation in `bfs_proof.cpp` performs exhaustive BFS over all 22,274,690 reachable states of Scenario 2.

The goal is first reached at depth 40, independently establishing that the 40-action plan is optimal.

### Analysis and Observations

The detailed analysis is available in `PS2/Report.txt`.

- **Plan length:** GBFS produces a plan 9 actions (36%) longer in Scenario 1 and 21 actions (52.5%) longer in Scenario 2 compared with the optimal solutions. It generally collects one rock per trip using Bay1.
- **Storage bays and drill:** Optimal plans utilize both bays to reduce return trips. The drill is acquired before collecting any hard rock.
- **Dust-storm scenario:** Since Base and SiteB are disconnected in both directions, the rover follows the route Base → SiteA → SiteC → SiteD → SiteB, respecting the one-way slope.

### Output Files

- `planner_output.txt` contains the complete search output.
- `plan_scenario1_gbfs.txt`, `plan_scenario1_astar.txt`, and `plan_scenario1_bfs.txt` contain Scenario 1 plans.
- `plan_scenario2_gbfs.txt` and `plan_scenario2_astar.txt` contain Scenario 2 plans. The latter stores the Weighted A* solution with a cost of 40.
- `Screenshots/` contains validation, scenario, comparison, and analysis outputs.

---

## PS3 — Royal Archive: Access Verification using Resolution Refutation

**Tool:** SWI-Prolog

The implementation is available in `PS3/royal_archive_access.pl`. It establishes the goal `trusted(mira)` from the given knowledge base using Resolution Refutation.

### Knowledge Base

The knowledge base consists of the following rules:

1. An archivist who verifies a record is trusted.
2. A trusted person with access to a sealed record is permitted to inspect it.
3. Anyone who inspects a record and finds a hidden mark in it verifies it.
4. Every stored record is sealed.

**Facts:**

- `stored(scroll_7)`
- `has_access(mira, scroll_7)`
- `inspects(mira, scroll_7)`
- `finds_mark(mira, scroll_7)`
- `archivist(mira)`

### Resolution Refutation Procedure

The program prints the following stages:

1. Predicate-logic representation.
2. Negation of the goal (`¬trusted(mira)`).
3. Implication removal.
4. Moving negation inward using De Morgan's laws.
5. Standardizing variables apart.
6. Skolemization — not required, as there are no existential quantifiers.
7. Conversion into CNF, splitting conjunctive facts into unit clauses.
8. Resolution refutation using set-of-support / linear resolution, starting from the negated goal.

### Final Result

The empty clause `[]` is derived in 5 resolution steps using c1, c3, c7a, c7b, and c8.

This establishes that `trusted(mira)` logically follows from the knowledge base. Clauses c2 and c4 are not required for this proof.

The complete execution output is available in `PS3/Screenshots/Output.png`.

---

## How to Run

### PS1 — Python and Jupyter Notebook

Install the required dependencies:

```bash
pip install numpy pandas matplotlib seaborn networkx jupyter
```

Launch the notebook:

```bash
jupyter notebook PS1/PS1.ipynb
```

Execute the cells sequentially to reproduce the Bayesian Network, inference queries, synthetic datasets, parameter learning, and comparative analysis.

### PS2 — Mars Rover Planning

Open `PS2/Q2_Mars_Rover.ipynb` and execute the cells in order. The notebook generates the PDDL files, solves both scenarios, validates the plans, and compiles `bfs_proof.cpp`.

Scenario 1 A* takes approximately 35 seconds. Scenario 2 A* uses a maximum execution limit of 1,800 seconds.

**Standalone Exhaustive BFS Verification**

```bash
cd PS2
g++ -O2 -o bfs_proof bfs_proof.cpp && ./bfs_proof
```

Requires `g++`.

### PS3 — SWI-Prolog

Execute the following commands:

```bash
cd PS3
swipl -q -s royal_archive_access.pl -g main -t halt
```

The program prints the complete resolution-refutation procedure and final proof result.

---

## Conclusion

This assignment demonstrates three major Artificial Intelligence approaches: probabilistic reasoning through Bayesian Networks, automated planning through PDDL and heuristic search, and logical inference through Resolution Refutation.

The implementations combine theoretical concepts with practical experimentation, algorithm comparisons, and validation of results.

**Course:** Artificial Intelligence  
**Assignment:** Group Assignment 2 (GA2)  
**Group:** Cognitive Crew  
**Institute:** IIT Bhilai
