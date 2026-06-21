# 🎯 Kişisel Dijital Asistan & Üretkenlik Paneli

İleri Programlama dersi dönem sonu final projesi. **Python 3.10+** ve **Streamlit** ile geliştirilmiş; kullanıcı girişi destekli, görev ve not takibini, performans analizini ve bir Pomodoro odaklanma sayacını tek bir panelde birleştiren kişisel üretkenlik uygulamasıdır.

---

## 📖 Proje Hakkında

Öğrencilerin ders/ödev/proje gibi sorumluluklarını, kişisel notlarını ve zaman yönetimini tek bir yerden takip edebilmesi amacıyla geliştirilmiştir. Her kullanıcı kendi hesabıyla giriş yapar; görevler ve notlar yalnızca o kullanıcıya özeldir, başka kullanıcılar tarafından görülemez veya değiştirilemez.

## ✨ Özellikler

**1. Kullanıcı Girişi ve Kayıt**
Uygulama açıldığında karşılayan ilk ekran giriş/kayıt formudur. Yeni kullanıcılar "Kayıt Ol" sekmesinden kullanıcı adı ve şifreyle hesap oluşturur, ardından "Giriş Yap" sekmesinden sisteme girer. Giriş yapılmadan dashboard, görevler, notlar gibi hiçbir bölüm görüntülenmez. Sidebar'da giriş yapan kullanıcının adı gösterilir ve "Çıkış Yap" butonuyla oturum kapatılabilir.

**2. Görev Yönetimi**
Başlık, açıklama, kategori (Ders/Proje/Kişisel/Spor/İş/Genel), öncelik (Düşük/Orta/Yüksek) ve son tarih bilgisiyle görev eklenir. Görevler "Hepsi / Sadece Bekleyenler / Sadece Tamamlananlar" şeklinde filtrelenebilir; tek tıkla tamamlanabilir veya silinebilir. Tüm bu işlemler yalnızca o anda giriş yapmış kullanıcının kendi görevleri üzerinde geçerlidir.

**3. Kişisel Notlar**
Başlık, içerik ve kategoriyle not eklenir; her not otomatik zaman damgası alır. Notlar listelenebilir ve silinebilir; her kullanıcı yalnızca kendi notlarını görür.

**4. Performans Analizi**
- Görev tamamlama oranı (çubuk grafik)
- Kategorilere göre görev dağılımı (alan grafiği)
- Önceliğe göre görev dağılımı (çubuk grafik)
- Tamamlama yüzdesine göre otomatik verimlilik tavsiyesi mesajı

**5. Pomodoro Sayacı**
1-120 dakika arası ayarlanabilir süreli; başlat / duraklat / sıfırla butonlarıyla kontrol edilen geri sayım sayacı. Süre dolduğunda görsel kutlama efekti gösterir.

**6. Akıllı Hatırlatma Sistemi**
Bugün veya yarın teslim tarihi olan bekleyen görevler için ekranda kırmızı/sarı uyarı gösterilir. `plyer` kütüphanesi kuruluysa aynı uyarı işletim sistemi masaüstü bildirimi olarak da gönderilir.

**7. Arka Plan Hatırlatma Servisi**
`app.py` çalıştığında `reminder_service.py` otomatik olarak ayrı bir process olarak başlar. Bu servis veritabanını 3 saatte bir kontrol eder, bugün/yarın teslim olan görev varsa masaüstü bildirimi gönderir.

## 🛠 Kullanılan Teknolojiler

| Bileşen | Teknoloji |
|---|---|
| Dil | Python 3.10+ |
| Arayüz | Streamlit |
| Veritabanı | SQLite (`sqlite3` standart kütüphanesi) |
| Veri/grafik | pandas, Streamlit'in yerleşik grafik bileşenleri |
| Masaüstü bildirimi | plyer *(opsiyonel — kurulu değilse uygulama yine çalışır, sadece bildirim gönderilmez)* |
| Loglama | logging standart kütüphanesi |

## 📂 Dosya Yapısı ve Görevleri

