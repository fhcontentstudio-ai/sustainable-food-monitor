# Sustainable Food Systems Economic Monitor

A bounded AI research agent that converts manually collected sector sources into structured economic and policy intelligence for the plant-based and alternative protein industry.

Built as a portfolio project for AI policy and economic research, with dual outputs designed for two audiences: fellowship/policy researchers and plant-based DTC brand operators.

---

## What This Does

Most AI systems summarize what you give them. This system does something different: it evaluates whether it has enough good evidence to support a conclusion before writing one, identifies what is missing, searches the web for candidates to fill gaps, and produces confidence-calibrated analysis that names its own limitations.

The pipeline classifies each source across 8 analytical dimensions, gates its output based on evidence quality thresholds, and generates two distinct reports from the same evidence base — a 15-section policy memo and a commercial client brief — each calibrated for a different reader.

---

## Architecture

sources.csv (human-curated input)
      ↓
source_loader.py    — validates input schema
      ↓
classifier.py       — classifies each source across 8 dimensions via Claude API
      ↓
evidence_analyzer.py — scores evidence quality, detects mixed signals, flags gaps
      ↓
decision_agent.py   — gates output: full report / limited / gap report only
      ↓
source_finder.py    — if gaps exist, searches web for candidate sources autonomously
      ↓
memo_generator.py   — generates policy memo and/or client brief based on decision

---

## Signal Classification Schema

Every source is tagged across 8 dimensions before any synthesis occurs:

Field | Purpose
signal_category | market_demand, investment, policy_regulation, consumer_adoption, corporate_strategy, macroeconomic_context
signal_direction | positive, negative, mixed, neutral
mechanism_type | demand_side, supply_side, policy_regulatory, market_structure
behavioral_mechanism | intention_action_gap, loss_aversion, reference_price_effect, naturalness_heuristic, status_quo_bias, default_effect, null
norm_type | descriptive_norm, injunctive_norm, institutional_norm, innovator_signal, early_majority_signal, null
framing_type | gain_frame, loss_frame, identity_frame, outcome_frame, risk_frame, null
time_horizon | near, medium, long, ongoing
evidence_quality_score | 1-5, conservative scoring with explicit rubric

Tagging occurs at classification time, making every downstream claim auditable against a specific signal in signals.csv.

---

## Evidence Sufficiency Gating

The decision agent evaluates the evidence base before generating any output. It will not produce a full report unless:

- Minimum 10 sources present
- Average evidence quality >= 3.0
- Average confidence >= 3.0
- At least 4 of 6 core categories represented
- Audience-specific required categories present

If thresholds are not met, the system produces a gap report with specific recommended sources instead of a confident-sounding memo based on thin evidence. This is a deliberate design choice, not a limitation.

---

## Policy Memo Structure (15 sections)

1. Executive Summary
2. Evidence Base
3. Key Market Signals
4. Investment Signals
5. Policy and Regulatory Risk
6. Mixed Signals and Uncertainty
7. Social Dynamics (norm diffusion analysis)
8. Stakeholder Incentive Analysis
9. Counter-Argument Stress Test
10. Strategic Implications
11. Sector Trajectory Assessment (RECOVERY / CONSOLIDATION / REPOSITIONING / STRUCTURAL DECLINE)
12. Analogous Sector Benchmarks
13. Evidence Quality Audit
14. Confidence and Limitations
15. Sources Reviewed

---

## Thesis

This project tests whether a bounded AI research agent can improve economic intelligence for emerging socially beneficial industries by structuring heterogeneous evidence, scoring market and policy signals, identifying evidence gaps and mixed signals, and producing confidence-calibrated analysis under uncertainty.

The plant-based and alternative protein sector serves as the case study. The system is designed to be sector-agnostic — the prompts and architecture can be redirected to any emerging industry with heterogeneous evidence and high policy and market uncertainty.

---

## Commercial Application

The same evidence base produces a parallel client brief for plant-based and alternative protein brands, with sections including:

- Market Snapshot
- Consumer Demand Signals
- Competitor and Category Movement
- Policy and Risk Watch
- Competitive Positioning Window (time-bounded opportunity identification)
- Messaging and Framing Intelligence (behavioral economics applied to brand strategy)
- Recommended Actions
- Evidence Quality Audit

---

## Setup

git clone https://github.com/fhcontentstudio-ai/sustainable-food-monitor.git
cd sustainable-food-monitor
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

Add your Anthropic API key to .env:

ANTHROPIC_API_KEY=your_key_here

Add sources to data/sources.csv following the schema in the existing file, then run:

python main.py

Reports are written to reports/policy_memo.md and reports/client_brief.md.

---

## Stack

- Python 3.9+
- Anthropic Claude API (claude-sonnet-4-6)
- pandas
- python-dotenv
- Web search via Anthropic built-in web_search tool

---

## Status

V1 — functional end-to-end. Current evidence base covers the US alternative protein sector (June 2026). Designed to be updated with new sources on a rolling basis.
