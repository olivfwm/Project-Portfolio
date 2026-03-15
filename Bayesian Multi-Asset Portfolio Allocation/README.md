# 🧠 Bayesian Multi-Asset Portfolio Allocation
### *Knowing When to Be Uncertain — and Acting on It*

**Team:** The Master Bayesians &nbsp;|&nbsp; **Course:** Bayesian Machine Learning &nbsp;|&nbsp; **University of Chicago**

> *"The value of Bayesian methods is not better point predictions, but knowing when to be uncertain — and acting conservatively when uncertain."*

---

## 📌 The Core Idea in Plain English

Most investment strategies ask: **"Which assets should I buy?"**

We asked a harder question: **"How confident should I be in my signal — and how should that uncertainty change my bet size?"**

A traditional momentum strategy that says *"Buy Bitcoin, it's been going up"* has no way to express *how sure* it is. Our Bayesian framework adds a second layer: *"Buy Bitcoin — but the model is highly uncertain about this prediction, so take a smaller position than you otherwise would."*

This is the difference between a point estimate and a **probability distribution over outcomes**.

---

## 🏗️ The Pipeline: Three Stages of Intelligence

```
Raw Market Data (5 assets, 2015–2025)
        │
        ▼
┌───────────────────────────────┐
│  Stage 1: VAE                 │  12 messy features → 4 clean latent signals
│  Variational Autoencoder      │  Encodes market state as a distribution, not a point
└───────────────┬───────────────┘
                │  z ~ N(μ, σ²)
                ▼
┌───────────────────────────────┐
│  Stage 2: HMM                 │  "Is this asset in Bull, Bear, or Sideways?"
│  Hidden Markov Model          │  Probabilistic answer — not a hard threshold rule
└───────────────┬───────────────┘
                │  P(regime_t | x_{1:t})
                ▼
┌───────────────────────────────┐
│  Stage 3: BNN                 │  Predict tomorrow's return + how uncertain we are
│  Bayesian Neural Network      │  MC Dropout: 50 forward passes → mean ± std
└───────────────┬───────────────┘
                │  (μ_pred, σ_pred) per asset
                ▼
        Portfolio Weights
  (bigger bet when confident, smaller when not)
  weights[t] applied to returns[t+1] — no look-ahead
```

**Assets Traded:** `SPY` · `GLD` · `BTC-USD` · `TLT` · `GSG`

| Asset | What it represents |
|---|---|
| **SPY** | US Stock Market (S&P 500) |
| **GLD** | Gold — inflation hedge, crisis hedge |
| **BTC-USD** | Bitcoin — high-volatility risk asset |
| **TLT** | Long-duration US Treasury Bonds |
| **GSG** | Commodities (oil, metals, agriculture) |

**Data:** 2015–2025 &nbsp;|&nbsp; **Train:** 2015–2023 &nbsp;|&nbsp; **Test (OOS):** 2024–2025

---

## 🔬 What Makes This "Bayesian"? Three Technologies Explained

### Stage 1 · Variational Autoencoder (VAE)

We compute **12 technical indicators** per asset across four categories:

| Category | Features |
|---|---|
| **Returns** | log_return, 5-day return, 20-day return |
| **Volatility** | 10-day rolling std, 20-day rolling std |
| **Trend** | SMA ratio (10/50), SMA ratio (20/100) |
| **Mean-reversion / Momentum** | RSI(14), MACD, MACD signal, MACD histogram, Bollinger Band position |

Feeding all 12 directly into downstream models causes overfit — they're correlated, noisy, and scale differently across assets. The VAE compresses them into 4 latent dimensions, with a critical Bayesian twist: each input is encoded as a **probability distribution** (μ ± σ), not a single point.

$$\mathcal{L}_{\text{ELBO}} = \underbrace{\mathbb{E}_{q(z|x)}[\log p(x|z)]}_{\text{reconstruction accuracy}} - \underbrace{D_{KL}(q(z|x) \| \mathcal{N}(0,I))}_{\text{regularization: keep latent space structured}}$$

The KL term forces the latent space to be smooth and compact — making the representations robust to small perturbations in the input data.

```python
def reparameterize(self, mu, logvar):
    std = torch.exp(0.5 * logvar)
    eps = torch.randn_like(std)
    return mu + eps * std          # differentiable stochastic sampling

def loss_function(self, recon, x, mu, logvar):
    recon_loss = F.mse_loss(recon, x, reduction='sum')
    kl_loss    = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + kl_loss
```

