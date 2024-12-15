import mysql.connector

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
    cursor.execute("SELECT ID_Pertanyaan, Kategori, Teks_Pertanyaan FROM Pertanyaan")
    return cursor.fetchall()

def classify_answers(cursor, answers):
    results = {'Sehat': [], 'Tidak Sehat': []}
    categories = {'Sehat': [], 'Tidak Sehat': []}
    
    for id_pertanyaan, jawaban in answers.items():
        cursor.execute("""
            SELECT Kondisi, Hasil_Klasifikasi, Nasihat, Kategori 
            FROM Aturan 
            JOIN Pertanyaan ON Aturan.ID_Pertanyaan = Pertanyaan.ID_Pertanyaan 
            WHERE Pertanyaan.ID_Pertanyaan = %s AND (
                (Kondisi LIKE '>= %' AND %s >= CAST(SUBSTRING(Kondisi, 4) AS SIGNED)) 
                OR (Kondisi LIKE '<= %' AND %s <= CAST(SUBSTRING(Kondisi, 4) AS SIGNED)) 
                OR (Kondisi LIKE '> %' AND %s > CAST(SUBSTRING(Kondisi, 3) AS SIGNED)) 
                OR (Kondisi LIKE '< %' AND %s < CAST(SUBSTRING(Kondisi, 3) AS SIGNED))
            )
        """, (id_pertanyaan, jawaban, jawaban, jawaban, jawaban))
        
        result = cursor.fetchone()
        if result:
            condition, result_class, advice, category = result
            results[result_class].append((category, result_class, advice))
            categories[result_class].append(category)
    return results, categories

def main():
    conn = connect_to_database()
    if conn is None:
        return
    cursor = conn.cursor()

    questions = get_questions(cursor)
    print("Jawab pertanyaan berikut:")
    answers = {}

    for id_pertanyaan, kategori, teks_pertanyaan in questions:
        jawaban = input(f"{teks_pertanyaan} (jawab angka): ")
        answers[id_pertanyaan] = int(jawaban)

    classifications, categories = classify_answers(cursor, answers)

    print("\nHasil Klasifikasi Gaya Hidup Anda:")
    sehat = "Sehat" in categories and len(categories["Sehat"]) > 0
    tidak_sehat = "Tidak Sehat" in categories and len(categories["Tidak Sehat"]) > 0
    
    for status, entries in classifications.items():
        for category, result_class, advice in entries:
            print(f"- Kategori {category}: {result_class}")
            print(f"  Nasihat: {advice}")
    
    if sehat and tidak_sehat:
        sehat_categories = ', '.join(categories["Sehat"])
        tidak_sehat_categories = ', '.join(categories["Tidak Sehat"])
        print(f"\nPola {sehat_categories} anda sudah baik, namun {tidak_sehat_categories} harus diperbaiki lagi.")
    elif sehat:
        sehat_categories = ', '.join(categories["Sehat"])
        print(f"\nPola {sehat_categories} anda sudah baik, terus pertahankan!")
    else:
        tidak_sehat_categories = ', '.join(categories["Tidak Sehat"])
        print(f"\nPola {tidak_sehat_categories} perlu perbaikan, perhatikan nasihat yang diberikan untuk meningkatkan kesehatan Anda.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

