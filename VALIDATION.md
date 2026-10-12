# Validation of the Figure 4b comparison

Checked on 2026-10-12 UTC (2026-10-11 in California).

## Source fidelity

Sources:

- [Published paper and Figure 4](https://pmc.ncbi.nlm.nih.gov/articles/PMC12007678/).
- [Original repository](https://github.com/anqi-j/supraoptimal-covert-search),
  inspected at commit `15a4a63bdbbb8a1ad2a813001c7505ab13d45964`.
- `simulation/Search Scan Ideal.ipynb` and `simulation/Search Scan Heuristic.ipynb`.

The notebooks confirm the 19 eccentricities, 10,000 trials, absent priors
0 and 0.5, central detectability 6, and generating falloff values 1,3,5,7,9.
The heuristic notebook includes a wider scan over assumed priors and maps;
this project selects the correct-prior flat-3.9 and declining-6.9/7 maps
used for the focused comparison. The original flat map uses an assumed
falloff parameter of 1e10, an effectively constant map. Here it is exactly 3.9.

The notebook shifts the target location's score by assumed detectability
times generating detectability. This code first adds generating detectability
to the sensory response, then scores it. The algebra and a deterministic
test confirm the two approaches are equivalent. Prior normalization by
the absent prior in the notebooks is a common score shift, leaving the
argmax unchanged.

Visual inspection of published Figure 4b and our generated figure supports
agreement in scale, ordering, and curve shape. Both heuristic maps are near
the ideal overall, with visible differences at low generating e2.
We have not digitized the original curve coordinates or reproduced its
random draws, so we do not claim exact numerical or pixel-level identity.

## Code checks

`python -m unittest -v test_model.py` passes seven tests:

1. Prior normalization and location counts.
2. Noise generation and state-to-array indexing, including absence and location 19.
3. Agreement of ideal decisions with independently calculated full joint Gaussian log likelihoods.
4. Zero detectability, prior-only decisions, and exclusion of absence when its prior is zero.
5. Correct recovery of every state at very high detectability.
6. Equivalence to the original notebook's score-shift formulation.
7. Thirty unique result combinations, accuracy accounting, and seeded repeatability.

The final simulator reproduces the uploaded script's complete 30-row output.

## Independent numerical accuracy check

As an additional development check, we integrated the Gaussian score
distributions using SciPy 1.17.0 outside the production scripts. This does
not fit parameters or use the simulation's random draws.

For assumed detectability $a_i>0$, let

$$
b_i=\ln p_i-\tfrac12a_i^2,\qquad S_i=b_i+a_i R'_i.
$$

Under absence, correct rejection probability is

$$
P(\widehat K=0\mid H_0)=
\prod_{i=1}^{19}\Phi\left(\frac{\ln p_0-b_i}{a_i}\right),
$$

when $p_0>0$. Under $H_j$, write $R'_j=z+d'_j$ and
$s_j(z)=b_j+a_j(z+d'_j)$. The correct-localization probability is

$$
P(\widehat K=j\mid H_j)=
\int_{L_j}^{\infty}\phi(z)
\prod_{i\ne j}\Phi\left(\frac{s_j(z)-b_i}{a_i}\right)\,dz,
$$

where $L_j=(\ln p_0-b_j)/a_j-d'_j$ for $p_0>0$, and $L_j=-\infty$
when $p_0=0$. Weight these conditional probabilities by the state priors
to obtain expected overall accuracy. Numerical integration used Gaussian
noise bounds -12 to 12, with reported quadrature errors below 1e-8.

The ideal observer's integrated expectations are:

| Generating e2 | Expected accuracy, p0 = 0 | Simulated | Expected accuracy, p0 = 0.5 | Simulated |
|---|---:|---:|---:|---:|
| 1 | 0.259929 | 0.2606 | 0.527685 | 0.5360 |
| 3 | 0.596747 | 0.6012 | 0.622615 | 0.6346 |
| 5 | 0.793915 | 0.7933 | 0.741077 | 0.7296 |
| 7 | 0.889985 | 0.8905 | 0.820791 | 0.8182 |
| 9 | 0.936963 | 0.9341 | 0.870511 | 0.8682 |

All 30 estimates, including both heuristics, were checked. The largest
absolute discrepancy is 2.62 marginal Monte Carlo standard errors, using
$\sqrt{A(1-A)/10000}$ for expected accuracy $A$. This is consistent with
sampling variability across the sweep; it is not a formal simultaneous
confidence guarantee. Observer estimates within a condition are correlated
because they use the same trials.

The integration check and source audit support the focused reproduction.
They do not validate the model's biological assumptions against human data.

## Complete numerical check

| p0 | Generating e2 | Observer | Simulated | Integrated expectation | Deviation / SE |
|---|---|---|---:|---:|---:|
| 0 | 1 | ideal | 0.2606 | 0.259929 | 0.15 |
| 0 | 1 | flat_heuristic | 0.2455 | 0.248952 | -0.80 |
| 0 | 1 | falloff_heuristic | 0.2324 | 0.237278 | -1.15 |
| 0 | 3 | ideal | 0.6012 | 0.596747 | 0.91 |
| 0 | 3 | flat_heuristic | 0.5875 | 0.585572 | 0.39 |
| 0 | 3 | falloff_heuristic | 0.5883 | 0.583425 | 0.99 |
| 0 | 5 | ideal | 0.7933 | 0.793915 | -0.15 |
| 0 | 5 | flat_heuristic | 0.7819 | 0.782024 | -0.03 |
| 0 | 5 | falloff_heuristic | 0.7889 | 0.790477 | -0.39 |
| 0 | 7 | ideal | 0.8905 | 0.889985 | 0.16 |
| 0 | 7 | flat_heuristic | 0.8781 | 0.880415 | -0.71 |
| 0 | 7 | falloff_heuristic | 0.8904 | 0.889012 | 0.44 |
| 0 | 9 | ideal | 0.9341 | 0.936963 | -1.18 |
| 0 | 9 | flat_heuristic | 0.9283 | 0.930167 | -0.73 |
| 0 | 9 | falloff_heuristic | 0.9343 | 0.936522 | -0.91 |
| 0.5 | 1 | ideal | 0.5360 | 0.527685 | 1.67 |
| 0.5 | 1 | flat_heuristic | 0.5210 | 0.512166 | 1.77 |
| 0.5 | 1 | falloff_heuristic | 0.5132 | 0.506236 | 1.39 |
| 0.5 | 3 | ideal | 0.6346 | 0.622615 | 2.47 |
| 0.5 | 3 | flat_heuristic | 0.6215 | 0.615186 | 1.30 |
| 0.5 | 3 | falloff_heuristic | 0.6188 | 0.611383 | 1.52 |
| 0.5 | 5 | ideal | 0.7296 | 0.741077 | -2.62 |
| 0.5 | 5 | flat_heuristic | 0.7217 | 0.729512 | -1.76 |
| 0.5 | 5 | falloff_heuristic | 0.7221 | 0.732622 | -2.38 |
| 0.5 | 7 | ideal | 0.8182 | 0.820791 | -0.68 |
| 0.5 | 7 | flat_heuristic | 0.8077 | 0.811810 | -1.05 |
| 0.5 | 7 | falloff_heuristic | 0.8173 | 0.817615 | -0.08 |
| 0.5 | 9 | ideal | 0.8682 | 0.870511 | -0.69 |
| 0.5 | 9 | flat_heuristic | 0.8620 | 0.864878 | -0.84 |
| 0.5 | 9 | falloff_heuristic | 0.8692 | 0.869974 | -0.23 |
