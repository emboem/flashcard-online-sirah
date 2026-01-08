import streamlit as st
import base64
import json
import os
import streamlit.components.v1 as components

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Flashcard Sirah Nabawiyah",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. DATA MATERI (50 SOAL)
# ==========================================
cards_data = [
    { "front": "Apa yang dimaksud dengan sirah nabawiyah secara bahasa dan istilah?", "back": "Secara bahasa artinya jalan. Secara istilah yaitu sejarah hidup Rasulullah ﷺ dari lahir hingga wafat, mencakup sifat fisik dan akhlak, serta peristiwa-peristiwa yang dialami beliau." },
    { "front": "Mengapa penting mempelajari sirah nabawiyah?", "back": "Agar kita dapat mengenal, mencintai, dan meneladani Rasulullah ﷺ dalam seluruh aspek kehidupan, serta memahami Islam dari sumber praktisnya." },
    { "front": "Sebutkan nasab Nabi Muhammad ﷺ dari pihak ayah hingga Adnan!", "back": "Muhammad bin Abdullah bin Abdul Muthalib bin Hasyim bin Abdu Manaf bin Qushay bin Kilab bin Murrah bin Ka’ab bin Luay bin Ghalib bin Fihr bin Malik bin an-Nadhr bin Kinanah bin Khuzaimah bin Mudrikah bin Ilyas bin Mudhar bin Nizar bin Ma’ad bin Adnan." },
    { "front": "Apa peristiwa besar yang terjadi pada tahun kelahiran Nabi Muhammad ﷺ?", "back": "Peristiwa penyerangan Ka’bah oleh pasukan bergajah yang dipimpin oleh Abrahah (Tahun Gajah)." },
    { "front": "Siapakah wanita yang menyusui Nabi Muhammad ﷺ setelah ibunya?", "back": "Tsuwaibah (hamba sahaya Abu Lahab) dan Halimah as-Sa’diyah dari Bani Sa’ad." },
    { "front": "Apa hikmah Nabi Muhammad ﷺ disusukan di perkampungan Bani Sa’ad?", "back": "Agar tumbuh di lingkungan yang udaranya bersih, terhindar dari penyakit kota, dan mempelajari bahasa Arab yang fasih." },
    { "front": "Peristiwa apa yang dialami Nabi Muhammad ﷺ saat kecil di perkampungan Bani Sa’ad?", "back": "Peristiwa pembelahan dada (syaqqush shadr) oleh Malaikat Jibril untuk membersihkan hatinya dari bagian setan." },
    { "front": "Pada usia berapa ibunda Nabi Muhammad ﷺ, Aminah, wafat dan di mana?", "back": "Pada usia 6 tahun, di Abwa (antara Makkah dan Madinah)." },
    { "front": "Siapakah yang mengasuh Nabi Muhammad ﷺ setelah ibunya wafat?", "back": "Kakeknya, Abdul Muthalib, hingga usia 8 tahun, kemudian pamannya, Abu Thalib." },
    { "front": "Pekerjaan apa yang dilakukan Nabi Muhammad ﷺ saat remaja sebelum berdagang?", "back": "Menggembala kambing bagi penduduk Makkah." },
    { "front": "Apa gelar yang diberikan penduduk Makkah kepada Nabi Muhammad ﷺ sebelum diangkat menjadi rasul, dan apa artinya?", "back": "Al-Amin, artinya orang yang dapat dipercaya." },
    { "front": "Ceritakan singkat peristiwa peletakan Hajar Aswad saat renovasi Ka’bah!", "back": "Para kabilah berselisih. Nabi mengusulkan Hajar Aswad diletakkan di atas kain, lalu setiap pemimpin kabilah memegang ujung kain dan mengangkatnya bersama. Nabi meletakkannya ke tempat semula." },
    { "front": "Berapa usia Nabi Muhammad ﷺ saat menikah dengan Khadijah, dan berapa usia Khadijah saat itu?", "back": "Nabi berusia 25 tahun, Khadijah berusia 40 tahun." },
    { "front": "Sebutkan putra-putri Nabi Muhammad ﷺ dari Khadijah!", "back": "Al-Qasim, Abdullah, Zainab, Ruqayyah, Ummu Kultsum, dan Fathimah." },
    { "front": "Di mana dan kapan wahyu pertama diturunkan kepada Nabi Muhammad ﷺ?", "back": "Di Gua Hira pada bulan Ramadan, saat beliau berusia 40 tahun." },
    { "front": "Apa ayat pertama yang diturunkan kepada Nabi Muhammad ﷺ?", "back": "Surah Al-’Alaq ayat 1-5 (“Iqra’ bismi rabbikalladzi khalaq…”)." },
    { "front": "Siapakah orang-orang pertama yang masuk Islam (Assabiqunal Awwalun)?", "back": "Wanita: Khadijah; Laki-laki: Abu Bakar; Anak-anak: Ali bin Abi Thalib; Hamba sahaya: Zaid bin Haritsah." },
    { "front": "Berapa lama dakwah dilakukan secara sembunyi-sembunyi, dan di mana pusat kegiatannya?", "back": "Selama 3 tahun, berpusat di rumah Arqam bin Abi Arqam." },
    { "front": "Apa yang menandai dimulainya dakwah secara terang-terangan?", "back": "Turunnya QS. Al-Hijr ayat 94: “Maka sampaikanlah secara terang-terangan...”" },
    { "front": "Bagaimana reaksi kaum Quraisy terhadap dakwah terang-terangan Nabi Muhammad ﷺ?", "back": "Menolak, mengejek, menuduh gila/sihir, dan menyiksa para sahabat." },
    { "front": "Sebutkan contoh sahabat yang mengalami penyiksaan berat di Makkah!", "back": "Bilal bin Rabah, Ammar bin Yasir, Sumayyah (syahidah pertama), Khabbab bin al-Arats." },
    { "front": "Ke mana kaum Muslimin melakukan hijrah pertama kali sebelum ke Madinah?", "back": "Ke Habasyah (Ethiopia), karena di sana ada raja yang adil (Najasyi)." },
    { "front": "Apa yang dimaksud dengan ‘Amul Huzni (Tahun Kesedihan)?", "back": "Tahun ke-10 kenabian, wafatnya Abu Thalib dan Khadijah." },
    { "front": "Ceritakan singkat peristiwa Isra’ dan Mi’raj!", "back": "Isra’: Perjalanan dari Masjidil Haram ke Masjidil Aqsha. Mi’raj: Naik ke Sidratul Muntaha untuk menerima perintah shalat 5 waktu." },
    { "front": "Apa isi Bai’at Aqabah Pertama?", "back": "Perjanjian 12 orang Yatsrib untuk tidak menyekutukan Allah, tidak mencuri, berzina, membunuh anak, berdusta, dan mendurhakai Nabi." },
    { "front": "Apa isi Bai’at Aqabah Kedua?", "back": "Janji setia 73 laki-laki dan 2 wanita Yatsrib untuk melindungi Nabi sebagaimana melindungi keluarga sendiri." },
    { "front": "Siapakah yang menemani Nabi Muhammad ﷺ saat hijrah ke Madinah?", "back": "Abu Bakar ash-Shiddiq, bersembunyi di Gua Tsur selama 3 hari." },
    { "front": "Apa yang pertama kali dilakukan Nabi Muhammad ﷺ setibanya di Quba?", "back": "Membangun Masjid Quba." },
    { "front": "Apa langkah strategis Nabi setelah tiba di Madinah?", "back": "Membangun Masjid Nabawi, mempersaudarakan Muhajirin dan Anshar, membuat Piagam Madinah." },
    { "front": "Apa yang dimaksud dengan Piagam Madinah?", "back": "Konstitusi tertulis pertama yang mengatur hubungan antar kelompok (Muslim, Yahudi, musyrik) di Madinah." },
    { "front": "Kapan Perang Badar terjadi dan apa sebab utamanya?", "back": "Ramadan th 2 H. Upaya mencegat kafilah dagang Abu Sufyan sebagai ganti rugi harta yang dirampas di Makkah." },
    { "front": "Hasil Perang Badar?", "back": "Kemenangan besar Muslim (313 orang) melawan Quraisy (1000 orang)." },
    { "front": "Kapan Perang Uhud terjadi dan apa pelajaran pentingnya?", "back": "Syawal th 3 H. Bahaya melanggar perintah Rasulullah ﷺ (pasukan pemanah meninggalkan pos)." },
    { "front": "Apa penyebab kekalahan sementara di Perang Uhud?", "back": "Pasukan pemanah turun mengambil ghanimah, sehingga kavaleri Quraisy menyerang dari belakang." },
    { "front": "Apa itu Perang Khandaq (Ahzab)?", "back": "Perang parit (th 5 H), Madinah dikepung koalisasi Quraisy, Yahudi, dan kabilah lain." },
    { "front": "Siapa pengusul strategi parit di Perang Khandaq?", "back": "Salman al-Farisi." },
    { "front": "Apa isi Perjanjian Hudaibiyah?", "back": "Gencatan senjata 10 tahun, umrah ditunda tahun depan, pengembalian orang Quraisy yang datang ke Nabi tanpa izin." },
    { "front": "Hikmah Perjanjian Hudaibiyah?", "back": "Suasana damai memungkinkan dakwah menyebar luas (Fathan Mubina)." },
    { "front": "Kepada siapa Nabi mengirim surat dakwah?", "back": "Heraklius (Romawi), Kisra (Persia), Muqauqis (Mesir), Najasyi (Habasyah)." },
    { "front": "Kapan dan sebab Fathu Makkah?", "back": "Ramadan th 8 H. Pelanggaran perjanjian oleh sekutu Quraisy (Bani Bakr) menyerang sekutu Muslim (Bani Khuza’ah)." },
    { "front": "Sikap Nabi saat Fathu Makkah?", "back": "Memberi amnesti umum: “Pergilah, kalian sekarang bebas!”" },
    { "front": "Apa yang dilakukan Nabi terhadap berhala di Ka’bah?", "back": "Menghancurkannya sambil membaca QS. Al-Isra: 81." },
    { "front": "Pelajaran Perang Hunain?", "back": "Jumlah banyak tidak menjamin kemenangan jika ujub (bangga diri)." },
    { "front": "Perang terakhir Nabi?", "back": "Perang Tabuk (th 9 H) melawan Romawi." },
    { "front": "Apa itu Haji Wada’?", "back": "Haji perpisahan, satu-satunya haji Nabi (th 10 H)." },
    { "front": "Pesan Haji Wada’?", "back": "Haram darah/harta sesama Muslim, larangan riba, muliakan wanita, pegang teguh Al-Qur’an dan Sunnah." },
    { "front": "Kapan Nabi wafat?", "back": "12 Rabiul Awal 11 H (632 M), usia 63 tahun. Dimakamkan di kamar Aisyah." },
    { "front": "Siapa yang memandikan jenazah Nabi?", "back": "Ali bin Abi Thalib, Abbas, Fadhl, Qutsam, Usamah, Syuqran." },
    { "front": "Sebutkan istri-istri Nabi!", "back": "Khadijah, Saudah, Aisyah, Hafshah, Zainab binti Khuzaimah, Ummu Salamah, Zainab binti Jahsy, Juwairiyah, Ummu Habibah, Shafiyah, Maimunah." },
    { "front": "Sebutkan mukjizat Nabi selain Al-Qur’an!", "back": "Terbelah bulan, air memancar dari jari, makanan jadi banyak, Isra’ Mi’raj." }
]

