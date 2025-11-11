# Simulasi Statistik Bose–Einstein untuk Emisi Cahaya

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
from lmfit import Model
from scipy.constants import h, c, k

# 1. Fungsi Distribusi Bose–Einstein / Planck

def bose_einstein(wavelength, T):
    wl = wavelength
    numerator = (2 * h * c**2) / wl**5
    denominator = np.exp((h * c) / (wl * k * T)) - 1
    return numerator / denominator

# 2. Membuat Data Sintetik (eksperimen simulasi)

np.random.seed(42)
wl_nm = np.linspace(400, 800, 200)
wl_m = wl_nm * 1e-9

T_true = 4500  # suhu LED simulasi
I_theory = bose_einstein(wl_m, T_true)
noise = np.random.normal(0, I_theory.max()*0.05, size=I_theory.shape)
I_exp = I_theory + noise

data = pd.DataFrame({'Wavelength (nm)': wl_nm, 'Intensity (a.u.)': I_exp})

# 3. Visualisasi Data Eksperimen dan Teori

plt.figure(figsize=(8,5))
plt.plot(wl_nm, I_exp, 'o', markersize=3, label='Data Eksperimen (simulasi)')
plt.plot(wl_nm, I_theory, '-', label=f'Model Teori (T={T_true} K)')
plt.xlabel('Panjang Gelombang (nm)')
plt.ylabel('Intensitas (a.u.)')
plt.title('Distribusi Spektral Emisi Cahaya (Statistik Bose–Einstein)')
plt.legend()
plt.grid(True)
plt.show()

# 4. Fitting Model Bose–Einstein dengan Data

model = Model(bose_einstein)
params = model.make_params(T=3000)  # tebakan awal
result = model.fit(I_exp, params, wavelength=wl_m)

print(result.fit_report())

# 5. Plot hasil fitting

plt.figure(figsize=(8,5))
plt.plot(wl_nm, I_exp, 'o', markersize=3, label='Data Eksperimen')
plt.plot(wl_nm, result.best_fit, '-', label=f'Fitting B–E (T={result.best_values["T"]:.1f} K)')
plt.xlabel('Panjang Gelombang (nm)')
plt.ylabel('Intensitas (a.u.)')
plt.title('Fitting Statistik Bose–Einstein terhadap Data Eksperimen')
plt.legend()
plt.grid(True)
plt.show()

# 6. Evaluasi Error (RMSE, MAPE, Chi-square)

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def chi_square(y_true, y_pred):
    return np.sum(((y_true - y_pred)**2) / y_pred)

I_fit = result.best_fit
print("Evaluasi Model:")
print(f"RMSE  = {rmse(I_exp, I_fit):.4e}")
print(f"MAPE  = {mape(I_exp, I_fit):.2f}%")
print(f"Chi²  = {chi_square(I_exp, I_fit):.4e}")
