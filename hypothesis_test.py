import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import json

df = pd.read_csv("ab_test_data.csv")

control = df[df["group"] == "control"]
treatment = df[df["group"] == "treatment"]

n_c, n_t = len(control), len(treatment)
x_c, x_t = control["converted"].sum(), treatment["converted"].sum()
p_c, p_t = x_c / n_c, x_t / n_t

# Chi-square test
contingency = np.array([[x_c, n_c - x_c], [x_t, n_t - x_t]])
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency, correction=False)

# Z-test
count = np.array([x_t, x_c])
nobs = np.array([n_t, n_c])
z_stat, p_z = proportions_ztest(count, nobs, alternative="two-sided")

# Effect size (Cohen's h)
def cohens_h(p1, p2):
    phi1 = 2 * np.arcsin(np.sqrt(p1))
    phi2 = 2 * np.arcsin(np.sqrt(p2))
    return phi1 - phi2

h = cohens_h(p_t, p_c)

# Confidence interval for difference
diff = p_t - p_c
se_diff = np.sqrt(p_c*(1-p_c)/n_c + p_t*(1-p_t)/n_t)
z_crit = stats.norm.ppf(0.975)
ci_low = diff - z_crit * se_diff
ci_high = diff + z_crit * se_diff

ci_c = proportion_confint(x_c, n_c, alpha=0.05, method='wilson')
ci_t = proportion_confint(x_t, n_t, alpha=0.05, method='wilson')

relative_lift = (p_t - p_c) / p_c * 100

results = {
    "n_control": int(n_c), "n_treatment": int(n_t),
    "conversions_control": int(x_c), "conversions_treatment": int(x_t),
    "rate_control": round(p_c, 4), "rate_treatment": round(p_t, 4),
    "absolute_diff_pct_points": round(diff*100, 2),
    "relative_lift_pct": round(relative_lift, 2),
    "chi2_statistic": round(chi2, 4), "chi2_p_value": round(p_chi2, 6),
    "z_statistic": round(z_stat, 4), "z_p_value": round(p_z, 6),
    "cohens_h": round(h, 4),
    "diff_ci_95_low": round(ci_low*100, 2), "diff_ci_95_high": round(ci_high*100, 2),
    "control_ci_95": [round(ci_c[0]*100,2), round(ci_c[1]*100,2)],
    "treatment_ci_95": [round(ci_t[0]*100,2), round(ci_t[1]*100,2)],
    "significant_at_95": bool(p_chi2 < 0.05)
}

with open("test_results.json", "w") as f:
    json.dump(results, f, indent=2)

for k, v in results.items():
    print(f"{k}: {v}")