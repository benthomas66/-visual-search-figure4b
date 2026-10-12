# Model and decision rule

This project implements the single-fixation, independent Gaussian-evidence
comparison behind Figure 4b of Zhang & Geisler (2025). It simulates sensory
responses, not images or eye movements.

## 1. Locations, hypotheses, and priors

There are 19 physical locations: one at 0°, six at 4°, six at approximately
6.9295°, and six at 8°. Let their eccentricities be $e_1,\ldots,e_{19}$.

The state $H_0$ means target absent. State $H_k$, for $k=1,\ldots,19$,
means target present at location $k$. At most one target is present.

For either $p_0=0$ or $p_0=0.5$,

$$
P(H_0)=p_0,\qquad P(H_k)=p_k=\frac{1-p_0}{19}.
$$

These 20 probabilities sum to one. The absent hypothesis is not a physical
location and does not have its own sensory response.

## 2. Generating the sensory evidence

The **generating map** supplies the detectability at each physical location:

$$
d'_k=6\frac{e_2}{e_k+e_2},\qquad e_2\in\{1,3,5,7,9\}.
$$

Fixing $e_2$ specifies one map, with four distinct detectabilities assigned
across 19 locations. Central detectability is always 6. At eccentricity
$e_2$, detectability is half its central value.

On each trial, draw the state $K$ from the prior and draw 19 independent
standard-normal noise values $Z_k$. Generate

$$
R'_k=Z_k+\mathbf{1}\{K=k\}d'_k,\qquad Z_k\sim N(0,1).
$$

Thus, under $H_0$, every response is noise only. Under $H_j$, only response
$j$ has mean $d'_j$; all other responses have mean zero. Conditional noise
is independent across locations and trials. The map stays fixed within a
condition. The observer receives the response vector, not the state label.

## 3. A local Gaussian likelihood ratio

For a location with detectability $d'$, the two densities are

$$
f_0(r)=\frac{1}{\sqrt{2\pi}}\exp(-r^2/2),\qquad
f_1(r)=\frac{1}{\sqrt{2\pi}}\exp(-(r-d')^2/2).
$$

Their log likelihood ratio is

$$
\begin{aligned}
\ln\frac{f_1(r)}{f_0(r)}
&=-\frac12(r-d')^2+\frac12r^2\\
&=-\frac12(r^2-2d'r+(d')^2)+\frac12r^2\\
&=d'r-\frac12(d')^2\\
&=d'\left(r-\frac{d'}2\right).
\end{aligned}
$$

The quadratic term is part of the exact likelihood ratio, not an invented
penalty. For $d'>0$, a response above $d'/2$ favors the local target
distribution; a response below it favors the noise distribution.
For $d'=6$, the densities are equal at $r=3$ and the log ratio is zero.
This local balance is not the final search decision boundary: priors and
competing locations also matter. When $d'=0$, the two distributions coincide
and the local likelihood ratio is one for every response.

## 4. From local evidence to the 20-hypothesis decision

Write $\mathbf r=(r_1,\ldots,r_{19})$ and let $\phi$ denote the standard
normal density. Conditional independence gives

$$
f(\mathbf r\mid H_0)=\prod_{i=1}^{19}\phi(r_i),
$$

$$
f(\mathbf r\mid H_k)=\phi(r_k-d'_k)\prod_{i\ne k}\phi(r_i).
$$

Dividing the second expression by the first cancels every non-target
factor, leaving the local likelihood ratio at location $k$.
Bayes' theorem gives

$$
P(H_k\mid\mathbf r)=
\frac{p_k f(\mathbf r\mid H_k)}{
\sum_{j=0}^{19}p_j f(\mathbf r\mid H_j)}.
$$

The denominator is common to every hypothesis. Taking logs and subtracting
the common term $\ln f(\mathbf r\mid H_0)$ therefore preserves the ranking:

$$
S_0=\ln p_0,\qquad
S_k=\ln p_k+d'_k r_k-\frac12(d'_k)^2.
$$