**What each latent dimension learns (SPY, from actual statistics):**
| Dim | Std | Range | Interpretation |
|-----|-----|-------|----------------|
| z₀ | 0.06 | [−0.58, +0.57] | Slow-moving trend anchor — near-constant, changes on multi-year timescales |
| z₁ | 0.53 | [−4.34, +3.35] | Return/trend direction — sharp activations during market stress events |
| z₂ | 0.92 | [−3.57, +4.07] | Volatility & tail-risk signals — activated during crises and regime transitions |
| z₃ | 0.99 | [−4.81, +2.94] | Regime-level drift — highest variance, sustained low-frequency bull/bear cycles |

![VAE Latent Dimensions — SPY](output_bayesian_portfolio/02_vae_latent_space.png)

---

### Stage 2 · Hidden Markov Model (HMM) with Forward-Only Filtering

The HMM takes VAE latent features as input and infers a hidden market regime for each asset at each time step: **Bull / Sideways / Bear**.

**Why not just use rules?** A rule like "if 30-day vol > 30% → Bear" responds only *after* volatility has already risen. The HMM maintains a probability distribution over states and updates it continuously as new data arrives — detecting transitions earlier and with more nuance.

$$P(\text{regime}_t \mid x_{1:t}) \propto P(x_t \mid \text{regime}_t) \cdot \sum_j P(\text{regime}_t \mid \text{regime}_{j}) \cdot P(\text{regime}_{j} \mid x_{1:t-1})$$

**Critical design choice:** We use *forward-only filtering* — the posterior at time *t* only uses observations up to *t*. We deliberately avoided the Viterbi algorithm, which decodes the full sequence and allows future states to influence past inferences, creating look-ahead bias. Forward filtering prioritizes online, real-world applicability: the regime estimate at any point uses only the information a live investor would actually have.

```python
# Forward pass only: P(state_t | x_{1:t}) — no backward smoothing
for t in range(1, T):
    log_pred  = np.logaddexp.reduce(log_transmat.T + log_alpha, axis=1)
    log_alpha = log_lik[t] + log_pred
    log_alpha -= np.logaddexp.reduce(log_alpha)   # normalize in log-space
    filtered_probs[t] = np.exp(log_alpha)
```

**Sample regime statistics (SPY, 2015–2023 training period, seed=42):**
| Regime | % of Days | Ann. Return | Ann. Volatility |
|--------|-----------|-------------|-----------------|
| 🐻 Bear | 29.8% | −21.6% | 17.0% |
| ➡️ Sideways | 25.8% | +24.1% | 28.0% |
| 🐂 Bull | 44.5% | +29.3% | 8.0% |

![Asset Prices with HMM Regime Detection](output_bayesian_portfolio/01_regime_detection.png)

---

### Stage 3 · Bayesian Neural Network (BNN) with MC Dropout

The BNN takes VAE latent features + regime one-hot encoding as input and generates a **predictive distribution** over tomorrow's return — not a single number, but a spread of possible outcomes. The variance of this distribution represents epistemic uncertainty: the model's "risk of ignorance." The Bayesian mechanism: **dropout stays on during inference**. Running 50 forward passes yields 50 slightly different predictions — their mean is the best estimate, their std is how much the model *doesn't know*.

```python
def predict_with_uncertainty(self, x, n_samples=50):
    self.train()   # keep dropout ACTIVE at inference time
    preds = [self.forward(x).numpy() for _ in range(n_samples)]
    preds = np.array(preds).squeeze()
    return preds.mean(axis=0), preds.std(axis=0)   # μ_pred, σ_pred
```

**Uncertainty is higher out-of-sample — exactly as Bayesian theory predicts:**
| Asset | Train σ | Test σ | Direction |
|-------|---------|--------|-----------|
| SPY | 0.0013 | 0.0017 | ↑ higher OOS |
| GLD | 0.0010 | 0.0026 | ↑↑ much higher OOS |
| BTC-USD | 0.0053 | 0.0062 | ↑ higher OOS |
| TLT | 0.0013 | 0.0011 | ↓ lower OOS |
| GSG | 0.0016 | 0.0010 | ↓ lower OOS |

This is epistemic uncertainty in action: the model knows it's less confident when asked to predict on data unlike its training distribution.

![BNN Prediction Uncertainty by Asset](output_bayesian_portfolio/04_bnn_uncertainty.png)

**Uncertainty → position sizing via log-softened discount:**

```python
# Raw: 1/(1 + k·σ) → near-zero weights for volatile assets like BTC (too aggressive)
# Log-softened: graceful degradation across all volatility levels
def bnn_confidence(bnn_std, k=10):
    return 1.0 / (1.0 + np.log1p(k * bnn_std))
```

