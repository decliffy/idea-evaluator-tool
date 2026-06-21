"""Renders the high-level AWS architecture diagram to architecture.png."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

# Palette
AWS_ORANGE = "#FF9900"
AWS_NAVY = "#232F3E"
BLUE = "#2E73B8"
GREEN = "#3F8624"
PURPLE = "#7D3AC1"
GREY = "#5A6B7B"
ANTHRO = "#D4A27F"

fig, ax = plt.subplots(figsize=(14, 7.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 7.5)
ax.axis("off")


def box(x, y, w, h, title, subtitle, color, text_color="white"):
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=1.5, edgecolor=color, facecolor=color, alpha=0.95,
            mutation_aspect=1,
        )
    )
    ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center",
            fontsize=11, fontweight="bold", color=text_color)
    if subtitle:
        ax.text(x + w / 2, y + h * 0.27, subtitle, ha="center", va="center",
                fontsize=8, color=text_color)


def arrow(x1, y1, x2, y2, label="", color=AWS_NAVY, offset=0.18, style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle=style, mutation_scale=18,
            linewidth=1.8, color=color, shrinkA=2, shrinkB=2,
        )
    )
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + offset, label, ha="center", va="bottom",
                fontsize=8, color=color, style="italic")


# Title
ax.text(7, 7.15, "Idea Evaluator — AWS Architecture", ha="center",
        fontsize=16, fontweight="bold", color=AWS_NAVY)
ax.text(7, 6.75, "FastAPI + React idea-scoring app  ·  account 237414921190  ·  us-east-1",
        ha="center", fontsize=9.5, color=GREY)

# AWS account boundary
ax.add_patch(
    Rectangle((2.55, 0.7), 8.4, 5.5, linewidth=1.4, edgecolor=AWS_ORANGE,
              facecolor="none", linestyle=(0, (6, 4)))
)
ax.text(2.75, 6.0, "AWS  (us-east-1)", fontsize=9, fontweight="bold", color=AWS_ORANGE)

# Nodes
box(0.25, 3.1, 1.9, 1.2, "Browser", "React SPA", GREY)
box(2.9, 3.1, 1.9, 1.6, "CloudFront", "HTTPS CDN\n(2 behaviors)", BLUE)
box(5.5, 4.5, 2.1, 1.3, "S3 bucket", "private · static build\n(OAC)", GREEN)
box(5.5, 1.3, 2.3, 1.4, "Lambda Function URL", "AWS_IAM · OAC SigV4", PURPLE)
box(8.2, 1.3, 2.5, 1.4, "Lambda", "FastAPI + Mangum\nPython 3.13", AWS_ORANGE, text_color=AWS_NAVY)
box(11.4, 1.3, 2.3, 1.4, "Claude API", "claude-sonnet-4-6", ANTHRO, text_color=AWS_NAVY)

# Arrows
arrow(2.15, 3.7, 2.9, 3.85, "HTTPS", color=AWS_NAVY)
# CloudFront -> S3 (default behavior)
arrow(4.8, 4.35, 5.5, 4.95, "", color=GREEN)
ax.text(4.55, 5.05, "default → static", ha="left", va="bottom",
        fontsize=8, color=GREEN, style="italic")
# CloudFront -> Lambda Function URL (/api/*)
arrow(4.85, 3.5, 5.6, 2.35, "", color=PURPLE)
ax.text(4.45, 2.95, "/api/*\n(OAC-signed)", ha="right", va="center",
        fontsize=8, color=PURPLE, style="italic")
# Function URL -> Lambda
arrow(7.8, 2.0, 8.2, 2.0, "", color=AWS_NAVY)
# Lambda -> Claude
arrow(10.7, 2.0, 11.4, 2.0, "HTTPS", color=AWS_NAVY)

# Note on body signing
ax.text(6.65, 0.95, "POST body hash sent as x-amz-content-sha256 so CloudFront OAC can sign requests",
        ha="center", fontsize=7.5, color=PURPLE, style="italic")

# Claude is external — small label
ax.text(12.55, 2.85, "external", ha="center", fontsize=7.5, color=GREY, style="italic")

plt.tight_layout()
out = __file__.rsplit("/", 1)[0] + "/architecture.png"
plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print("wrote", out)
