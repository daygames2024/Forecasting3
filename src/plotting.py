
import matplotlib
import matplotlib.pyplot as plt

# Use Agg for headless environments, but you can switch to TkAgg if running locally
matplotlib.use("Agg")

def plot_part_quarter(part, series_q, fc, plots_dir):
    try:
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 4))

        # Plot historical data
        series_q.plot(ax=ax, marker="o", label="Historical")

        # Plot forecast data
        ax.plot(fc["quarters"], fc["values"], marker="x", label="Forecast")

        # Title and labels
        ax.set_title(f"Part: {part}")
        ax.set_xlabel("Quarter")
        ax.set_ylabel("Value")
        ax.legend()

        # ✅ Safe axis limits
        # Handle cases where series or forecast has only one point
        if len(series_q) > 0 and len(fc["values"]) > 0:
            x_min = -0.5
            x_max = len(series_q) + len(fc["quarters"]) + 0.5
            y_max = max(series_q.max(), max(fc["values"])) * 1.1
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(0, y_max)
        else:
            ax.set_xlim(-1, 1)
            ax.set_ylim(0, 1)

        # ✅ Save plot
        plot_path = plots_dir / f"{part}_forecast.png"
        fig.savefig(plot_path, bbox_inches="tight")
        plt.close(fig)

        print(f"[INFO] Plot saved for {part}: {plot_path}")
        return plot_path

    except Exception as e:
        # Print error for visibility and return None
        print(f"[PLOT ERROR] Part {part}: {e}")
        return None
``
