# Model notes

These notes derive the decision rule used in `simulate_search.py` and
explain how the Figure 4b simulation is set up. The model works with
simulated sensory responses (one number per location), not images.

## 1. Locations, states, and priors

There are 19 possible target locations on a hexagonal grid (Figure 4e)
with 4° spacing: one at 0°, six at 4°, six at about 6.93°, and six at 8°.
Call their eccentricities $e_1,\ldots,e_{19}$. The code uses 6.9295°,
matching the value in the authors' notebooks.

There are 20 possible states. $H_0$ means the target is absent.
$H_k$, for $k=1,\ldots,19$, means the target is at location $k$.
At most one target is present. The priors are

$$
P(H_0)=p_0,\qquad P(H_k)=p_k=\frac{1-p_0}{19},
$$

with $p_0=0$ or $p_0=0.5$. Absence is a state, not a location, so it has
no sensory response of its own.

## 2. Generating the responses

The **generating map** sets the true detectability $d'$ at each location
(Equation 6 in the paper):

$$
d'_k=d'_{\max}\,\frac{e_2}{e_k+e_2},\qquad d'_{\max}=6,\quad e_2\in\{1,3,5,7,9\}.
$$

$d'$ equals 6 at the center and falls to half that at eccentricity $e_2$.
Small $e_2$ means visibility drops off quickly away from the center.

On each trial, draw the true state $K$ from the prior, then draw 19
independent standard normal values $Z_k$. The responses are

$$
R'_k=Z_k+\mathbf{1}\{K=k\}\,d'_k,\qquad Z_k\sim N(0,1).
$$

So when the target is absent, every response is pure noise. When the
target is at location $j$, response $j$ has mean $d'_j$ and every other
response has mean 0. All responses have variance 1 and are independent.
The observer sees the 19 responses, not the true state.

## 3. Likelihood ratio at one location

At a single location with detectability $d'$, the response density is