**The core decision logic in one line — this is "Acting conservatively when uncertain":**

```python
# The higher the BNN uncertainty, the smaller the position — regardless of signal strength
position_size = base_signal * bnn_confidence(bnn_uncertainty) * regime_multiplier
#                                   ↑ shrinks toward 0 as uncertainty grows
```

When `bnn_uncertainty` is low (familiar market conditions), `bnn_confidence ≈ 1` and the full signal is used. When uncertainty is high (novel regime, volatile asset), `bnn_confidence → 0` and the position is automatically reduced — without any hand-tuned threshold.

---

## ⚖️ The Experiment Design: A Controlled Paired Comparison

Each Bayesian strategy is paired with a non-Bayesian version using the **exact same base signal** — the only difference is the uncertainty quantification layer. Any performance gap is attributable to Bayesian reasoning alone.

| Pair | Bayesian Strategy | Non-Bayesian Strategy | Shared Signal |
|------|-------------------|-----------------------|---------------|
| 1 | Regime-Based (B) | Rule-Based Regime (NB) | Bull/Sideways/Bear → weight mapping |
| 2 | Bayesian Momentum (B) | Classical Momentum (NB) | 60-day past returns |
| 3 | Bayesian Risk Parity (B) | Inverse Volatility (NB) | 1 / historical volatility |

Plus **Equal Weight (1/N)** as a universal benchmark.

**No look-ahead in trading — weights shifted forward by one day:**
```python
# Weights decided at close of day t → applied to returns of day t+1
def apply_weights_with_shift(returns_df, weights_df):
    shifted_weights = weights_df.shift(1).iloc[1:]
    aligned_returns = returns_df.iloc[1:]
    return (aligned_returns * shifted_weights).sum(axis=1)
```

---

## 📊 Results & Analysis

### In-Sample (2015–2023)

> ⚠️ Models were trained on this period. IS advantages may partly reflect curve-fitting; **OOS is the only honest test**.

*Green shading = Bayesian leads. The advantage concentrates around high-turbulence periods: COVID crash (2020), 2022 cross-asset selloff.*

![IS Cumulative Returns](output_bayesian_portfolio/is_01_cumulative_returns.png)

*Green shading = Bayesian has shallower drawdown.*

![IS Drawdown](output_bayesian_portfolio/is_02_drawdown.png)

*Bayesian Advantage Delta: all three pairs show positive Sharpe and drawdown improvements in-sample.*

![IS Delta](output_bayesian_portfolio/is_04_bayesian_advantage_delta.png)

---

### Out-of-Sample (2024–2025) — The Real Test

> *$100,000 deployed January 1, 2024. Models trained exclusively on 2015–2023 data.*

![OOS Cumulative Returns](output_bayesian_portfolio/oos_01_cumulative_returns.png)

![OOS Drawdown](output_bayesian_portfolio/oos_02_drawdown.png)

*OOS Bayesian Advantage Delta: Momentum maintains a positive Sharpe delta; Regime Detection and Risk Parity show slight Non-Bayesian edges on Sharpe, though Bayesian wins drawdown in all three pairs.*

![OOS Delta](output_bayesian_portfolio/oos_04_bayesian_advantage_delta.png)

---

### Full Scorecard — All 6 Pairs, Both Periods

| Period | Pair | Sharpe (B) | Sharpe (NB) | Δ Sharpe | Max DD (B) | Max DD (NB) | Winner |
|--------|------|-----------|------------|---------|-----------|-----------|--------|
| In-Sample (2015–2023) | Regime Detection | 0.931 | 0.275 | **+0.656** | −28.8% | −32.9% | 🟦 Bayesian |
| In-Sample (2015–2023) | Momentum | 0.951 | 0.945 | **+0.006** | −51.4% | −55.0% | 🟦 Bayesian |
| In-Sample (2015–2023) | Risk Parity | 0.449 | 0.265 | **+0.184** | −24.0% | −25.4% | 🟦 Bayesian |
| Out-of-Sample (2024+) | Regime Detection | 1.302 | 1.673 | −0.371 | **−8.2%** | −9.6% | Non-Bayesian (Sharpe) |
| Out-of-Sample (2024+) | Momentum | **1.151** | 1.120 | **+0.031** | **−10.5%** | −12.7% | 🟦 Bayesian |
| Out-of-Sample (2024+) | Risk Parity | 1.341 | 1.356 | −0.015 | **−7.5%** | −8.7% | Non-Bayesian (Sharpe) |

