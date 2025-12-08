Real Estate Investment Evaluation Platform

This document explains the business logic, feature engineering decisions, ROI modeling, scenario design, risk assessment, and deal scoring methodology used in the platform.

## Table of Contents
1. Overview
2. Data Entities and Relationships
3. Area Feature Engineering
4. Developer Feature Engineering
5. Deal Feature Engineering
6. ROI and Cashflow Model
7. Scenario Modeling (Bear/ Base/ Bull)
8. Risk Model
9. Deal Scoring Model (0-100)

## 1. Overview

The purpose of this platform is to evaluate real estate investment deals across Abu Dhabi using a combination of financial metrics, market indicators, developer reputation, and risk factors. 

The platform provides:
- Area-level insights (growth, yields, liquidity)
- Developer reliability metrics
- Deal-level profit and ROI calculations
- Bear/Base/Bull scenario outcomes
- A transparent risk matrix
- A unified 0-100 deal scoring mechanism


## 2. Data Entities and Relationships

The core entities used in the platform are:

### Areas
Represents geographic locations such as Yas Island, Reem Island, etc.  
Stores growth, yield, and liquidity-related attributes.

### Developers
Represents real estate developers (Tier 1, Tier 2, Tier 3).  
Includes reliability and track record metrics.

### Projects
Represents named property projects within an area, linked to a developer.

### Market History
Yearly historical price and growth data for each area.

### Deals
A user-defined investment scenario that includes booking price, expected flip price, strategy, and unit type.

### Payment Plans
A schedule of cash outflows for a deal, including booking, installments, and handover fees.

These entities connect as follows:

- One area -> many projects  
- One developer -> many projects  
- One project -> many deals  
- One deal -> many payment plan entries  
- One area -> many market history entries  

## 3. Area Feature Engineering

Area-level metrics describe the attractiveness, stability, and investment quality of a geographic location. These metrics influence liquidity, growth expectations, and the likelihood of achieving projected ROI.

### 3.1 Rental Yield Midpoint
Each area includes a minimum and maximum rental yield range.  
The midpoint provides a stable representative estimate:

**Formula:**
rental_yield_mid = (rental_yield_min + rental_yield_max) / 2


**Reasoning:**  
Rental yields fluctuate, and using the midpoint avoids over- or under-estimating returns. It gives a consistent benchmark across areas.

---

### 3.2 Normalization of Growth and Yield
Different areas operate on different scales. To compare them fairly, growth and yield values are normalized to a 0-100 scale using min-max normalization.

**Formula:**
normalized_x = 100 * (x - x_min) / (x_max - x_min)

Applied to:
- past_growth_rate  
- rental_yield_mid  

---

### 3.3 Stability Score
Price stability is measured by evaluating how often an area experiences non-negative annual growth.

**Formula:**
stability_raw = (number of years with growth_rate >= 0) / total_years
stability_score = stability_raw * 100


**Reasoning:**  
Investors prefer areas where prices rarely decline. A stability score captures volatility in a simple, explainable way.

---

### 3.4 Liquidity Score (0-100)
Liquidity represents how easily a property can be resold in an area. The score combines demand (growth), investor interest (yield), and stability.

**Formula:**
liquidity_score =
0.4 * growth_normalized +
0.35 * yield_normalized +
0.25 * stability_score

**Reasoning:**  
- Growth reflects overall buyer demand (40%).  
- Yield reflects investor appetite (35%).  
- Stability reduces uncertainty (25%).  

Higher liquidity indicates faster and more reliable exit opportunities for investors.

---

### 3.5 Area Viability Score (0-100)
This is an overall assessment of an area's quality as an investment location.

**Formula:**
area_viability_score =
0.5 * liquidity_score +
0.3 * growth_normalized +
0.2 * yield_normalized

**Reasoning:**  
- Liquidity is weighted highest (50%) because the ability to exit a property strongly influences investor decisions.  
- Growth (30%) signals long-term appreciation potential.  
- Rental yield (20%) reflects ongoing investor interest.  

