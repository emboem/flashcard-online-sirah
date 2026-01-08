import streamlit as st
import base64
import json
import os
import random
import streamlit.components.v1 as components

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Flashcard Sirah Nabawiyah",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DATA DAILY HIKMAH
# ==========================================
hikmah_list = [
    "Barangsiapa menempuh jalan untuk menuntut ilmu, Allah akan mudahkan baginya jalan menuju Surga. (HR. Muslim)",
    "Sebaik-baik kalian adalah orang yang mempelajari Al-Qur'an dan mengajarkannya. (HR. Bukhari)",
    "Cintailah kekasihmu sekadarnya saja, boleh jadi ia akan menjadi musuhmu suatu hari nanti. (Ali bin Abi Thalib)",
    "Ketahuilah bahwa kemenangan itu beriringan dengan kesabaran. (HR. Tirmidzi)",
    "Tidaklah seorang muslim tertimpa keletihan, penyakit, kesedihan, melainkan Allah akan menghapus dosa-dosanya. (HR. Bukhari)",
    "Akhlak Rasulullah ﷺ adalah Al-Qur'an.",
    "Shalat adalah tiang agama.",
    "Senyummu di hadapan saudaramu adalah sedekah. (HR. Tirmidzi)",
    "Orang yang paling dekat denganku di hari kiamat adalah yang paling baik akhlaknya. (HR. Tirmidzi)",
    "Jangan marah, maka bagimu Surga. (HR. Thabrani)"
]