| Metric | IS: B vs NB | OOS: B vs NB |
|--------|------------|--------------|
| Sharpe Ratio | **B wins all 3** | **B wins 1 of 3** (Momentum only) |
| Max Drawdown | **B wins all 3** | **B wins all 3** |

> **Key pattern:** Bayesian wins Sharpe on all 3 IS pairs and **1 of 3 OOS pairs** (Momentum). However, **Bayesian delivers better drawdown protection in all 6 pairs** — the most robust finding.

---

### Why: Pair-by-Pair Causal Explanation

#### Pair 1 · Regime Detection — *"Best in crises, costly in calm"*

**Why B wins IS (Sharpe 3.4×):** HMM posterior updates detected COVID crash and 2022 selloff earlier than vol/drawdown thresholds → smoother regime transitions, less damage during ambiguous periods.

**Why B loses OOS Sharpe (−0.371):** Simple thresholds correctly stayed "Bull" throughout the 2024–2025 uptrend — HMM's probabilistic transitions introduced conservatism that wasn't needed. But B still achieved 1.4pp better drawdown protection.

#### Pair 2 · Momentum — *"The only OOS Sharpe winner"*

**Why B wins both periods:** BNN uncertainty acts as a "signal quality filter" — when the model can't explain *why* an asset is rising, it trims the position. Classical momentum blindly chases all winners; Bayesian only trusts the ones it understands.

**Raw return trade-off:** Classical reached $162,822 vs Bayesian's $154,893 — but Bayesian achieved higher Sharpe with 2.2pp less drawdown. Better *quality* of returns, not just quantity.

#### Pair 3 · Risk Parity — *"Always protects the downside"*

**Why B wins IS (+0.184 Sharpe):** BNN uncertainty inflated risk estimates during genuinely volatile regimes → allocated less to high-uncertainty assets *before* large drawdowns materialized.

**Why B narrowly loses OOS Sharpe (−0.015):** In 2024–2025's calm environment, BNN uncertainty penalty mildly over-attenuated allocations. But drawdown protection (−7.5%, best of any strategy) still held — BNN captures downside-specific risk that symmetric Sharpe doesn't fully reward.

---

### When: Three Market Scenarios, Three Bayesian Behaviors

| Market Environment | Bayesian Behavior | What Drives It | Evidence |
|---|---|---|---|
| **Regime transitions & crises** | Detects shifts early, cuts exposure *before* damage | HMM posterior updates continuously; BNN uncertainty spikes at turning points | Regime Detection: IS Sharpe 3.4× vs rule-based |
| **Strong trending markets** | Rides the trend, but filters false signals | BNN confidence stays high on genuine trends; uncertainty discount trims only the noise | Momentum: OOS Sharpe +0.031, DD +2.2pp vs classical |
| **Sideways / choppy markets** | Stays cautious, avoids whipsaw | HMM probability-weights regime transitions instead of binary 0/1 switching; BNN inflates risk estimates | Risk Parity: best OOS DD (−7.5%) across all strategies |

---

### So What: Signal Scaling vs Classification

| Bayesian Task | How It Works | IS | OOS |
|---|---|---|---|
| **Signal scaling** (Momentum) | BNN uncertainty adjusts *magnitude* of signals — "soft brake" proportional to confidence | B wins | **B wins** |
| **Risk estimation** (Risk Parity) | BNN adds forward-looking risk signal beyond historical vol | B wins | NB wins (Sharpe), **B wins** (DD) |
| **Classification** (Regime Detection) | HMM makes discrete Bull/Bear/Sideways calls | B wins | NB wins |
| **Drawdown protection** (all pairs) | Higher uncertainty → smaller positions → less downside | B wins | **B wins** |

**For practical deployment**, Bayesian methods are most valuable when:
- Used to **scale position sizes** based on uncertainty (Momentum) rather than making binary regime calls
- Deployed during **elevated VIX environments** (>25) where uncertainty is genuinely high
- Applied to **non-stationary assets** (like BTC) where historical vol alone is insufficient
- Evaluated on **drawdown protection** as primary metric — this is where Bayesian most consistently wins

> **Bottom line:** The consistent drawdown improvement across all pairs and both periods is the strongest practical argument for Bayesian portfolio methods — **reliable downside protection as a structural feature**, not an artifact of in-sample fitting.

---

### Weight Allocation Over Time

*Bayesian strategies show more dynamic, regime-responsive allocation shifts. Compare Regime-Based (B) vs Rule-Based (NB): the Bayesian version reacts to probabilistic regime transitions, not just threshold crossings. Red dashed line = train/test split.*

