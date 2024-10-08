from datetime import datetime
import sqlite3
import time

DATABASE_FILE = "professional_tax_order_records.db"

def initialize_database():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professionals(
                professional_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def get_table_name(cursor, license_no):
    cursor.execute("""
        SELECT last_name 
        FROM professionals 
        WHERE license_no = ?
    """, (license_no,))
    info = cursor.fetchall()
    last_name = info[0][0]
    table_name = license_no + "_" + last_name

    return table_name

def create_table_name(new_license_no, last_name):
    new_table_name = new_license_no + "_" + last_name

    return new_table_name

def check_license_no(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT license_no 
        FROM professionals 
        WHERE license_no 
            = '{license_no}'
    """
    )

    checking = cursor.fetchone()
    conn.close()

    return checking

def check_na_iteration(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT 
            COUNT(license_no)
        FROM professionals
        WHERE license_no
            LIKE '%{license_no}%'
    """
    )

    result = cursor.fetchone()
    count = result[0] + 1

    conn.close()

    return count

def check_receipt_no(license_no, receipt_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"""
        SELECT receipt_no
        FROM '{table_name}' 
        WHERE receipt_no 
            = '{receipt_no}'
    """
    )

    checking = cursor.fetchone()
    conn.close()

    return checking

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
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS '{table_name}' (
            license_no TEXT,
            receipt_no TEXT,
            type_of_payment TEXT,
            receipt_date TEXT,
            amount TEXT,
            penalty TEXT DEFAULT 'None' NOT NULL,
            total_amount TEXT,
            verified_by TEXT
        )
    """)

    conn.commit()
    conn.close()

def change_table_name():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    

def open_record(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * FROM professionals WHERE license_no = '{license_no}'
    """)

    record = cursor.fetchall()
    conn.close()

    return record

def edit_record(professional_id, cur_license_no, new_license_no, last_name, 
                first_name, middle_name, address, profession):
    
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    old_table_name = get_table_name(cursor, cur_license_no)
    new_table_name = create_table_name(new_license_no, last_name)

    try:
        cursor.execute(f"""
            ALTER TABLE '{old_table_name}'
                RENAME TO '{new_table_name}';
        """)
    except sqlite3.Error as e:
        pass

    conn.commit()

    cursor.execute("""
        UPDATE professionals SET license_no = ?, last_name = ?, first_name = ?, 
                   middle_name = ?, address = ?, profession = ?
        WHERE professional_id = ?
    """, (new_license_no, last_name, first_name, middle_name, address, profession,
          professional_id))

    record = cursor.fetchall()

    conn.commit()
    conn.close()

    return record

def delete_record(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"DROP TABLE IF EXISTS '{table_name}'")
    cursor.execute(f"DELETE FROM professionals WHERE license_no = '{license_no}'")

    conn.commit()
    conn.close()

def get_receipts(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"""
        SELECT 
            receipt_no, type_of_payment, 
            receipt_date, amount, penalty,
            total_amount, verified_by
        FROM '{table_name}'
    """
    )
    receipts = cursor.fetchall()

    conn.close()

    return receipts

def detect_newness(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"""SELECT type_of_payment 
                   FROM '{table_name}'
                   WHERE type_of_payment = 'New'""")

    count = cursor.fetchone()
    conn.close()

    return count

