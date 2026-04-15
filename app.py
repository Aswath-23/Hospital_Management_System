import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aswath@23*",   # 🔴 change this
    database="hospital_db"
)

cursor = conn.cursor()

print("✅ Connected to Database")

while True:
    print("\n--- Hospital Management & Analytics System ---")
    print("1. Add Patient")
    print("2. View Patients")
    print("3. Add Doctor")
    print("4. View Doctors")
    print("5. Book Appointment")
    print("6. View Appointments")
    print("7. Add Treatment")
    print("8. View Treatments")
    print("9. Most Consulted Doctor")
    print("10. Total Revenue")
    print("11. Most Common Disease")
    print("12. Patient Visit Frequency")
    print("13. Doctor Performance")
    print("14. Exit")

    choice = input("Enter choice: ")

    # 1 Add Patient
    if choice == "1":
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        gender = input("Enter gender: ")

        cursor.execute(
            "INSERT INTO patients (name, age, gender) VALUES (%s, %s, %s)",
            (name, age, gender)
        )
        conn.commit()
        print("✅ Patient Added")

    # 2 View Patients
    elif choice == "2":
        cursor.execute("SELECT * FROM patients")
        for row in cursor.fetchall():
            print(row)

    # 3 Add Doctor
    elif choice == "3":
        name = input("Doctor name: ")
        spec = input("Specialization: ")

        cursor.execute(
            "INSERT INTO doctors (name, specialization) VALUES (%s, %s)",
            (name, spec)
        )
        conn.commit()
        print("✅ Doctor Added")

    # 4 View Doctors
    elif choice == "4":
        cursor.execute("SELECT * FROM doctors")
        for row in cursor.fetchall():
            print(row)

    # 5 Book Appointment
    elif choice == "5":
        patient_id = int(input("Patient ID: "))
        doctor_id = int(input("Doctor ID: "))
        date = input("Date (YYYY-MM-DD): ")

        cursor.execute(
            "INSERT INTO appointments (patient_id, doctor_id, date) VALUES (%s, %s, %s)",
            (patient_id, doctor_id, date)
        )
        conn.commit()
        print("✅ Appointment Booked")

    # 6 View Appointments
    elif choice == "6":
        cursor.execute("""
        SELECT p.name, d.name, a.date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        """)
        for row in cursor.fetchall():
            print(f"Patient: {row[0]} | Doctor: {row[1]} | Date: {row[2]}")

    # 7 Add Treatment
    elif choice == "7":
        patient_id = int(input("Patient ID: "))
        diagnosis = input("Diagnosis: ")
        cost = float(input("Cost: "))

        cursor.execute(
            "INSERT INTO treatments (patient_id, diagnosis, cost) VALUES (%s, %s, %s)",
            (patient_id, diagnosis, cost)
        )
        conn.commit()
        print("✅ Treatment Added")

    # 8 View Treatments
    elif choice == "8":
        cursor.execute("""
        SELECT p.name, t.diagnosis, t.cost
        FROM treatments t
        JOIN patients p ON t.patient_id = p.patient_id
        """)
        for row in cursor.fetchall():
            print(f"Patient: {row[0]} | Disease: {row[1]} | Cost: {row[2]}")

    # 9 Most Consulted Doctor
    elif choice == "9":
        cursor.execute("""
        SELECT d.name, COUNT(*) AS total
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        GROUP BY d.name
        ORDER BY total DESC
        LIMIT 1
        """)
        print("🏆 Most Consulted Doctor:", cursor.fetchone())

    # 10 Total Revenue
    elif choice == "10":
        cursor.execute("SELECT SUM(cost) FROM treatments")
        print("💰 Total Revenue:", cursor.fetchone()[0])

    # 11 Most Common Disease
    elif choice == "11":
        cursor.execute("""
        SELECT diagnosis, COUNT(*) AS total
        FROM treatments
        GROUP BY diagnosis
        ORDER BY total DESC
        LIMIT 1
        """)
        print("🦠 Most Common Disease:", cursor.fetchone())

    # 12 Patient Visit Frequency
    elif choice == "12":
        cursor.execute("""
        SELECT patient_id, COUNT(*) AS visits
        FROM appointments
        GROUP BY patient_id
        """)
        for row in cursor.fetchall():
            print(row)

    # 13 Doctor Performance
    elif choice == "13":
        cursor.execute("""
        SELECT d.name, COUNT(a.appointment_id) AS total
        FROM doctors d
        JOIN appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.name
        """)
        for row in cursor.fetchall():
            print(row)

    # 14 Exit
    elif choice == "14":
        print("👋 Exiting...")
        break

    else:
        print("❌ Invalid choice")

conn.close()