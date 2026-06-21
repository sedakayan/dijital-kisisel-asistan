# 🎯 Kişisel Dijital Asistan & Üretkenlik Paneli

İleri Programlama dersi dönem sonu final projesi. **Python 3.10+** ve **Streamlit** ile geliştirilmiş; görev ve not takibini, performans analizini ve bir Pomodoro odaklanma sayacını tek bir panelde birleştiren kişisel üretkenlik uygulamasıdır.

---

## 📖 Proje Hakkında

Öğrencilerin ders/ödev/proje gibi sorumluluklarını, kişisel notlarını ve zaman yönetimini tek bir yerden takip edebilmesi amacıyla geliştirilmiştir. Görevler önceliklerine ve son tarihlerine göre kaydedilir, tamamlanma durumu izlenir, yaklaşan teslimler için uyarı verilir ve genel ilerleme grafiklerle görselleştirilir.

## ✨ Özellikler

**1. Görev Yönetimi**
Başlık, açıklama, kategori (Ders/Proje/Kişisel/Spor/İş/Genel), öncelik (Düşük/Orta/Yüksek) ve son tarih bilgisiyle görev eklenir. Görevler "Hepsi / Sadece Bekleyenler / Sadece Tamamlananlar" şeklinde filtrelenebilir; tek tıkla tamamlanabilir veya silinebilir.

**2. Kişisel Notlar**
Başlık, içerik ve kategoriyle not eklenir; her not otomatik zaman damgası alır. Notlar listelenebilir ve silinebilir.

**3. Performans Analizi**
- Görev tamamlama oranı (çubuk grafik)
- Kategorilere göre görev dağılımı (alan grafiği)
- Önceliğe göre görev dağılımı (çubuk grafik)
- Tamamlama yüzdesine göre otomatik verimlilik tavsiyesi mesajı

**4. Pomodoro Sayacı**
1-120 dakika arası ayarlanabilir süreli; başlat / duraklat / sıfırla butonlarıyla kontrol edilen geri sayım sayacı. Süre dolduğunda görsel kutlama efekti gösterir.

**5. Akıllı Hatırlatma Sistemi**
Bugün veya yarın teslim tarihi olan bekleyen görevler için ekranda kırmızı/sarı uyarı gösterilir. `plyer` kütüphanesi kuruluysa aynı uyarı işletim sistemi masaüstü bildirimi olarak da gönderilir (oturum başına bir kez otomatik, istenirse "Bildirim Gönder" butonuyla manuel).

**6. Arka Plan Hatırlatma Servisi**
`app.py` çalıştığında `reminder_service.py` otomatik olarak ayrı bir process olarak başlar. Bu servis veritabanını 3 saatte bir kontrol eder, bugün/yarın teslim olan görev varsa masaüstü bildirimi gönderir. Bir soket portuna (`45678`) bağlanarak aynı anda yalnızca tek bir kopyasının çalışmasını garanti eder; uygulama kapatılsa bile arka planda çalışmaya devam edebilir.

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
app.py                 → Streamlit arayüzü: sayfa düzeni, 4 sekme (Görevler/Notlar/Analiz/Pomodoro), tüm kullanıcı etkileşimleri
models.py              → Task ve Note sınıfları (veritabanından bağımsız, saf veri modelleri)
database.py            → DatabaseManager sınıfı: SQLite bağlantısı, tablo oluşturma, güvenli CRUD sorguları
services.py            → TaskService ve NoteService sınıfları: doğrulama ve iş mantığı katmanı
reminder_service.py    → Arka planda bağımsız çalışan, periyodik hatırlatma/bildirim scripti
requirements.txt       → Proje bağımlılıkları listesi
pda.db                 → Uygulama ilk çalıştığında otomatik oluşan SQLite veritabanı dosyası
```

**Katman mantığı:** `app.py` doğrudan veritabanıyla konuşmaz; `services.py` üzerinden işlem yapar. `services.py` da `database.py`'deki `DatabaseManager`'ı kullanır. `models.py`'deki `Task`/`Note` sınıfları ise bu üç katman arasında taşınan veri nesneleridir. Bu ayrım, kodun okunabilir ve test edilebilir kalmasını sağlar.

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

Tarayıcıda otomatik olarak `http://localhost:8501` açılır. İlk çalıştırmada `pda.db` dosyası oluşturulur ve birkaç örnek görev/not otomatik eklenir (tablo boşsa). `reminder_service.py` ayrıca elle de çalıştırılabilir:

```bash
python reminder_service.py
```

## 🏗 Sınıf Tasarımı (OOP)

**`Task`** (models.py)
Attribute'lar: `id`, `title`, `description`, `category`, `due_date`, `priority`, `status`
Metotlar: `to_dict()` — sözlüğe çevirir; `from_row(row)` *(statik)* — SQLite satırından nesne üretir.

**`Note`** (models.py)
Attribute'lar: `id`, `title`, `content`, `category`, `created_at`
Metotlar: `to_dict()`, `from_row(row)` *(statik)*

**`DatabaseManager`** (database.py)
Tüm SQLite işlemlerini kapsülleyen veri erişim katmanı. `execute_non_query()` (INSERT/UPDATE/DELETE), `fetch_all()`, `fetch_one()` metotlarıyla çalışır; her sorgu `try/except` ile korunur, hata durumunda program çökmez.

**`TaskService` / `NoteService`** (services.py)
`DatabaseManager` nesnesini kullanarak ekleme öncesi doğrulama (örn. boş başlık reddedilir) ve iş kurallarını uygular; `add_task`, `get_all_tasks`, `get_pending_tasks`, `complete_task`, `delete_task`, `get_tasks_due_today/tomorrow` gibi metotları içerir.

## 🗄 Veritabanı Şeması

**`tasks`**: id (PK), title, description, category, due_date, priority, status (varsayılan: "Bekliyor")
**`notes`**: id (PK), title, content, category, created_at

## 💡 Olası Geliştirmeler

- Görev/not düzenleme (update) özelliği
- JSON/CSV olarak dışa aktarma
- Harici bir API entegrasyonu (örn. günlük motivasyon sözü)
- Çoklu kullanıcı desteği
