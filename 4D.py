# ======================================================
# STREAMLIT APP: SIMULASI STATISTIK BOSE–EINSTEIN
# ======================================================
# Fitur:
# 1. Input parameter suhu, pendinginan, waktu
# 2. Plot spektrum emisi Bose–Einstein
# 3. Visualisasi 3D interaktif (λ–T–I)
# 4. Animasi pendinginan (4D dengan slider waktu)
# ======================================================

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.constants import h, c, k

# ======================================================
# 1. Header dan Deskripsi
# ======================================================
st.title("🌈 Simulasi Statistik Bose–Einstein untuk Emisi Cahaya")
st.markdown("""
Aplikasi ini mensimulasikan **distribusi foton** berdasarkan Statistik **Bose–Einstein (Hukum Planck)**.
Kamu bisa mempelajari bagaimana **spektrum cahaya bergeser** ketika sumber **mendingin atau memanas**.
""")

# ======================================================
# 2. Input Parameter
# ======================================================
col1, col2 = st.columns(2)
with col1:
    T0 = st.slider("Suhu Awal (K)", 1000, 10000, 6000, 500)
    T_env = st.slider("Suhu Lingkungan (K)", 100, 1000, 300, 50)
with col2:
    k_cool = st.slider("Konstanta Pendinginan (1/s)", 0.05, 1.0, 0.25, 0.05)
    waktu_akhir = st.slider("Durasi Simulasi (detik)", 5, 30, 15, 1)

st.markdown("---")

# ======================================================
# 3. Fungsi Bose–Einstein
# ======================================================
def bose_einstein(wavelength, T):
    wl = wavelength
    numerator = (2 * h * c**2) / wl**5
    denominator = np.exp((h * c) / (wl * k * T)) - 1
    return numerator / denominator

# ======================================================
# 4. Hitung dan Siapkan Data
# ======================================================
wl_nm = np.linspace(400, 800, 200)
wl_m = wl_nm * 1e-9
time_steps = np.linspace(0, waktu_akhir, 80)

# Model pendinginan Newton
T_t = T_env + (T0 - T_env) * np.exp(-k_cool * time_steps)

I_time = []
for T in T_t:
    I_t = bose_einstein(wl_m, T)
    I_time.append(I_t)
I_time = np.array(I_time)
I_time /= I_time.max()  # normalisasi

st.subheader("📉 Distribusi Spektrum Awal dan Akhir")
col3, col4 = st.columns(2)

with col3:
    fig_start = go.Figure()
    fig_start.add_trace(go.Scatter(x=wl_nm, y=I_time[0],
                                   mode='lines', line=dict(color='orange', width=3)))
    fig_start.update_layout(title=f"Suhu Awal: {T_t[0]:.0f} K",
                            xaxis_title="Panjang Gelombang (nm)",
                            yaxis_title="Intensitas Relatif")
    st.plotly_chart(fig_start, use_container_width=True)

with col4:
    fig_end = go.Figure()
    fig_end.add_trace(go.Scatter(x=wl_nm, y=I_time[-1],
                                 mode='lines', line=dict(color='red', width=3)))
    fig_end.update_layout(title=f"Suhu Akhir: {T_t[-1]:.0f} K",
                          xaxis_title="Panjang Gelombang (nm)",
                          yaxis_title="Intensitas Relatif")
    st.plotly_chart(fig_end, use_container_width=True)

st.markdown("---")

# ======================================================
# 5. Animasi Interaktif 4D (λ, T, I, waktu)
# ======================================================
st.subheader("🎬 Animasi Pendinginan Emisi Cahaya")

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
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, {"frame": {"duration": 150, "redraw": True},
                                  "fromcurrent": True, "mode": "immediate"}]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], {"frame": {"duration": 0}, "mode": "immediate"}])
            ]
        )]
    ),
    frames=frames
)

sliders = [dict(
    steps=[dict(method="animate",
                args=[[str(i)], {"frame": {"duration": 0, "redraw": True},
                                 "mode": "immediate"}],
                label=f"{T:.0f} K") for i, T in enumerate(T_t)],
    transition={"duration": 0},
    x=0.1, y=0,
    currentvalue={"font": {"size": 14},
                  "prefix": "Suhu: ", "visible": True, "xanchor": "center"},
    len=0.9
)]

fig_anim.update_layout(sliders=sliders)
st.plotly_chart(fig_anim, use_container_width=True)

st.markdown("---")

# ======================================================
# 6. Visualisasi 3D Interaktif λ–T–I
# ======================================================
st.subheader("🌌 Permukaan Distribusi 3D (λ–T–I)")

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
    scene=dict(
        xaxis_title='Panjang Gelombang (nm)',
        yaxis_title='Suhu (K)',
        zaxis_title='Intensitas Relatif (a.u.)'
    ),
    title="Distribusi Bose–Einstein terhadap Panjang Gelombang dan Suhu",
    width=900, height=700
)

st.plotly_chart(fig3d, use_container_width=True)
# ======================================================
# Tambahan: Jalur Puncak Wien di Permukaan 3D
# ======================================================

# Hukum Pergeseran Wien: lambda_max = 2.898e-3 / T (meter)
lambda_max_m = 2.898e-3 / T_t
lambda_max_nm = lambda_max_m * 1e9

# Ambil intensitas di sekitar lambda_max untuk plot
I_peak = []
for i, T in enumerate(T_t):
    idx = np.abs(wl_nm - lambda_max_nm[i]).argmin()
    I_peak.append(I_time[i, idx])

# Tambahkan garis puncak ke grafik 3D
fig3d.add_trace(go.Scatter3d(
    x=lambda_max_nm,
    y=T_t,
    z=I_peak,
    mode='lines+markers',
    line=dict(color='cyan', width=5),
    marker=dict(size=4, color='white'),
    name='Puncak λₘₐₓ (Hukum Wien)'
))

fig3d.update_layout(title="Distribusi Bose–Einstein dan Jalur Pergeseran Wien")
st.plotly_chart(fig3d, use_container_width=True)

st.markdown("""
---
### 💡 Keterangan Fisika:
- **Distribusi Bose–Einstein** menjelaskan sebaran energi foton pada sistem termal.  
- Saat suhu turun, **puncak spektrum bergeser ke panjang gelombang lebih besar (efek Wien)**.  
- Intensitas total juga menurun, menunjukkan **penurunan energi total radiasi**.  
---
""")
