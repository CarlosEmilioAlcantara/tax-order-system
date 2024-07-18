import sqlite3

DATABASE_FILE = "professional_tax_order_records.db"

def initialize_database():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professionals(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_no TEXT,
                last_name TEXT,
                first_name TEXT,
                middle_name TEXT,
                address TEXT,
                profession TEXT
            )
        """)

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error occurred: {e}")

def get_license_numbers():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT license_no FROM professionals")
    license_numbers = cursor.fetchall()

    conn.close()

    return license_numbers

def search_license_numbers(search_number):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT license_no 
        FROM professionals 
        WHERE license_no 
            LIKE '%{search_number}%'
    """
    )

    results = cursor.fetchall()
    conn.close()

    return results

def add_record(license_no, last_name, first_name, middle_name, address, 
               profession):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO professionals (license_no, last_name, first_name, middle_name, address, profession)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (license_no, last_name, first_name, middle_name, address, profession))

    conn.commit()
    conn.close()

def open_record(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM professionals WHERE license_no = {license_no}
    """)

    record = cursor.fetchall()
    conn.close()

    return record

def edit_record(license_no, last_name, first_name, middle_name, address, 
                profession):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE professionals SET last_name = ?, first_name = ?, middle_name = ?,
                   address = ?, profession = ?
        WHERE license_no = ?
    """, (last_name, first_name, middle_name, address, profession, license_no))

    # cursor.execute(f"""
    #     UPDATE professionals 
    #     SET 
    #         last_name = {last_name}, 
    #         first_name = {first_name},
    #         middle_name = {middle_name},
    #         address = {address},
    #         profession = {profession}
    #     WHERE
    #         license_no = {license_no}
    # """)
    record = cursor.fetchall()

    conn.commit()
    conn.close()

    return record

def delete_record(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""DELETE FROM professionals WHERE license_no = ?""",
                   (license_no,))

    conn.commit()
    conn.close()