A high viability score indicates a strong overall location for both flips and long-term holding.

## 4. Developer Feature Engineering

Developer-related features measure the reliability, reputation, and execution quality of a real estate developer. These features strongly influence project delivery risk, investor confidence, and liquidity.

### 4.1 Developer Tier Score (50-100)

Developers are classified into three tiers based on brand strength, reputation, and historical performance.

The platform assigns a tier score as follows:
Tier 1 -> 100
Tier 2 -> 75
Tier 3 -> 50

**Reasoning:**  
- Tier 1 developers (e.g., major established firms) deliver consistently and have strong resale demand.  
- Tier 2 developers are reliable but lack premium brand influence.  
- Tier 3 developers may be smaller, newer, or less consistent.

A 100/75/50 scale creates meaningful separation without extreme penalties.

---

### 4.2 Track Record Score (0-100)

This score reflects:
- customer satisfaction  
- quality of past project delivery  
- market reputation  

It is provided as part of the dataset or derived from project completion stats.

---

### 4.3 On-Time Completion Rate (0-100)

This represents the developer's history of delivering projects on or before schedule.
Higher values indicate lower execution risk.

---

### 4.4 Developer Trust Score (0-100)

The trust score aggregates tier, track record, and delivery reliability into a single metric.

**Formula:**
developer_trust_score =
0.5 * developer_tier_score +
0.3 * track_record_score +
0.2 * on_time_completion_rate

**Reasoning:**  
- Tier is weighted highest (50%) because brand confidence strongly impacts resale demand and investor trust.  
- Track record (30%) captures project quality and past performance.  
- On-time delivery (20%) addresses timeline and handover risk.

A high trust score indicates a low-risk developer with strong market confidence.

## 5. Deal Feature Engineering

Deal-level features quantify the financial characteristics of a specific investment opportunity. These metrics are used to evaluate cost efficiency, profitability, cash requirements, and return potential.

### 5.1 Effective Cost per Sqm
Represents the normalized price of the unit based on its size.

**Formula:**
effective_cost_per_sqm = booking_price / avg_unit_size_sqm

**Reasoning:**  
Total price alone is not a fair comparison across units. Cost per sqm allows consistent comparison across different areas, buildings, and unit types.

---

### 5.2 Price-to-Area Ratio
Compares the deal's price per sqm to the area's average price per sqm.

**Formula:**
price_to_area_ratio = effective_cost_per_sqm / area_avg_price_per_sqm


**Interpretation:**  
- < 1.0 -> Undervalued (attractive)  
- = 1.0 -> Fair market value  
- > 1.0 -> Overpriced (higher risk)

**Reasoning:**  
This ratio indicates whether the deal is priced above or below market norms. Undervalued deals have stronger resale potential and higher ROI likelihood.

---

### 5.3 Margin (Absolute Profit)
The expected profit in currency terms.

**Formula:**
margin = expected_flip_price - booking_price

**Reasoning:**  
Margin quantifies raw profit and acts as the basis for ROI calculations. It reflects upside potential without considering cashflow.

---

### 5.4 Margin Percentage
Profit relative to purchase cost.

**Formula:**
margin_pct = (margin / booking_price) * 100

**Reasoning:**  
Margin % enables investors to compare expected profit across deals of different price ranges. It represents deal attractiveness on a relative scale.

---

### 5.5 Capital Required 
Represents the total cash outflows the investor must pay before the exit.

**Formula:**
capital_required = sum(all payment_plan amounts due before exit_date)

**Reasoning:**  
Capital required reflects the investor's cash exposure. It is essential for matching deals to investor budgets and computing ROI.

---

### 5.6 Base ROI Percentage
A foundational ROI estimate assuming the "expected flip price" scenario.

**Formula:**
base_roi_pct = (margin / capital_required) * 100

**Reasoning:**  
Base ROI reflects return relative to the investor's maximum cash commitment. It provides a clear and interpretable metric for comparing deals.

## 6. ROI and Cashflow Model

