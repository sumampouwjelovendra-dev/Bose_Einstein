# ======================================================
# SIMULASI KOMPLET STATISTIK BOSE–EINSTEIN UNTUK EMISI CAHAYA
# ======================================================
# Fitur:
# 1. Simulasi distribusi spektral Bose–Einstein (Hukum Planck)
# 2. Model pendinginan Newton (T menurun terhadap waktu)
# 3. Animasi 4D (λ, I, waktu, T)
# 4. Plot 3D interaktif (λ, T, I)
# ======================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.constants import h, c, k
import plotly.graph_objects as go

# ------------------------------------------------------
# 1. Fungsi Fisik Utama: Distribusi Bose–Einstein / Planck
# ------------------------------------------------------
def bose_einstein(wavelength, T):
    wl = wavelength
    numerator = (2 * h * c**2) / wl**5
    denominator = np.exp((h * c) / (wl * k * T)) - 1
    return numerator / denominator

# ------------------------------------------------------
# 2. Parameter Simulasi
# ------------------------------------------------------
wl_nm = np.linspace(400, 800, 200)      # panjang gelombang (nm)
wl_m = wl_nm * 1e-9                     # konversi ke meter

T0 = 6000                               # suhu awal (K)
T_env = 300                             # suhu lingkungan (K)
k_cool = 0.25                           # konstanta pendinginan (1/s)
time_steps = np.linspace(0, 15, 80)     # waktu simulasi (detik)

# Model pendinginan Newton: T(t) = T_env + (T0 - T_env)*exp(-k*t)
T_t = T_env + (T0 - T_env) * np.exp(-k_cool * time_steps)

# ------------------------------------------------------
# 3. Hitung Distribusi Spektrum untuk Tiap Waktu
# ------------------------------------------------------
I_time = []
for T in T_t:
    I_t = bose_einstein(wl_m, T)
    I_time.append(I_t)
I_time = np.array(I_time)
I_time /= I_time.max()  # normalisasi intensitas agar relatif

# ======================================================
# BAGIAN 1 — ANIMASI 4D (PENDINGINAN WAKTU)
# ======================================================
print("Menjalankan animasi pendinginan...")

fig, ax = plt.subplots(figsize=(8,5))
line, = ax.plot([], [], lw=2)
ax.set_xlim(400, 800)
ax.set_ylim(0, 1.05)
ax.set_xlabel('Panjang Gelombang (nm)')
ax.set_ylabel('Intensitas Relatif (a.u.)')
ax.set_title('Simulasi Pendinginan Emisi Cahaya (Bose–Einstein)')

# fungsi konversi suhu ke warna
def temp_to_color(T):
    T_norm = (T - 300) / (6000 - 300)
    return plt.cm.plasma(T_norm)

def init():
    line.set_data([], [])
    return line,

def update(frame):
    wl = wl_nm
    I = I_time[frame]
    T_now = T_t[frame]
    line.set_data(wl, I)
    line.set_color(temp_to_color(T_now))
    ax.set_title(f'Spektrum Emisi Cahaya (T = {T_now:.0f} K)')
    return line,

ani = FuncAnimation(fig, update, frames=len(time_steps),
                    init_func=init, blit=True, interval=150)
plt.show()

# ======================================================
# BAGIAN 2 — VISUALISASI 3D INTERAKTIF (λ–T–I)
# ======================================================
print("Membuat plot 3D interaktif...")

W, T = np.meshgrid(wl_nm, T_t)

fig3d = go.Figure(
    data=[go.Surface(
        x=W, y=T, z=I_time,
        colorscale='plasma',
        showscale=True,
        colorbar=dict(title='Intensitas Relatif')
    )]
)

fig3d.update_layout(
    title="Distribusi Bose–Einstein terhadap Panjang Gelombang dan Suhu",
    scene=dict(
        xaxis_title='Panjang Gelombang (nm)',
        yaxis_title='Suhu (K)',
        zaxis_title='Intensitas Relatif (a.u.)'
    ),
    width=900, height=650
)

fig3d.show()

# ======================================================
# BAGIAN 3 — VERSI INTERAKTIF DENGAN SLIDER WAKTU (Plotly)
# ======================================================
print("Membuat animasi interaktif dengan slider waktu...")

frames = []
for i, T in enumerate(T_t):
    frame = go.Frame(
        data=[go.Scatter(
            x=wl_nm,
            y=I_time[i],
            mode="lines",
            line=dict(color="firebrick", width=3),
            name=f"T = {T:.0f} K"
        )],
        name=str(i)
    )
    frames.append(frame)

fig_anim = go.Figure(
    data=[go.Scatter(x=wl_nm, y=I_time[0], mode="lines", line=dict(color="firebrick", width=3))],
    layout=go.Layout(
        xaxis=dict(title="Panjang Gelombang (nm)", range=[400, 800]),
        yaxis=dict(title="Intensitas Relatif (a.u.)", range=[0, 1.05]),
        title=f"Simulasi Pendinginan Emisi Cahaya (T = {T_t[0]:.0f} K)",
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            y=1.05,
            x=1.15,
            xanchor="right",
            yanchor="top",
            buttons=[
                dict(label="Play", method="animate", args=[None, {"frame": {"duration": 150, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]),
                dict(label="Pause", method="animate", args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}])
            ]
        )]
    ),
    frames=frames
)

sliders = [dict(
    steps=[dict(method="animate",
                args=[[str(i)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                label=f"{T:.0f} K") for i, T in enumerate(T_t)],
    transition={"duration": 0},
    x=0.1, y=0,
    currentvalue={"font": {"size": 14}, "prefix": "Suhu: ", "visible": True, "xanchor": "center"},
    len=0.9
)]

fig_anim.update_layout(sliders=sliders)
fig_anim.show()
