import streamlit as st
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Calculatrice ACE-III France", layout="wide")

st.title("📊 Analyse Normative ACE-III")
st.markdown("---")

# --- Paramètres du Modèle ---
INTERCEPTO = 132.93
B_AGE = -0.66
B_SCOLARITE = 0.17
RSE = 10.70 

# --- Sidebar : Entrée des données ---
st.sidebar.header("📋 Profil du Patient")
age = st.sidebar.slider("Âge du patient", 60, 95, 75)
scolarite = st.sidebar.slider("Années de scolarité", 0, 25, 12)
score_ace = st.sidebar.number_input("Score obtenu au ACE-III", 0, 100, 85)

# --- Calculs ---
moyenne_attendue = INTERCEPTO + (age * B_AGE) + (scolarite * B_SCOLARITE)
z_score = (score_ace - moyenne_attendue) / RSE
centile = norm.cdf(z_score) * 100

# --- Affichage des Métriques ---
col1, col2, col3 = st.columns(3)
col1.metric("Moyenne Attendue", f"{moyenne_attendue:.1f}")
col2.metric("Z-Score", f"{z_score:.2f}")
col3.metric("Rang Centile", f"{centile:.1f}%")

st.markdown("---")

# --- Visualisation : La Courbe de Gauss ---
st.subheader("📍 Positionnement sur la Courbe de Distribution")

x = np.linspace(-4, 4, 1000)
y = norm.pdf(x, 0, 1)

fig = go.Figure()

# Dessiner la courbe de Gauss
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='gray', width=2), name='Population Normale'))

# Zone de déficit (Z < -1.645)
x_fill = np.linspace(-4, -1.645, 100)
y_fill = norm.pdf(x_fill, 0, 1)
fig.add_trace(go.Scatter(x=list(x_fill)+[-1.645, -4], y=list(y_fill)+[0, 0], fill='toself', fillcolor='rgba(231, 76, 60, 0.3)', line=dict(color='rgba(255,255,255,0)'), name='Zone de Déficit'))

# Point du patient
fig.add_trace(go.Scatter(x=[z_score], y=[norm.pdf(z_score, 0, 1)], mode='markers+text', 
                         marker=dict(color='blue', size=15, symbol='diamond'),
                         text=["Patient"], textposition="top center", name='Position du Patient'))

fig.update_layout(
    xaxis_title="Z-Score",
    yaxis_showticklabels=False,
    template="plotly_white",
    height=400,
    margin=dict(l=20, r=20, t=20, b=20)
)

# Correction du paramètre obsolète selon votre avertissement
st.plotly_chart(fig, width="stretch")

# --- Interprétation ---
if z_score <= -1.645:
    st.error(f"**Interprétation :** Déficit Clinique. Score inférieur à la norme attendue (Centile {centile:.1f}).")
elif z_score <= -1.28:
    st.warning(f"**Interprétation :** Performance Limite (Zone de Risque).")
else:
    st.success(f"**Interprétation :** Performance Normale.")