# ==========================================
# 3. DATA MATERI LENGKAP DENGAN KATEGORI
# ==========================================
# Saya telah menambahkan field 'category' untuk setiap kartu
full_cards_data = [
    # --- PENGANTAR & NASAB ---
    { "category": "Pengantar & Nasab", "front": "Apa yang dimaksud dengan sirah nabawiyah secara bahasa dan istilah?", "back": "Secara bahasa artinya jalan. Secara istilah yaitu sejarah hidup Rasulullah ﷺ dari lahir hingga wafat, mencakup sifat fisik dan akhlak." },
    { "category": "Pengantar & Nasab", "front": "Mengapa penting mempelajari sirah nabawiyah?", "back": "Agar kita dapat mengenal, mencintai, dan meneladani Rasulullah ﷺ dalam seluruh aspek kehidupan, serta memahami Islam dari sumber praktisnya." },
    { "category": "Pengantar & Nasab", "front": "Sebutkan nasab Nabi Muhammad ﷺ dari pihak ayah hingga Adnan!", "back": "Muhammad bin Abdullah bin Abdul Muthalib bin Hasyim bin Abdu Manaf ... bin Adnan." },
    
    # --- MASA KECIL & REMAJA ---
    { "category": "Masa Kecil & Remaja", "front": "Apa peristiwa besar yang terjadi pada tahun kelahiran Nabi Muhammad ﷺ?", "back": "Peristiwa penyerangan Ka’bah oleh pasukan bergajah yang dipimpin oleh Abrahah (Tahun Gajah)." },
    { "category": "Masa Kecil & Remaja", "front": "Siapakah wanita yang menyusui Nabi Muhammad ﷺ setelah ibunya?", "back": "Tsuwaibah (hamba sahaya Abu Lahab) dan Halimah as-Sa’diyah dari Bani Sa’ad." },
    { "category": "Masa Kecil & Remaja", "front": "Apa hikmah Nabi Muhammad ﷺ disusukan di perkampungan Bani Sa’ad?", "back": "Agar tumbuh di lingkungan yang udaranya bersih, terhindar dari penyakit kota, dan mempelajari bahasa Arab yang fasih." },
    { "category": "Masa Kecil & Remaja", "front": "Peristiwa apa yang dialami Nabi Muhammad ﷺ saat kecil di perkampungan Bani Sa’ad?", "back": "Peristiwa pembelahan dada (syaqqush shadr) oleh Malaikat Jibril untuk membersihkan hatinya." },
    { "category": "Masa Kecil & Remaja", "front": "Pada usia berapa ibunda Nabi Muhammad ﷺ, Aminah, wafat dan di mana?", "back": "Pada usia 6 tahun, di Abwa (antara Makkah dan Madinah)." },
    { "category": "Masa Kecil & Remaja", "front": "Siapakah yang mengasuh Nabi Muhammad ﷺ setelah ibunya wafat?", "back": "Kakeknya, Abdul Muthalib (sampai usia 8 th), lalu pamannya, Abu Thalib." },
    { "category": "Masa Kecil & Remaja", "front": "Pekerjaan apa yang dilakukan Nabi Muhammad ﷺ saat remaja sebelum berdagang?", "back": "Menggembala kambing bagi penduduk Makkah." },
    { "category": "Masa Kecil & Remaja", "front": "Apa gelar yang diberikan penduduk Makkah kepada Nabi Muhammad ﷺ sebelum menjadi rasul?", "back": "Al-Amin, artinya orang yang dapat dipercaya." },
    { "category": "Masa Kecil & Remaja", "front": "Ceritakan singkat peristiwa peletakan Hajar Aswad saat renovasi Ka’bah!", "back": "Nabi meletakkan Hajar Aswad di atas kain, lalu setiap pemimpin kabilah mengangkat ujung kain bersama-sama." },
    
    # --- KELUARGA NABI ---
    { "category": "Keluarga Nabi", "front": "Berapa usia Nabi Muhammad ﷺ saat menikah dengan Khadijah?", "back": "Nabi berusia 25 tahun, Khadijah berusia 40 tahun." },
    { "category": "Keluarga Nabi", "front": "Sebutkan putra-putri Nabi Muhammad ﷺ dari Khadijah!", "back": "Al-Qasim, Abdullah, Zainab, Ruqayyah, Ummu Kultsum, dan Fathimah." },
    { "category": "Keluarga Nabi", "front": "Sebutkan istri-istri Nabi Muhammad ﷺ (Ummahatul Mukminin)!", "back": "Khadijah, Saudah, Aisyah, Hafshah, Zainab binti Khuzaimah, Ummu Salamah, Zainab binti Jahsy, Juwairiyah, Ummu Habibah, Shafiyah, Maimunah." },

    # --- PERIODE MAKKAH ---
    { "category": "Periode Makkah", "front": "Di mana dan kapan wahyu pertama diturunkan?", "back": "Di Gua Hira pada bulan Ramadan, saat beliau berusia 40 tahun." },
    { "category": "Periode Makkah", "front": "Apa ayat pertama yang diturunkan kepada Nabi Muhammad ﷺ?", "back": "Surah Al-’Alaq ayat 1-5 (“Iqra’ bismi rabbikalladzi khalaq…”)." },
    { "category": "Periode Makkah", "front": "Siapakah Assabiqunal Awwalun (orang pertama masuk Islam)?", "back": "Wanita: Khadijah; Laki-laki: Abu Bakar; Anak: Ali bin Abi Thalib; Hamba sahaya: Zaid bin Haritsah." },
    { "category": "Periode Makkah", "front": "Berapa lama dakwah sembunyi-sembunyi dan di mana pusatnya?", "back": "3 tahun, di rumah Arqam bin Abi Arqam." },
    { "category": "Periode Makkah", "front": "Apa tanda dimulainya dakwah terang-terangan?", "back": "Turunnya QS. Al-Hijr ayat 94: “Maka sampaikanlah secara terang-terangan...”" },
    { "category": "Periode Makkah", "front": "Bagaimana reaksi Quraisy terhadap dakwah terang-terangan?", "back": "Menolak, mengejek, menuduh gila/sihir, dan menyiksa sahabat." },
    { "category": "Periode Makkah", "front": "Sebutkan sahabat yang disiksa berat di Makkah!", "back": "Bilal bin Rabah, Ammar bin Yasir, Sumayyah, Khabbab bin al-Arats." },
    { "category": "Periode Makkah", "front": "Ke mana hijrah pertama kali sebelum ke Madinah?", "back": "Ke Habasyah (Ethiopia), karena rajanya (Najasyi) adil." },
    { "category": "Periode Makkah", "front": "Apa itu ‘Amul Huzni (Tahun Kesedihan)?", "back": "Tahun ke-10 kenabian, wafatnya Abu Thalib dan Khadijah." },
    { "category": "Periode Makkah", "front": "Ceritakan singkat Isra’ dan Mi’raj!", "back": "Isra’: Masjidil Haram ke Masjidil Aqsha. Mi’raj: Naik ke Sidratul Muntaha menerima perintah shalat." },
    { "category": "Periode Makkah", "front": "Apa isi Bai’at Aqabah Pertama?", "back": "Janji 12 orang Yatsrib untuk tidak menyekutukan Allah, mencuri, berzina, dll." },
    { "category": "Periode Makkah", "front": "Apa isi Bai’at Aqabah Kedua?", "back": "Janji setia 75 orang Yatsrib untuk melindungi Nabi seperti keluarga sendiri." },

    # --- HIJRAH & MADINAH ---
    { "category": "Hijrah & Awal Madinah", "front": "Siapa yang menemani Nabi saat hijrah ke Madinah?", "back": "Abu Bakar ash-Shiddiq (sembunyi di Gua Tsur 3 hari)." },
    { "category": "Hijrah & Awal Madinah", "front": "Apa yang pertama kali dilakukan Nabi di Quba?", "back": "Membangun Masjid Quba." },
    { "category": "Hijrah & Awal Madinah", "front": "Apa langkah strategis Nabi setiba di Madinah?", "back": "Membangun Masjid Nabawi, mempersaudarakan Muhajirin-Anshar, Piagam Madinah." },
    { "category": "Hijrah & Awal Madinah", "front": "Apa itu Piagam Madinah?", "back": "Konstitusi tertulis pertama yang mengatur hubungan antar kelompok (Muslim, Yahudi, musyrik) di Madinah." },

    # --- PEPERANGAN ---
    { "category": "Peperangan", "front": "Kapan Perang Badar terjadi dan apa sebabnya?", "back": "Ramadan th 2 H. Mencegat kafilah dagang Abu Sufyan sebagai ganti rugi harta yang dirampas." },
    { "category": "Peperangan", "front": "Hasil Perang Badar?", "back": "Kemenangan besar Muslim (313 orang) melawan Quraisy (1000 orang)." },
    { "category": "Peperangan", "front": "Kapan Perang Uhud terjadi dan pelajarannya?", "back": "Syawal th 3 H. Bahaya melanggar perintah Rasulullah (pemanah meninggalkan pos)." },
    { "category": "Peperangan", "front": "Penyebab kekalahan sementara di Uhud?", "back": "Pasukan pemanah turun mengambil ghanimah, diserang balik dari belakang." },
    { "category": "Peperangan", "front": "Apa itu Perang Khandaq (Ahzab)?", "back": "Perang parit (th 5 H), Madinah dikepung koalisasi musuh." },
    { "category": "Peperangan", "front": "Siapa pengusul strategi parit?", "back": "Salman al-Farisi." },
    { "category": "Peperangan", "front": "Kapan Perang Hunain terjadi?", "back": "Syawal th 8 H (setelah Fathu Makkah). Pelajaran: Jumlah banyak tak jamin menang jika ujub." },
    { "category": "Peperangan", "front": "Perang terakhir Nabi?", "back": "Perang Tabuk (th 9 H) melawan Romawi." },

    # --- PERJANJIAN & FATHU MAKKAH ---
    { "category": "Perjanjian & Kemenangan", "front": "Apa isi Perjanjian Hudaibiyah?", "back": "Gencatan senjata 10 th, umrah tunda tahun depan, pengembalian orang Quraisy tanpa izin." },
    { "category": "Perjanjian & Kemenangan", "front": "Hikmah Perjanjian Hudaibiyah?", "back": "Suasana damai memungkinkan dakwah menyebar luas (Fathan Mubina)." },
    { "category": "Perjanjian & Kemenangan", "front": "Kepada siapa Nabi mengirim surat dakwah?", "back": "Heraklius (Romawi), Kisra (Persia), Muqauqis (Mesir), Najasyi (Habasyah)." },
    { "category": "Perjanjian & Kemenangan", "front": "Kapan dan sebab Fathu Makkah?", "back": "Ramadan th 8 H. Pelanggaran perjanjian oleh sekutu Quraisy." },
    { "category": "Perjanjian & Kemenangan", "front": "Sikap Nabi saat Fathu Makkah?", "back": "Memberi amnesti umum: “Pergilah, kalian sekarang bebas!”" },
    { "category": "Perjanjian & Kemenangan", "front": "Apa yang dilakukan Nabi terhadap berhala?", "back": "Menghancurkannya sambil membaca QS. Al-Isra: 81." },

    # --- AKHIR HAYAT & LAINNYA ---
    { "category": "Akhir Hayat & Mukjizat", "front": "Apa itu Haji Wada’?", "back": "Haji perpisahan, satu-satunya haji Nabi (th 10 H)." },
    { "category": "Akhir Hayat & Mukjizat", "front": "Pesan Haji Wada’?", "back": "Haram darah/harta sesama, larangan riba, muliakan wanita, pegang Al-Qur’an & Sunnah." },
    { "category": "Akhir Hayat & Mukjizat", "front": "Kapan Nabi wafat?", "back": "12 Rabiul Awal 11 H (632 M), usia 63 tahun." },
    { "category": "Akhir Hayat & Mukjizat", "front": "Siapa yang memandikan jenazah Nabi?", "back": "Ali bin Abi Thalib, Abbas, Fadhl, Qutsam, Usamah, Syuqran." },
    { "category": "Akhir Hayat & Mukjizat", "front": "Sebutkan mukjizat Nabi selain Al-Qur’an!", "back": "Terbelah bulan, air memancar dari jari, makanan jadi banyak, Isra’ Mi’raj." },
]

