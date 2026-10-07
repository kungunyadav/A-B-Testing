import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

with open("test_results.json") as f:
    r = json.load(f)

df = pd.read_csv("ab_test_data.csv")

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

groups = ["Control", "Treatment"]
rates = [r["rate_control"]*100, r["rate_treatment"]*100]
ci_low = [r["control_ci_95"][0], r["treatment_ci_95"][0]]
ci_high = [r["control_ci_95"][1], r["treatment_ci_95"][1]]
err_low = [rates[i]-ci_low[i] for i in range(2)]
err_high = [ci_high[i]-rates[i] for i in range(2)]

colors = ["#94a3b8", "#2563eb"]
bars = axes[0].bar(groups, rates, color=colors, width=0.55, zorder=3)
axes[0].errorbar(groups, rates, yerr=[err_low, err_high], fmt='none',
                  ecolor='black', capsize=6, linewidth=1.5, zorder=4)

for bar, rate, top in zip(bars, rates, ci_high):
    axes[0].text(bar.get_x() + bar.get_width()/2, top + 0.5, f"{rate:.2f}%",
                 ha='center', fontsize=11, fontweight='bold')

axes[0].set_ylabel("Conversion Rate (%)", fontsize=11)
axes[0].set_title(f"Conversion Rate by Group\n(p = {r['chi2_p_value']:.1e})",
                   fontsize=12, fontweight='bold')
axes[0].set_ylim(0, max(ci_high)+3)
axes[0].grid(axis='y', alpha=0.3, zorder=0)
axes[0].spines[['top','right']].set_visible(False)

control_time = df[df["group"]=="control"]["time_on_page_sec"]
treatment_time = df[df["group"]=="treatment"]["time_on_page_sec"]

axes[1].hist(control_time, bins=40, alpha=0.6, label="Control", color="#94a3b8", density=True)
axes[1].hist(treatment_time, bins=40, alpha=0.6, label="Treatment", color="#2563eb", density=True)
axes[1].set_xlabel("Time on Page (seconds)", fontsize=11)
axes[1].set_ylabel("Density", fontsize=11)
axes[1].set_title("Engagement Distribution by Group", fontsize=12, fontweight='bold')
axes[1].legend(frameon=False)
axes[1].spines[['top','right']].set_visible(False)

plt.tight_layout()
plt.savefig("ab_test_results.png", dpi=150, bbox_inches="tight")
print("Saved chart to ab_test_results.png")
plt.show()