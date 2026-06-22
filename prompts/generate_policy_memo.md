You are writing a rigorous policy/economic intelligence memo.

Audience: AI policy and economic research fellowship reviewers.

Use the provided signals and decision object.

Return JSON only:
{
  "report_markdown": "..."
}

The memo should include:
# Policy/Economic Intelligence Memo
## Executive Summary
## Evidence Base
## Key Market Signals
## Investment Signals
## Policy and Regulatory Risk
## Mixed Signals and Uncertainty
## Social Dynamics
## Stakeholder Incentive Analysis
## Counter-Argument Stress Test
## Strategic Implications for Emerging Sector Policy
## Sector Trajectory Assessment
## Analogous Sector Benchmarks
## Evidence Quality Audit
## Confidence and Limitations
## Sources Reviewed

Analytical standards — apply these throughout:

1. For each major finding, explicitly identify the underlying economic mechanism at work. Use one of these four labels and briefly explain why it applies:
   - Demand-side effect: the finding operates through changing consumer behavior, preferences, or willingness to pay
   - Supply-side effect: the finding operates through changing producer costs, input prices, or production incentives
   - Market structure effect: the finding operates through changing competition, concentration, or barriers to entry/exit
   - Policy/regulatory mechanism: the finding operates through changing what is legally permissible, mandated, or economically viable

2. When signals conflict or point in different directions, explain the tension using economic logic — do not merely note that disagreement exists. Relevant concepts include: price elasticity of demand, cross-price substitution effects, regulatory uncertainty's chilling effect on investment timing, the distinction between short-run and long-run supply responses, and the difference between quantity demanded and willingness to pay at a given price point.

3. When signals carry a behavioral_mechanism value other than null, explain why rational economic models alone are insufficient to account for the observed consumer behavior, and what that implies for policy design. Reference the specific mechanism:
   - intention_action_gap: standard demand models assume revealed preference — if consumers say they want plant-based but don't buy it, the gap signals a decision architecture problem, not a preference problem. Policy responses include default design, friction reduction at point of purchase, and commitment devices.
   - loss_aversion: consumers weigh price premiums more heavily than equivalent savings. Policy responses include subsidy framing (presenting plant-based as the discounted option rather than the premium one) and reference point manipulation.
   - reference_price_effect: consumer price sensitivity is anchored to conventional protein benchmarks. Policy responses include comparative labeling and price transparency rules that surface total-cost-of-production comparisons.
   - naturalness_heuristic: consumers systematically discount nutritionally equivalent products perceived as artificial. Policy responses include labeling standards that distinguish processing from safety, and public information campaigns grounded in transparency rather than persuasion.
   - social_norm_signal: adoption follows visible peer behavior. Policy responses include institutional adoption programs, public sector procurement as norm-setter, and social proof in public communications.
   - status_quo_bias: inertia favors conventional products independent of preference. Policy responses include default changes in institutional settings (school cafeterias, hospital menus, government procurement).
   - default_effect: adoption is structurally determined by what institutions present as the baseline choice. Policy intervention can shift defaults at scale without restricting consumer freedom.

4. The ## Social Dynamics section must analyze all signals that carry a non-null norm_type or framing_type. It must:
   - Group signals by norm_type and explain what the combination of descriptive vs. injunctive norms implies for actual adoption velocity. If descriptive norms (what people do) lag injunctive norms (what people say they value), this signals an intention-action gap at the population level and suggests that social proof interventions matter more than persuasion campaigns.
   - Identify any institutional_norm signals and explain what policy leverage they represent. Defaults set by institutions (school cafeterias, hospital menus, government procurement, corporate catering) reach populations at scale without requiring individual decision-making — policy changes here have higher expected impact per unit of effort than information-based campaigns.
   - Assess where in the diffusion curve the sector likely sits based on the balance of innovator_signal vs. early_majority_signal content. If signals are predominantly from innovator segments, the sector has not yet crossed the chasm to mainstream adoption; if early_majority signals are present, mainstream movement may be beginning. Note the implications for policy timing.
   - Note any framing types present and flag mismatches between current framing and what behavioral economics suggests would be more effective given the behavioral mechanisms tagged in the signal set.

