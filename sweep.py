"""
Parametric sweep of the Brayton cycle: thermal efficiency and net specific work as function of pressure ratio for representative gas turbine technology eras.
"""

import numpy as np
import matplotlib.pyplot as plt

from brayton import compute_cycle


# Global style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
})

# Color palette: blue, orange, green
COLORS = ['#0072B2', '#D55E00', '#009E73']

# Turbine inlet temperature cases [°C]
TIT_cases = [
    (1100, '1100°C (E-class, 80s-90s)'),
    (1500, '1500°C (H-class, current)'),
    (1700, '1700°C (HL-class, future)'),
]

# Reference turbine for vertical line
Ref_turbine_pi = 22
Ref_turbine_label = 'Modern industrial GT range'



def main():
    pi_range = np.linspace(3, 50, 100)  # pressure ratio range

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    for i, (TIT, label) in enumerate(TIT_cases):     # Outer loop walks through TIT values
        T3 = TIT + 273.15
        eta_th = []
        w = []
        for pi in pi_range:                    # Inner loop walks through pi range and appends results to the lists
            try:
                r = compute_cycle(pi=pi, T3=T3)
                eta_th.append(r['eta_th'] * 100)
                w.append(r['w_net'] /1000)
            except Exception:                  # Exceptions catches errors due to extreme pi/TIT combinations
                eta_th.append(np.nan)
                w.append(np.nan)
        
        eta_arr = np.array(eta_th)
        w_arr = np.array(w)

        ax1.plot(pi_range, eta_th, label=label, color=COLORS[i], linewidth=1.5)
        ax2.plot(pi_range, w, label=label, color=COLORS[i], linewidth=1.5)


        # Mark optimum points
        i_eta = np.nanargmax(eta_arr)
        i_w = np.nanargmax(w_arr)

        ax1.plot(pi_range[i_eta], eta_arr[i_eta], 'o',
                 color=COLORS[i], markersize=7, markeredgecolor='white',
                 markeredgewidth=1.0, zorder=5)
        ax2.plot(pi_range[i_w], w_arr[i_w], 'o',
                 color=COLORS[i], markersize=7, markeredgecolor='white',
                 markeredgewidth=1.0, zorder=5)
    

    # Reference vertical line of current engine
    for ax in (ax1, ax2):
        ax.axvspan(20, 24, color='grey', alpha=0.15, zorder=1)
        ax.axvline(22, color='grey', linestyle=':', linewidth=1.2, alpha=0.7)

    # Place the label inside each subplot
    ax1.text(Ref_turbine_pi + 0.5, 5, Ref_turbine_label,
             fontsize=9, color='grey', rotation=90,
             verticalalignment='bottom')
    ax2.text(Ref_turbine_pi + 0.5, 30, Ref_turbine_label,
             fontsize=9, color='grey', rotation=90,
             verticalalignment='bottom')
    

    # Axis formatting    
    ax1.set_xlabel('Pressure ratio π [-]')
    ax1.set_ylabel('Thermal efficiency η_th [%]')
    ax1.set_title('Efficiency vs pressure ratio')
    ax1.set_xlim(0, 55)
    ax1.set_ylim(0, 50)
    ax1.grid(True, alpha=0.5)
    ax1.legend(loc='lower right', frameon=True, framealpha=0.7, title='Turbine inlet temperature')

    ax2.set_xlabel('Pressure ratio π [-]')
    ax2.set_ylabel('Net specific work w_net [kJ/kg]')
    ax2.set_title('Specific work vs pressure ratio')
    ax2.set_xlim(0, 55)
    ax2.set_ylim(0, 700)
    ax2.grid(True, alpha=0.5)
    ax2.legend(loc='lower right', frameon=True, framealpha=0.7, title='Turbine inlet temperature')

    fig.suptitle('Brayton cycle - Turbine inlet temperature\n'
                 '(η_C = 0.85, η_T = 0.90, T_amb = 15°C)')
    plt.tight_layout()

    out_path = 'results/eta_and_work_vs_pi.png'
    plt.savefig(out_path, dpi=300)
    print(f"Saved figure to {out_path}")
    plt.show()


if __name__ == '__main__':
    main()