import select  # Sistem seviyesinde giriş/çıkış işlemleri için kullanılır.
from flask import Flask, render_template, request, redirect, url_for, session  # Flask kütüphanesinden gerekli modüller.
import psycopg2  # PostgreSQL veritabanı bağlantısı için gerekli modül.
from datetime import datetime, timedelta  # Tarih ve zaman işlemleri için.
import os  # Ortam değişkenlerini okumak ve yönetmek için.

# Flask uygulamasını başlatıyoruz.
app = Flask(__name__)
# Uygulama için gizli anahtar tanımlıyoruz (Oturumları güvenli hale getirmek için gerekli).
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')
# Oturum süresi, 30 dakika olarak belirleniyor.
app.permanent_session_lifetime = timedelta(minutes=30)

# PostgreSQL veritabanına bağlantı kuruyoruz.
conn = psycopg2.connect(
    dbname="kulupdb",  # Veritabanı adı.
    user="postgres",  # Veritabanı kullanıcı adı.
    password="123",  # Veritabanı kullanıcı şifresi.
    host="/cloudsql/bulut-445110:europe-west1:my-sql-instance"  # Cloud SQL bağlantı adresi.
)

# Ana sayfaya gelen istekleri yönlendiriyoruz.
@app.route('/')
def home():
    # Kullanıcıyı doğrudan kayıt olma sayfasına yönlendiriyoruz.
    return redirect(url_for('register'))

# Kullanıcı kaydı için rota.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Eğer istek yöntemi POST ise:
        # Formdan gelen verileri alıyoruz.
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']  # Kullanıcının rolü (örneğin: "admin" veya "member").

        # Kullanıcı verilerini veritabanına ekliyoruz.
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, username, password, role) VALUES (%s, %s, %s, %s)",
            (email, username, password, role)
        )
        conn.commit()  # Veritabanına değişiklikleri kaydediyoruz.
        cur.close()  # Cursor'ı kapatıyoruz.
        return redirect(url_for('login'))  # Kayıt tamamlandığında giriş sayfasına yönlendiriyoruz.
    return render_template('register.html')  # GET isteğinde kayıt formunu gösteriyoruz.

# Kullanıcı girişi için rota.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Eğer istek yöntemi POST ise:
        # Formdan gelen giriş bilgilerini alıyoruz.
        email = request.form['email']
        password = request.form['password']

        # Veritabanında kullanıcıyı kontrol ediyoruz.
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        user = cur.fetchone()  # Sorgu sonucunda ilk kullanıcıyı alıyoruz.
        cur.close()  # Cursor'ı kapatıyoruz.

        if user:  # Kullanıcı bulunursa:
            # Kullanıcı bilgilerini oturuma kaydediyoruz.
            session['username'] = user[2]  # Kullanıcı adı.
            session['role'] = user[4]  # Kullanıcı rolü.
            return redirect(url_for('dashboard'))  # Kullanıcıyı panele yönlendiriyoruz.
        return "Login failed! Check your credentials."  # Giriş başarısız olursa hata mesajı.
    return render_template('login.html')  # GET isteğinde giriş formunu gösteriyoruz.

# Kullanıcı profili için rota.
@app.route('/profile')
def profile():
    if 'username' in session:  # Eğer oturum açık ise:
        current_user = session['username']  # Oturumdaki kullanıcı adını alıyoruz.

        cur = conn.cursor()
        cur.execute(
            "SELECT username, email, password FROM users WHERE username = %s",
            (current_user,)
        )
        user_info = cur.fetchone()  # Kullanıcı bilgilerini alıyoruz.
        cur.close()

        if user_info:  # Kullanıcı bilgileri varsa:
            username, email, password = user_info
            return render_template(
                'profile.html',
                username=username,
                email=email,
                password=password
            )
        else:
            return "Kullanıcı bulunamadı!"  # Kullanıcı bilgisi yoksa hata mesajı.
    return redirect(url_for('login'))  # Oturum yoksa giriş sayfasına yönlendir.