![Weight Allocation](output_bayesian_portfolio/wt_01_weight_allocation.png)

---

## 🌍 Bonus Finding: Asset Correlations Break Down in Risk-Off

One of the most actionable insights from our cross-regime correlation analysis:

| Asset Pair | Risk-On | Mixed | Risk-Off |
|---|---|---|---|
| SPY ↔ TLT (stocks/bonds) | −0.14 | −0.25 | **≈ 0.00** |
| SPY ↔ BTC | 0.03 | **0.29** | 0.25 |
| SPY ↔ GSG (commodities) | 0.25 | 0.37 | 0.31 |
| SPY ↔ GLD (gold) | 0.03 | 0.02 | 0.16 |

**Key insight:** The classic stock-bond diversification benefit **disappears exactly when you need it most** — in Risk-Off environments, bonds provide almost no hedge against equity losses. This is why static inverse-volatility weighting fails during crises, and why regime-aware dynamic allocation matters.

---

## 🔭 Future Work

| Direction | Problem It Solves | Approach |
|---|---|---|
| **Adaptive uncertainty thresholds** | Regime Detection's fixed conservatism drags Sharpe in calm markets | Scale the uncertainty discount based on current volatility regime — aggressive in crises, relaxed in trends |
| **Macro-informed priors** | BNN priors are currently uninformative; model is purely data-driven | Encode CPI trajectory, yield curve slope, Fed policy stance as informative BNN priors — genuine Bayesian information fusion at turning points |
| **Richer uncertainty estimation** | MC Dropout may underestimate true posterior variance | Replace with deep ensembles or variational inference for better-calibrated confidence discounts |
| **Longer OOS validation** | Only ~2 years of calm bull market OOS | Walk-forward validation across multiple market cycles, including a genuine bear market |

---

## 🛡️ Data Integrity: How We Prevented Look-Ahead Bias

Financial backtests are famously easy to overfit accidentally. We implemented strict safeguards at every stage:

| Risk | Our Solution |
|---|---|
| Look-ahead in features | All technical indicators use only data up to time *t* |
| Look-ahead in regime detection | HMM uses forward-only filtering, never full-sequence Viterbi |
| Look-ahead in prediction | BNN: features at day *t* predict returns at day *t+1* (`X[:-1]` / `y[1:]`) |
| Look-ahead in trading | Portfolio weights at day *t* applied to returns at *t+1* (1-day shift) |
| Training data leakage | VAE, scaler, HMM, and BNN all fit on 2015–2023 **only** |

---

## 🔮 Bayesian Concepts Demonstrated

| Concept | Where It Appears |
|---|---|
| Variational Inference / ELBO | VAE training objective |
| Reparameterization trick | VAE stochastic sampling |
| Expectation-Maximization / Baum-Welch | HMM fitting |
| Forward filtering (no smoothing) | Online regime inference |
| MC Dropout as approximate posterior | BNN uncertainty quantification |
| Posterior predictive uncertainty | Return confidence intervals |
| Epistemic vs aleatoric uncertainty | OOS uncertainty inflation analysis |
| Bayesian decision theory | Uncertainty → conservative position sizing |

---

## 🚀 Quick Start

**Requirements:** Python 3.9+

```bash
# Install dependencies
pip install torch hmmlearn yfinance pandas numpy matplotlib seaborn scikit-learn pymc

# Launch notebook
jupyter notebook main.ipynb
```

Run all cells top to bottom. The pipeline will automatically download data, train all models on 2015–2023, and evaluate out-of-sample on 2024–2025. Full run time: ~10–15 minutes on CPU.

> **Note:** BTC-USD trades 7 days/week while equity markets trade 5 days/week. The notebook handles this alignment automatically by forward-filling BTC prices to match the equity calendar.

---

## 📁 Repository Structure

```
├── main.ipynb                        # Full pipeline — run all cells top to bottom
├── README.md                         # This document
└── output_bayesian_portfolio/
    ├── performance_metrics.csv
    ├── performance_metrics_insample.csv
    ├── performance_metrics_outofsample.csv
    ├── cumulative_returns.csv
    ├── regime_data.csv
    └── *.png                         # All figures
```

---

## 👥 Team: The Master Bayesians

| Member |
|---|
| Zhulin Wang |
| Martin Zou |
| Mina Qu |
| Olivia Fang |
| Wade Chen |

---

*Built with PyTorch · hmmlearn · PyMC · yfinance · University of Chicago, 2025*
