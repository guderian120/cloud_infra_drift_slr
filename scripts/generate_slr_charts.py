"""
SLR Visualization Generator
============================
Generates all relevant charts and diagrams for the Systematic Literature Review:
"Cloud Infrastructure Drift Detection and Remediation in Multi-Cloud Environments (2019-2025)"

Output: ./images/<chart_name>.png
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import patheffects

# ──────────────────────────────────────────────
# Global style
# ──────────────────────────────────────────────
BG_DARK   = "#1a1a2e"
BG_CARD   = "#16213e"
ACCENT_1  = "#0f3460"
ACCENT_2  = "#533483"
TEXT_COL  = "#e0e0e0"
GRID_COL  = "#2a2a4a"

PALETTE = [
    "#00d2ff", "#7b2ff7", "#f72585", "#4cc9f0",
    "#3a86ff", "#8338ec", "#ff006e", "#fb5607",
    "#ffbe0b", "#06d6a0", "#118ab2", "#ef476f",
]

plt.rcParams.update({
    "figure.facecolor":  BG_DARK,
    "axes.facecolor":    BG_CARD,
    "axes.edgecolor":    GRID_COL,
    "axes.labelcolor":   TEXT_COL,
    "axes.grid":         True,
    "grid.color":        GRID_COL,
    "grid.alpha":        0.4,
    "text.color":        TEXT_COL,
    "xtick.color":       TEXT_COL,
    "ytick.color":       TEXT_COL,
    "font.family":       "sans-serif",
    "font.size":         12,
    "legend.facecolor":  BG_CARD,
    "legend.edgecolor":  GRID_COL,
    "savefig.facecolor": BG_DARK,
    "savefig.dpi":       300,
})

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT_DIR, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  [OK] {name}")


# ═══════════════════════════════════════════════
# 1. PRISMA Flow Diagram
# ═══════════════════════════════════════════════
def prisma_flow():
    fig, ax = plt.subplots(figsize=(14, 18))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 22)
    ax.axis("off")
    fig.patch.set_facecolor(BG_DARK)

    # ---- helpers ----
    def box(x, y, w, h, text, color="#0f3460", fontsize=10, bold=False):
        bx = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.3", linewidth=1.5,
            edgecolor=color, facecolor=color + "33",
        )
        ax.add_patch(bx)
        weight = "bold" if bold else "normal"
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fontsize, color=TEXT_COL, weight=weight,
                wrap=True,
                path_effects=[patheffects.withStroke(linewidth=0, foreground=BG_DARK)])

    def arrow(x1, y1, x2, y2, color="#4cc9f0"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                     arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))

    def side_box(x, y, w, h, text, color="#f72585"):
        box(x, y, w, h, text, color=color, fontsize=9)

    # Title
    ax.text(7, 21.3, "PRISMA Flow Diagram", ha="center", va="center",
            fontsize=18, color="#00d2ff", weight="bold")
    ax.text(7, 20.8, "Cloud Infrastructure Drift Detection & Remediation SLR (2019-2025)",
            ha="center", va="center", fontsize=10, color="#7b7b9b")

    # --- Identification ---
    ax.text(1.0, 19.5, "IDENTIFICATION", fontsize=11, color="#00d2ff",
            weight="bold", rotation=90, va="center")

    box(7, 19.5, 8, 1.2,
        "Records identified through\ndatabase searching (n = 830)\n"
        "SciSpace: 600  |  Google Scholar: 110  |  ArXiv: 120",
        color="#3a86ff", fontsize=10, bold=True)

    arrow(7, 18.9, 7, 18.1)

    box(7, 17.5, 6, 1.0,
        "Records after duplicates removed\n(n = 683)  [Duplicates removed: 147, 17.7%]",
        color="#3a86ff", fontsize=10)

    side_box(12, 17.5, 3, 0.8,
             "Duplicates\nremoved\n(n = 147)", color="#f72585")
    arrow(10, 17.5, 10.5, 17.5, color="#f72585")

    # --- Screening ---
    ax.text(1.0, 15.0, "SCREENING", fontsize=11, color="#4cc9f0",
            weight="bold", rotation=90, va="center")

    arrow(7, 17.0, 7, 16.1)
    box(7, 15.5, 6, 1.0,
        "Records after year filter (2019-2025)\n(n = 391)",
        color="#533483", fontsize=10)

    side_box(12, 15.5, 3, 0.8,
             "Excluded\nby year\n(n = 292)", color="#f72585")
    arrow(10, 15.5, 10.5, 15.5, color="#f72585")

    arrow(7, 15.0, 7, 14.1)
    box(7, 13.5, 6, 1.0,
        "Records after abstract screening\n(Relevance Score ≥ 3.0)\n(n = 156)",
        color="#533483", fontsize=10)

    side_box(12, 13.5, 3, 0.8,
             "Excluded at\nabstract screening\n(n = 235)", color="#f72585")
    arrow(10, 13.5, 10.5, 13.5, color="#f72585")

    # --- Eligibility ---
    ax.text(1.0, 11.0, "ELIGIBILITY", fontsize=11, color="#7b2ff7",
            weight="bold", rotation=90, va="center")

    arrow(7, 13.0, 7, 12.1)
    box(7, 11.5, 6, 1.0,
        "Full-text articles assessed\nfor eligibility\n(n = 104)",
        color="#7b2ff7", fontsize=10)

    side_box(12, 11.5, 3, 0.8,
             "Full-text not\navailable\n(n = 52 retained\nfrom abstract)", color="#ff006e")
    arrow(10, 11.5, 10.5, 11.5, color="#ff006e")

    arrow(7, 11.0, 7, 10.1)
    box(7, 9.5, 6, 1.0,
        "Full-text articles included\nafter screening\n(n = 44)",
        color="#7b2ff7", fontsize=10)

    side_box(12, 9.5, 3, 0.8,
             "Excluded at\nfull-text screening\n(n = 60)", color="#f72585")
    arrow(10, 9.5, 10.5, 9.5, color="#f72585")

    # --- Included ---
    ax.text(1.0, 7.0, "INCLUDED", fontsize=11, color="#06d6a0",
            weight="bold", rotation=90, va="center")

    arrow(7, 9.0, 7, 8.1)
    box(7, 7.0, 8, 1.8,
        "Studies included in\nfinal synthesis (n = 96)\n\n"
        "Full-text reviewed: 44 (45.8%)\n"
        "Abstract-only reviewed: 52 (54.2%)",
        color="#06d6a0", fontsize=11, bold=True)

    save(fig, "prisma_flow_diagram.png")


# ═══════════════════════════════════════════════
# 2. Temporal Distribution
# ═══════════════════════════════════════════════
def temporal_distribution():
    years   = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    papers  = [5, 12, 5, 17, 15, 18, 24]
    pct     = [5.2, 12.5, 5.2, 17.7, 15.6, 18.8, 25.0]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(years, papers, color=PALETTE[:len(years)],
                  edgecolor="white", linewidth=0.5, width=0.65, zorder=3)
    ax.plot(years, papers, color="#00d2ff", linewidth=2, marker="o",
            markersize=8, zorder=4, markerfacecolor="#00d2ff")

    for bar, p, pv in zip(bars, papers, pct):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8,
                f"{p}\n({pv}%)", ha="center", va="bottom", fontsize=10,
                color=TEXT_COL, weight="bold")

    ax.set_xlabel("Publication Year", fontsize=13)
    ax.set_ylabel("Number of Papers", fontsize=13)
    ax.set_title("Temporal Distribution of Included Studies (2019–2025)\n"
                 "380% growth from 2019 to 2025",
                 fontsize=15, weight="bold", color="#00d2ff", pad=15)
    ax.set_xticks(years)
    ax.set_ylim(0, 32)

    # Annotation
    ax.annotate("380% increase", xy=(2025, 24), xytext=(2023.2, 28),
                fontsize=11, color="#f72585", weight="bold",
                arrowprops=dict(arrowstyle="->", color="#f72585", lw=1.5))
    fig.tight_layout()
    save(fig, "temporal_distribution.png")


# ═══════════════════════════════════════════════
# 3. Study Types Distribution
# ═══════════════════════════════════════════════
def study_types():
    labels = [
        "Tool/Framework\nProposals",
        "Empirical\nStudies",
        "Comparative\nAnalyses",
        "Experimental\nEvaluations",
        "Case\nStudies",
        "Literature\nReviews",
    ]
    sizes  = [40, 27, 13, 10, 7, 3]
    colors = PALETTE[:len(labels)]
    explode = (0.06, 0.03, 0, 0, 0, 0)

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.1f%%",
        startangle=140, pctdistance=0.78, explode=explode,
        textprops={"color": TEXT_COL, "fontsize": 11},
        wedgeprops={"edgecolor": BG_DARK, "linewidth": 2},
    )
    for t in autotexts:
        t.set_fontsize(11)
        t.set_weight("bold")

    ax.set_title("Study Types & Methodologies\n(Top 30 Papers)",
                 fontsize=15, weight="bold", color="#00d2ff", pad=20)
    fig.tight_layout()
    save(fig, "study_types_distribution.png")


# ═══════════════════════════════════════════════
# 4. Publication Venues
# ═══════════════════════════════════════════════
def publication_venues():
    venues = [
        "ArXiv Preprints",
        "IEEE Cloud Computing\nConferences",
        "ACM Symposiums",
        "ICSE / SE Conferences",
        "IEEE Access",
        "IEEE Trans. on SE",
        "IEEE Trans. on CC",
        "Info & Soft. Tech.",
        "Domain-Specific\nJournals",
    ]
    counts = [18, 3, 2, 2, 2, 1, 1, 1, 10]

    fig, ax = plt.subplots(figsize=(12, 7))
    y_pos = np.arange(len(venues))
    bars = ax.barh(y_pos, counts, color=PALETTE[:len(venues)],
                   edgecolor="white", linewidth=0.5, height=0.6, zorder=3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(venues, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Papers", fontsize=13)
    ax.set_title("Publication Venues Distribution",
                 fontsize=15, weight="bold", color="#00d2ff", pad=15)

    for bar, c in zip(bars, counts):
        pct = c / 96 * 100
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{c} ({pct:.1f}%)", va="center", fontsize=10, color=TEXT_COL, weight="bold")

    ax.set_xlim(0, max(counts) + 5)
    fig.tight_layout()
    save(fig, "publication_venues.png")


# ═══════════════════════════════════════════════
# 5. Geographic Distribution
# ═══════════════════════════════════════════════
def geographic_dist():
    regions = ["North America\n(US, Canada)", "Europe\n(UK, DE, PT, NL)",
               "Asia\n(IN, CN, SG)", "Other\n(AU, BR)"]
    shares  = [35, 30, 25, 10]
    colors  = ["#3a86ff", "#7b2ff7", "#f72585", "#ffbe0b"]

    fig, ax = plt.subplots(figsize=(9, 8))
    wedges, texts, autotexts = ax.pie(
        shares, labels=regions, colors=colors, autopct="%1.0f%%",
        startangle=90, pctdistance=0.75,
        textprops={"color": TEXT_COL, "fontsize": 12},
        wedgeprops={"edgecolor": BG_DARK, "linewidth": 2, "width": 0.45},
    )
    for t in autotexts:
        t.set_fontsize(13)
        t.set_weight("bold")

    ax.set_title("Geographic Distribution of Author Affiliations",
                 fontsize=15, weight="bold", color="#00d2ff", pad=20)
    fig.tight_layout()
    save(fig, "geographic_distribution.png")


# ═══════════════════════════════════════════════
# 6. Drift Detection Methods — Radar Chart
# ═══════════════════════════════════════════════
def detection_radar():
    methods = ["State-Based", "API Trace", "Policy-Based",
               "Continuous\nReconciliation", "ML-Based"]
    # Scored 1-5 from SLR Table 1
    accuracy    = [4, 5, 3, 4, 2]
    latency     = [3, 5, 5, 4, 3]   # lower is better → inverted
    coverage    = [3, 5, 3, 5, 2]
    automation  = [4, 5, 4, 5, 3]
    multicloud  = [2, 5, 5, 5, 3]

    categories = ["Accuracy", "Latency\n(inverse)", "Coverage",
                  "Automation", "Multi-Cloud\nSupport"]
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_facecolor(BG_CARD)
    fig.patch.set_facecolor(BG_DARK)

    colors_r = ["#3a86ff", "#00d2ff", "#f72585", "#06d6a0", "#ffbe0b"]
    datasets = [accuracy, latency, coverage, automation, multicloud]

    # Actually plot each method across categories
    all_methods_data = list(zip(accuracy, latency, coverage, automation, multicloud))
    for i, (method, color) in enumerate(zip(methods, colors_r)):
        vals = list(all_methods_data[i]) + [all_methods_data[i][0]]
        ax.plot(angles, vals, "o-", linewidth=2, label=method.replace("\n", " "), color=color)
        ax.fill(angles, vals, alpha=0.10, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, color=TEXT_COL)
    ax.set_ylim(0, 5.5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=9, color="#7b7b9b")
    ax.yaxis.grid(True, color=GRID_COL, alpha=0.4)
    ax.xaxis.grid(True, color=GRID_COL, alpha=0.4)
    ax.spines["polar"].set_color(GRID_COL)

    ax.set_title("Drift Detection Methods — Comparative Radar",
                 fontsize=15, weight="bold", color="#00d2ff", pad=25)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=10)
    fig.tight_layout()
    save(fig, "drift_detection_comparison.png")


# ═══════════════════════════════════════════════
# 7. Remediation Strategies Comparison
# ═══════════════════════════════════════════════
def remediation_strategies():
    strategies = ["Manual", "Semi-\nAutomated", "Fully\nAutomated", "Rollback", "Forward\nCorrection"]

    # Encode ordinal scores (1-5) for each dimension
    mttr        = [1, 3, 5, 5, 4]     # higher is better (faster)
    automation  = [1, 3, 5, 5, 4]
    risk        = [3, 4, 4, 5, 3]     # higher = lower risk = better
    scalability = [1, 3, 5, 5, 3]

    x = np.arange(len(strategies))
    w = 0.18

    fig, ax = plt.subplots(figsize=(13, 7))
    colors = ["#3a86ff", "#7b2ff7", "#06d6a0", "#f72585"]
    dims = ["MTTR (speed)", "Automation Level", "Safety (inverse risk)", "Scalability"]

    for i, (vals, label, col) in enumerate(zip(
            [mttr, automation, risk, scalability], dims, colors)):
        bars = ax.bar(x + i * w, vals, w, label=label, color=col,
                      edgecolor="white", linewidth=0.5, zorder=3)

    ax.set_xticks(x + 1.5 * w)
    ax.set_xticklabels(strategies, fontsize=12)
    ax.set_ylabel("Score (1 = lowest, 5 = highest)", fontsize=12)
    ax.set_ylim(0, 6.2)
    ax.set_title("Remediation Strategies — Multi-Dimension Comparison",
                 fontsize=15, weight="bold", color="#00d2ff", pad=15)
    ax.legend(fontsize=10, ncol=2)
    fig.tight_layout()
    save(fig, "remediation_strategies_comparison.png")


# ═══════════════════════════════════════════════
# 8. IaC Tools Market Share & Comparison
# ═══════════════════════════════════════════════
def iac_tools():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7),
                                    gridspec_kw={"width_ratios": [1, 1.4]})

    # --- Left: Market share donut ---
    tools  = ["Terraform", "Ansible", "CloudFormation", "Pulumi/CDK", "Others"]
    shares = [62, 15, 10, 8, 5]
    colors = ["#00d2ff", "#7b2ff7", "#f72585", "#06d6a0", "#ffbe0b"]
    explode = (0.05, 0, 0, 0, 0)

    wedges, texts, autotexts = ax1.pie(
        shares, labels=tools, colors=colors, autopct="%1.0f%%",
        startangle=90, pctdistance=0.78, explode=explode,
        textprops={"color": TEXT_COL, "fontsize": 11},
        wedgeprops={"edgecolor": BG_DARK, "linewidth": 2, "width": 0.45},
    )
    for t in autotexts:
        t.set_fontsize(12)
        t.set_weight("bold")
    ax1.set_title("IaC Tools Market Share (2025)",
                  fontsize=13, weight="bold", color="#00d2ff", pad=15)

    # --- Right: Feature comparison heatmap ---
    tool_names = ["Terraform", "CloudFormation", "Ansible", "Pulumi", "CDK"]
    features = ["Multi-Cloud", "Drift Detection", "State Mgmt",
                "Learning Curve\n(easy→hard)", "Community"]
    # Scores 1-5
    data = np.array([
        [5, 1, 4, 4, 3],   # Multi-Cloud
        [5, 3, 2, 4, 4],   # Drift Detection
        [5, 3, 1, 4, 4],   # State Mgmt
        [3, 3, 2, 4, 4],   # Learning Curve (inverted: 5=easy)
        [5, 3, 4, 3, 3],   # Community
    ])

    cmap = plt.cm.get_cmap("cool")
    im = ax2.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=5)

    ax2.set_xticks(np.arange(len(tool_names)))
    ax2.set_xticklabels(tool_names, fontsize=11, rotation=30, ha="right")
    ax2.set_yticks(np.arange(len(features)))
    ax2.set_yticklabels(features, fontsize=11)

    for i in range(len(features)):
        for j in range(len(tool_names)):
            ax2.text(j, i, str(data[i, j]), ha="center", va="center",
                     fontsize=13, weight="bold",
                     color="white" if data[i, j] < 3 else BG_DARK)

    ax2.set_title("IaC Tools Feature Comparison (1-5 scale)",
                  fontsize=13, weight="bold", color="#00d2ff", pad=15)
    cbar = fig.colorbar(im, ax=ax2, fraction=0.03, pad=0.04)
    cbar.ax.tick_params(colors=TEXT_COL)

    fig.tight_layout(w_pad=4)
    save(fig, "iac_tools_comparison.png")


# ═══════════════════════════════════════════════
# 9. Thematic Clusters
# ═══════════════════════════════════════════════
def thematic_clusters():
    themes = [
        "AI-Augmented\nDrift Reconciliation",
        "Policy-Driven\nFrameworks",
        "GitOps\nMethodologies",
        "Multi-Cloud\nOrchestration",
        "State\nManagement",
        "IaC Tool\nEvolution",
    ]
    # Approximate weight of each theme in the literature (relative)
    weights = [18, 16, 14, 15, 12, 25]
    highlights = [
        "97% accuracy",
        "78% misconfig\nreduction",
        "30s-5min\nreconciliation",
        "94% adoption\nrate",
        "Defect\nanalysis",
        "62% Terraform\nmarket share",
    ]

    colors = PALETTE[:6]
    fig, ax = plt.subplots(figsize=(13, 7))
    bars = ax.barh(np.arange(len(themes)), weights, color=colors,
                   edgecolor="white", linewidth=0.5, height=0.6, zorder=3)
    ax.set_yticks(np.arange(len(themes)))
    ax.set_yticklabels(themes, fontsize=12)
    ax.invert_yaxis()
    ax.set_xlabel("Relative Presence in Literature (%)", fontsize=12)
    ax.set_title("Six Thematic Clusters in Drift Management Research",
                 fontsize=15, weight="bold", color="#00d2ff", pad=15)

    for bar, h, c in zip(bars, highlights, colors):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
                h, va="center", fontsize=10, color=c, weight="bold")

    ax.set_xlim(0, max(weights) + 12)
    fig.tight_layout()
    save(fig, "thematic_clusters.png")


# ═══════════════════════════════════════════════
# 10. Key Metrics Dashboard
# ═══════════════════════════════════════════════
def key_metrics():
    metrics = [
        ("97%",   "AI-Augmented\nDetection Accuracy",   "#00d2ff"),
        ("78%",   "Security Misconfig\nReduction",       "#7b2ff7"),
        ("83%",   "Fewer Audit\nFindings",               "#f72585"),
        ("91%",   "Credential Incident\nDecrease",       "#06d6a0"),
        ("62%",   "Terraform\nMarket Share",             "#3a86ff"),
        ("50-67%","MTTR\nReduction",                     "#ffbe0b"),
        ("60%",   "Faster Infrastructure\nDeployment",   "#ff006e"),
        ("380%",  "Research Growth\n2019→2025",           "#8338ec"),
        ("94%",   "Multi-Cloud\nAdoption Rate",          "#4cc9f0"),
        ("42%",   "Operational\nEfficiency Gain",        "#fb5607"),
    ]

    fig, axes = plt.subplots(2, 5, figsize=(20, 8))
    axes = axes.flatten()

    for ax, (val, label, col) in zip(axes, metrics):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        # Card background
        card = FancyBboxPatch(
            (0.05, 0.05), 0.9, 0.9,
            boxstyle="round,pad=0.05", linewidth=2,
            edgecolor=col, facecolor=col + "18",
        )
        ax.add_patch(card)

        ax.text(0.5, 0.62, val, ha="center", va="center",
                fontsize=26, weight="bold", color=col)
        ax.text(0.5, 0.28, label, ha="center", va="center",
                fontsize=10, color=TEXT_COL, linespacing=1.3)

    fig.suptitle("Key Metrics from the Systematic Literature Review",
                 fontsize=17, weight="bold", color="#00d2ff", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "key_metrics_dashboard.png")


# ═══════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════
if __name__ == "__main__":
    print(f"\nGenerating SLR Visualizations -> {OUT_DIR}\n")
    prisma_flow()
    temporal_distribution()
    study_types()
    publication_venues()
    geographic_dist()
    detection_radar()
    remediation_strategies()
    iac_tools()
    thematic_clusters()
    key_metrics()
    print(f"\nAll 10 charts saved to {OUT_DIR}\n")
