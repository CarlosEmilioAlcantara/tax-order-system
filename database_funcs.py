from datetime import datetime
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

    cursor.execute("""
        SELECT id FROM professionals WHERE license_no = ?
    """, (license_no,))
    id = cursor.fetchall()
    id = id[0][0]
    table_name = str(id) + "_" + last_name

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{table_name}' (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_no TEXT,
            receipt_no TEXT,
            type_of_payment TEXT,
            receipt_date TEXT,
            amount TEXT,
            penalty TEXT DEFAULT 'None' NOT NULL
        )
    """)

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

    cursor.execute("""
        SELECT id, last_name FROM professionals WHERE license_no = ?
    """, (license_no,))
    info = cursor.fetchall()
    id = info[0][0]
    last_name = info[0][1]
    table_name = str(id) + "_" + last_name

    cursor.execute(f"DROP TABLE IF EXISTS '{table_name}'")
    cursor.execute(f"DELETE FROM professionals WHERE id = '{id}'")

    conn.commit()
    conn.close()

def get_receipts(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, last_name FROM professionals WHERE license_no = ?
    """, (license_no,))
    info = cursor.fetchall()
    id = info[0][0]
    last_name = info[0][1]
    table_name = str(id) + "_" + last_name

    cursor.execute(f"""
        SELECT 
            license_no, receipt_no, type_of_payment, 
            receipt_date, amount, penalty
        FROM '{table_name}'
    """
    )
    receipts = cursor.fetchall()

    conn.close()

    return receipts

def add_receipt(license_no, receipt_no, type_of_payment, receipt_date, amount):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, last_name FROM professionals WHERE license_no = ?
    """, (license_no,))
    info = cursor.fetchall()
    id = info[0][0]
    last_name = info[0][1]
    table_name = str(id) + "_" + last_name

    year = datetime.now().strftime("%y")
    date1 = datetime.strptime(receipt_date, "%m/%d/%y")
    date2 = datetime.strptime(f"01/31/{year}", "%m/%d/%y")

    if date1 > date2:
        amount = float(amount)
        penalty = amount * 0.30 
        print(penalty)

    # # Check gamit if statement kung meron na new sa penalty column 
    # cursor.execute(f"""
    #     SELECT EXISTS(SELECT 'New' FROM '{table_name}')
    # """)
    # new = cursor.fetchall()

    # if new:
    #     cursor.execute(f"""
    #         INSERT INTO '{table_name}' (
    #             license_no, receipt_no, type_of_payment, receipt_date, 
    #             amount
    #         )
    #         VALUES (
    #             '{license_no}', '{receipt_no}', '{type_of_payment}',
    #             '{receipt_date}', '{amount}'
    #         )
    #     """)
    # else:
    #     penalty = "test"
    #     cursor.execute(f"""
    #         INSERT INTO '{table_name}' (
    #             license_no, receipt_no, type_of_payment, receipt_date, 
    #             amount, penalty
    #         )
    #         VALUES (
    #             '{license_no}', '{receipt_no}', '{type_of_payment}',
    #             '{receipt_date}', '{amount}', '{penalty}'
    #         )
    #     """)

    # conn.commit()
    conn.close()

def detect_newness(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, last_name FROM professionals WHERE license_no = ?
    """, (license_no,))
    info = cursor.fetchall()
    id = info[0][0]
    last_name = info[0][1]
    table_name = str(id) + "_" + last_name

    # Check gamit if statement kung meron na new sa penalty column 
    cursor.execute(f"SELECT count(*) FROM '{table_name}'")

    count = cursor.fetchall()[0][0]

    return count