# Mengubah data ke JSON string agar bisa dibaca JavaScript
json_data = json.dumps(cards_data)

# ==========================================
# 3. FUNGSI LOAD GAMBAR (BASE64)
# ==========================================
def get_image_base64(image_path):
    """Membaca file gambar lokal dan mengubahnya menjadi string base64."""
    try:
        # Coba ekstensi jpg dan webp
        if not os.path.exists(image_path):
            return None
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        return None

# Sesuaikan nama file logo Anda di sini
logo_filename = "logo_ummul_qura.jpg"  # Atau .jpg sesuai file Anda
logo_base64 = get_image_base64(logo_filename)

logo_src = ""
if logo_base64:
    # Deteksi ekstensi untuk mime type yang benar
    ext = "webp" if logo_filename.endswith("webp") else "jpeg"
    logo_src = f"data:image/{ext};base64,{logo_base64}"

# ==========================================
# 4. APLIKASI WEB (HTML/JS/CSS INJECTION)
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

        /* Container 3D - Animasinya dipisah ke sini */
        .card-container-3d {{
            perspective: 1000px;
            width: 320px;
            height: 520px;
            position: relative;
            transition: transform 0.2s ease-in-out; /* Animasi untuk navigation squeeze */
        }}
        
        /* Class untuk animasi squeeze saat pindah kartu */
        .card-container-3d.squeeze {{
            transform: scale(0.95);
        }}

        /* Inner Card - Khusus untuk Flip */
        .card-inner {{
            width: 100%;
            height: 100%;
            position: relative;
            text-align: center;
            transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            transform-style: preserve-3d;
            cursor: pointer;
        }}

        .card-inner.flipped {{
            transform: rotateY(180deg);
        }}

        .card-face {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            -webkit-backface-visibility: hidden; backface-visibility: hidden;
            border-radius: 1.5rem;
            display: flex; flex-direction: column;
            padding: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .card-front {{
            background-color: white; color: #1f2937; border: 1px solid #e5e7eb; z-index: 2;
        }}

        .card-back {{
            background-color: #4338ca; color: white; transform: rotateY(180deg); border: 1px solid #3730a3; z-index: 1;
        }}

        .scrollbar-hide::-webkit-scrollbar {{ display: none; }}
        .scrollbar-hide {{ -ms-overflow-style: none; scrollbar-width: none; }}

        .nav-btn {{ transition: all 0.2s; }}
        .nav-btn:active {{ transform: scale(0.95); }}
    </style>
</head>
<body>

    <div class="flex flex-col items-center gap-6 w-full">
        
        <div class="w-[320px] flex justify-between items-center px-1">
            <div>
                <h1 class="text-lg font-bold text-gray-800">Sirah Nabawiyah</h1>
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

        const cardContainer = document.getElementById('card-container'); // Container untuk animasi Scale
        const cardInner = document.getElementById('flashcard');       // Inner untuk animasi Flip
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

        window.nextCard = (e) => {{
            e.stopPropagation();
            if (currentIndex < cards.length - 1) {{
                changeCard(currentIndex + 1);
            }}
        }};

        window.prevCard = (e) => {{
            e.stopPropagation();
            if (currentIndex > 0) {{
                changeCard(currentIndex - 1);
            }}
        }};

        function changeCard(newIndex) {{
            if (isFlipped) {{
                // Jika kartu sedang terbalik, balikkan dulu
                flipCard(); 
                setTimeout(() => {{ 
                    currentIndex = newIndex; 
                    renderCard(); 
                }}, 300); // Tunggu animasi flip selesai setengah jalan
            }} else {{
                // Jika posisi normal, mainkan animasi "squeeze" pada container
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

