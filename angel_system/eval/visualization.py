import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox, TextArea, AnchoredText
import numpy as np
import PIL
from pathlib import Path
import os


def plot_activity_confidence(label, gt_ranges, det_ranges, output_dir, custom_range=None, custom_range_color="red"):
    """
    Plot activity confidences
    :param label: String label of the activity class predictions to render.
    :param gt_ranges: A sequence of tuples indicating the starting and ending time of ground-truth
                      time ranges the label activity occurred in the image sequence.
    :param custom_range: Optional tuple indicating the starting and ending times of an additional
                         range to highlight in addition to the `gt_ranges`.
    :param custom_range_color: The color of the additional range to be drawn. If not set, we will
                               use "red".
    """
    # Determine time range to plot
    all_start_times = [p["time"][0] for p in gt_ranges]
    all_start_times.extend([p["time"][0] for p in det_ranges[label]])
    all_end_times = [p["time"][1] for p in gt_ranges]
    all_end_times.extend([p["time"][1] for p in det_ranges[label]])
    min_start_time = min(all_start_times)
    max_end_time = max(all_end_times)
    total_time_delta = max_end_time - min_start_time
    pad = 0.05 * total_time_delta

    # Setup figure
    fig = plt.figure(figsize=(14, 6))
    ax = fig.add_subplot(111)
    ax.set_title(f"Window Confidence over time for \"{label}\"")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Confidence")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(min_start_time - pad, max_end_time + pad)

    # ============================
    # Ground truth
    # ============================
    # Bar plt to show bars where the "true" time ranges are for the activity.
    xs_bars = [p["time"][0] for p in gt_ranges]
    ys_gt_regions = [1 for _ in gt_ranges]
    bar_widths = [(p["time"][1]-p["time"][0]) for p in gt_ranges]
    ax.bar(xs_bars, ys_gt_regions, width=bar_widths, align="edge", color="lightgreen", label="Ground truth")

    if custom_range:
        assert len(custom_range) == 2, "Assuming only two float values for custom range"
        xs_bars2 = [custom_range[0]]
        ys_height = [1.025] #[0.1]
        bar_widths2 = [custom_range[1]-custom_range[0]]
        ys_bottom = [0] #[1.01]
        # TODO: Make this something that is added be clicking?
        ax.bar(xs_bars2, ys_height,
               width=bar_widths2, bottom=ys_bottom, align="edge",
               color=custom_range_color, alpha=0.5)

    # ============================
    # Actual Detections
    # ============================
    det_ranges = det_ranges[label]

    xs2_bars = [p["time"][0] for p in det_ranges]
    ys2_det_regions = [p["conf"] for p in det_ranges]
    bar_widths2 = [(p["time"][1] - p["time"][0]) for p in det_ranges]
    ax.bar(xs2_bars, ys2_det_regions, width=bar_widths2, align="edge", edgecolor="blue", fill=False, label="Detections")

    ax.legend(loc="upper right")
    ax.plot

    # ============================
    # Save
    # ============================
    #plt.show()
    Path(os.path.join(output_dir, "plots/activities")).mkdir(parents=True, exist_ok=True)
    fig.savefig(f"{output_dir}/plots/activities/{label.replace(' ', '_')}.png")