The ROI model evaluates the financial performance of a deal using its payment schedule, exit price assumptions, and holding period. 

---

### 6.1 Cashflow Timeline

Each deal contains a set of scheduled payments (booking, installments, handover fees).  
These are treated as **cash outflows** until the investor exits.

At exit, the investor receives a **single inflow** equal to the sale price.

---

### 6.2 Total Cash Out (Before Exit)
The total outflow includes all payments scheduled before the exit date.

**Formula:**
total_cash_out = sum(payment.amount for all payments with due_date <= exit_date)

---

### 6.3 Capital Required

Capital required is the total amount of cash the investor must commit before selling the property.

**Formula:**
capital_required = total_cash_out

**Reasoning:**  
This is intuitive and matches investor behavior: "How much money do I need to put in before I can sell?"

---

### 6.4 Profit

Profit is the difference between the investor's final inflow and all cash outflows.

**Formula:**
profit = exit_price - total_cash_out


## 7. Scenario Modeling (Bear / Base / Bull)

The platform evaluates each deal under three scenarios to illustrate how returns change based on market conditions. 

Scenario modeling focuses on:
- Exit price variation  
- Potential delays to resale  
- Changes in profit and ROI under each scenario  

---

### 7.1 Base Scenario (Expected Case)

The base scenario represents the investor's original expectation.

**Assumptions:**
exit_price_base = expected_flip_price
exit_months_base = planned_exit_months

**Reasoning:**  
This scenario assumes the investor sells at the intended price and timeline. It forms the anchor for evaluating upside and downside.

---

### 7.2 Bear Scenario (Conservative Case)

The bear scenario models a softer market with lower demand and slower sales.

**Assumptions:**
bear_price_multiplier = 0.95 # 5% lower exit price
bear_exit_delay_months = +6 # delayed exit due to weaker demand

exit_price_bear = expected_flip_price * bear_price_multiplier
exit_months_bear = planned_exit_months + bear_exit_delay_months


**Reasoning:**  
A 5% downward adjustment reflects a mild market correction rather than a crash.  
A 6-month delay is realistic for off-plan flips when market activity slows.  
This scenario helps investors understand downside exposure.

---

### 7.3 Bull Scenario (Optimistic Case)

The bull case represents strong demand and favorable market conditions.

**Assumptions:**
bull_price_multiplier = 1.10 # 10% above expected flip price
bull_exit_delta_months = 0 # exit on originally planned timeline

exit_price_bull = expected_flip_price * bull_price_multiplier
exit_months_bull = planned_exit_months + bull_exit_delta_months


**Reasoning:**  
A 10% upside reflects realistic appreciation in high-demand areas.  
Most optimistic outcomes do not reduce holding periods, so the timeline remains unchanged for clarity.

---

### 7.4 Scenario Outputs

For each scenario (bear, base, bull), the platform recomputes:
total_cash_out_s
capital_required_s
profit_s
simple_roi_pct_s
holding_period_s


## 8. Risk Model

Risk assessment provides a qualitative understanding of downside exposure across multiple dimensions.  
Each dimension is classified as **Low**, **Medium**, or **High** based on objective thresholds derived from the underlying data.

The risk model includes:

- Market Risk  
- Developer Risk  
- Liquidity Risk  
- Payment Plan Risk  
- Overall Risk Rating  

---

### 8.1 Market Risk

Market risk reflects the stability and growth characteristics of the area.

**Logic:**
If stability_score ≥ 70 AND growth_normalized ≥ 50 -> Low
If stability_score ≥ 40 AND growth_normalized ≥ 30 -> Medium
Else -> High


**Reasoning:**  
Areas with stable historical pricing and positive growth trends present lower market risk.  
Volatile or underperforming areas carry greater downside exposure.

---

### 8.2 Developer Risk

Developer risk evaluates the reliability and execution quality of the developer.

**Logic:**
If developer_trust_score ≥ 80 -> Low
If 60 ≤ developer_trust_score < 80 -> Medium
Else -> High

