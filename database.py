"""
database.py
Bu modül, SQLite veritabanı işlemlerini ve veri kalıcılığını yönetir.
Tüm işlemler try/except blokları ile çökme önleyici (hata yönetimli) hale getirilmiştir.
"""
import sqlite3
from models import Gorev, Not

DB_NAME = "asistan.db"

def veritabanini_hazirla():
    """Uygulama ilk açıldığında tabloları otomatik oluşturur."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            # Görevler Tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gorevler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    baslik TEXT NOT NULL,
                    aciklama TEXT,
                    durum TEXT NOT NULL,
                    tarih TEXT
                )
            """)
            # Notlar Tablosu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notlar (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    baslik TEXT NOT NULL,
                    icerik TEXT,
                    olusturma_tarihi TEXT
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Veritabanı oluşturulurken hata çıktı: {e}")

# --- GÖREV İŞLEMLERİ ---

def gorev_ekle(gorev: Gorev):
    """Veritabanına yeni bir görev ekler."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gorevler (baslik, aciklama, durum, tarih) VALUES (?, ?, ?, ?)",
                (gorev.baslik, gorev.aciklama, gorev.durum, gorev.tarih)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Görev eklenirken hata: {e}")
        return False

def gorevleri_getir():
    """Veritabanındaki tüm görevleri sınıf nesnesi olarak listeler."""
    gorev_listesi = []
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, baslik, aciklama, durum, tarih FROM gorevler")
            rows = cursor.fetchall()
            for row in rows:
                gorev_listesi.append(Gorev(row[0], row[1], row[2], row[3], row[4]))
    except sqlite3.Error as e:
        print(f"Görevler çekilirken hata: {e}")
    return gorev_listesi

def gorev_durum_guncelle(gorev_id, yeni_durum):
    """Görevin durumunu tamamlandı/tamamlanmadı olarak günceller."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE gorevler SET durum = ? WHERE id = ?", (yeni_durum, gorev_id))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Görev güncellenirken hata: {e}")
        return False

def gorev_sil(gorev_id):
    """Id değerine göre görevi siler."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM gorevler WHERE id = ?", (gorev_id,))
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Görev silinirken hata: {e}")
        return False

# --- NOT İŞLEMLERİ ---

def not_ekle(yeni_not: Not):
    """Veritabanına yeni bir not ekler."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notlar (baslik, icerik, olusturma_tarihi) VALUES (?, ?, ?)",
                (yeni_not.baslik, yeni_not.icerik, yeni_not.olusturma_tarihi)
            )
            conn.commit()
            return True
    except sqlite3.Error as e:
        print(f"Not eklenirken hata: {e}")
        return False

def notlari_getir():
    """Veritabanındaki tüm notları sınıf nesnesi olarak listeler."""
    not_listesi = []
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, baslik, icerik, olusturma_tarihi FROM notlar")
            rows = cursor.fetchall()
            for row in rows:
                not_listesi.append(Not(row[0], row[1], row[2], row[3]))
    except sqlite3.Error as e:
        print(f"Notlar çekilirken hata: {e}")
    return not_listesi