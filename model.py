import math

def poisson_pmf(k, lam):
    if lam <= 0: return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)

def poisson_over(expected, line):
    threshold = math.ceil(line)
    p_less = sum(poisson_pmf(k, expected) for k in range(threshold))
    return 1 - p_less

def kelly_stake(bank, prob, odds, fraction=0.25, max_pct=0.05):
    b = odds - 1
    if b <= 0: return 0
    f = (prob * b - (1 - prob)) / b
    if f <= 0: return 0
    return round(bank * min(f * fraction, max_pct), 2)

def predict_hockey(exp1, exp2, home_boost=1.0, max_goals=15):
    if exp1 <= 0: exp1 = 0.1
    if exp2 <= 0: exp2 = 0.1
    exp1 *= home_boost
    p1 = px = p2 = 0.0
    for g1 in range(max_goals + 1):
        pg1 = poisson_pmf(g1, exp1)
        for g2 in range(max_goals + 1):
            p = pg1 * poisson_pmf(g2, exp2)
            if g1 > g2: p1 += p
            elif g1 == g2: px += p
            else: p2 += p
    return {"p1": p1, "px": px, "p2": p2, "total_exp": exp1 + exp2}