**Reasoning:**  
High-trust developers reduce delivery risk and improve resale confidence.  
Lower scores indicate greater uncertainty around project execution.

---

### 8.3 Liquidity Risk

Liquidity risk is the inverse of how easy it is to exit a property.

**Logic:**
If liquidity_score ≥ 70 -> Low
If 50 ≤ liquidity_score < 70 -> Medium
Else -> High

**Reasoning:**  
High-liquidity areas support faster resale, while low-liquidity areas may require longer holding periods or price reductions.

---

### 8.4 Payment Plan Risk

Payment plan risk reflects the cashflow burden on the investor, especially the percentage due at handover.

Let:
handover_share = (sum of handover payments) / booking_price

**Logic:**
If handover_share ≤ 40% -> Low
If 41%-60% -> Medium
If > 60% -> High

**Reasoning:**  
Front-loaded payment plans reduce risk by spreading out cash commitments.  
Heavy handover payments create liquidity stress and financing uncertainty.

---

### 8.5 Overall Risk Rating

Overall risk consolidates individual risk categories.

**Logic:**
If 2 or more categories are High -> Overall Risk = High
Else if at least 1 High OR 2 Medium -> Overall Risk = Medium
Else -> Low

**Reasoning:**  
A deal is considered high risk if weaknesses appear in multiple dimensions.  
Medium risk reflects moderate concerns in one or two areas.  
Low risk indicates a well-balanced deal with minimal downside exposure.

## 9. Deal Scoring Model (0-100)

The deal scoring model aggregates area quality, developer reliability, liquidity strength, ROI potential, and risk exposure into a single numerical rating between 0 and 100.

The goal is to provide a transparent, easily interpretable summary of overall deal attractiveness.

---

### 9.1 Components Used in Deal Scoring

The score is derived from the following engineered features:

- **Area Viability Score**  
- **Developer Trust Score**  
- **Liquidity Score**  
- **ROI Score** 
- **Risk Penalty** 

---

### 9.2 ROI Score Conversion (0-100)

ROI percentage is converted into a score using simple tiered thresholds:

**Logic:**
If base_roi_pct ≥ 25% -> roi_score = 100
If 15% ≤ base_roi_pct < 25% -> roi_score = 80
If 8% ≤ base_roi_pct < 15% -> roi_score = 60
Else -> roi_score = scaled value between 0-50

**Reasoning:**  
- ROI ≥ 25% is considered highly attractive for off-plan flips.  
- 15-25% represents strong returns.  
- 8-15% is moderate but acceptable.  
- Below 8% signals limited upside.

---

### 9.3 Risk Penalty

Risk is incorporated by subtracting a penalty from the overall score:

**Logic:**
High Risk -> penalty = 30
Medium Risk -> penalty = 15
Low Risk -> penalty = 0

**Reasoning:**  
This adjustment prevents high-risk deals from appearing overly attractive even if ROI is strong.

---

### 9.4 Weighted Deal Score Formula

The final score is computed using a weighted combination of components:

**Formula:**
raw_deal_score =
0.30 * area_viability_score +
0.25 * developer_trust_score +
0.20 * liquidity_score +
0.15 * roi_score -
0.10 * risk_penalty

**Reasoning:**  
- **Area viability (30%)** is the strongest driver, as location fundamentally determines demand and pricing.  
- **Developer trust (25%)** reflects execution and delivery reliability.  
- **Liquidity (20%)** captures the ability to exit the investment.  
- **ROI (15%)** measures return potential but depends on assumptions, so weighted moderately.  
- **Risk penalty (10%)** ensures downside exposure is appropriately represented.

---

### 9.5 Score Interpretation

| Score Range | Interpretation |
|-------------|----------------|
| **80-100** | Very Attractive - strong fundamentals and low risk |
| **60-79**  | Attractive - good overall deal with manageable risks |
| **40-59**  | Neutral - mixed signals, moderate risk or limited upside |
| **0-39**   | Weak / High Risk - poor fundamentals or high downside |


