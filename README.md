# Covert search model reproduction

A small Python reproduction of the simulation behind Figure 4b of
Zhang & Geisler (2025), *Optimal visual search with highly heuristic decision rules*.

Paper: https://doi.org/10.1167/jov.25.4.5

Original repository: https://github.com/anqi-j/supraoptimal-covert-search

This is a reproduction and learning project, not a new scientific result.

![Accuracy curves](figures/figure4b_reproduction.png)

## What the simulation does

There are 19 possible target locations and at most one target. Sensory
responses are independent Gaussian values, not actual images.

The generating visibility map is d′(e) = 6 e2 / (e + e2).
We use five generating e2 values: 1, 3, 5, 7, and 9 degrees.
We use two absent priors: 0 and 0.5. Present locations are equally likely.

For each of those ten conditions, the simulator generates 10,000 trials.
Three observers judge the same responses on each trial:

- Ideal: uses the map that generated the responses.
- Flat heuristic: assumes d′ = 3.9 everywhere.
- Declining heuristic: assumes d′(e) = 6.9 × 7 / (e + 7).

The two heuristic maps remain fixed. All observers use the correct prior.
Ten conditions × three observers produce 30 accuracies: six curves,
each containing five points. We separate the priors into two panels;
the original Figure 4b shows both priors in one panel.

## Run the code

Open a terminal in this repository folder. Tested with Python 3.12.

```bash
python -m pip install -r requirements.txt
python simulate_search.py
python test_model.py
python make_figure.py
```

The simulator uses seed 0 and saves `search_accuracy.csv` in this folder.
The figure script reads that file and saves `figures/figure4b_reproduction.png`.
Run the commands in the order shown; the tests also check the generated CSV.

## Files

| File | Purpose |
|---|---|
| `simulate_search.py` | Trial generation, decision rules, condition sweep |
| `make_figure.py` | Plot the saved accuracies |
| `model_notes.md` | Mathematical derivation and assumptions |
| `test_model.py` | Basic checks and comparison with full Gaussian likelihoods |
| `requirements.txt` | NumPy and Matplotlib dependencies |
| `search_accuracy.csv` | The 30 generated results |
| `figures/figure4b_reproduction.png` | The generated figure |
| `LICENSE` | MIT license and preserved source notice |

## Checks and limitations

The geometry, sweep, and heuristic parameters were checked against the
paper and the original ideal and heuristic scan notebooks, at source
commit `15a4a63bdbbb8a1ad2a813001c7505ab13d45964`.
The notebook's score shift and our sensory-response shift are algebraically
equivalent. The original flat map uses a very large falloff parameter
(1e10); we use the exactly flat value 3.9.

The basic checks pass. After simplifying the scripts, all 30 results
are identical to the earlier implementation. The curves agree with the
published Figure 4b pattern. No parameters were tuned to match the plot.
We have not digitized the published points or reproduced the authors'
random draws, so this is not a claim of exact numerical identity.

Accuracy has Monte Carlo variability. For example, at absent prior 0.5
and generating e2 = 7, this run gives 0.8182 (ideal), 0.8077 (flat), and
0.8173 (declining). A heuristic can slightly exceed the ideal in a finite
sample without having higher expected accuracy.

This project does not reproduce human data or simulate eye movements,
correlated noise, or attentional gain. The original source is MIT-licensed,
copyright Anqi Zhang; its notice is preserved in `LICENSE`. The figure
here is newly generated; no original figure is bundled.
