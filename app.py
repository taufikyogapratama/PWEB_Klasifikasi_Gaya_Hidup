from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="klasifikasi"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def get_questions(cursor):
    cursor.execute("SELECT ID_Pertanyaan, Kategori, Teks_Pertanyaan FROM pertanyaan")
    return cursor.fetchall()

def classify_answers(cursor, answers):
    results = {'Sehat': [], 'Tidak Sehat': []}
    categories = {'Sehat': [], 'Tidak Sehat': []}

    for id_pertanyaan, jawaban in answers.items():
        cursor.execute(
            """
            SELECT Kondisi, Hasil_Klasifikasi, Nasihat, Kategori 
            FROM aturan 
            JOIN pertanyaan ON aturan.ID_Pertanyaan = pertanyaan.ID_Pertanyaan 
            WHERE pertanyaan.ID_Pertanyaan = %s AND (
                (Kondisi LIKE '>= %' AND %s >= CAST(SUBSTRING(Kondisi, 4) AS SIGNED)) 
                OR (Kondisi LIKE '<= %' AND %s <= CAST(SUBSTRING(Kondisi, 4) AS SIGNED)) 
                OR (Kondisi LIKE '> %' AND %s > CAST(SUBSTRING(Kondisi, 3) AS SIGNED)) 
                OR (Kondisi LIKE '< %' AND %s < CAST(SUBSTRING(Kondisi, 3) AS SIGNED))
            )
            """,
            (id_pertanyaan, jawaban, jawaban, jawaban, jawaban)
        )

        result = cursor.fetchone()
        if result:
            condition, result_class, advice, category = result
            results[result_class].append((category, result_class, advice))
            categories[result_class].append(category)

    return results, categories

@app.route("/input_biodata")
def input_biodata():
    return render_template("input_biodata.html")

@app.route("/save_biodata", methods=["POST"])
def save_biodata():
    nama = request.form.get("nama")
    umur = request.form.get("umur")
    berat_badan = request.form.get("berat_badan")
    tinggi_badan = request.form.get("tinggi_badan")
    
    session['biodata'] = {
        'nama': nama,
        'umur': int(umur),
        'berat_badan': float(berat_badan),
        'tinggi_badan': float(tinggi_badan),
    }
    
    return redirect("/input_lifestyle")

@app.route('/input_lifestyle', methods=['GET', 'POST'])
def input_lifestyle():
    conn = connect_to_database()
    if conn is None:
        return "Database connection error", 500
    cursor = conn.cursor()

    questions = get_questions(cursor)
    
    if request.method == 'POST':
        answers = {}
        for question in questions:
            id_pertanyaan = question[0]
            answers[id_pertanyaan] = int(request.form.get(str(id_pertanyaan)))

        classifications, categories = classify_answers(cursor, answers)

        cursor.execute(
            "INSERT INTO hasil (Nama, Umur, Berat_Badan, Tinggi_Badan, Olahraga, Tidur, Stres, Makanan, Hidrasi) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                session['nama'], session['umur'], session['berat_badan'], session['tinggi_badan'],
                categories['Sehat'][0] if 'Sehat' in categories and len(categories['Sehat']) > 0 else 'Tidak Sehat',
                categories['Tidak Sehat'][0] if 'Tidak Sehat' in categories and len(categories['Tidak Sehat']) > 0 else 'Sehat',
                None, None, None
            )
        )
        conn.commit()

        return render_template(
            'hasil.html', classifications=classifications, categories=categories
        )

    return render_template('input_lifestyle.html', questions=questions)

@app.route('/admin')
def admin():
    conn = connect_to_database()
    if conn is None:
        return "Database connection error", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hasil")
    results = cursor.fetchall()
    return render_template('admin.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