$$
f_0(r)=\frac{1}{\sqrt{2\pi}}e^{-r^2/2}\ \ \text{(no target)},\qquad
f_1(r)=\frac{1}{\sqrt{2\pi}}e^{-(r-d')^2/2}\ \ \text{(target)}.
$$

The log likelihood ratio is

$$
\begin{aligned}
\ln\frac{f_1(r)}{f_0(r)}
&=-\tfrac12(r-d')^2+\tfrac12r^2\\
&=-\tfrac12\left(r^2-2d'r+d'^2\right)+\tfrac12r^2\\
&=d'r-\tfrac12d'^2\\
&=d'\left(r-\tfrac12d'\right).
\end{aligned}
$$

The last two lines are the same expression, expanded and factored. The
paper writes the expanded form in Equation 1 and, for a heuristic map
$\widehat d'$, the factored form in Equation 5. The $-\tfrac12d'^2$ term comes straight out of the Gaussian
densities. A response above $d'/2$ favors "target here"; below $d'/2$
favors "no target here."

## 4. Combining 19 locations with Bayes' theorem

Write $\mathbf r=(r_1,\ldots,r_{19})$ and let $\phi$ be the standard normal
density. Because the responses are independent,

$$
f(\mathbf r\mid H_0)=\prod_{i=1}^{19}\phi(r_i),\qquad
f(\mathbf r\mid H_k)=\phi(r_k-d'_k)\prod_{i\ne k}\phi(r_i).
$$

Dividing, every factor except location $k$ cancels:

$$
\frac{f(\mathbf r\mid H_k)}{f(\mathbf r\mid H_0)}
=\frac{\phi(r_k-d'_k)}{\phi(r_k)}
=\exp\!\left(d'_kr_k-\tfrac12d'^2_k\right).
$$

Bayes' theorem gives the posterior of each state:

$$
P(H_k\mid\mathbf r)=
\frac{p_k\,f(\mathbf r\mid H_k)}{\sum_{j=0}^{19}p_j\,f(\mathbf r\mid H_j)}.
$$

The denominator is the same for every state, and so is
$f(\mathbf r\mid H_0)$. Dividing by both and taking logs does not change
which state is largest. That leaves one score per state:

$$
S_0=\ln p_0,\qquad S_k=\ln p_k+d'_kr_k-\tfrac12d'^2_k\quad(k=1,\ldots,19).
$$

The observer picks the state with the highest score:

$$
\widehat K=\arg\max_{k\in\{0,\ldots,19\}}S_k.
$$

This is Equation 1 of the paper. Picking the most probable state gives
the highest chance of being correct. A decision is correct only if it is
the exact true state: the right location when a target is present, or
"absent" when it is not.

## 5. The absent state

The absent state has no response, and its likelihood ratio with itself
is 1, so its score is just $\ln p_0$. (The paper writes this as
$d'_0=0$ in Equation 1.) When $p_0=0$, the code sets $S_0=-\infty$ so
"absent" is never chosen. The authors' notebooks also subtract $\ln p_0$
from every score when $p_0>0$; shifting all scores by the same amount
does not change the decision.

## 6. Generating versus assumed maps

The **generating map** produces the responses. The **assumed map** is
what an observer plugs into the score. Writing the assumed values as
$\widehat d'_k$:

$$
\widehat S_0=\ln p_0,\qquad
\widehat S_k=\ln p_k+\widehat d'_k\,r_k-\tfrac12\widehat d'^2_k .
$$

| Observer | Assumed map $\widehat d'_k$ |
|---|---|
| Ideal | the generating map, $6\,e_2/(e_k+e_2)$ |
| Flat heuristic | $3.9$ at every location |
| Fall-off heuristic | $6.9\cdot 7/(e_k+7)$ |

The two heuristic maps stay the same in all 10 conditions, while the
generating map changes with $e_2$. All three observers use the correct
prior and score the same 19 responses on each trial. Only the ideal
observer's scores are true log posteriors (up to a shared constant);
the heuristic scores would be correct only if their assumed map were true.

Example: with generating $e_2=1$ and a target at 4°, the true $d'$ is
$6\cdot1/5=1.2$. A noise draw of 0.8 gives a response of 2.0. All three
observers see 2.0, but weight it with 1.2, 3.9, and
$6.9\cdot7/11\approx4.39$.

## 7. The sweep and the 30 accuracies

A condition is one absent prior (0 or 0.5) and one generating $e_2$
(1, 3, 5, 7, or 9), giving 10 conditions. Each condition runs 10,000
trials, and each observer's accuracy is

$$
\widehat A=\frac{\text{number of correct decisions}}{10{,}000}.
$$

10 conditions × 3 observers = 30 accuracy estimates. In the figure,
each curve fixes one observer and one prior and plots accuracy against
$e_2$: two panels (one per prior) with three curves each, so 6 curves
with 5 points each. The three accuracies in each condition are within
0.03 of each other, so some curves overlap.

Each estimate has a Monte Carlo standard error of about
$\sqrt{A(1-A)/10{,}000}\le0.005$, so a heuristic can land slightly above
the ideal observer in one run without being better on average.

## 8. Indexing in the code

| Meaning | Python |
|---|---|
| Absent prior $p_0$ | `prior[0]` |
| Prior for location $k$ | `prior[k]` |
| Response at location $k$ | `responses[k - 1]` |
| $d'$ at location $k$ | `generating_dprime[k - 1]` |
| Score for state $k$ (0 = absent) | `scores[k]` |

States run 0–19, but the response and map arrays have 19 entries
(Python indices 0–18), hence the `k - 1`. `np.argmax` returns the first
index if scores tie; ties essentially never happen with continuous
responses.

One random generator (seed 0) is created before the sweep, so every
condition gets different trials, and the three observers within a
condition share the same trials.

## References

Zhang, A., & Geisler, W. S. (2025). Optimal visual search with highly
heuristic decision rules. *Journal of Vision, 25*(4), 5.
<https://doi.org/10.1167/jov.25.4.5>

Original code: <https://github.com/anqi-j/supraoptimal-covert-search>,
`simulation/Search Scan Ideal.ipynb` and
`simulation/Search Scan Heuristic.ipynb`.
