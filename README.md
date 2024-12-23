### **README.md**

# **Kulüp Yönetim Sistemi**

Bu proje, öğrenci kulüplerinin etkinliklerini, üyelerini ve bütçe yönetimlerini kolaylaştırmak için tasarlanmış bir web uygulamasıdır. Flask ile geliştirilen backend, PostgreSQL veritabanı ve Google Cloud üzerinde çalıştırılmak üzere Docker konteyneriyle hazırlanmıştır.

---

## **Proje Özellikleri**

### **1. Kullanıcı Yönetimi**
- **Kayıt ve Giriş:** Kullanıcılar kayıt olabilir ve sisteme giriş yapabilir.
- **Roller:** Sistemde iki farklı kullanıcı rolü bulunmaktadır:
  - **Admin:** Sistemi yönetebilir, etkinlik ekleyebilir ve silebilir.
  - **Üye:** Etkinlikleri görüntüleyebilir.
- **Profil Yönetimi:** Kullanıcılar kendi profillerini görüntüleyebilir ve şifrelerini güncelleyebilir.

### **2. Etkinlik Yönetimi**
- **Etkinlik Ekleme:** Admin kullanıcılar yeni etkinlikler ekleyebilir.
- **Etkinlik Silme:** Admin kullanıcılar etkinlikleri silebilir.
- **Etkinlik Listeleme:** Tüm kullanıcılar etkinlik listesini görüntüleyebilir.


### **4. Belge Yönetimi**
- Kulüp ile ilgili belgeler yüklenebilir ve yönetilebilir.

---

## **Kullanılan Teknolojiler**
- **Backend:** Flask (Python)
- **Veritabanı:** PostgreSQL
- **Frontend:** HTML, CSS
- **Bulut Platformu:** Google Cloud Platform (GCP)
- **Konteynerizasyon:** Docker

---

## **Kurulum ve Çalıştırma**

### **1. Gerekli Araçlar**
- Python 3.10 veya üstü
- PostgreSQL
- Docker
- Google Cloud SDK

### **2. Bağımlılıkların Yüklenmesi**
Proje dizininde aşağıdaki komutları çalıştırarak bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

### **3. Veritabanı Kurulumu**
- `backup.sql` dosyasını PostgreSQL'e yükleyin:
```bash
psql -U postgres -d kulupdb -f backup.sql
```

### **4. Çalıştırma**
- Flask uygulamasını çalıştırmak için aşağıdaki komutu kullanabilirsiniz:
```bash
python app.py
```
- Alternatif olarak, Docker ile çalıştırmak için:
```bash
docker build -t kulup-yonetim-sistemi .
docker run -p 8080:8080 kulup-yonetim-sistemi
```

---

## **Proje Yapısı**

```
├── app.py                 # Ana Flask uygulama dosyası
├── templates/             # HTML şablonları
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── events.html
│   ├── profile.html
│   ├── add_events.html
│   ├── update_password.html
├── static/                # Statik dosyalar (CSS, resimler vb.)
│   ├── css/
│       └── style.css
├── requirements.txt       # Python bağımlılıkları
├── Dockerfile             # Docker yapılandırma dosyası
├── backup.sql             # PostgreSQL veritabanı yedeği
└── README.md              # Proje açıklamaları
```

---

## **Google Cloud Üzerinde Çalıştırma**
1. Projenizi Google Cloud Platform'a yükleyin.
2. Cloud SQL ve Cloud Run hizmetlerini etkinleştirin.
3. `Dockerfile` ve gerekli ortam değişkenlerini kullanarak projeyi çalıştırın.

---

## **Geliştirme**
- Flask modüler yapı kullanılarak geliştirilmiştir.
- PostgreSQL veritabanı tabloları detaylı şekilde yapılandırılmıştır.

---

## **Katkıda Bulunma**
Projeye katkıda bulunmak isterseniz lütfen bir "Pull Request" gönderin veya bir "Issue" açın.

---

## **Lisans**
Bu proje açık kaynaklıdır ve herkes tarafından geliştirilmeye açıktır. Kullanım koşulları için lütfen lisans dosyasını kontrol edin.