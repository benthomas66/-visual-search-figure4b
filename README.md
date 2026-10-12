# Covert search model reproduction

A small Python reproduction of the model comparison behind **Figure 4b** in
Zhang & Geisler (2025), *Optimal visual search with highly heuristic decision
rules*, [Journal of Vision, 25(4), 5](https://doi.org/10.1167/jov.25.4.5).

I made this to work through the mathematics and implementation of the ideal
and heuristic decision rules. This is a reproduction and learning project,
not a new scientific result.

Original code: [anqi-j/supraoptimal-covert-search](https://github.com/anqi-j/supraoptimal-covert-search).

![Simulated accuracy under two absent priors](figures/figure4b_reproduction.png)

## What is simulated?

Single-fixation covert search with 19 possible target locations and at most
one target. The model generates abstract, independent Gaussian sensory
responses; it does not process images or simulate eye movements.

- Locations: one at 0°, six at 4°, six at approximately 6.9295°, six at 8°.
- Generating map: $d'(e)=6e_2/(e+e_2)$, with $e_2=1,3,5,7,9$.
- Absent prior: $p_0=0$ or $0.5$; the remaining probability is uniform over locations.
- Observers: ideal, fixed flat map ($\widehat d'=3.9$), and fixed declining
  map ($\widehat d'(e)=6.9\times7/(e+7)$). All use the correct prior.
- 10,000 trials per map/prior condition; all three observers see the same
  evidence within a trial. NumPy generator seed: 0.

Two priors × five maps = ten conditions. Three observer accuracies per
condition give **30 estimates**, shown as **six curves with five points each**.
The original Figure 4b overlays both priors; this figure separates them into
two panels for readability.

## Run it

Tested with Python 3.12.14. From the repository directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest -v test_model.py
python simulate_search.py
python make_figure.py
```

On Windows, activate with `.venv\Scripts\activate` instead. The pinned
dependencies are NumPy 2.3.5 and Matplotlib 3.10.8. CSV and figure outputs
are saved relative to the scripts, regardless of the shell working directory.

## Files

| File | Purpose |
|---|---|
| `simulate_search.py` | Generate trials, score observers, save accuracies |
| `make_figure.py` | Plot the six accuracy curves |
| `model_notes.md` | Derive the Gaussian likelihood ratio and Bayesian decision rule |
| `test_model.py` | Check likelihoods, indexing, boundaries, source-rule equivalence, and reproducibility |
| `results/search_accuracy.csv` | All 30 seeded simulation estimates and correct counts |
| `figures/figure4b_reproduction.png` | Generated figure |
| `VALIDATION.md` | Source comparison, numerical checks, and limits |

## Results

At $p_0=0.5$, the included run gives:

| Generating $e_2$ | Ideal | Flat heuristic | Declining heuristic |
|---|---:|---:|---:|
| 1 | 0.5360 | 0.5210 | 0.5132 |
| 3 | 0.6346 | 0.6215 | 0.6188 |
| 5 | 0.7296 | 0.7217 | 0.7221 |
| 7 | 0.8182 | 0.8077 | 0.8173 |
| 9 | 0.8682 | 0.8620 | 0.8692 |

The curves reproduce the published pattern: accuracy rises as the generating
map declines more slowly with eccentricity, and the fixed heuristics perform
close to the ideal observer. They are not identical at every setting.
At $p_0=0$, $e_2=1$, the declining heuristic is about 2.8 percentage points
below the ideal in this run. A heuristic can also slightly exceed the ideal
in a finite simulation sample; that does not imply higher expected accuracy.

## Scope and attribution

The geometry, parameters, and scoring were checked against the paper and
the source notebooks. All seven tests pass. An independent numerical
integration check supports the Monte Carlo estimates; details are in
`VALIDATION.md`.

This reproduces the focused Figure 4b comparison. It does not reproduce human
data, fit observer parameters, implement attentional gain or correlated noise,
or simulate successive fixations. No parameters were adjusted to match the
published plot. Exact published Monte Carlo values were not digitized; this
run uses its own seeded trials and a different plotting layout.

The original repository is MIT-licensed, copyright Anqi Zhang. Its notice is
preserved in `THIRD_PARTY_NOTICES.md` and `LICENSE`. The present Python code
is organized around explicit response generation and short functions for
readability. Mathematical exposition here is newly written from the model.
