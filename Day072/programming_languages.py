import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

years = np.arange(2014, 2024)
languages = ["Python", "JavaScript", "Java", "C++", "TypeScript", "Go", "Rust", "PHP"]
colors = ["#3776AB", "#F7DF1E", "#ED8B00", "#00599C", "#3178C6", "#00ADD8", "#DEA584", "#777BB4"]

popularity = {}
for lang in languages:
    trend = np.random.uniform(0.5, 3.0) * (years - 2014)
    noise = np.random.normal(0, 1.5, len(years))
    base = np.random.uniform(5, 25)
    popularity[lang] = np.clip(base + trend + noise, 0, 100)

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle("Programming Language Popularity 2014-2023", fontsize=18, fontweight="bold")

ax1 = axes[0, 0]
for lang, color in zip(languages, colors):
    ax1.plot(years, popularity[lang], marker="o", label=lang, color=color, linewidth=2, markersize=4)
ax1.set_title("Popularity Over Time")
ax1.set_xlabel("Year")
ax1.set_ylabel("Popularity Index")
ax1.legend(fontsize=8, loc="upper left")
ax1.grid(True, alpha=0.3)

ax2 = axes[0, 1]
latest = {lang: popularity[lang][-1] for lang in languages}
sorted_langs = sorted(latest.items(), key=lambda x: x[1], reverse=True)
bar_colors = [colors[languages.index(l)] for l, _ in sorted_langs]
ax2.barh([l for l, _ in sorted_langs], [v for _, v in sorted_langs], color=bar_colors)
ax2.set_title("2023 Rankings")
ax2.set_xlabel("Popularity Index")
ax2.invert_yaxis()

ax3 = axes[1, 0]
shares = [max(popularity[lang][-1], 0.5) for lang in languages]
total = sum(shares)
wedges, texts, autotexts = ax3.pie(
    shares, labels=[f"{l} ({s/total*100:.1f}%)" for l, s in zip(languages, shares)],
    colors=colors, autopct="", startangle=140, textprops={"fontsize": 8}
)
ax3.set_title("Market Share (2023)")

ax4 = axes[1, 1]
growth = {}
for lang in languages:
    first_half = np.mean(popularity[lang][:5])
    second_half = np.mean(popularity[lang][5:])
    growth[lang] = ((second_half - first_half) / max(first_half, 0.1)) * 100

sorted_growth = sorted(growth.items(), key=lambda x: x[1], reverse=True)
grow_colors = [colors[languages.index(l)] for l, _ in sorted_growth]
ax4.bar([l for l, _ in sorted_growth], [v for _, v in sorted_growth], color=grow_colors)
ax4.set_title("Growth Rate (First vs Second Half)")
ax4.set_ylabel("Growth %")
ax4.tick_params(axis="x", rotation=45)
ax4.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("Day072/programming_languages.png", dpi=150, bbox_inches="tight")
print("Chart saved to Day072/programming_languages.png")
plt.close()
