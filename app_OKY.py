import streamlit as st
import math

st.title("OKY's Alopecia Areata Risk Hesaplayıcı")

# Kullanıcıdan veri al
calreticulin = st.number_input("Calreticulin düzeyi (µg/mL) (0–6)", min_value=0.0, max_value=6.0, step=0.1, format="%.2f")
aso10 = st.text_input("ASO-10 skoru (0–40)", value="")
ai_hastalik_yok = st.selectbox("Otoimmün hastalık", ["Var", "Yok"]) == "Yok"
cinsiyet_kadin = st.selectbox("Cinsiyet", ["Erkek", "Kadın"]) == "Kadın"
antitpo_yuksek = st.selectbox("Anti-TPO antikor", ["Normal", "Yüksek"]) == "Yüksek"

# Hesapla butonu
if st.button("Riski Hesapla"):
    try:
        aso10 = float(aso10)

        # --- MODEL KATSAYILARI (0.1 µg/mL bazında) ---
        intercept = 0.030165
        b_calreticulin = 0.032975   # her 0.1 µg/mL artışa göre
        b_aso10 = 0.091883
        b_ai = -2.348336
        b_cinsiyet = -1.041297
        b_antitpo = 0.844441

        # --- Calreticulin 0.1 µg/mL biriminde ölçekle ---
        crt_per_0p1 = calreticulin / 0.1

        # --- Lojit hesapla ---
        logit = (
            intercept
            + b_calreticulin * crt_per_0p1
            + b_aso10 * aso10
            + b_ai * (1 if ai_hastalik_yok else 0)
            + b_cinsiyet * (1 if cinsiyet_kadin else 0)
            + b_antitpo * (1 if antitpo_yuksek else 0)
        )

        # --- Olasılık ---
        probability = 1 / (1 + math.exp(-logit))
        st.success(f"Alopecia Areata riski: %{probability * 100:.1f}")
    except:
        st.error("Lütfen sayısal alanları (Calreticulin ve ASO-10) doldurunuz.")
