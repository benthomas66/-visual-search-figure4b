# Figure 4b reproduction

A small Python exercise reproducing the ideal-versus-heuristic search
comparison in Figure 4b of Zhang & Geisler (2025),
*Optimal visual search with highly heuristic decision rules*.

- Paper: https://doi.org/10.1167/jov.25.4.5
- Original code: https://github.com/anqi-j/supraoptimal-covert-search

## Simulation

The target is absent or present at one of 19 locations. The model generates
independent Gaussian sensory responses and compares three observers:

- Ideal: uses the map that generated the responses.
- Flat heuristic: assumes d′ = 3.9 everywhere.
- Fall-off heuristic: assumes d′(e) = 6.9 × 7 / (e + 7).

All three observers use the correct prior and judge the same trials.
The heuristic maps remain fixed while the generating map changes.

The simulation uses five generating e2 values (1, 3, 5, 7, 9), two absent
priors (0 and 0.5), and 10,000 trials per condition. This gives 30 accuracy
estimates, plotted as three curves in each of two panels.

![Accuracy curves](figure4b_reproduction.png)

The heuristics perform close to the ideal, as in the published figure.
The comparison with the published curves is visual; the original points
were not digitized.

## Run

From this folder, with NumPy and Matplotlib installed:

python3 simulate_search.py
python3 test_model.py
python3 make_figure.py

To install the package versions used for the reproduction:

python3 -m pip install -r requirements.txt

The simulator saves search_accuracy.csv, and the plotting script saves
figure4b_reproduction.png. The random seed is 0.