def add_receipt(license_no, receipt_no, type_of_payment, receipt_date, amount,
                verified_by):

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    date_arr = receipt_date.split('/')
    date1 = datetime(int(date_arr[2]), int(date_arr[0]), int(date_arr[1]))

    cur_year = str(date1.year)
    date2 = datetime.strptime(f"31/1/{cur_year}", "%d/%m/%Y")

    checking = detect_newness(license_no)
    penalty = "None"
    amount = float(amount)
    total_amount = float(amount)

    if checking and date1 > date2:
        penalty = amount * 0.25 
        total_amount = amount + penalty

        cursor.execute(f"""
            INSERT INTO '{table_name}' (
                license_no, receipt_no, type_of_payment, receipt_date, 
                amount, penalty, total_amount, verified_by
            )
            VALUES (
                '{license_no}', '{receipt_no}', '{type_of_payment}',
                '{receipt_date}', '{"Php " + str(f"{amount:.2f}")}', 
                '{"Php " + str(f"{penalty:.2f}")}', 
                '{"Php " + str(f"{total_amount:.2f}")}', '{verified_by}'
            )
        """)
    else:
        cursor.execute(f"""
            INSERT INTO '{table_name}' (
                license_no, receipt_no, type_of_payment, receipt_date, 
                amount, penalty, total_amount, verified_by
            )
            VALUES (
                '{license_no}', '{receipt_no}', '{type_of_payment}',
                '{receipt_date}', '{"Php " + str(f"{amount:.2f}")}', 
                '{penalty}', '{"Php " + str(f"{total_amount:.2f}")}',
                '{verified_by}'
            )
        """)

    conn.commit()
    conn.close()

def delete_receipt(license_no, receipt_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"DELETE FROM '{table_name}' WHERE receipt_no = '{receipt_no}'")

    conn.commit()
    conn.close()

def edit_receipt(license_no, old_receipt_no, new_receipt_no, type_of_payment, 
                 receipt_date, amount, verified_by):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    date_arr = receipt_date.split('/')
    date1 = datetime(int(date_arr[2]), int(date_arr[0]), int(date_arr[1]))

    cur_year = str(date1.year)
    date2 = datetime.strptime(f"31/1/{cur_year}", "%d/%m/%Y")

    checking = detect_newness(license_no)
    penalty = "None"
    amount = float(amount)
    total_amount = float(amount)

    if checking and date1 > date2:
        penalty = amount * 0.25 
        total_amount = amount + penalty

        cursor.execute(f"""
            UPDATE '{table_name}' 
            SET receipt_no = '{new_receipt_no}',
                type_of_payment = '{type_of_payment}', 
                receipt_date = '{receipt_date}', 
                amount = '{"Php " + str(f"{amount:.2f}")}',
                penalty = '{"Php " + str(f"{penalty:.2f}")}', 
                total_amount = '{"Php " + str(f"{total_amount:.2f}")}',
                verified_by = '{verified_by}'
            WHERE receipt_no = '{old_receipt_no}'
        """)
    else:
        cursor.execute(f"""
            UPDATE '{table_name}' 
            SET receipt_no = '{new_receipt_no}',
                type_of_payment = '{type_of_payment}', 
                receipt_date = '{receipt_date}', 
                amount = '{"Php " + str(f"{amount:.2f}")}',
                penalty = '{penalty}', 
                total_amount = '{"Php " + str(f"{total_amount:.2f}")}',
                verified_by = '{verified_by}'
            WHERE receipt_no = '{old_receipt_no}'
        """)

    conn.commit()
    conn.close()

def search_receipts(license_no, search_term):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"""
        SELECT receipt_no, type_of_payment, receipt_date, amount, penalty, 
               total_amount, verified_by
        FROM '{table_name}' 
        WHERE 
            receipt_no LIKE '%{search_term}%' OR
            type_of_payment LIKE '%{search_term}%' OR
            receipt_date LIKE '%{search_term}%' OR
            amount LIKE '%{search_term}%' OR
            penalty LIKE '%{search_term}%' OR
            total_amount LIKE '%{search_term}%' OR
            verified_by LIKE '%{search_term}%'
    """
    )

    results = cursor.fetchall()
    conn.close()

    return results

def ready_professional(license_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT * 
        FROM professionals 
        WHERE 
            license_no = '{license_no}'
    """
    )

    professional_record = cursor.fetchall()
    conn.close()

    return professional_record

def ready_receipt(license_no, receipt_no):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    table_name = get_table_name(cursor, license_no)

    cursor.execute(f"""
        SELECT * 
        FROM '{table_name}' 
        WHERE 
            receipt_no = '{receipt_no}'
    """
    )

    receipt_record = cursor.fetchall()
    conn.close()

    return receipt_record