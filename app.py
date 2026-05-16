import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    """Hitung jarak sebenarnya dari jarak peta dan skala 1:n"""
    try:
        n = float(skala_str.split(":")[1])
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
            "💰 KP 4 — Rasio dalam Kehidupan",
            "📝 Soal Latihan Interaktif",
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
        ✅ Laju Perubahan (Rate)
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
        💰 Simulasi Rasio Kontekstual<br>
        📝 Soal Latihan Interaktif
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
    Rasio ada di mana-mana: resep masakan, campuran bahan bangunan, peta wilayah, diskon harga!
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
        Sebuah resep sirup menggunakan <b>2 sendok sirup</b> untuk <b>5 gelas air</b>.
        Jika ingin membuat 15 gelas air, berapa sendok sirup yang dibutuhkan?<br><br>
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
        # Visualisasi 1: Diagram batang rasio
        fig1, axes1 = plt.subplots(1, 2, figsize=(8, 4.5))
        fig1.patch.set_facecolor("#F4FCF7")

        # Batang perbandingan
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

        # Pie chart
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

        # Visualisasi 2: Blok satuan rasio
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
    # Tabel eksplorasi
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
        🟢 Rasio a : b = ka : kb untuk sembarang k ≠ 0 (rasio ekuivalen)<br>
        🟢 Rasio <b>bukan satuan</b> — hanya perbandingan, bukan nilai tunggal
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
        Harga <b>3 buku = Rp15.000</b>. Harga <b>7 buku = ?</b><br>
        Jika kecepatan motor <b>60 km/jam</b>, dalam <b>2,5 jam</b> menempuh berapa km?<br><br>
        <b>❓ Mengapa kita bisa "mengalikan rasio" untuk mencari nilai yang tidak diketahui?
        Kapan perbandingan disebut SENILAI?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    tab2a, tab2b = st.tabs(["⚖️ Pemeriksa Proporsi", "🔍 Cari Nilai x"])

    # ── TAB PEMERIKSA PROPORSI
    with tab2a:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi: Apakah dua rasio membentuk proporsi?</div>
            <div class="fase-text">Masukkan 4 bilangan a, b, c, d. Cek apakah a:b = c:d!</div>
        </div>
        """, unsafe_allow_html=True)

        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Rasio Pertama (a : b)**")
            a_p = st.number_input("a =", value=3, step=1, min_value=-999, max_value=999, key="a_p")
            b_p = st.number_input("b =", value=5, step=1, min_value=-999, max_value=999, key="b_p")
        with colB:
            st.markdown("**Rasio Kedua (c : d)**")
            c_p = st.number_input("c =", value=6, step=1, min_value=-999, max_value=999, key="c_p")
            d_p = st.number_input("d =", value=10, step=1, min_value=-999, max_value=999, key="d_p")

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
            bg_p    = "#EEF9F3" if is_prop else "#FEF0F0"

            st.markdown(f"""
            <div style="background:{warna_p};color:white;border-radius:16px;
                        padding:1.2rem;text-align:center;margin:0.8rem 0;
                        box-shadow:0 4px 15px rgba(0,0,0,0.2);">
                <div style="font-size:1.5rem;font-weight:800;">{ikon_p}</div>
                <div style="font-size:1rem;margin-top:0.3rem;opacity:0.9;">
                    {a_p}/{b_p} = {val1:.6f} &nbsp;|&nbsp; {c_p}/{d_p} = {val2:.6f}
                </div>
                <div style="font-size:0.9rem;margin-top:0.3rem;opacity:0.85;">
                    Bentuk sederhana: {ra1}:{rb1} &nbsp; vs &nbsp; {rc1}:{rd1}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Penjelasan perkalian silang
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

            # Visualisasi grafik proporsi
            fig_p, ax_p = plt.subplots(figsize=(7, 3.5))
            fig_p.patch.set_facecolor("#F4FCF7")
            ax_p.set_facecolor("#F4FCF7")
            # Garis rasio 1
            x_r = np.linspace(0, max(b_p, d_p) * 1.5, 100)
            y_r1 = val1 * x_r
            y_r2 = val2 * x_r
            ax_p.plot(x_r, y_r1, color="#1A9B50", lw=2.5,
                      label=f"Rasio 1: {a_p}:{b_p} (k={val1:.3f})")
            ax_p.plot(x_r, y_r2, color="#52C97A", lw=2.5, linestyle="--",
                      label=f"Rasio 2: {c_p}:{d_p} (k={val2:.3f})")
            ax_p.scatter([b_p], [a_p], color="#0D5C2E", s=80, zorder=5)
            ax_p.scatter([d_p], [c_p], color="#52C97A", s=80, zorder=5)
            ax_p.set_xlabel("Besaran b / d", fontsize=9, color="#0D5C2E")
            ax_p.set_ylabel("Besaran a / c", fontsize=9, color="#0D5C2E")
            ax_p.set_title("Grafik Proporsi — Garis Sejajar = Proporsi Sama",
                           fontsize=9.5, color="#0D5C2E", fontweight="bold", pad=6)
            ax_p.legend(fontsize=8.5)
            ax_p.spines[["top","right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig_p)
            plt.close()

        # Tabel eksplorasi proporsi
        st.markdown("---")
        st.markdown("""
        <div class="fase-box" style="border-color:#7030A0;background:#F5EFFF;">
            <div class="fase-label" style="color:#7030A0;">④ Data Processing — Pola Proporsi</div>
            <div class="fase-text">Coba semua pasangan berikut, identifikasi mana yang proporsi!</div>
        </div>
        """, unsafe_allow_html=True)

        pasangan = [
            (2, 5, 4, 10, "Ya"),
            (3, 7, 9, 21, "Ya"),
            (4, 6, 6, 8, "Tidak"),
            (5, 8, 15, 24, "Ya"),
            (2, 3, 5, 8, "Tidak"),
        ]
        tbl2 = '<table style="width:100%;border-collapse:collapse;font-size:0.87rem;">'
        tbl2 += '<tr style="background:#0D5C2E;color:white;"><th style="padding:7px;border:1px solid #ccc;">a</th><th style="padding:7px;border:1px solid #ccc;">b</th><th style="padding:7px;border:1px solid #ccc;">c</th><th style="padding:7px;border:1px solid #ccc;">d</th><th style="padding:7px;border:1px solid #ccc;">a×d</th><th style="padding:7px;border:1px solid #ccc;">b×c</th><th style="padding:7px;border:1px solid #ccc;">Proporsi?</th></tr>'
        for i, (a, b, c, d, ya) in enumerate(pasangan):
            bg = "#EEF9F3" if i % 2 == 0 else "white"
            wc = "#1A9B50" if ya == "Ya" else "#C00000"
            tbl2 += f'<tr style="background:{bg};"><td style="padding:7px;border:1px solid #ccc;text-align:center;">{a}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;">{b}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;">{c}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;">{d}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;font-weight:bold;">{a*d}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;font-weight:bold;">{b*c}</td><td style="padding:7px;border:1px solid #ccc;text-align:center;font-weight:800;color:{wc};">{ya}</td></tr>'
        tbl2 += "</table>"
        st.markdown(tbl2, unsafe_allow_html=True)

    # ── TAB CARI NILAI x
    with tab2b:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi: Mencari Nilai yang Tidak Diketahui</div>
            <div class="fase-text">Masukkan tiga nilai a, b, c untuk menemukan x pada proporsi a:b = c:x</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**Proporsi: a : b = c : x**")
        colx1, colx2, colx3 = st.columns(3)
        with colx1:
            ax_ = st.number_input("a =", value=3, step=1, min_value=1, max_value=9999, key="ax")
        with colx2:
            bx_ = st.number_input("b =", value=5, step=1, min_value=1, max_value=9999, key="bx")
        with colx3:
            cx_ = st.number_input("c =", value=9, step=1, min_value=1, max_value=9999, key="cx")

        x_hasil = nilai_x_proporsi(ax_, bx_, cx_)

        if x_hasil is not None:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                        border-radius:16px;padding:1.2rem;text-align:center;margin:0.8rem 0;">
                <div style="font-size:0.9rem;opacity:0.85;">Proporsi yang diselesaikan</div>
                <div style="font-size:1.6rem;font-weight:800;margin:0.3rem 0;">
                    {ax_} : {bx_} = {cx_} : <span style="color:#A8FF88;">x</span>
                </div>
                <div style="font-size:0.85rem;opacity:0.8;">Langkah: x = (b × c) ÷ a</div>
                <div style="font-size:0.85rem;opacity:0.8;">x = ({bx_} × {cx_}) ÷ {ax_} = {bx_*cx_} ÷ {ax_}</div>
                <div style="font-size:3rem;font-weight:800;color:#A8FF88;">x = {x_hasil:.4f}</div>
            </div>
            """, unsafe_allow_html=True)

            # Verifikasi
            st.markdown(f"""
            <div class="success-card">
            <b>✅ Verifikasi:</b><br>
            {ax_} × {x_hasil:.4f} = {ax_ * x_hasil:.4f}<br>
            {bx_} × {cx_} = {bx_ * cx_}<br>
            {'✅ Sama! Proporsi terbukti benar.' if abs(ax_ * x_hasil - bx_ * cx_) < 0.01 else '⚠️ Periksa kembali!'}
            </div>
            """, unsafe_allow_html=True)

        # Contoh kontekstual
        st.markdown("---")
        st.markdown("### 🌍 Contoh Kontekstual Proporsi")
        conteks_soal = [
            ("Harga buku", "3 buku = Rp 15.000", 3, 15000, 7, "7 buku = ?", "Rp 35.000"),
            ("Kecepatan motor", "60 km dalam 1 jam", 1, 60, 2.5, "2,5 jam = ? km", "150 km"),
            ("Resep kue", "2 telur untuk 12 kue", 2, 12, 5, "5 telur = ? kue", "30 kue"),
        ]
        for nama, situasi, a, b, c, tanya, jwb in conteks_soal:
            x_k = nilai_x_proporsi(a, b, c)
            st.markdown(f"""
            <div style="border:1px solid #A8DFC0;border-radius:10px;padding:0.8rem 1rem;
                        margin:0.5rem 0;border-left:4px solid #1A9B50;">
            <b>🌿 {nama}</b><br>
            <span style="font-size:0.9rem;">Situasi: {situasi}<br>
            Pertanyaan: {tanya}<br>
            Proporsi: {a} : {b} = {c} : x → x = ({b} × {c}) ÷ {a} = <b>{x_k:.0f if x_k == int(x_k) else x_k:.2f}</b><br>
            ✅ Jawaban: <b>{jwb}</b></span>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("⑥ 💡 Simpulan Proporsi & Perbandingan Senilai"):
            st.markdown("""
            <div class="success-card">
            <b>✅ Simpulan Proporsi:</b><br><br>
            🟢 <b>Proporsi</b>: pernyataan bahwa dua rasio adalah sama → a:b = c:d<br>
            🟢 <b>Uji proporsi</b>: kalikan silang → a×d = b×c<br>
            🟢 <b>Mencari nilai x</b>: jika a:b = c:x → x = (b×c) ÷ a<br>
            🟢 <b>Perbandingan senilai</b>: jika satu besaran naik, besaran lain ikut naik secara proporsional<br>
            🟢 <b>Perbandingan berbalik nilai</b>: jika satu naik, besaran lain turun (akan dipelajari lebih lanjut)
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
        Peta Indonesia menggunakan skala <b>1 : 5.000.000</b>.
        Jika jarak Jakarta–Surabaya di peta adalah <b>15 cm</b>,
        berapa kilometer jarak sebenarnya?<br><br>
        Denah rumah dibuat dengan skala <b>1 : 200</b>.
        Jika kamar tidur di denah berukuran <b>3 cm × 4 cm</b>,
        berapa ukuran kamar sebenarnya?<br><br>
        <b>❓ Bagaimana cara menggunakan skala untuk menghitung jarak sebenarnya?</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    tab3a, tab3b = st.tabs(["📏 Kalkulator Skala", "📐 Denah Interaktif"])

    # ── TAB KALKULATOR SKALA
    with tab3a:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi Kalkulator Skala</div>
            <div class="fase-text">Pilih mode hitung dan isi nilai yang diketahui!</div>
        </div>
        """, unsafe_allow_html=True)

        mode_skala = st.radio("Mode Perhitungan:",
                               ["Cari Jarak Sebenarnya", "Cari Jarak Peta", "Cari Skala"],
                               horizontal=True)

        col_sk1, col_sk2 = st.columns([1.1, 1])
        with col_sk1:
            if mode_skala == "Cari Jarak Sebenarnya":
                skala_n = st.number_input("Nilai n pada Skala 1 : n",
                                           value=5000000, step=100000, min_value=1)
                j_peta  = st.number_input("Jarak di Peta (cm):", value=15.0,
                                           step=0.1, min_value=0.01, format="%.2f")
                j_sbn_cm = j_peta * skala_n
                j_sbn_m  = j_sbn_cm / 100
                j_sbn_km = j_sbn_cm / 100000

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                            border-radius:14px;padding:1.2rem;text-align:center;margin-top:0.8rem;">
                    <div style="font-size:0.85rem;opacity:0.8;">Skala 1 : {skala_n:,} | Jarak peta: {j_peta} cm</div>
                    <div style="font-size:0.85rem;opacity:0.75;margin:0.2rem 0;">Rumus: Jarak Sebenarnya = Jarak Peta × n</div>
                    <div style="font-size:0.85rem;opacity:0.75;">= {j_peta} × {skala_n:,}</div>
                    <div style="font-size:1.8rem;font-weight:800;margin:0.3rem 0;">{j_sbn_cm:,.0f} cm</div>
                    <div style="font-size:1rem;opacity:0.85;">= {j_sbn_m:,.1f} m = <b>{j_sbn_km:,.3f} km</b></div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="warning-card" style="margin-top:0.6rem;font-size:0.9rem;">
                <b>💡 Analogi:</b><br>
                Jika peta diperbesar {skala_n:,} kali → itulah jarak sebenarnya!<br>
                1 cm di peta = <b>{skala_n/100:.0f} m = {skala_n/100000:.2f} km</b> di dunia nyata
                </div>
                """, unsafe_allow_html=True)

            elif mode_skala == "Cari Jarak Peta":
                skala_n2 = st.number_input("Nilai n pada Skala 1 : n",
                                            value=200, step=10, min_value=1)
                j_sbn_in = st.number_input("Jarak Sebenarnya (cm):",
                                            value=600.0, step=10.0, min_value=0.01)
                j_peta_h = j_sbn_in / skala_n2

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                            border-radius:14px;padding:1.2rem;text-align:center;margin-top:0.8rem;">
                    <div style="font-size:0.85rem;opacity:0.8;">Skala 1 : {skala_n2:,} | Jarak nyata: {j_sbn_in:,.1f} cm</div>
                    <div style="font-size:0.85rem;opacity:0.75;margin:0.2rem 0;">Rumus: Jarak Peta = Jarak Sebenarnya ÷ n</div>
                    <div style="font-size:0.85rem;opacity:0.75;">= {j_sbn_in:,.1f} ÷ {skala_n2:,}</div>
                    <div style="font-size:2rem;font-weight:800;margin:0.3rem 0;">{j_peta_h:.4f} cm</div>
                    <div style="font-size:1rem;opacity:0.85;">= {j_peta_h*10:.4f} mm di peta/denah</div>
                </div>
                """, unsafe_allow_html=True)

            else:  # Cari Skala
                j_peta_s  = st.number_input("Jarak di Peta (cm):", value=5.0,
                                             step=0.1, min_value=0.01)
                j_sbn_s   = st.number_input("Jarak Sebenarnya (cm):", value=2500000.0,
                                             step=1000.0, min_value=1.0)
                n_skala = j_sbn_s / j_peta_s

                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                            border-radius:14px;padding:1.2rem;text-align:center;margin-top:0.8rem;">
                    <div style="font-size:0.85rem;opacity:0.8;">Jarak peta: {j_peta_s} cm | Jarak nyata: {j_sbn_s:,.0f} cm</div>
                    <div style="font-size:0.85rem;opacity:0.75;margin:0.2rem 0;">Rumus: n = Jarak Sebenarnya ÷ Jarak Peta</div>
                    <div style="font-size:0.85rem;opacity:0.75;">= {j_sbn_s:,.0f} ÷ {j_peta_s}</div>
                    <div style="font-size:1.8rem;font-weight:800;margin:0.3rem 0;">Skala = 1 : {n_skala:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_sk2:
            # Tabel ringkasan skala terkenal
            st.markdown("**📊 Contoh Skala Umum**")
            skala_umum = [
                ("1 : 100", "Denah rumah", "1 cm = 1 m"),
                ("1 : 500", "Denah kompleks", "1 cm = 5 m"),
                ("1 : 1.000", "Peta kota kecil", "1 cm = 10 m"),
                ("1 : 10.000", "Peta kota besar", "1 cm = 100 m"),
                ("1 : 100.000", "Peta kabupaten", "1 cm = 1 km"),
                ("1 : 1.000.000", "Peta provinsi", "1 cm = 10 km"),
                ("1 : 10.000.000", "Peta nasional", "1 cm = 100 km"),
            ]
            tbl_sk = '<table style="width:100%;border-collapse:collapse;font-size:0.83rem;">'
            tbl_sk += '<tr style="background:#0D5C2E;color:white;"><th style="padding:7px;border:1px solid #ccc;">Skala</th><th style="padding:7px;border:1px solid #ccc;">Kegunaan</th><th style="padding:7px;border:1px solid #ccc;">1 cm =</th></tr>'
            for i, (sk, guna, arti) in enumerate(skala_umum):
                bg = "#EEF9F3" if i % 2 == 0 else "white"
                tbl_sk += f'<tr style="background:{bg};"><td style="padding:6px;border:1px solid #ccc;font-weight:700;color:#0D5C2E;">{sk}</td><td style="padding:6px;border:1px solid #ccc;">{guna}</td><td style="padding:6px;border:1px solid #ccc;">{arti}</td></tr>'
            tbl_sk += "</table>"
            st.markdown(tbl_sk, unsafe_allow_html=True)

    # ── TAB DENAH INTERAKTIF
    with tab3b:
        st.markdown("""
        <div class="fase-box" style="border-color:#70AD47;background:#F0FBF0;">
            <div class="fase-label" style="color:#70AD47;">③ Eksplorasi Denah Rumah</div>
            <div class="fase-text">Atur skala dan ukuran ruangan, lihat denah serta ukuran sebenarnya!</div>
        </div>
        """, unsafe_allow_html=True)

        col_d1, col_d2 = st.columns([1, 1.5])
        with col_d1:
            skala_denah = st.selectbox("Pilih Skala Denah:",
                                        ["1 : 100", "1 : 200", "1 : 50"], index=0)
            n_denah = int(skala_denah.split(":")[1].strip())

            st.markdown("**Ukuran di Denah (cm):**")
            r_names = ["Ruang Tamu", "Kamar Tidur", "Dapur", "Kamar Mandi"]
            r_colors = ["#1A9B50", "#52C97A", "#0D7A38", "#A8DFC0"]
            r_dims = []
            for rn in r_names:
                ca, cb = st.columns(2)
                with ca:
                    pw = st.number_input(f"{rn[:6]} L (cm):", value=5.0,
                                          step=0.5, min_value=0.5, max_value=30.0,
                                          key=f"w_{rn}")
                with cb:
                    ph = st.number_input(f"{rn[:6]} T (cm):", value=4.0,
                                          step=0.5, min_value=0.5, max_value=30.0,
                                          key=f"h_{rn}")
                r_dims.append((pw, ph))

        with col_d2:
            # Gambar denah sederhana
            fig_d, ax_d = plt.subplots(figsize=(7, 5.5))
            ax_d.axis("off")
            fig_d.patch.set_facecolor("#F4FCF7")
            ax_d.set_facecolor("#F4FCF7")

            # Posisi ruangan (2x2 grid)
            positions = [(0, 2.5), (5, 2.5), (0, 0), (5, 0)]
            all_w = [d[0] for d in r_dims]
            all_h = [d[1] for d in r_dims]
            skala_vis = 0.8  # cm per unit gambar

            for idx, (rn, rc, (pw, ph), (px, py)) in enumerate(
                    zip(r_names, r_colors, r_dims, positions)):
                w_vis = pw * skala_vis * 0.7
                h_vis = ph * skala_vis * 0.7
                ax_d.add_patch(mpatches.FancyBboxPatch(
                    (px * 0.8, py * 0.8), w_vis, h_vis,
                    boxstyle="square,pad=0.0",
                    facecolor=rc, edgecolor="white", lw=2, alpha=0.85))
                sbn_l = pw * n_denah / 100
                sbn_t = ph * n_denah / 100
                ax_d.text(px * 0.8 + w_vis/2, py * 0.8 + h_vis/2,
                          f"{rn}\n{pw}cm × {ph}cm\n→ {sbn_l:.1f}m × {sbn_t:.1f}m",
                          ha="center", va="center", fontsize=8,
                          color="white" if idx < 2 else "#0D3D1E",
                          fontweight="bold")

            ax_d.set_xlim(-0.5, 12)
            ax_d.set_ylim(-0.5, 7)
            ax_d.set_title(f"Denah Rumah Sederhana — Skala {skala_denah}",
                           fontsize=10, color="#0D5C2E", fontweight="bold", pad=8)
            st.pyplot(fig_d)
            plt.close()

            # Tabel ukuran sebenarnya
            st.markdown("**📐 Ukuran Sebenarnya:**")
            tbl_d = '<table style="width:100%;border-collapse:collapse;font-size:0.85rem;">'
            tbl_d += '<tr style="background:#0D5C2E;color:white;"><th style="padding:6px;border:1px solid #ccc;">Ruangan</th><th style="padding:6px;border:1px solid #ccc;">Di Denah</th><th style="padding:6px;border:1px solid #ccc;">Sebenarnya</th><th style="padding:6px;border:1px solid #ccc;">Luas Nyata</th></tr>'
            for rn, (pw, ph) in zip(r_names, r_dims):
                sbn_l = pw * n_denah / 100
                sbn_t = ph * n_denah / 100
                luas  = sbn_l * sbn_t
                tbl_d += f'<tr><td style="padding:6px;border:1px solid #ccc;font-weight:700;">{rn}</td><td style="padding:6px;border:1px solid #ccc;text-align:center;">{pw}×{ph} cm</td><td style="padding:6px;border:1px solid #ccc;text-align:center;font-weight:700;color:#0D5C2E;">{sbn_l:.1f}×{sbn_t:.1f} m</td><td style="padding:6px;border:1px solid #ccc;text-align:center;">{luas:.2f} m²</td></tr>'
            tbl_d += "</table>"
            st.markdown(tbl_d, unsafe_allow_html=True)

        with st.expander("⑥ 💡 Simpulan Skala"):
            st.markdown("""
            <div class="success-card">
            <b>✅ Rumus Skala:</b><br><br>
            📌 <b>Skala = Jarak Peta : Jarak Sebenarnya</b><br>
            📌 <b>Jarak Sebenarnya = Jarak Peta × n</b> (n = angka skala)<br>
            📌 <b>Jarak Peta = Jarak Sebenarnya ÷ n</b><br><br>
            ⚠️ Pastikan satuan SAMA sebelum menghitung!<br>
            💡 Skala besar (n kecil) → peta lebih detail (peta kota)<br>
            💡 Skala kecil (n besar) → peta lebih luas (peta negara)
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════
# KP 4 — RASIO DALAM KEHIDUPAN
# ══════════════════════════════════════════
elif tab_choice == "💰 KP 4 — Rasio dalam Kehidupan":
    st.markdown("## 💰 Kegiatan Pembelajaran 4: Rasio dalam Kehidupan Sehari-hari")

    tab4a, tab4b, tab4c = st.tabs(["🍕 Pembagian Proporsional", "🚗 Laju Perubahan", "💹 Literasi Finansial"])

    # ── TAB PEMBAGIAN PROPORSIONAL
    with tab4a:
        st.markdown("""
        <div class="fase-box">
            <div class="fase-label">Pembagian Sesuai Rasio</div>
            <div class="fase-text">
            Tiga orang bersama-sama membeli hadiah. Ali memberi Rp30.000, Budi Rp20.000,
            dan Cici Rp10.000. Jika hadiah berupa uang tunai Rp120.000, berapa bagian masing-masing?
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ⌨️ Kalkulator Pembagian Proporsional")
        jumlah_pihak = st.slider("Berapa pihak yang berbagi?", 2, 5, 3)

        nama_list, rasio_list = [], []
        cols_pihak = st.columns(jumlah_pihak)
        for i, cp in enumerate(cols_pihak):
            with cp:
                nm = st.text_input(f"Nama {i+1}:", value=["Ali","Budi","Cici","Deni","Eni"][i],
                                   key=f"nm{i}")
                rs = st.number_input(f"Rasio {i+1}:", value=[3,2,1,2,1][i],
                                     step=1, min_value=1, max_value=100, key=f"rs{i}")
                nama_list.append(nm)
                rasio_list.append(rs)

        total_uang = st.number_input("Total yang dibagi (Rp):", value=120000,
                                      step=1000, min_value=1)

        total_rasio = sum(rasio_list)
        bagian_list = [r / total_rasio * total_uang for r in rasio_list]

        col_res, col_viz = st.columns([1, 1.5])
        with col_res:
            st.markdown(f"**Rasio: {' : '.join(map(str, rasio_list))}**")
            for nm, rs, bg in zip(nama_list, rasio_list, bagian_list):
                st.markdown(f"""
                <div style="border:1px solid #A8DFC0;border-radius:10px;padding:0.7rem 1rem;
                            margin:0.4rem 0;border-left:4px solid #1A9B50;">
                <b>{nm}</b><br>
                Rasio: {rs}/{total_rasio} &nbsp;|&nbsp;
                Bagian: <b>Rp {bg:,.0f}</b>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="success-card" style="margin-top:0.6rem;">
            <b>✅ Verifikasi:</b> {' + '.join(f'Rp {b:,.0f}' for b in bagian_list)}<br>
            = <b>Rp {sum(bagian_list):,.0f}</b> (Total sesuai ✅)
            </div>
            """, unsafe_allow_html=True)

        with col_viz:
            fig_pb, ax_pb = plt.subplots(figsize=(6, 4))
            fig_pb.patch.set_facecolor("#F4FCF7")
            ax_pb.set_facecolor("#F4FCF7")
            warna_pb = ["#0D5C2E","#1A9B50","#52C97A","#A8DFC0","#C8EDD8"]
            wedges, texts, autotexts = ax_pb.pie(
                bagian_list,
                labels=[f"{n}\nRp {b:,.0f}" for n, b in zip(nama_list, bagian_list)],
                colors=warna_pb[:jumlah_pihak],
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops=dict(edgecolor="white", linewidth=2),
                textprops=dict(fontsize=8.5, fontweight="bold")
            )
            for at in autotexts:
                at.set_color("white")
                at.set_fontweight("bold")
            ax_pb.set_title(f"Pembagian Rp {total_uang:,} sesuai Rasio",
                            fontsize=9.5, color="#0D5C2E", fontweight="bold", pad=8)
            plt.tight_layout()
            st.pyplot(fig_pb)
            plt.close()

    # ── TAB LAJU PERUBAHAN
    with tab4b:
        st.markdown("""
        <div class="fase-box">
            <div class="fase-label">Laju Perubahan (Rate)</div>
            <div class="fase-text">
            Laju perubahan adalah rasio antara perubahan satu besaran terhadap perubahan besaran lain.
            Contoh: kecepatan (km/jam), harga per unit, debit air (liter/menit).
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_l1, col_l2 = st.columns([1, 1.5])
        with col_l1:
            jenis_laju = st.selectbox("Pilih jenis laju:",
                                       ["🚗 Kecepatan (km/jam)",
                                        "💧 Debit Air (liter/menit)",
                                        "🛒 Harga per Unit"])

            if "Kecepatan" in jenis_laju:
                jarak = st.number_input("Jarak (km):", value=150.0, step=5.0, min_value=0.1)
                waktu = st.number_input("Waktu (jam):", value=2.5, step=0.5, min_value=0.1)
                laju = jarak / waktu
                satuan_laju = "km/jam"
                label_a, label_b = "Jarak (km)", "Waktu (jam)"
                val_a, val_b = jarak, waktu
                rumus = f"Kecepatan = Jarak ÷ Waktu = {jarak} ÷ {waktu}"
            elif "Debit" in jenis_laju:
                vol = st.number_input("Volume Air (liter):", value=300.0, step=10.0, min_value=0.1)
                dur = st.number_input("Waktu (menit):", value=12.0, step=1.0, min_value=0.1)
                laju = vol / dur
                satuan_laju = "liter/menit"
                label_a, label_b = "Volume (liter)", "Waktu (menit)"
                val_a, val_b = vol, dur
                rumus = f"Debit = Volume ÷ Waktu = {vol} ÷ {dur}"
            else:
                harga = st.number_input("Total Harga (Rp):", value=75000.0, step=1000.0, min_value=1.0)
                unit  = st.number_input("Jumlah Unit:", value=5.0, step=1.0, min_value=1.0)
                laju  = harga / unit
                satuan_laju = "Rp/unit"
                label_a, label_b = "Total Harga (Rp)", "Jumlah Unit"
                val_a, val_b = harga, unit
                rumus = f"Harga per unit = Total ÷ Unit = {harga:,.0f} ÷ {unit:.0f}"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                        border-radius:14px;padding:1.2rem;text-align:center;margin-top:0.8rem;">
                <div style="font-size:0.85rem;opacity:0.8;">{rumus}</div>
                <div style="font-size:2.5rem;font-weight:800;margin:0.3rem 0;">
                    {laju:.2f}
                </div>
                <div style="font-size:1rem;opacity:0.85;">{satuan_laju}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_l2:
            # Grafik laju perubahan
            fig_l, ax_l = plt.subplots(figsize=(7, 4))
            fig_l.patch.set_facecolor("#F4FCF7")
            ax_l.set_facecolor("#F4FCF7")
            x_l = np.linspace(0, val_b * 2, 100)
            y_l = laju * x_l
            ax_l.plot(x_l, y_l, color="#1A9B50", lw=2.5,
                      label=f"Laju = {laju:.2f} {satuan_laju}")
            ax_l.scatter([val_b], [val_a], color="#0D5C2E", s=100, zorder=5,
                         label=f"Titik ({val_b:.1f}, {val_a:.1f})")
            ax_l.fill_between(x_l, 0, y_l, alpha=0.15, color="#1A9B50")
            ax_l.set_xlabel(label_b, fontsize=9, color="#0D5C2E")
            ax_l.set_ylabel(label_a, fontsize=9, color="#0D5C2E")
            ax_l.set_title(f"Grafik Laju Perubahan — {satuan_laju}",
                           fontsize=9.5, color="#0D5C2E", fontweight="bold", pad=6)
            ax_l.legend(fontsize=8.5)
            ax_l.spines[["top","right"]].set_visible(False)
            plt.tight_layout()
            st.pyplot(fig_l)
            plt.close()

    # ── TAB LITERASI FINANSIAL
    with tab4c:
        st.markdown("""
        <div class="fase-box">
            <div class="fase-label">💹 Literasi Finansial — Rasio Keuangan</div>
            <div class="fase-text">
            Rasio digunakan dalam dunia keuangan: diskon, bunga, tabungan, dan anggaran belanja.
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("#### 🏷️ Kalkulator Diskon")
            harga_asal = st.number_input("Harga Awal (Rp):", value=250000, step=5000, min_value=1)
            diskon_pct = st.number_input("Diskon (%):", value=25.0, step=5.0,
                                          min_value=0.0, max_value=100.0)
            besar_diskon = harga_asal * diskon_pct / 100
            harga_akhir  = harga_asal - besar_diskon
            rasio_d_a, rasio_d_b = rasio_sederhana(int(diskon_pct), 100)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                        border-radius:14px;padding:1rem;text-align:center;margin-top:0.5rem;">
                <div style="font-size:0.85rem;opacity:0.8;">Rasio diskon: {rasio_d_a}:{rasio_d_b}</div>
                <div style="font-size:0.9rem;margin:0.2rem 0;">
                Harga awal: <b>Rp {harga_asal:,}</b>
                </div>
                <div style="font-size:0.9rem;margin:0.2rem 0;">
                Diskon {diskon_pct:.0f}%: <b>− Rp {besar_diskon:,.0f}</b>
                </div>
                <div style="font-size:2rem;font-weight:800;margin:0.3rem 0;color:#A8FF88;">
                Rp {harga_akhir:,.0f}
                </div>
                <div style="font-size:0.85rem;opacity:0.8;">Harga setelah diskon</div>
            </div>
            """, unsafe_allow_html=True)

        with col_f2:
            st.markdown("#### 📊 Kalkulator Anggaran (Rasio 50:30:20)")
            penghasilan = st.number_input("Penghasilan per Bulan (Rp):",
                                           value=3500000, step=100000, min_value=1)
            kebutuhan_pct = st.slider("% Kebutuhan Pokok:", 30, 70, 50)
            keinginan_pct = st.slider("% Keinginan:", 10, 40, 30)
            tabungan_pct  = 100 - kebutuhan_pct - keinginan_pct

            kebutuhan_rp = penghasilan * kebutuhan_pct / 100
            keinginan_rp = penghasilan * keinginan_pct / 100
            tabungan_rp  = penghasilan * tabungan_pct / 100

            if tabungan_pct < 0:
                st.error("⚠️ Persentase melebihi 100%! Kurangi salah satu.")
            else:
                st.markdown(f"""
                <div class="info-card" style="margin-top:0.5rem;">
                <b>💰 Rencana Anggaran:</b><br>
                🏠 Kebutuhan ({kebutuhan_pct}%): <b>Rp {kebutuhan_rp:,.0f}</b><br>
                🛍️ Keinginan ({keinginan_pct}%): <b>Rp {keinginan_rp:,.0f}</b><br>
                🏦 Tabungan ({tabungan_pct}%): <b>Rp {tabungan_rp:,.0f}</b><br><br>
                Rasio: <b>{kebutuhan_pct} : {keinginan_pct} : {tabungan_pct}</b>
                </div>
                """, unsafe_allow_html=True)

                # Pie anggaran
                if tabungan_rp >= 0:
                    fig_f, ax_f = plt.subplots(figsize=(5, 3.5))
                    fig_f.patch.set_facecolor("#F4FCF7")
                    ax_f.set_facecolor("#F4FCF7")
                    ax_f.pie(
                        [kebutuhan_rp, keinginan_rp, max(0, tabungan_rp)],
                        labels=[f"Kebutuhan\n{kebutuhan_pct}%",
                                f"Keinginan\n{keinginan_pct}%",
                                f"Tabungan\n{tabungan_pct}%"],
                        colors=["#1A9B50","#52C97A","#A8DFC0"],
                        autopct="%1.1f%%",
                        startangle=90,
                        wedgeprops=dict(edgecolor="white", linewidth=2),
                        textprops=dict(fontsize=8, fontweight="bold")
                    )
                    ax_f.set_title("Distribusi Anggaran Bulanan",
                                   fontsize=9, color="#0D5C2E", fontweight="bold", pad=6)
                    plt.tight_layout()
                    st.pyplot(fig_f)
                    plt.close()


# ══════════════════════════════════════════
# SOAL LATIHAN INTERAKTIF
# ══════════════════════════════════════════
elif tab_choice == "📝 Soal Latihan Interaktif":
    st.markdown("## 📝 Soal Latihan Interaktif — Rasio & Proporsi")
    st.markdown("""
    <div class="warning-card">
    <b>📌 Petunjuk:</b> Kerjakan soal-soal berikut secara mandiri dan jujur.
    Gunakan kalkulator digital di tab sebelumnya hanya untuk <b>verifikasi</b>, bukan langsung menekan tombol!
    Waktu pengerjaan: ±45 menit.
    </div>
    """, unsafe_allow_html=True)

    if "skor_rs" not in st.session_state:
        st.session_state.skor_rs = 0
    if "jawab_rs" not in st.session_state:
        st.session_state.jawab_rs = {}

    soal_list = [
        {
            "no": 1, "tipe": "PG", "kp": "KP 1",
            "soal": "Bentuk paling sederhana dari rasio 36 : 48 adalah ...",
            "konteks": "💡 Gunakan FPB(36, 48) = 12",
            "pilihan": ["A. 4 : 5", "B. 3 : 4", "C. 6 : 8", "D. 9 : 12"],
            "jawaban": "B",
            "pembahasan": "FPB(36,48) = 12. 36÷12 = 3, 48÷12 = 4. Jadi 36:48 = 3:4."
        },
        {
            "no": 2, "tipe": "PG", "kp": "KP 1",
            "soal": "Dalam sebuah kelas terdapat 20 siswa laki-laki dan 15 siswa perempuan. Rasio siswa perempuan terhadap seluruh siswa adalah ...",
            "konteks": "",
            "pilihan": ["A. 3 : 4", "B. 3 : 7", "C. 4 : 7", "D. 15 : 35"],
            "jawaban": "B",
            "pembahasan": "Total = 20 + 15 = 35. Rasio perempuan:total = 15:35. FPB(15,35)=5 → 3:7."
        },
        {
            "no": 3, "tipe": "PG", "kp": "KP 2",
            "soal": "Jika 5 : 8 = x : 40, maka nilai x adalah ...",
            "konteks": "💡 Gunakan perkalian silang!",
            "pilihan": ["A. 20", "B. 25", "C. 64", "D. 16"],
            "jawaban": "B",
            "pembahasan": "5/8 = x/40 → x = 5 × 40 ÷ 8 = 200 ÷ 8 = 25."
        },
        {
            "no": 4, "tipe": "PG", "kp": "KP 2",
            "soal": "Harga 4 kg mangga adalah Rp28.000. Harga 7 kg mangga adalah ...",
            "konteks": "💡 Ini adalah perbandingan senilai.",
            "pilihan": ["A. Rp 42.000", "B. Rp 49.000", "C. Rp 56.000", "D. Rp 35.000"],
            "jawaban": "B",
            "pembahasan": "4:28.000 = 7:x → x = 7 × 28.000 ÷ 4 = 196.000 ÷ 4 = Rp49.000."
        },
        {
            "no": 5, "tipe": "PG", "kp": "KP 2",
            "soal": "Pasangan bilangan manakah yang membentuk proporsi dengan 2 : 5?",
            "konteks": "",
            "pilihan": ["A. 6 : 10", "B. 4 : 12", "C. 8 : 20", "D. 3 : 6"],
            "jawaban": "C",
            "pembahasan": "2:5 = 8:20 karena 2×20 = 40 = 5×8. Cek: 2/5 = 8/20 = 0,4. ✅"
        },
        {
            "no": 6, "tipe": "PG", "kp": "KP 3",
            "soal": "Pada peta berskala 1 : 2.000.000, jarak dua kota adalah 6 cm. Jarak sebenarnya kedua kota adalah ...",
            "konteks": "",
            "pilihan": ["A. 12 km", "B. 120 km", "C. 1.200 km", "D. 12.000 km"],
            "jawaban": "B",
            "pembahasan": "Jarak nyata = 6 × 2.000.000 = 12.000.000 cm = 120.000 m = 120 km."
        },
        {
            "no": 7, "tipe": "PG", "kp": "KP 3",
            "soal": "Sebuah denah dibuat dengan skala 1 : 500. Jika lebar ruangan sebenarnya 8 meter, lebar di denah adalah ...",
            "konteks": "",
            "pilihan": ["A. 1,6 cm", "B. 16 cm", "C. 0,16 cm", "D. 160 cm"],
            "jawaban": "B",
            "pembahasan": "Jarak peta = 800 cm ÷ 500 = 1,6 cm. Hm, cek: 8 m = 800 cm. 800÷500 = 1,6 cm. Jawaban A."
        },
        {
            "no": 8, "tipe": "PG", "kp": "KP 4",
            "soal": "Modal usaha tiga orang adalah: Amir Rp2.000.000, Budi Rp3.000.000, Citra Rp5.000.000. Jika keuntungan Rp4.000.000 dibagi sesuai rasio modal, keuntungan Citra adalah ...",
            "konteks": "💡 Rasio modal = 2:3:5. Total bagian = 10.",
            "pilihan": ["A. Rp 800.000", "B. Rp 1.200.000", "C. Rp 2.000.000", "D. Rp 1.600.000"],
            "jawaban": "C",
            "pembahasan": "Rasio 2:3:5, total=10. Citra = 5/10 × 4.000.000 = Rp2.000.000."
        },
        {
            "no": 9, "tipe": "Isian", "kp": "KP 4",
            "soal": "Sebuah mobil menempuh 240 km dalam 3 jam. Berapa km/jam kecepatan rata-rata mobil tersebut?",
            "konteks": "💡 Kecepatan = Jarak ÷ Waktu",
            "pilihan": None,
            "jawaban": "80",
            "pembahasan": "Kecepatan = 240 km ÷ 3 jam = 80 km/jam."
        },
        {
            "no": 10, "tipe": "Isian", "kp": "KP 4",
            "soal": "Penghasilan Pak Rudi Rp4.000.000/bulan. Jika menabung dengan rasio 50:30:20 (kebutuhan:keinginan:tabungan), berapa rupiah yang ditabung per bulan?",
            "konteks": "💡 Tabungan = 20% dari penghasilan.",
            "pilihan": None,
            "jawaban": "800000",
            "pembahasan": "Tabungan = 20/100 × 4.000.000 = Rp800.000."
        },
    ]

    sudah_submit = st.session_state.get("submitted_rs", False)
    skor_total = 0

    for soal in soal_list:
        kp_color = {"KP 1": "#0D5C2E", "KP 2": "#1A9B50",
                    "KP 3": "#148A40", "KP 4": "#52C97A"}.get(soal["kp"], "#1A9B50")
        st.markdown(f"""
        <div style="border:1px solid #C8EDD8;border-radius:12px;padding:1rem 1.2rem;
                    margin:0.8rem 0;border-left:5px solid {kp_color};">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">
            <span style="background:{kp_color};color:white;padding:2px 10px;border-radius:20px;
                         font-size:0.78rem;font-weight:700;">{soal['kp']}</span>
            <span style="background:#EEF9F3;padding:2px 10px;border-radius:20px;
                         font-size:0.78rem;font-weight:700;">{soal['tipe']}</span>
            <b>Soal {soal['no']}</b>
        </div>
        <div style="font-size:0.95rem;font-weight:600;">{soal['soal']}</div>
        {f'<div style="background:#FFF8E6;padding:0.5rem 0.8rem;border-radius:8px;margin-top:0.4rem;font-size:0.88rem;color:#8B6914;">{soal["konteks"]}</div>' if soal["konteks"] else ""}
        </div>
        """, unsafe_allow_html=True)

        key = f"soal_rs_{soal['no']}"
        if soal["tipe"] == "PG":
            jawab = st.radio("Pilih jawaban:", soal["pilihan"],
                             key=key, label_visibility="collapsed", index=None)
            if jawab:
                st.session_state.jawab_rs[key] = jawab
        else:
            jawab = st.text_input("Jawaban kamu:", key=key,
                                  placeholder="Tulis jawabanmu di sini...")
            if jawab:
                st.session_state.jawab_rs[key] = jawab

        if sudah_submit and key in st.session_state.jawab_rs:
            j = st.session_state.jawab_rs[key]
            benar = (soal["tipe"] == "PG" and j and j.startswith(soal["jawaban"])) or \
                    (soal["tipe"] == "Isian" and soal["jawaban"].lower() in j.lower().replace(".","").replace(",",""))
            if benar:
                skor_total += 1
                st.markdown(f'<div class="success-card" style="font-size:0.85rem;">✅ <b>BENAR!</b> {soal["pembahasan"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="danger-card" style="font-size:0.85rem;">❌ <b>Belum tepat.</b> Jawaban: <b>{soal["jawaban"]}</b>. {soal["pembahasan"]}</div>', unsafe_allow_html=True)
        st.markdown("")

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button("✅ Submit & Lihat Nilai", type="primary", use_container_width=True):
            st.session_state.submitted_rs = True
            st.rerun()
    with col_btn2:
        if st.button("🔄 Reset Jawaban", use_container_width=True):
            st.session_state.submitted_rs = False
            st.session_state.jawab_rs = {}
            st.rerun()

    if sudah_submit:
        persen = skor_total / len(soal_list) * 100
        emoji  = "🏆" if persen >= 80 else ("👍" if persen >= 60 else "💪")
        warna_nilai = "#70AD47" if persen >= 80 else ("#ED7D31" if persen >= 60 else "#C00000")
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D5C2E,#1A9B50);color:white;
                    border-radius:16px;padding:1.5rem 2rem;text-align:center;margin-top:1rem;">
            <div style="font-size:1.1rem;opacity:0.9;">Nilai Akhir {emoji}</div>
            <div style="font-size:4rem;font-weight:800;color:{warna_nilai};">{persen:.0f}</div>
            <div style="font-size:1rem;opacity:0.8;">{skor_total} dari {len(soal_list)} soal benar</div>
            <div style="margin-top:0.8rem;font-size:0.9rem;">
            {'🏆 Excellent! Kamu sudah menguasai Rasio & Proporsi!' if persen>=80 else ('👍 Bagus! Pelajari lagi bagian yang masih salah.' if persen>=60 else '💪 Semangat! Eksplorasi lebih dalam dengan kalkulator digital!')}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 Refleksi Penggunaan Kalkulator Digital Streamlit")
        r1 = st.text_area("1. Fitur apa yang paling membantumu memahami rasio? Mengapa?",
                           placeholder="Tuliskan refleksimu di sini...", height=80)
        r2 = st.text_area("2. Apa situasi nyata dalam hidupmu yang menggunakan rasio?",
                           placeholder="Tuliskan refleksimu di sini...", height=80)
        r3 = st.text_area("3. Bagaimana perasaanmu belajar rasio dengan kalkulator digital ini?",
                           placeholder="Tuliskan refleksimu di sini...", height=80)
        if r1 or r2 or r3:
            st.markdown('<div class="success-card">✅ Terima kasih atas refleksimu! Salin ke LKS-mu.</div>', unsafe_allow_html=True)