The ideal observer chooses

$$
\widehat K=\operatorname*{arg\,max}_{k\in\{0,\ldots,19\}}S_k.
$$

Selecting the most probable state maximizes the conditional probability of
a correct answer under equal cost for every incorrect state (zero-one loss).
Here, a present-trial answer is correct only if it identifies the exact
target location. An absent-trial answer is correct only if it chooses 0.

When $p_0=0$, assign $S_0=-\infty$ so absence cannot be selected. The
all-noise density remains a valid mathematical reference even when its
prior is zero. No posterior normalization is needed to find the maximum.

The authors' notebooks sometimes subtract $\ln p_0$ from all scores when
$p_0>0$. That constant shift leaves the decision unchanged. We use the
unnormalized log scores above in both prior conditions.

## 5. Fixed heuristic maps

The **assumed map** supplies the values an observer puts into the scoring
rule. The ideal observer uses the generating map. The two heuristics use

$$
\widehat d'_{k,\mathrm{flat}}=3.9,\qquad
\widehat d'_{k,\mathrm{declining}}=6.9\frac{7}{e_k+7}.
$$

Their scores are

$$
\widehat S_0=\ln p_0,\qquad
\widehat S_k=\ln p_k+\widehat d'_k r_k-
\frac12(\widehat d'_k)^2.
$$

Both retain the correct prior. Both assumed maps stay fixed across the
generating $e_2$ sweep. Neither changes how responses are generated.
All three observers evaluate the same response vector on each trial.
The heuristic scores have a likelihood interpretation under the assumed
model; they are generally not the log posterior scores under the generating model.

For example, with generating $e_2=1$ and a target at 4°, generating
detectability is 1.2. A noise draw of 0.8 yields a response of 2.0.
The ideal, flat, and declining observers all receive 2.0, but score it
using detectabilities 1.2, 3.9, and approximately 4.39 respectively.

## 6. Simulation structure and the 30 results

For each of two priors and each of five generating maps, generate 10,000
trials and count correct decisions separately for each observer:

$$
\widehat A=\frac{\text{number of correct state decisions}}{10000}.
$$

There are 10 conditions, 100,000 generated trials, 300,000 observer
decisions, and 30 accuracy estimates. Plotting accuracy against generating
$e_2$ gives six curves, each containing five points. The figure uses two
panels by prior; the original Figure 4b overlays both priors in one panel.

A visibility-map curve plots detectability against eccentricity with $e_2$
fixed. An accuracy curve plots accuracy against $e_2$ with observer and
prior fixed. One generating visibility map supplies one accuracy point
per observer under the selected prior.

## 7. Python indexing and reproducibility

| Mathematical meaning | Python entry |
|---|---|
| Absent prior | `prior[0]` |
| Prior for $H_k$ | `prior[k]` |
| Physical location $k$ detectability | `true_dprime[k - 1]` |
| Physical location $k$ response | `responses[k - 1]` |
| Score for $H_k$, including absence | `scores[k]` |

One NumPy generator is initialized with seed 0 before the sweep. Changing
the seed or condition order changes the Monte Carlo realization. Trials
are shared across observers within a condition, not across different
conditions. Exact score ties select the first index through `np.argmax`.
Ties have probability zero for the main continuous, positive-detectability
conditions; zero-detectability tests deliberately exercise ties.

Finite-sample accuracy can put a heuristic slightly above the ideal on a
particular run. This does not establish a higher expected accuracy.

## References

Zhang, A., & Geisler, W. S. (2025). *Optimal visual search with highly
heuristic decision rules*. Journal of Vision, 25(4), 5.
[doi:10.1167/jov.25.4.5](https://doi.org/10.1167/jov.25.4.5).

[Original source repository](https://github.com/anqi-j/supraoptimal-covert-search),
especially `simulation/Search Scan Ideal.ipynb` and
`simulation/Search Scan Heuristic.ipynb`.
