import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

plt.rcParams["figure.dpi"] = 300
sns.set_theme(style="whitegrid")

panel = pd.read_csv("panel_final.csv", parse_dates=["date"])

# set Micron's announcment date as announcement and set the control counties into "control counties" variable
ANNOUNCEMENT = pd.Timestamp("2022-10-01")
CONTROL_COUNTIES = ["Erie County", "Monroe County", "Lackawanna County", "Lucas County"]

print("pre v. post counties comparison")

# group into 4 groups
summary = (panel.groupby(["treated", "post"])[["home_value_idx", "rent_idx"]].mean().round(2))
summary.index = summary.index.map({
    (0, 0): "Control (Pre)",
    (0, 1): "Control (Post)",
    (1, 0): "Treated (Pre)",
    (1, 1): "Treated (Post)",
})
print(summary.to_string())

home_value = summary["home_value_idx"]
rent = summary["rent_idx"]

did_home_value = (home_value["Treated (Post)"] - home_value["Treated (Pre)"]) - \
         (home_value["Control (Post)"] - home_value["Control (Pre)"])
did_rent_index = (rent["Treated (Post)"] - rent["Treated (Pre)"]) - \
         (rent["Control (Post)"] - rent["Control (Pre)"])

print("\n(index: Jan 2022=100)")
print(f"DiD estimate (home value index): {did_home_value:+.2f}")
print(f"DiD estimate (rent index): {did_rent_index:+.2f}")

control = panel[panel["treated"] == 0].groupby("date")[["home_value_idx", "rent_idx"]].mean().reset_index()
control["RegionName"] = "Control Average"
treated = panel[panel["treated"] == 1][["date", "home_value_idx", "rent_idx", "RegionName"]].copy()

plot_df = pd.concat([treated, control], ignore_index=True)

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Parallel Trend of Home Value Index (Jan 2022 = 100)", fontsize=13)

for name, grp in plot_df.groupby("RegionName"):
    lw = 2.2 if name == "Onondaga County" else 1.2
    ls = "-" if name == "Onondaga County" else "--"
    color = "tomato" if name == "Onondaga County" else "steelblue"
    ax.plot(grp["date"], grp["home_value_idx"], label=name, linewidth=lw, linestyle=ls, color=color)

# announcement date critera
ax.axvline(ANNOUNCEMENT, color="black", linestyle=":", linewidth=1.5, label="Micron announcement")

ax.set_xlabel("")
ax.set_ylabel("Index")
ax.legend(fontsize=8)
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("01. Parellel Trends of Home Value Index.png")
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Parallel Trends of Rent Index (Jan 2022 = 100)", fontsize=13)

for name, grp in plot_df.groupby("RegionName"):
    lw = 2.2 if name == "Onondaga County" else 1.2
    ls = "-" if name == "Onondaga County" else "--"
    color = "tomato" if name == "Onondaga County" else "steelblue"
    ax.plot(grp["date"], grp["rent_idx"], label=name, linewidth=lw, linestyle=ls, color=color)

# announcement date critera
ax.axvline(ANNOUNCEMENT, color="black", linestyle=":", linewidth=1.5, label="Micron announcement")

ax.set_xlabel("")
ax.set_ylabel("Index")
ax.legend(fontsize=8)
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("01. Parallel Trends of Rent Index.png")
plt.show()

onondaga = panel[panel["treated"] == 1][["date", "home_value_idx", "rent_idx"]].set_index("date")
ctrl_avg  = control.set_index("date")[["home_value_idx", "rent_idx"]]

gap = (onondaga - ctrl_avg).reset_index()
gap.columns = ["date", "gap_home_value", "gap_rent"]

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Gap Between Onondaga and Control Average (Home Value Index)", fontsize=13)

ax.plot(gap["date"], gap["gap_home_value"], color="tomato", linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)
ax.axvline(ANNOUNCEMENT, color="black", linestyle=":", linewidth=1.5, label="Micron announcement")
ax.axvspan(ANNOUNCEMENT, gap["date"].max(), alpha=0.08, color="gray", label="Post-announcement")
ax.set_ylabel("Difference")
ax.legend(fontsize=9)
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("02. Gap (Home Value Index).png")
plt.show()

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Gap Between Onondaga and Control Average (Rent Index)", fontsize=13)

ax.plot(gap["date"], gap["gap_rent"], color="steelblue", linewidth=2)
ax.axhline(0, color="black", linewidth=0.8)

# announcement date criteria
ax.axvline(ANNOUNCEMENT, color="black", linestyle=":", linewidth=1.5, label="Micron announcement")
ax.axvspan(ANNOUNCEMENT, gap["date"].max(), alpha=0.08, color="gray", label="Post-announcement")

ax.set_ylabel("Difference")
ax.legend(fontsize=9)
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("02. Gap (Rent Index).png")
plt.show()

did_results = pd.DataFrame({
    "Metric": ["Home Value", "Rent"],
    "DiD": [did_home_value, did_rent_index],
})

fig, ax = plt.subplots(figsize=(6, 4))
colors = ["tomato" if v > 0 else "steelblue" for v in did_results["DiD"]]
bars = ax.bar(did_results["Metric"], did_results["DiD"], color=colors, width=0.4, edgecolor="white")

ax.axhline(0, color="black", linewidth=0.8)
ax.set_title("Index Difference by Micron Announcement Effect (Index points")
ax.set_ylabel("Difference")

for bar, val in zip(bars, did_results["DiD"]):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (0.1 if val >= 0 else -0.3),
            f"{val:+.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")

plt.tight_layout()
plt.savefig("03. Index Difference.png")
plt.show()

palette = {
    "Onondaga County":   "tomato",
    "Erie County":       "#4878CF",
    "Monroe County":     "#6ACC65",
    "Lackawanna County": "#D65F5F",
    "Lucas County":      "#B47CC7",
}

fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Home Value Index by County (Jan 2022 = 100)", fontsize=13)

for name, grp in panel.groupby("RegionName"):
    lw = 2.5 if name == "Onondaga County" else 1.2
    ax.plot(grp["date"], grp["home_value_idx"],
            label=name, linewidth=lw, color=palette.get(name, "gray"))

ax.axvline(ANNOUNCEMENT, color="black", linestyle=":", linewidth=1.5)
ax.set_ylabel("Index (Jan 2022 = 100)")
ax.legend(fontsize=8)
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("04. Home Value Index by County.png")
plt.show()

# Fig 4-2: Rent Index by County
fig, ax = plt.subplots(figsize=(8, 5))
fig.suptitle("Rent Index by County (Jan 2022 = 100)", fontsize=13)

for name, grp in panel.groupby("RegionName"):
    lw = 2.5 if name == "Onondaga County" else 1.2
    ax.plot(grp["date"], grp["rent_idx"],
            label=name, linewidth=lw, color=palette.get(name, "gray"))

ax.axvline(ANNOUNCEMENT, color="black", linestyle=":", linewidth=1.5)
ax.set_ylabel("Index (Jan 2022 = 100)")
ax.legend(fontsize=8)
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right")
plt.tight_layout()
plt.savefig("04. Rent Index by County.png")
plt.show()