# ==========================================
# 4. LOGIC: FILTER KATEGORI & HIKMAH
# ==========================================

# 1. Tampilkan Hikmah Harian (Random)
selected_hikmah = random.choice(hikmah_list)
st.markdown(f"""
<div style="background-color: #e0e7ff; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #4f46e5;">
    <p style="margin:0; font-size: 14px; color: #3730a3;">✨ <b>Hikmah Hari Ini:</b></p>
    <p style="margin:5px 0 0 0; font-style: italic; color: #1f2937;">"{selected_hikmah}"</p>
</div>
""", unsafe_allow_html=True)

# 2. Filter Kategori
# Ambil list kategori unik
categories = ["Semua Kategori"] + sorted(list(set([card["category"] for card in full_cards_data])))

# Pilihan Kategori di atas kartu (bisa juga di sidebar pakai st.sidebar.selectbox)
selected_category = st.selectbox("Pilih Topik Belajar:", categories)

# Filter data berdasarkan pilihan
if selected_category == "Semua Kategori":
    cards_data = full_cards_data
else:
    cards_data = [card for card in full_cards_data if card["category"] == selected_category]

# Ubah ke JSON untuk JS
json_data = json.dumps(cards_data)


# ==========================================
# 5. FUNGSI GAMBAR
# ==========================================
def get_image_base64(image_path):
    try:
        if not os.path.exists(image_path):
            return None
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        return None

