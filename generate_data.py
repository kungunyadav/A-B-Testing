import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)  # taaki har baar same random data bane (testing ke liye)


n_control = 5000
n_treatment = 5000


control_conversion_rate = 0.10
treatment_conversion_rate = 0.12

start_date = datetime(2025, 6, 1)

def generate_group(n, rate, group_name):
    
    conversions = np.random.binomial(1, rate, n)
    user_ids = [f"{group_name[:1].upper()}{i:06d}" for i in range(1, n+1)]
    days_offset = np.random.randint(0, 30, n)
    signup_dates = [start_date + timedelta(days=int(d)) for d in days_offset]
    time_on_page = np.random.gamma(shape=2.0, scale=25 if group_name=="control" else 28, size=n)
    return pd.DataFrame({
        "user_id": user_ids,
        "group": group_name,
        "signup_date": signup_dates,
        "time_on_page_sec": time_on_page.round(1),
        "converted": conversions
    })

df_control = generate_group(n_control, control_conversion_rate, "control")
df_treatment = generate_group(n_treatment, treatment_conversion_rate, "treatment")

df = pd.concat([df_control, df_treatment], ignore_index=True)
df = df.sample(frac=1, random_state=1).reset_index(drop=True)

df.to_csv("ab_test_data.csv", index=False)

print(df.head(10))
print("\nShape:", df.shape)
print("\nConversion counts by group:")
print(df.groupby("group")["converted"].agg(["count", "sum", "mean"]))