```
app.py                 → Streamlit arayüzü: giriş/kayıt ekranı, sidebar, dashboard, 4 sekme
models.py              → Task ve Note sınıfları (veritabanından bağımsız veri modelleri)
database.py            → DatabaseManager: SQLite bağlantısı, users/tasks/notes tabloları
services.py            → TaskService, NoteService, AuthService: iş mantığı ve kimlik doğrulama
reminder_service.py    → Arka planda çalışan hatırlatma servisi
requirements.txt       → Bağımlılıklar (streamlit, pandas, plyer)
.streamlit/config.toml → Arayüz tema ayarları (renkler, açık tema)
pda.db                 → Uygulama ilk çalıştığında otomatik oluşan SQLite veritabanı dosyası
```

**Katman mantığı:** `app.py` doğrudan veritabanıyla konuşmaz; `services.py` üzerinden işlem yapar. `services.py` da `database.py`'deki `DatabaseManager`'ı kullanır. Her görev/not işlemi, giriş yapan kullanıcının adını (`username`) parametre olarak taşır; bu sayede bir kullanıcı başka bir kullanıcının verisine asla erişemez.

## ⚙️ Kurulum

```bash
# (Önerilir) sanal ortam oluştur
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# bağımlılıkları yükle
pip install -r requirements.txt
```

## ▶️ Çalıştırma

```bash
streamlit run app.py
```

Tarayıcıda otomatik olarak `http://localhost:8501` açılır.

1. İlk açılışta karşına **Giriş Yap / Kayıt Ol** ekranı gelir.
2. **Kayıt Ol** sekmesinden bir kullanıcı adı ve şifre belirleyip hesap oluştur.
3. **Giriş Yap** sekmesinden aynı bilgilerle giriş yap.
4. Giriş yaptıktan sonra dashboard ve tüm sekmeler (Görevler, Notlar, Analiz, Pomodoro) açılır; eklediğin her görev/not yalnızca senin hesabına kaydedilir.

İlk çalıştırmada `pda.db` dosyası otomatik oluşturulur. `reminder_service.py` ayrıca elle de çalıştırılabilir:

```bash
python reminder_service.py
```

## 🏗 Sınıf Tasarımı (OOP)

**`Task`** (models.py)
Attribute'lar: `id`, `title`, `description`, `category`, `due_date`, `priority`, `status`
Metotlar: `to_dict()`, `from_row(row)` *(statik)*

**`Note`** (models.py)
Attribute'lar: `id`, `title`, `content`, `category`, `created_at`
Metotlar: `to_dict()`, `from_row(row)` *(statik)*

**`DatabaseManager`** (database.py)
Tüm SQLite işlemlerini kapsülleyen veri erişim katmanı. `execute_non_query()`, `fetch_all()`, `fetch_one()` metotlarıyla çalışır; her sorgu `try/except` ile korunur.

**`TaskService` / `NoteService`** (services.py)
`DatabaseManager` nesnesini kullanarak doğrulama ve iş kurallarını uygular. Her metot bir `username` parametresi alır ve sorguları o kullanıcıyla sınırlar (`WHERE username = ?`).

**`AuthService`** (services.py)
`register(username, password)` ile yeni hesap oluşturur, `login(username, password)` ile giriş bilgilerini doğrular. *(Not: şifreler bu projede düz metin olarak saklanır; bu, bir okul projesi için kabul edilebilir, gerçek bir üretim uygulamasında hash'lenmesi gerekir.)*

## 🗄 Veritabanı Şeması

**`users`**: id (PK), username (UNIQUE), password
**`tasks`**: id (PK), username, title, description, category, due_date, priority, status (varsayılan: "Bekliyor")
**`notes`**: id (PK), username, title, content, category, created_at

## 💡 Olası Geliştirmeler

- Görev/not düzenleme (update) özelliği
- Şifrelerin hash'lenerek saklanması (örn. bcrypt)
- JSON/CSV olarak dışa aktarma
- Harici bir API entegrasyonu (örn. günlük motivasyon sözü)
