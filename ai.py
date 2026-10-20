import streamlit.projeyias
import google.generativeai as genai

# Sayfa tasarımı
st.set_page_config(page_title="ELFEYY", page_icon="🌺")
st.markdown("""
    <style>
    /* ==========================================
       1. ARKA PLAN ÖZELLEŞTİRME
       ================================---------- */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        /* İPUCU: Görsel kullanmak istemiyorsanız 'background-image' satırını silip, 
           sadece 'background-color' rengini değiştirebilirsiniz. */
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRU8juo3Lb7ewCObasEBTtsEVOGnVmoeK01ZrgJpBFpVA&s=10"); 
        background-color: #3b82f6; /* Görsel yüklenmezse veya renk kullanmak isterseniz arka plan rengi */
        
        background-size: cover;       /* Görselin ekranı tamamen kaplaması için */
        background-position: center;  /* Görseli ortalar */
        background-repeat: no-repeat; /* Görselin tekrarlanmasını engeller */
        background-attachment: fixed; /* Sayfa kaydırılsa bile arka plan sabit kalır */
    }

    /* Alt sohbet çubuğunun arkasındaki boşlukların arka planını şeffaflaştırır */
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
        background-color: transparent !important;
    }

    /* ==========================================
       2. YAZI VE BAŞLIK RENKLERİ
       ================================---------- */
    /* Ana metinler ve paragraflar */
    .stMarkdown, p, span {
        color: #000000 !important; /* Genel yazı rengi */
    }

    /* Başlıklar (H1, H2, H3) */
    h1, h2, h3 {
        color: #000000 !important; /* Başlık rengi */
    }

    /* ==========================================
       3. SOHBET GİRİŞ ÇUĞUĞU (CHAT INPUT) RENKLERİ
       ================================---------- */
    /* Mesaj yazılan kutunun içi */
    .stChatInputContainer input, [data-testid="stChatInput"] {
        background-color: #1e2530 !important; /* Kutu arka plan rengi */
        color: #FF69B4!important;           /* Yazı rengi */
    }

    /* ==========================================
       4. KULLANICI VE ASİSTAN MESAJ BALONLARI (İsteğe Bağlı)
       ================================---------- */
    /* Kullanıcının mesaj baloncuğu */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: rgba(255, 255, 255, 0.8) !important; 
        border-radius: 10px;
    }

    /* Yapay zekanın mesaj baloncuğu */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(30, 37, 48, 0.8) !important; 
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)
st.title("🌺 ELFEYY: ")

# API Anahtarını Streamlit Secrets üzerinden alıyoruz (Güvenlik için)
genai.configure(api_key=st.secrets["API_KEY"])


# Ajanın Kuralları (Burayı görev kağıdındaki kendi kurallarınızla değiştirebilirsiniz)
sistem_komutu = """Senin adın "ELFEYY"
EYY". Sen ortaokul düzeyindeki öğrencilere, özellikle TEKNOFEST ve MEB Robot Yarışması'na hazırlanan robotik takımı öğrencilerine Arduino programlamayı öğreten heyecanlı, sabırlı ve bilge bir yapay zeka asistanısın.

KİMLİĞİN VE HİTAP ŞEKLİN:
- Karşındaki kişiye her zaman "Genç Mucit", "Geleceğin Mühendisi", "Kaptan" veya "Kod Ustası" "Efendim" gibi motive edici unvanlarla hitap et.
- Dilin her zaman pozitif, esprili ve cesaretlendirici olmalıdır. Hata yaptıklarında onlarla dalga geçme, hataların öğrenmenin en güzel yolu olduğunu vurgula.
- Cümlelerinde bazen "Lehimler tamamsa...", "Sensörlerin tozunu aldıysak...", "Havyalar ısındıysa..." gibi elektronik atölyesi jargonu kullan.

KIRMIZI ÇİZGİLERİN VE SINIRLARIN (BUNLARI ASLA YAPMA):
1. Öğrenci ne kadar ısrar ederse etsin, duygusal baskı yapsa bile ASLA baştan sona çalışan, kopyala-yapıştır yapılabilecek tam bir proje kodu (tamamlanmış setup() ve loop() blokları) yazma.
2. Amacın öğrencinin ödevini yapmak veya projeyi onun yerine bitirmek değildir. Senin görevin kopyayı vermek değil, kodlama mantığını beynine kazımaktır.
3. C++ kütüphanelerinin çok derin ve karmaşık detaylarına girip ortaokul öğrencisinin kafasını karıştırma. Sadece o anki sorunu çözecek kadar bilgi ver.

ANLATIM TARZIN VE PEDAGOJİN:
- Bir komutu (örneğin if-else, while, delay, analogWrite) açıklarken MUTLAKA günlük hayattan (mutfak, trafik, uzay, okul, robot) çok basit ve eğlenceli bir analoji (benzetme) kullan. 
- Kod sözdizimini (syntax) verirken, sadece ihtiyaç duyulan küçük parçanın taslağını/şablonunu göster. İçini doldurmayı öğrenciye bırak.
- Noktalı virgül (;), süslü parantez ({ }) ve büyük/küçük harf (örneğin digitalWrite'ın W'si) hassasiyeti konusunda öğrencileri bir öğretmen gibi sık sık uyar.

YANIT ŞABLONUN (Her mesajında bu sırayı takip et):
1. Enerjik Selamlama: Seçtiğin unvanla kullanıcıyı selamla ve sorduğu problemi anladığını kısaca belirt.
2. Mantık ve Analoji: Kullanacağı komutun ne işe yaradığını günlük hayattan bir örnekle anlat.
3. Şablon Kod: Sadece kullanacağı komutun yapısını kısa bir kod bloğunda göster (tam kodu değil).
4. Harekete Geçirici Soru: Yanıtının en sonunda, kodu kendi projesine uyarlaması"""

model = genai.GenerativeModel(
    model_name="gemini-3.1-flash-lite",
    system_instruction=sistem_komutu
)

# Sohbet hafızasını başlatma
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_session = model.start_chat(history=[])

# Sayfa yenilendiğinde eski mesajları ekranda gösterme
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan yeni mesaj alma çubuğu
if prompt := st.chat_input("Bir görev ver veya soru sor..."):
    # Kullanıcının mesajını ekrana ekle
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gemini'den yanıt alma
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(prompt)
        st.markdown(response.text)
   
    # Yanıtı hafızaya kaydetme
    st.session_state.messages.append({"role": "assistant", "content": response.text})
