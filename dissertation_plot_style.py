# Shared preferred house style for all dissertation figures
# %run once per kernel session in EC_Cohort_Characteristics and EC_PRS_Analysis rather than redefining them locally.
import subprocess
import matplotlib.pyplot as plt
import matplotlib as mpl

NAVY   = '#17365D'
GREY   = '#9CA3AF'
CORAL  = '#C17A56'
TEAL   = '#5D99A1'
LIGHT_GREY = '#D9D9D9'

mpl.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'legend.fontsize': 9.5,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.edgecolor': '#444444',
    'savefig.dpi': 300,
    'figure.dpi': 120,
})


def style_ax(ax):
    """Removes top/right spines, lightens remaining ones, removes heavy gridlines."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#888888')
    ax.tick_params(colors='#444444')
    ax.grid(False)
    return ax


def savefig_both(fig, stem, project_id, bucket_output):
    """Saves a PDF (vector, for Overleaf) and a high-res PNG (preview), uploads
    both to the output bucket. Raises if either upload fails."""
    fig.savefig(f'/home/jupyter/{stem}.pdf', bbox_inches='tight')
    fig.savefig(f'/home/jupyter/{stem}.png', dpi=300, bbox_inches='tight')
    for ext in ('pdf', 'png'):
        result = subprocess.run(
            ['gsutil', '-u', project_id, 'cp', f'/home/jupyter/{stem}.{ext}',
             f'{bucket_output}/{stem}.{ext}'],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"gsutil upload failed for {stem}.{ext} (exit {result.returncode}):\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}"
            )
    print(f"Saved and uploaded {stem}.pdf and {stem}.png")