# Şifre güncelleme için rota.
@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if 'username' in session:  # Eğer oturum açık ise:
        if request.method == 'POST':  # Eğer istek yöntemi POST ise:
            # Formdan gelen mevcut ve yeni şifre bilgilerini alıyoruz.
            current_password = request.form['current_password']
            new_password = request.form['new_password']

            cur = conn.cursor()
            cur.execute(
                "SELECT password FROM users WHERE username = %s",
                (session['username'],)
            )
            stored_password = cur.fetchone()[0]  # Veritabanındaki mevcut şifreyi alıyoruz.

            if stored_password == current_password:  # Mevcut şifre doğru ise:
                cur.execute(
                    "UPDATE users SET password = %s WHERE username = %s",
                    (new_password, session['username'])
                )
                conn.commit()  # Değişiklikleri kaydediyoruz.
                cur.close()
                return redirect(url_for('profile'))  # Kullanıcıyı profil sayfasına yönlendiriyoruz.
            cur.close()
            return "Current password is incorrect."  # Şifre yanlışsa hata mesajı.
        return render_template('update_password.html')  # GET isteğinde şifre güncelleme formunu gösteriyoruz.
    return redirect(url_for('login'))  # Oturum yoksa giriş sayfasına yönlendir.

# Kullanıcı paneli için rota.
@app.route('/dashboard')
def dashboard():
    if 'username' in session:  # Eğer oturum açık ise:
        username = session['username']  # Kullanıcı adı.
        role = session['role']  # Kullanıcı rolü.

        cur = conn.cursor()
        cur.execute("SELECT username, email FROM users")  # Tüm kullanıcı bilgilerini alıyoruz.
        members = cur.fetchall()  # Tüm kullanıcıları liste olarak alıyoruz.
        cur.close()

        return render_template('dashboard.html', username=username, role=role, members=members)  # Panel sayfasını gösteriyoruz.
    return redirect(url_for('login'))  # Oturum yoksa giriş sayfasına yönlendir.

# Etkinlik listeleme için rota.
@app.route('/events')
def events():
    try:
        cur = conn.cursor()
        cur.execute("SELECT title, description, event_date, id FROM events")  # Etkinlikleri veritabanından çekiyoruz.
        events = cur.fetchall()
        cur.close()

        # Etkinlik tarihlerini düzenli bir formatta dönüştürüyoruz.
        formatted_events = [
            {
                'title': event[0],
                'description': event[1],
                'event_date': datetime.strftime(event[2], "%d/%m/%Y"),
                'id': event[3]
            }
            for event in events
        ]

        role = session.get('role', 'guest')  # Oturumdaki rolü alıyoruz.
        return render_template('events.html', events=formatted_events, role=role)  # Etkinlik sayfasını gösteriyoruz.
    except Exception as e:
        return f"Error: {str(e)}"  # Hata olursa hata mesajı döndürüyoruz.

# Etkinlik ekleme için rota.
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if 'username' in session and session['role'] == 'admin':  # Sadece admin kullanıcılar etkinlik ekleyebilir.
        if request.method == 'POST':  # Eğer istek yöntemi POST ise:
            try:
                # Formdan gelen etkinlik bilgilerini alıyoruz.
                title = request.form['title']
                description = request.form['description']
                event_date = request.form['event_date']

                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO events (title, description, event_date) VALUES (%s, %s, %s)",
                    (title, description, event_date)
                )
                conn.commit()  # Veritabanına değişiklikleri kaydediyoruz.
                cur.close()

                return redirect(url_for('events'))  # Başarılı ise etkinlik sayfasına yönlendiriyoruz.
            except Exception as e:
                return f"Error while adding event: {str(e)}"  # Hata mesajı döndürüyoruz.

        return render_template('add_events.html')  # GET isteğinde etkinlik ekleme formunu gösteriyoruz.
    return redirect(url_for('login'))  # Yetki yoksa giriş sayfasına yönlendir.

# Etkinlik silme için rota.
@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    if 'username' in session and session['role'] == 'admin':  # Sadece admin kullanıcılar etkinlik silebilir.
        cur = conn.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", (event_id,))  # Belirtilen etkinliği siliyoruz.
        conn.commit()
        cur.close()

        return redirect(url_for('events'))  # Silme işlemi tamamlandığında etkinlik sayfasına yönlendiriyoruz.
    return redirect(url_for('login'))  # Yetki yoksa giriş sayfasına yönlendir.

# Kullanıcı çıkışı için rota.
@app.route('/logout')
def logout():
    session.clear()  # Tüm oturum bilgilerini temizliyoruz.
    return redirect(url_for('login'))  # Kullanıcıyı giriş sayfasına yönlendiriyoruz.

# Uygulamayı çalıştırıyoruz.
if __name__ == '__main__':
    app.run(debug=True, host="/cloudsql/bulut-445110:europe-west1:my-sql-instance", port=8080)
