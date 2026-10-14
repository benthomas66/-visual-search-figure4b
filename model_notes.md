# Model notes

Figure 4b: one fixation, 19 locations, at most one target. Eccentricities:
$0^\circ$ (one), $4^\circ$ (six), $6.9295^\circ$ (six), $8^\circ$ (six).
The code uses the values in the authors' notebooks.

$H_0$: absent. $H_k$: target at location $k$, for $k=1,\ldots,19$.

$$
p_0\in\{0,0.5\},\qquad p_k=\frac{1-p_0}{19},\qquad
\sum_{k=0}^{19}p_k=1.
$$

Generating map and sensory responses:

$$
d'_k=6\frac{e_2}{e_k+e_2},\qquad e_2\in\{1,3,5,7,9\}.
$$

$$
P(K=k)=p_k,\qquad Z_k\overset{\mathrm{iid}}{\sim}N(0,1),\qquad
R'_k=Z_k+\mathbf{1}\{K=k\}\,d'_k\quad(k=1,\ldots,19).
$$

Only the target location gets the signal shift. Given the state, responses
are independent; noise draws are also independent across trials. The map
stays fixed within a condition. The observer receives the responses, not $K$.

At one location, the noise and target densities are

$$
f_0(r)=\frac{1}{\sqrt{2\pi}}e^{-r^2/2},\qquad
f_1(r)=\frac{1}{\sqrt{2\pi}}e^{-(r-d')^2/2}.
$$

$$
\begin{aligned}
\ln\frac{f_1(r)}{f_0(r)}
&=-\frac12(r-d')^2+\frac12r^2\\
&=-\frac12\left(r^2-2d'r+(d')^2\right)+\frac12r^2\\
&=d'r-\frac12(d')^2\\
&=d'\left(r-\frac{d'}2\right).
\end{aligned}
$$

For $d'>0$, $r>d'/2$ favors a target at that location; $r<d'/2$ favors
noise. For $d'=6$, the densities are equal at $r=3$. This is a local
likelihood comparison; priors and other locations still affect the decision.

Let $\mathbf r=(r_1,\ldots,r_{19})$ and $\phi$ be the standard normal density.

$$
f(\mathbf r\mid H_0)=\prod_{i=1}^{19}\phi(r_i),\qquad
f(\mathbf r\mid H_k)=\phi(r_k-d'_k)\prod_{i\ne k}\phi(r_i).
$$

Every factor except location $k$ cancels:

$$
\frac{f(\mathbf r\mid H_k)}{f(\mathbf r\mid H_0)}
=\frac{\phi(r_k-d'_k)}{\phi(r_k)}
=\exp\left(d'_kr_k-\frac12(d'_k)^2\right).
$$

By Bayes' theorem,

$$
P(H_k\mid\mathbf r)
=\frac{p_kf(\mathbf r\mid H_k)}{
\sum_{j=0}^{19}p_jf(\mathbf r\mid H_j)}.
$$

The denominator is common to all states, so it does not affect the ranking.
Taking logs of the numerators and subtracting the common
$\ln f(\mathbf r\mid H_0)$ gives the scores

$$
S_0=\ln p_0,\qquad
S_k=\ln p_k+d'_kr_k-\frac12(d'_k)^2.
$$

$$
\widehat K=\underset{k\in\{0,\ldots,19\}}{\mathrm{arg\,max}}\;S_k.
$$

Under equal costs for wrong answers, selecting the most probable state
maximizes accuracy. Correct means $\widehat K=K$, including absence.
Absence has no physical location or sensory response. When $p_0=0$,
set $S_0=-\infty$. When $p_0>0$, subtracting $\ln p_0$ from all scores,
as the notebooks do, leaves the decision unchanged.

The generating map produces the responses. Each observer uses an assumed
map to score them, with the same correct prior:

$$
\begin{aligned}
\text{Ideal:}\quad &\widehat d'_k=d'_k,\\
\text{Flat:}\quad &\widehat d'_k=3.9,\\
\text{Fall-off:}\quad &\widehat d'_k=6.9\frac{7}{e_k+7}.
\end{aligned}
$$

$$
\widehat S_0=\ln p_0,\qquad
\widehat S_k=\ln p_k+\widehat d'_kr_k-\frac12(\widehat d'_k)^2
=\ln p_k+\widehat d'_k\left(r_k-\frac{\widehat d'_k}{2}\right).
$$

The expanded and factored scores are equivalent (paper Equations 1 and 5).
Both heuristic maps stay fixed throughout the sweep. All three observers
score the same responses; only the ideal uses the generating detectabilities.

$$
2\text{ priors}\times5\text{ maps}=10\text{ conditions},\qquad
\widehat A=\frac{n_{\mathrm{correct}}}{10000}.
$$

Ten conditions give 30 accuracies: six curves, each with five points.
A curve fixes the prior and observer, then varies generating $e_2$.
One generator, seed 0, is initialized before the sweep.

$$
\mathrm{SE}(\widehat A)=\sqrt{A(1-A)/10000}\le0.005.
$$

Here $A$ is expected accuracy. Sampling variation can put a heuristic
slightly above the ideal in one run without higher expected accuracy.

Python: `prior[k]` and `scores[k]` refer to state $k$.
Physical location $k$ uses `responses[k - 1]` and
`generating_dprime[k - 1]`. States run 0–19; physical arrays run 0–18.

Source: Zhang & Geisler (2025),
[Journal of Vision 25(4):5](https://doi.org/10.1167/jov.25.4.5).
Original [ideal scan](https://github.com/anqi-j/supraoptimal-covert-search/blob/15a4a63bdbbb8a1ad2a813001c7505ab13d45964/simulation/Search%20Scan%20Ideal.ipynb)
and [heuristic scan](https://github.com/anqi-j/supraoptimal-covert-search/blob/15a4a63bdbbb8a1ad2a813001c7505ab13d45964/simulation/Search%20Scan%20Heuristic.ipynb).
