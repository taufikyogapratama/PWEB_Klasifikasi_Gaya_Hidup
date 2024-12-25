from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "klasifikasi"
app.config['SECRET_KEY'] = 'kunci_rahasia'

mysql = MySQL(app)

@app.route("/")
def masuk():
    return render_template("masuk.html")

@app.route("/user_biodata")
def user_biodata():
    return render_template("user_biodata.html")

@app.route("/save_user_biodata", methods=['GET', 'POST'])
def save_user_biodata():
    if request.method == "POST":
        nama = request.form['nama']
        umur = request.form['umur']
        berat_badan = request.form['berat_badan']
        tinggi_badan = request.form['tinggi_badan']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (nama_user, umur, berat_badan, tinggi_badan) VALUES (%s, %s, %s, %s)", (nama, umur, berat_badan, tinggi_badan))
        mysql.connection.commit()
        user_id = cur.lastrowid
        session['user_id'] = user_id
        return redirect(url_for("user_lifestyle"))

@app.route("/user_lifestyle")
def user_lifestyle():
    return render_template("user_lifestyle.html")

@app.route("/save_user_lifestyle", methods=['GET', 'POST'])
def save_user_lifestyle():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for("masuk"))
    
    if request.method == "POST":
        olahraga = int(request.form['olahraga'])
        tidur = int(request.form['tidur'])
        stres = int(request.form['stres'])
        makanan = int(request.form['makanan'])
        hidrasi = int(request.form['hidrasi'])

        kategori_olahraga = ""
        kategori_tidur = ""
        kategori_stres = ""
        kategori_makanan = ""
        kategori_hidrasi = ""

        if olahraga >= 3:
            kategori_olahraga = "Bagus"
        else:
            kategori_olahraga = "Kurang"

        if tidur >= 7:
            kategori_tidur = "Bagus"
        else:
            kategori_tidur = "Kurang"

        if stres >= 7:
            kategori_stres = "Buruk"
        else:
            kategori_stres = "Bagus"

        if makanan >= 7:
            kategori_makanan = "Buruk"
        else:
            kategori_makanan = "Bagus"

        if hidrasi >= 8:
            kategori_hidrasi = "Bagus"
        else:
            kategori_hidrasi = "Kurang"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO hasil (id_user, olahraga, tidur, stres, makanan, hidrasi) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, kategori_olahraga, kategori_tidur, kategori_stres, kategori_makanan, kategori_hidrasi))
        mysql.connection.commit()
        return redirect(url_for("hasil"))

@app.route("/hasil")
def hasil():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for("masuk"))
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT olahraga, tidur, stres, makanan, hidrasi FROM hasil WHERE id_user = %s", (user_id,))

    data = cur.fetchone()
    cur.close()
    session.pop('user_id', None)

    if data:
        kesimpulan = []
        
        if data[0] == 'Bagus':
            kesimpulan.append("Aktivitas olahraga Anda sudah bagus")
        else:
            kesimpulan.append("Aktivitas olahraga Anda perlu ditingkatkan")
        

        if data[1] == 'Bagus':
            kesimpulan.append("Waktu tidur Anda sudah cukup")
        else:
            kesimpulan.append("Waktu tidur Anda perlu ditingkatkan")
        

        if data[2] == 'Buruk':
            kesimpulan.append("Stres Anda perlu diperbaiki")
        else:
        
            kesimpulan.append("Stres Anda sudah terkendali")
        
        if data[3] == 'Buruk':
            kesimpulan.append("Jenis makanan Anda perlu diperbaiki")
        else:
            kesimpulan.append("Jenis makanan Anda sudah bagus")
        

        if data[4] == 'Bagus':
            kesimpulan.append("Kebutuhan cairan Anda sudah tercukupi dengan baik")
        else:
            kesimpulan.append("Kebutuhan cairan Anda perlu diperbaiki")

        hasil_kesimpulan = ", ".join(kesimpulan)
        
        return render_template("hasil.html", hasil_kesimpulan=hasil_kesimpulan)
    else:
        return "Data tidak ditemukan", 404

@app.route("/validasi_admin")
def validasi_admin():
    return render_template("validasi_admin.html")

@app.route("/cek_validasi_admin", methods=['GET', 'POST'])
def cek_validasi_admin():
    if request.method == "POST":
        nama = request.form['nama']
        password = request.form['password']

        if nama == "admin lelah" and password == "tugas banyak":
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("masuk"))


@app.route("/admin")
def admin():
    
    cur = mysql.connection.cursor()

    
    cur.execute("""
        SELECT u.nama_user, u.umur, u.berat_badan, u.tinggi_badan, 
               h.olahraga, h.tidur, h.stres, h.makanan, h.hidrasi
        FROM hasil h
        JOIN user u ON h.id_user = u.id_user;
    """)

    
    data = cur.fetchall()

    
    cur.close()

    
    return render_template("admin.html", data=data)

@app.route("/hapus_semua_data", methods=["POST"])
def hapus_semua_data():
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM hasil")
        
        cur.execute("DELETE FROM user")
        
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return f"Terjadi kesalahan: {e}", 500
    finally:
        cur.close()

    return redirect(url_for("admin"))

if __name__ == '__main__':
    app.run(debug=True)