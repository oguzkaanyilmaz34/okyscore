import streamlit as st
import math

st.title("OKY's Alopecia Areata Risk Hesaplayıcı")

# --- Kullanıcıdan veri al ---
calreticulin = st.number_input("Calreticulin düzeyi (µg/mL) – 0–10 arası", min_value=0.0, max_value=6.0, step=0.1, format="%.2f")
aso10 = st.number_input("ASÖ-10 skoru – 0–40 arası", min_value=0.0, max_value=40.0, step=1.0, format="%.0f")
cinsiyet_kadin = st.selectbox("Cinsiyet", ["Erkek", "Kadın"]) == "Kadın"
ai_hastalik_yok = st.selectbox("Otoimmün hastalık", ["Var", "Yok"]) == "Yok"
antitpo_yuksek = st.selectbox("Anti-TPO antikor", ["Normal", "Yüksek"]) == "Yüksek"

# --- Hesapla butonu ---
if st.button("Riski Hesapla"):
    try:
        # --- MODEL KATSAYILARI (güncel) ---
        intercept = 0.030165
        b_calreticulin = 0.032975   # per 0.1 µg/mL
        b_aso10 = 0.091883
        b_cinsiyet = -1.041297      # Kadın=1
        b_ai = -2.348336            # AI hastalık yokluğu=1
        b_antitpo = 0.844441        # Anti-TPO yüksek=1

        # --- 0.1 µg/mL bazında ölçekle ---
        crt_per_0p1 = calreticulin / 0.1

        # --- Logit ---
        logit = (
            intercept
            + b_calreticulin * crt_per_0p1
            + b_aso10 * aso10
            + b_cinsiyet * (1 if cinsiyet_kadin else 0)
            + b_ai * (1 if ai_hastalik_yok else 0)
            + b_antitpo * (1 if antitpo_yuksek else 0)
        )

        # --- Olasılık ---
        probability = 1 / (1 + math.exp(-logit))
        risk_pct = probability * 100

        # --- Yorum ---
        if probability < 0.25:
            yorum = "Düşük risk"
        elif probability < 0.5:
            yorum = "Orta-düşük risk"
        elif probability < 0.75:
            yorum = "Orta-yüksek risk"
        else:
            yorum = "Yüksek risk"

        # --- Sonuç ---
        st.success(f"Alopecia Areata riski: %{risk_pct:.1f} ({yorum})")

        # --- Detaylı çıktı ---
        st.markdown(f"""
        **Girdi Özeti**
        - Calreticulin (µg/mL): {calreticulin:.2f}
        - ASÖ-10 skoru: {aso10:.0f}
        - Cinsiyet: {"Kadın" if cinsiyet_kadin else "Erkek"}
        - Otoimmün hastalık: {"Yok" if ai_hastalik_yok else "Var"}
        - Anti-TPO: {"Yüksek" if antitpo_yuksek else "Normal"}
        """)
    except Exception as e:
        st.error(f"Hata: {e}")
