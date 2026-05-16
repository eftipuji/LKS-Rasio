import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches mpatches
import numpy as np
from math import gcd

# ─────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Jelajah Rasio & Proporsi",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CSS KUSTOM  (selaras dengan seri LKS)
# ─────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Nunito', sans-serif; }

    .main-header {
        background: linear-gradient(135deg, #0D5C2E 0%, #1A9B50 55%, #52C97A 100%);
        color: white; padding: 1.5rem 2rem; border-radius: 16px;
        text-align: center; margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(13,92,46,0.35);
    }
    .main-header h1 { font-size: 2rem; font-weight: 800; margin: 0; }
    .main-header p  { font-size: 1rem; margin: 0.3rem 0 0; opacity: 0.9; }

    .fase-box {
        border-left: 5px solid #1A9B50; background: #EEF9F3;
        padding: 0.8rem 1rem; border-radius: 0 10px 10px 0; margin: 0.7rem 0;
    }
    .fase-box .fase-label {
        font-weight: 800; color: #0D5C2E; font-size: 0.85rem;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .fase-box .fase-text { color: #2C3E50; font-size: 0.95rem; margin-top: 0.2rem; }

    .info-card {
        background: #EEF9F3; border: 1px solid #A8DFC0;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .warning-card {
        background: #FFF8E6; border: 1px solid #FFD966;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .success-card {
        background: #F0FBF4; border: 1px solid #1A9B50;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }
    .danger-card {
        background: #FEF0F0; border: 1px solid #E74C3C;
        border-radius: 12px; padding: 1rem 1.2rem; margin: 0.5rem 0;
    }

    .result-display {
        background: linear-gradient(135deg, #0D5C2E, #1A9B50);
        color: white; border-radius: 16px; padding: 1.5rem;
        text-align: center; font-size: 2.5rem; font-weight: 800;
        box-shadow: 0 4px 15px rgba(13,92,46,0.35); margin: 1rem 0;
    }

    .sidebar-title {
        background: #0D5C2E; color: white;
        padding: 0.7rem 1rem; border-radius: 10px;
        font-weight: 800; text-align: center; margin-bottom: 0.5rem;
    }

    .stButton > button {
        border-radius: 10px; font-weight: 700; transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-2px); }

    [data-testid="metric-container"] {
        background: #EEF9F3; border: 1px solid #A8DFC0;
        border-radius: 12px; padding: 0.8rem; text-align: center;
    }

    hr { border: none; border-top: 2px solid #C8EDD8; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def sederhanakan(a, b):
    if b == 0:
        return a, b
    g = gcd(abs(int(a)), abs(int(b)))
    return int(a // g), int(b // g)

def rasio_sederhana(a, b):
    if a <= 0 or b <= 0:
        return None, None
    g = gcd(int(a), int(b))
    return int(a // g), int(b // g)

def skala_hitung(jarak_peta_cm, skala_str):
    """Hitung jarak sebenarnya dari jarak peta dan skala 1:n (Aman dari Typo)"""
    try:
        skala_str = skala_str.replace(" ", "").replace(".", "")
        if ":" in skala_str:
            n = float(skala_str.split(":")[1])
        else:
            n = float(skala_str)
        jarak_sbn_cm = jarak_peta_cm * n
        jarak_sbn_km = jarak_sbn_cm / 100000
        return jarak_sbn_cm, jarak_sbn_km
    except Exception:
        return None, None

def proporsi_cek(a, b, c, d):
    """Cek apakah a/b = c/d (proporsi)"""
    if b == 0 or d == 0:
        return False
    return abs(a * d - b * c) < 1e-9

def nilai_x_proporsi(a, b, c):
    """a/b = c/x  →  x = b*c/a"""
    if a == 0:
        return None
    return (b * c) / a

# ─────────────────────────────────────────
# HEADER UTAMA
# ─────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>⚖️ Jelajah Rasio & Proporsi</h1>
    <p>Kalkulator Digital Interaktif • Metode Discovery Learning • SMP/MTs Kelas VII</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SIDEBAR NAVIGASI
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🧭 Menu Navigasi</div>', unsafe_allow_html=True)
    tab_choice = st.radio(
        "Pilih Fitur:",
        options=[
            "🏠 Beranda",
            "📍 KP 1 — Konsep Rasio",
            "⚖️ KP 2 — Proporsi & Perbandingan Senilai",
            "🗺️ KP 3 — Skala & Peta",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("""
    <div style="background:#EEF9F3;padding:0.8rem;border-radius:10px;font-size:0.82rem;color:#0D5C2E;">
    <b>📚 Petunjuk Penggunaan</b><br><br>
    1. Pilih fitur sesuai kegiatan pembelajaran<br>
    2. Ikuti langkah-langkah Discovery Learning<br>
    3. Catat temuan di LKS<br>
    4. Diskusikan dengan kelompokmu<br>
    5. Kerjakan soal latihan di akhir
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#7F7F7F;text-align:center;">
    🎓 Kurikulum Merdeka Fase D<br>
    Penulis: Efti Puji Lestari
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# HALAMAN BERANDA
# ══════════════════════════════════════════
if tab_choice == "🏠 Beranda":
    st.markdown("## 👋 Selamat Datang, Penjelajah Rasio & Proporsi!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="info-card">
        <b>🎯 Fokus Kemampuan</b><br><br>
        ✅ Konsep Rasio & Cara Penulisan<br>
        ✅ Proporsi & Perbandingan Senilai<br>
        ✅ Skala Peta & Denah<br>
        ✅ Rasio dalam Masalah Kontekstual<br>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card">
        <b>🔬 Metode Pembelajaran</b><br><br>
        🟢 Discovery Learning (utama)<br>
        🟡 Problem Based Learning<br>
        🔵 Cooperative Learning
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="info-card">
        <b>📱 Fitur Aplikasi</b><br><br>
        📍 Kalkulator Rasio Interaktif<br>
        ⚖️ Pemeriksa Proporsi<br>
        🗺️ Kalkulator Skala Peta<br>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔬 Alur Discovery Learning dalam Aplikasi Ini")
    fases = [
        ("① STIMULATION", "Resep masakan, campuran cat, peta kota — semuanya melibatkan rasio! Apa kesamaannya?", "#1A9B50"),
        ("② PROBLEM STATEMENT", "Kamu merumuskan pertanyaan: 'Bagaimana cara menyatakan perbandingan dua besaran?'", "#52C97A"),
        ("③ DATA COLLECTION", "Eksplorasi kalkulator: masukkan berbagai nilai rasio, amati pola penyederhanaan!", "#0D5C2E"),
        ("④ DATA PROCESSING", "Analisis: kapan dua rasio disebut proporsi? Apa artinya 'setara'?", "#148A40"),
        ("⑤ VERIFICATION", "Bandingkan temuanmu dengan teman. Uji dengan soal kontekstual!", "#1A9B50"),
        ("⑥ GENERALIZATION", "Rumuskan sendiri: apa itu rasio, proporsi, dan skala? Tuliskan di LKS!", "#0D5C2E"),
    ]
    cols = st.columns(3)
    for i, (label, text, color) in enumerate(fases):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border-left:4px solid {color};background:#FAFAFA;
                        padding:0.8rem 1rem;border-radius:0 10px 10px 0;margin-bottom:0.8rem;">
                <div style="font-weight:800;color:{color};font-size:0.9rem;">{label}</div>
                <div style="font-size:0.85rem;color:#444;margin-top:0.3rem;">{text}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗺️ Peta Konsep Rasio & Proporsi")

    fig0, ax0 = plt.subplots(figsize=(11, 4.5))
    ax0.axis("off")
    fig0.patch.set_facecolor("#F4FCF7")
    ax0.set_facecolor("#F4FCF7")
    ax0.set_xlim(0, 11)
    ax0.set_ylim(0, 4.5)

    def kotak(ax, x, y, w, h, teks, warna_bg="#0D5C2E", warna_txt="white", fs=9):
        ax.add_patch(mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.12", facecolor=warna_bg,
            edgecolor="white", lw=1.8))
        ax.text(x, y, teks, ha="center", va="center", fontsize=fs,
                color=warna_txt, fontweight="bold")

    def panah(ax, x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#0D5C2E", lw=1.5))

    kotak(ax0, 5.5, 4.0, 3.8, 0.7, "RASIO & PROPORSI", "#0D5C2E", "white", 11)
    kotak(ax0, 2.0, 2.8, 2.8, 0.65, "Rasio  a : b", "#1A9B50", "white", 9.5)
    kotak(ax0, 5.5, 2.8, 2.8, 0.65, "Proporsi  a:b = c:d", "#148A40", "white", 9.5)
    kotak(ax0, 9.0, 2.8, 2.8, 0.65, "Skala  1 : n", "#0D7A38", "white", 9.5)

    kotak(ax0, 1.0, 1.2, 2.2, 0.55, "Penyederhanaan\nRasio", "#52C97A", "#0D3D1E", 8.5)
    kotak(ax0, 3.3, 1.2, 2.2, 0.55, "Perbandingan\nSenilai", "#52C97A", "#0D3D1E", 8.5)
    kotak(ax0, 5.5, 1.2, 2.2, 0.55, "Nilai yang\nTidak Diketahui", "#52C97A", "#0D3D1E", 8.5)
    kotak(ax0, 7.8, 1.2, 2.2, 0.55, "Jarak Peta\nvs Nyata", "#52C97A", "#0D3D1E", 8.5)
    kotak(ax0, 10.0, 1.2, 1.8, 0.55, "Laju\nPerubahan", "#52C97A", "#0D3D1E", 8.5)

    for (x1, y1, x2, y2) in [
        (5.5, 3.65, 2.0, 3.12), (5.5, 3.65, 5.5, 3.12), (5.5, 3.65, 9.0, 3.12),
        (2.0, 2.47, 1.0, 1.47), (2.0, 2.47, 3.3, 1.47),
        (5.5, 2.47, 5.5, 1.47),
        (9.0, 2.47, 7.8, 1.47), (9.0, 2.47, 10.0, 1.47),
    ]:
        panah(ax0, x1, y1, x2, y2)

    ax0.set_title("Peta Konsep Rasio & Proporsi — Kelas VII",
                 pad=8, fontsize=10, color="#0D5C2E", fontweight="bold")
    st.pyplot(fig0)
    plt.close()

    st.markdown("""
    <div class="warning-card">
    <b>💡 Tips Belajar Efektif</b><br>
    Rasio ada di mana-mana: resep masakan, campuran bahan bangunan, peta wilayah!
    Sebelum mengeksplorasi, baca petunjuk di LKS, lalu gunakan kalkulator ini untuk
    <b>menemukan pola</b> dan <b>membuktikan hipotesismu</b>. Catat semua temuanmu!
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 1 — KONSEP RASIO
# ══════════════════════════════════════════
elif tab_choice == "📍 KP 1 — Konsep Rasio":
    st.markdown("## 📍 Kegiatan Pembelajaran 1: Mengenal Konsep Rasio")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Dalam sebuah kelas terdapat <b>18 siswa laki-laki</b> dan <b>12 siswa perempuan</b>.
        Bagaimana cara menyatakan <b>perbandingan</b> jumlah siswa laki-laki terhadap perempuan?<br><br>
        <b>❓ Bagaimana cara menyatakan dan menyederhanakan perbandingan dua besaran?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fase-box" style="border-color:#52C97A;background:#F0FDF4;">
        <div class="fase-label" style="color:#52C97A;">② Problem Statement — Hipotesis</div>
        <div class="fase-text">
        Sebelum bereksplorasi, tuliskan hipotesismu di LKS:<br>
        <i>"Menurutku, rasio adalah... dan cara menyederhanakannya adalah..."</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
        <div class="fase-label" style="color:#70AD47;">③ Data Collection — Eksplorasi Kalkulator Rasio</div>
        <div class="fase-text">Masukkan dua bilangan, amati rasio dan bentuk sederhananya!</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.8])
    with col1:
        st.markdown("#### ⌨️ Masukkan Dua Besaran")
        nama_a = st.text_input("Nama besaran A:", value="Laki-laki")
        nilai_a = st.number_input("Nilai A:", value=18, step=1, min_value=1, max_value=9999)
        nama_b = st.text_input("Nama besaran B:", value="Perempuan")
        nilai_b = st.number_input("Nilai B:", value=12, step=1, min_value=1, max_value=9999)

        ra, rb = rasio_sederhana(nilai_a, nilai_b)
        desimal_r = nilai_a / nilai_b if nilai_b != 0 else 0

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                    border-radius:16px;padding:1.2rem;text-align:center;margin-top:0.8rem;
                    box-shadow:0 4px 15px rgba(13,92,46,0.35);">
            <div style="font-size:0.85rem;opacity:0.8;">Rasio  {nama_a} : {nama_b}</div>
            <div style="font-size:2.8rem;font-weight:800;margin:0.2rem 0;">
                {nilai_a} : {nilai_b}
            </div>
            <div style="font-size:1rem;opacity:0.85;">
                = <b>{ra} : {rb}</b> (disederhanakan)
            </div>
            <div style="font-size:0.85rem;opacity:0.75;margin-top:0.3rem;">
                = {desimal_r:.4f} (bentuk desimal)
            </div>
        </div>
        """, unsafe_allow_html=True)

        pct_a = nilai_a / (nilai_a + nilai_b) * 100
        pct_b = nilai_b / (nilai_a + nilai_b) * 100
        st.markdown(f"""
        <div class="info-card" style="margin-top:0.6rem;">
        <b>📊 Persentase terhadap total:</b><br>
        {nama_a}: <b>{nilai_a} / {nilai_a+nilai_b} = {pct_a:.2f}%</b><br>
        {nama_b}: <b>{nilai_b} / {nilai_a+nilai_b} = {pct_b:.2f}%</b><br><br>
        <b>💡 FPB({nilai_a},{nilai_b}) = {gcd(int(nilai_a),int(nilai_b))}</b>
        (digunakan untuk menyederhanakan)
        </div>
        """, unsafe_allow_html=True)

    with col2:
        fig1, axes1 = plt.subplots(1, 2, figsize=(8, 4.5))
        fig1.patch.set_facecolor("#F4FCF7")

        ax_bar = axes1[0]
        ax_bar.set_facecolor("#F4FCF7")
        bar_colors = ["#1A9B50", "#52C97A"]
        bars = ax_bar.bar([nama_a[:8], nama_b[:8]], [nilai_a, nilai_b],
                          color=bar_colors, edgecolor="white", linewidth=2, width=0.5)
        for bar, val in zip(bars, [nilai_a, nilai_b]):
            ax_bar.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() + max(nilai_a, nilai_b) * 0.02,
                        str(int(val)), ha="center", va="bottom",
                        fontsize=11, color="#0D5C2E", fontweight="bold")
        ax_bar.set_title(f"Rasio: {nilai_a} : {nilai_b} = {ra} : {rb}",
                         fontsize=9.5, color="#0D5C2E", fontweight="bold", pad=6)
        ax_bar.tick_params(colors="#0D5C2E")
        ax_bar.set_ylabel("Nilai", fontsize=9, color="#0D5C2E")
        ax_bar.spines[["top","right"]].set_visible(False)

        ax_pie = axes1[1]
        ax_pie.set_facecolor("#F4FCF7")
        wedges, texts, autotexts = ax_pie.pie(
            [nilai_a, nilai_b],
            labels=[f"{nama_a[:8]}\n{pct_a:.1f}%", f"{nama_b[:8]}\n{pct_b:.1f}%"],
            colors=["#1A9B50", "#52C97A"],
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(edgecolor="white", linewidth=2),
            textprops=dict(fontsize=8.5, color="#0D3D1E", fontweight="bold")
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
        ax_pie.set_title(f"Proporsi {nama_a[:8]} vs {nama_b[:8]}",
                         fontsize=9.5, color="#0D5C2E", fontweight="bold", pad=6)

        plt.tight_layout(pad=1.0)
        st.pyplot(fig1)
        plt.close()

        fig2, ax2 = plt.subplots(figsize=(8, 1.8))
        ax2.axis("off")
        fig2.patch.set_facecolor("#F4FCF7")
        ax2.set_facecolor("#F4FCF7")
        ax2.set_xlim(0, max(ra, rb) + 1)
        ax2.set_ylim(-0.2, 2.2)

        blok_w = 0.85
        for i in range(ra):
            ax2.add_patch(mpatches.FancyBboxPatch((i * 1.0 + 0.07, 1.1),
                blok_w, 0.75, boxstyle="round,pad=0.05",
                facecolor="#1A9B50", edgecolor="white", lw=1.5))
            ax2.text(i * 1.0 + 0.07 + blok_w/2, 1.47, str(i+1),
                     ha="center", va="center", fontsize=8,
                     color="white", fontweight="bold")
        ax2.text(-0.08, 1.47, f"{nama_a[:6]}:", ha="right", va="center",
                 fontsize=8.5, color="#0D5C2E", fontweight="bold")

        for i in range(rb):
            ax2.add_patch(mpatches.FancyBboxPatch((i * 1.0 + 0.07, 0.2),
                blok_w, 0.75, boxstyle="round,pad=0.05",
                facecolor="#52C97A", edgecolor="white", lw=1.5))
            ax2.text(i * 1.0 + 0.07 + blok_w/2, 0.57, str(i+1),
                     ha="center", va="center", fontsize=8,
                     color="#0D3D1E", fontweight="bold")
        ax2.text(-0.08, 0.57, f"{nama_b[:6]}:", ha="right", va="center",
                 fontsize=8.5, color="#0D5C2E", fontweight="bold")

        ax2.set_title(f"Diagram Blok Satuan Rasio Sederhana: {ra} : {rb}",
                      fontsize=9, color="#0D5C2E", fontweight="bold", pad=4)
        st.pyplot(fig2)
        plt.close()

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
        <div class="fase-label" style="color:#7030A0;">④ Data Processing — Tabel Eksplorasi Rasio</div>
        <div class="fase-text">Coba berbagai pasangan bilangan, catat pola penyederhanaannya di LKS!</div>
    </div>
    """, unsafe_allow_html=True)

    contoh_rasio = [
        (18, 12, *rasio_sederhana(18, 12), gcd(18, 12)),
        (15, 25, *rasio_sederhana(15, 25), gcd(15, 25)),
        (36, 48, *rasio_sederhana(36, 48), gcd(36, 48)),
        (7,  14, *rasio_sederhana(7,  14), gcd(7,  14)),
        ("...", "...", "...", "...", "..."),
    ]
    tbl = '<table style="width:100%;border-collapse:collapse;font-size:0.87rem;">'
    tbl += '<tr style="background:#0D5C2E;color:white;"><th style="padding:8px;border:1px solid #ccc;">Nilai A</th><th style="padding:8px;border:1px solid #ccc;">Nilai B</th><th style="padding:8px;border:1px solid #ccc;">FPB</th><th style="padding:8px;border:1px solid #ccc;">Rasio A:B</th><th style="padding:8px;border:1px solid #ccc;">Rasio Sederhana</th><th style="padding:8px;border:1px solid #ccc;">Desimal</th></tr>'
    for i, row in enumerate(contoh_rasio):
        bg = "#EEF9F3" if i % 2 == 0 else "white"
        a, b, ra_r, rb_r, fpb = row
        dec = f"{a/b:.4f}" if isinstance(a, int) and b != 0 else "..."
        tbl += f'<tr style="background:{bg};"><td style="padding:7px;border:1px solid #ccc;text-align:center;">{a}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;">{b}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;font-weight:bold;color:#0D5C2E;">{fpb}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;">{a}:{b}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;font-weight:bold;">{ra_r}:{rb_r}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;">{dec}</td></tr>'
    tbl += "</table>"
    st.markdown(tbl, unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("⑥ 💡 Lihat Simpulan Konsep Rasio (setelah mencoba sendiri dulu!)"):
        st.markdown("""
        <div class="success-card">
        <b>✅ Simpulan Rasio:</b><br><br>
        🟢 <b>Rasio</b> adalah perbandingan dua besaran sejenis dengan satuan yang sama<br>
        🟢 Rasio a terhadap b ditulis: <b>a : b</b> atau <b>a/b</b><br>
        🟢 <b>Menyederhanakan rasio</b>: bagi kedua nilai dengan FPB-nya<br>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 2 — PROPORSI & PERBANDINGAN SENILAI
# ══════════════════════════════════════════
elif tab_choice == "⚖️ KP 2 — Proporsi & Perbandingan Senilai":
    st.markdown("## ⚖️ Kegiatan Pembelajaran 2: Proporsi & Perbandingan Senilai")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Harga <b>3 buku = Rp15.000</b>. Harga <b>7 buku = ?</b><br><br>
        <b>❓ Mengapa kita bisa "mengalikan rasio" untuk mencari nilai yang tidak diketahui? Kapan perbandingan disebut SENILAI?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    tab2a, tab2b = st.tabs(["⚖️ Pemeriksa Proporsi", "🔍 Cari Nilai x"])

    with tab2a:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Data Collection: Apakah dua rasio membentuk proporsi?</div>
            <div class="fase-text">Masukkan 4 bilangan a, b, c, d. Cek apakah a:b = c:d!</div>
        </div>
        """, unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Rasio Pertama (a : b)**")
            a_p = st.number_input("a =", value=3, step=1, key="a_p")
            b_p = st.number_input("b =", value=5, step=1, key="b_p")
        with colB:
            st.markdown("**Rasio Kedua (c : d)**")
            c_p = st.number_input("c =", value=6, step=1, key="c_p")
            d_p = st.number_input("d =", value=10, step=1, key="d_p")

        if b_p == 0 or d_p == 0:
            st.error("b dan d tidak boleh nol!")
        else:
            is_prop = proporsi_cek(a_p, b_p, c_p, d_p)
            val1 = a_p / b_p
            val2 = c_p / d_p
            ra1, rb1 = rasio_sederhana(abs(a_p), abs(b_p))
            rc1, rd1 = rasio_sederhana(abs(c_p), abs(d_p))

            warna_p = "#1A9B50" if is_prop else "#C00000"
            ikon_p  = "✅ YA, PROPORSI!" if is_prop else "❌ BUKAN Proporsi"

            st.markdown(f"""
            <div style="background:{warna_p};color:white;border-radius:16px;
                        padding:1.2rem;text-align:center;margin:0.8rem 0;">
                <div style="font-size:1.5rem;font-weight:800;">{ikon_p}</div>
                <div style="font-size:1rem;margin-top:0.3rem;opacity:0.9;">
                    {a_p}/{b_p} = {val1:.4f} &nbsp;|&nbsp; {c_p}/{d_p} = {val2:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)

            ad = a_p * d_p
            bc = b_p * c_p
            st.markdown(f"""
            <div class="warning-card">
            <b>🔍 Uji Perkalian Silang (Cross Multiplication):</b><br><br>
            a × d = {a_p} × {d_p} = <b>{ad}</b><br>
            b × c = {b_p} × {c_p} = <b>{bc}</b><br><br>
            {'✅ a×d = b×c → Proporsi terbukti!' if ad == bc else '❌ a×d ≠ b×c → Bukan proporsi!'}
            </div>
            """, unsafe_allow_html=True)

            fig_p, ax_p = plt.subplots(figsize=(7, 3.5))
            fig_p.patch.set_facecolor("#F4FCF7")
            ax_p.set_facecolor("#F4FCF7")
            x_r = np.linspace(0, max(b_p, d_p) * 1.5, 100)
            ax_p.plot(x_r, val1 * x_r, color="#1A9B50", lw=2.5, label=f"Rasio 1 ({a_p}:{b_p})")
            ax_p.plot(x_r, val2 * x_r, color="#52C97A", lw=2.5, linestyle="--", label=f"Rasio 2 ({c_p}:{d_p})")
            ax_p.scatter([b_p, d_p], [a_p, c_p], color="#0D5C2E", s=80, zorder=5)
            ax_p.legend()
            st.pyplot(fig_p)
            plt.close()

    with tab2b:
        st.markdown("**Proporsi: a : b = c : x**")
        colx1, colx2, colx3 = st.columns(3)
        with colx1:
            ax_ = st.number_input("a =", value=3, step=1, key="ax")
        with colx2:
            bx_ = st.number_input("b =", value=5, step=1, key="bx")
        with colx3:
            cx_ = st.number_input("c =", value=9, step=1, key="cx")

        x_hasil = nilai_x_proporsi(ax_, bx_, cx_)
        if x_hasil is not None:
            st.markdown(f"""
            <div class="result-display">
                x = {x_hasil:.2f}
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 3 — SKALA & PETA
# ══════════════════════════════════════════
elif tab_choice == "🗺️ KP 3 — Skala & Peta":
    st.markdown("## 🗺️ Kegiatan Pembelajaran 3: Skala Peta & Denah")

    st.markdown("""
    <div class="fase-box">
        <div class="fase-label">① Stimulation — Pemantik</div>
        <div class="fase-text">
        Pada sebuah peta Provinsi Jawa Tengah, jarak kota Pekalongan ke Semarang adalah <b>4 cm</b>. 
        Di sudut peta tertulis skala <b>1 : 2.500.000</b>. Apa arti dari angka perbandingan tersebut?<br><br>
        <b>❓ Bagaimana kita memanfaatkan konsep rasio untuk mengukur jarak dunia nyata menggunakan selembar kertas peta?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fase-box" style="border-color:#52C97A;background:#F0FDF4;">
        <div class="fase-label" style="color:#52C97A;">② Problem Statement — Rumusan Masalah</div>
        <div class="fase-text">
        Diskusikan di kelompokmu: Jika skala makin besar nilainya (misal 1:5.000.000), apakah gambar peta akan terlihat semakin detail atau semakin luas wilayahnya?
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
        <div class="fase-label" style="color:#70AD47;">③ Data Collection — Kalkulator Konversi Skala</div>
        <div class="fase-text">Gunakan simulator di bawah ini untuk menguji berbagai nilai jarak peta dan skala!</div>
    </div>
    """, unsafe_allow_html=True)

    col_sk1, col_sk2 = st.columns([1, 1.2])

    with col_sk1:
        st.markdown("#### ⌨️ Masukan Data Komponen Peta")
        jp = st.number_input("Jarak pada Peta / Gambar (cm):", value=4.0, step=0.5, min_value=0.1)
        skala_inp = st.text_input("Skala Peta (Format 1:n atau angkanya saja):", value="1:2.500.000", placeholder="Contoh: 1:2.500.000 atau 2500000")

        js_cm, js_km = skala_hitung(jp, skala_inp)

    with col_sk2:
        if js_cm is not None:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                        border-radius:16px;padding:1.5rem;text-align:center;
                        box-shadow:0 4px 15px rgba(13,92,46,0.35);">
                <div style="font-size:0.9rem;opacity:0.85;">Jarak Sebenarnya (Hasil Konversi)</div>
                <div style="font-size:3.2rem;font-weight:800;margin:0.2rem 0;color:#A8FF88;">
                    {js_km:.2f} KM
                </div>
                <div style="font-size:1rem;opacity:0.85;border-top:1px solid rgba(255,255,255,0.2);padding-top:0.5rem;margin-top:0.5rem;">
                    Sama dengan <b>{js_cm:,.0f} cm</b> di lapangan
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="info-card">
            <b>🔍 Langkah Hitung (Data Processing):</b><br>
            1. Jarak Sebenarnya = Jarak Peta &times; Nilai Skala<br>
            2. Jarak Sebenarnya = {jp} cm &times; {js_cm/jp:,.0f}<br>
            3. Jarak Sebenarnya = {js_cm:,.0f} cm<br>
            4. Mengubah ke KM (Bagi 100.000) = <b>{js_km:.2f} KM</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Format penulisan skala salah! Pastikan menggunakan angka yang valid.")

    st.markdown("---")
    with st.expander("⑥ 💡 Simpulan Konsep Skala"):
        st.markdown("""
        <div class="success-card">
        <b>✅ Simpulan Skala:</b><br><br>
        🟢 <b>Skala</b> adalah rasio perbandingan antara jarak pada gambar dengan jarak sebenarnya.<br>
        🟢 Skala 1 : $n$ berarti 1 cm pada gambar mewakili $n$ cm pada keadaan sebenarnya.<br>
        🟢 Rumus dasar perbandingan senilai pada peta:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Jarak Sebenarnya = Jarak Peta &times; $n$<br>
        &nbsp;&nbsp;&nbsp;&nbsp;• Jarak Peta = Jarak Sebenarnya / $n$
        </div>
        """, unsafe_allow_html=True)