logo_filename = "logo_ummul_qura.jpg"
logo_base64 = get_image_base64(logo_filename)
logo_src = ""
if logo_base64:
    ext = "webp" if logo_filename.endswith("webp") else "jpeg"
    logo_src = f"data:image/{ext};base64,{logo_base64}"


# ==========================================
# 6. HTML/JS INJECTION (DENGAN AUDIO)
# ==========================================
html_code = f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body {{ 
            font-family: 'Inter', sans-serif; 
            background-color: transparent; 
            margin: 0; padding: 0;
            display: flex; justify-content: center; align-items: center;
            height: 680px;
        }}

        .card-container-3d {{
            perspective: 1000px;
            width: 320px;
            height: 520px;
            position: relative;
            transition: transform 0.2s ease-in-out;
        }}
        
        .card-container-3d.squeeze {{ transform: scale(0.95); }}

        .card-inner {{
            width: 100%; height: 100%; position: relative;
            text-align: center;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
            cursor: pointer;
        }}

        .card-inner.flipped {{ transform: rotateY(180deg); }}

        .card-face {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            -webkit-backface-visibility: hidden; backface-visibility: hidden;
            border-radius: 1.5rem; display: flex; flex-direction: column;
            padding: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .card-front {{ background-color: white; color: #1f2937; border: 1px solid #e5e7eb; z-index: 2; }}
        .card-back {{ background-color: #4338ca; color: white; transform: rotateY(180deg); border: 1px solid #3730a3; z-index: 1; }}

        .scrollbar-hide::-webkit-scrollbar {{ display: none; }}
        .scrollbar-hide {{ -ms-overflow-style: none; scrollbar-width: none; }}

        .nav-btn {{ transition: all 0.2s; }}
        .nav-btn:active {{ transform: scale(0.95); }}

        /* Button Speaker Style */
        .audio-btn {{
            position: absolute; top: 1rem; right: 1rem;
            background: rgba(255,255,255,0.2);
            padding: 8px; border-radius: 50%;
            cursor: pointer; transition: background 0.2s;
            z-index: 10;
        }}
        .card-front .audio-btn {{ background: #f3f4f6; color: #4f46e5; }}
        .card-back .audio-btn {{ background: rgba(255,255,255,0.2); color: white; }}
        .audio-btn:hover {{ transform: scale(1.1); }}
    </style>
</head>
<body>

    <div class="flex flex-col items-center gap-6 w-full">
        
        <div class="w-[320px] flex justify-between items-center px-1">
            <div>
                <h1 class="text-lg font-bold text-gray-800">Flashcard Online</h1>
                <p class="text-xs text-gray-500" id="progress-text">Memuat...</p>
            </div>
            <div class="p-2 bg-white rounded-full shadow-sm border border-gray-100">
                <i data-lucide="book-open" class="w-4 h-4 text-indigo-600"></i>
            </div>
        </div>

        <div class="card-container-3d" id="card-container" onclick="flipCard()">
            <div class="card-inner" id="flashcard">
                
                <div class="card-face card-front">
                    <span class="absolute top-5 left-5 text-[10px] font-bold uppercase tracking-widest text-gray-400">Tanya</span>
                    
                    <button class="audio-btn shadow-sm" onclick="playAudio(event, 'front')" title="Dengarkan Pertanyaan">
                        <i data-lucide="volume-2" class="w-4 h-4"></i>
                    </button>

                    <div class="flex-1 w-full flex items-center justify-center my-8 overflow-hidden">
                        <div class="w-full max-h-full overflow-y-auto scrollbar-hide flex items-center justify-center">
                             <p class="text-lg font-semibold text-center leading-relaxed px-1" id="card-front-text"></p>
                        </div>
                    </div>
                    <div class="w-full flex flex-col items-center justify-end shrink-0 gap-3 pb-1">
                         <img src="{logo_src}" alt="Ummul Qura" class="h-8 object-contain opacity-75 grayscale hover:grayscale-0 transition duration-300">
                         <div class="text-[9px] uppercase tracking-wider text-gray-400 flex items-center gap-1 font-semibold">
                             <i data-lucide="rotate-cw" class="w-3 h-3"></i> Klik kartu untuk balik
                         </div>
                    </div>
                </div>

                <div class="card-face card-back">
                    <span class="absolute top-5 left-5 text-[10px] font-bold uppercase tracking-widest text-indigo-200/70">Jawab</span>
                    
                    <button class="audio-btn" onclick="playAudio(event, 'back')" title="Dengarkan Jawaban">
                        <i data-lucide="volume-2" class="w-4 h-4"></i>
                    </button>

                    <div class="w-full h-full flex items-center justify-center overflow-hidden">
                         <div class="w-full max-h-full overflow-y-auto scrollbar-hide py-4">
                            <p class="text-lg font-medium text-center leading-relaxed" id="card-back-text"></p>
                         </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="flex justify-center items-center gap-4">
            <button onclick="prevCard(event)" class="nav-btn p-3 bg-white rounded-full shadow-sm border border-gray-200 text-gray-600 hover:text-indigo-600 hover:border-indigo-200" id="btn-prev">
                <i data-lucide="arrow-left" class="w-5 h-5"></i>
            </button>
            <button onclick="shuffleCards(event)" class="nav-btn p-3 bg-white rounded-full shadow-sm border border-gray-200 text-gray-400 hover:text-indigo-600 hover:border-indigo-200">
                <i data-lucide="shuffle" class="w-5 h-5"></i>
            </button>
            <button onclick="nextCard(event)" class="nav-btn p-3 bg-indigo-600 rounded-full shadow-lg shadow-indigo-200 text-white hover:bg-indigo-700" id="btn-next">
                <i data-lucide="arrow-right" class="w-5 h-5"></i>
            </button>
        </div>

    </div>

    <script>
        let cards = {json_data};
        let currentIndex = 0;
        let isFlipped = false;

        const cardContainer = document.getElementById('card-container');
        const cardInner = document.getElementById('flashcard');
        const frontText = document.getElementById('card-front-text');
        const backText = document.getElementById('card-back-text');
        const progressText = document.getElementById('progress-text');
        const btnNext = document.getElementById('btn-next');
        const btnPrev = document.getElementById('btn-prev');

        function renderCard() {{
            frontText.textContent = cards[currentIndex].front;
            backText.textContent = cards[currentIndex].back;
            progressText.textContent = `Kartu ${{currentIndex + 1}} dari ${{cards.length}}`;
            
            btnPrev.disabled = currentIndex === 0;
            btnPrev.style.opacity = currentIndex === 0 ? "0.5" : "1";
            btnNext.disabled = currentIndex === cards.length - 1;
            btnNext.style.opacity = currentIndex === cards.length - 1 ? "0.5" : "1";
            
            lucide.createIcons();
        }}

        window.flipCard = () => {{
            isFlipped = !isFlipped;
            cardInner.classList.toggle('flipped');
        }};

        // LOGIC AUDIO (TEXT TO SPEECH)
        window.playAudio = (e, side) => {{
            e.stopPropagation(); // Mencegah kartu berbalik saat tombol audio diklik
            
            // Hentikan suara sebelumnya jika ada
            window.speechSynthesis.cancel();

            let textToRead = "";
            if(side === 'front') {{
                textToRead = cards[currentIndex].front;
            }} else {{
                textToRead = cards[currentIndex].back;
            }}

            let utterance = new SpeechSynthesisUtterance(textToRead);
            utterance.lang = "id-ID"; // Bahasa Indonesia
            utterance.rate = 0.9;     // Kecepatan sedikit diperlambat agar jelas
            
            window.speechSynthesis.speak(utterance);
        }};

        window.nextCard = (e) => {{
            e.stopPropagation();
            // Stop audio jika pindah kartu
            window.speechSynthesis.cancel();
            if (currentIndex < cards.length - 1) {{
                changeCard(currentIndex + 1);
            }}
        }};

        window.prevCard = (e) => {{
            e.stopPropagation();
            window.speechSynthesis.cancel();
            if (currentIndex > 0) {{
                changeCard(currentIndex - 1);
            }}
        }};

        function changeCard(newIndex) {{
            if (isFlipped) {{
                flipCard(); 
                setTimeout(() => {{ 
                    currentIndex = newIndex; 
                    renderCard(); 
                }}, 300);
            }} else {{
                cardContainer.classList.add('squeeze');
                setTimeout(() => {{
                    currentIndex = newIndex;
                    renderCard();
                    cardContainer.classList.remove('squeeze');
                }}, 200);
            }}
        }}

        window.shuffleCards = (e) => {{
            e.stopPropagation();
            window.speechSynthesis.cancel();
            for (let i = cards.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [cards[i], cards[j]] = [cards[j], cards[i]];
            }}
            currentIndex = 0;
            if (isFlipped) flipCard();
            renderCard();
        }};

        renderCard();
        lucide.createIcons();
    </script>
</body>
</html>
"""

components.html(html_code, height=700)