5. The ## Stakeholder Incentive Analysis section must map the key stakeholders in the alternative protein policy environment and analyze their incentives explicitly. For each of the following groups, identify: (a) their primary incentive, (b) the policy outcome they are pushing toward, and (c) where their incentives conflict with other groups:
   - Federal regulators (FDA/USDA): mandate scope, jurisdiction conflicts between agencies, enforcement capacity constraints
   - State legislatures: constituent and agricultural industry pressure, interstate commerce tensions, federal preemption risk
   - Conventional meat industry: incumbent protection incentives, lobbying strategy, co-optation vs. opposition trade-offs
   - Plant-based brands: market access, labeling compliance costs, the tension between differentiation and commoditization
   - Institutional buyers (schools, hospitals, corporate cafeterias): cost pressure, sustainability mandates, procurement inertia
   - Consumer advocacy groups: health claims credibility, transparency demands, environmental and animal welfare framing
   - Investment community: return timeline expectations, regulatory risk pricing, portfolio exposure management
   The section must conclude with: which stakeholder currently has the most leverage over sector outcomes, and what specific condition or event would shift that leverage balance.

6. The ## Counter-Argument Stress Test section must formally steelman the strongest case AGAINST the sector trajectory conclusion reached in ## Sector Trajectory Assessment. It must:
   - State the opposing argument in its most compelling form — not a strawman, but the version a rigorous skeptic would actually make
   - Identify which specific signals in the current dataset most support the counter-argument (cite by signal_id)
   - Explain why, despite this counter-argument, the trajectory assessment stands — or explicitly acknowledge if the counter-argument is strong enough to qualify or soften the conclusion
   - Rate the counter-argument strength: WEAK / MODERATE / STRONG with one sentence of justification
   This section is mandatory regardless of trajectory label. A policy memo that does not engage with its strongest opposition is advocacy, not analysis.

7. The ## Sector Trajectory Assessment section must synthesize all signals, mechanism types, and behavioral mechanisms into a single named trajectory. Choose exactly one:
   - RECOVERY: evidence of demand stabilization + investment returning + policy environment improving
   - CONSOLIDATION: weak players exiting, stronger players gaining share, investment concentrating around proven segments
   - REPOSITIONING: sector strategy shifting (e.g., from retail CPG to foodservice, from meat analogs to dairy/beverages, from domestic to international)
   - STRUCTURAL DECLINE: sustained demand loss + capital exit + hostile policy environment converging
   The section must: (a) name the trajectory in bold, (b) cite the specific signals that support it by signal_id, (c) name which mechanism types are driving the trajectory, (d) explicitly identify the signals that most contradict the chosen trajectory and explain why they do not change the assessment. This section must make an argument, not a description.

8. The ## Analogous Sector Benchmarks section must identify the closest historical analogue to the current plant-based sector trajectory from the list below and explain what that analogue predicts about the sector's next phase. It must:
   - Name the closest analogue from this list:
     * Organic food mainstreaming (US, 2000–2010): niche to mass market via retail channel expansion and price compression
     * Oat milk breakout (US, 2018–2020): single product category achieving rapid mainstream crossover driven by taste parity and social norm cascade
     * Early electric vehicle adoption (US, 2010–2020): technology adoption curve with innovator/early majority gap, policy subsidy dependence, infrastructure chicken-and-egg problem
     * Low-fat food transition (US, 1980s–1990s): health-driven category shift that overshot, created backlash, and partially reversed
     * Craft beer mainstreaming (US, 2010–2018): fragmented premium category consolidating as majors acquired independents
   - Explain the specific structural similarities between the analogue and the current plant-based sector — mechanism, adoption phase, policy environment, and competitive dynamics
   - Identify where the analogy breaks down — what is fundamentally different about the plant-based sector that limits the predictive power of the historical comparison
   - State what the historical precedent predicts about the timing and mechanism of the next phase transition, and how confident that prediction should be given the analogy's limitations

9. The ## Evidence Quality Audit section is mandatory in every output. It must:
   - State the total number of sources reviewed and list the source types represented (e.g., market_report, trade_press, government_data, academic)
   - Flag any signal categories where the average evidence_quality_score across signals in that category is below 3.0 — name the category and the average score
   - Flag any behavioral_mechanism tags (other than null) that appear on only one signal — low replication weakens any behavioral claim
   - State explicitly what the single biggest gap in the current evidence base is and what specific type of source would fill it
   - Give an overall evidence confidence rating — HIGH, MODERATE, or LOW — with one sentence of justification

Respect the decision object's confidence cap and disclaimer.
Do not overclaim.
If mixed signals are present, explicitly discuss them using the analytical standards above.
