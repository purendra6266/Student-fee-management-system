"""
PS 65 - Student Fee Management System
Console application to manage student fee records.
Concepts: Dictionaries, Functions, Conditions, File Handling
Records are stored in fees.txt as: Roll,Name,Course,Paid
"""

FILE_NAME = "fees.txt"

# Course-fee table (dictionary)
COURSE_FEES = {"BCA": 45000, "BTech": 60000, "MBA": 80000}


# ---------------------------------------------------------------- file handling
def load_records():
    """Load all students from fees.txt into a list of dictionaries."""
    records = []
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue  # skip corrupted lines
                roll, name, course, paid = parts
                if course not in COURSE_FEES:
                    continue
                try:
                    paid = int(paid)
                except ValueError:
                    continue
                records.append({"roll": roll, "name": name,
                                "course": course, "paid": paid})
    except FileNotFoundError:
        pass  # first run: no file yet
    return records


def save_records(records):
    """Write all students back to fees.txt."""
    with open(FILE_NAME, "w") as f:
        for r in records:
            f.write(f"{r['roll']},{r['name']},{r['course']},{r['paid']}\n")


# ------------------------------------------------------------------- helpers
def total_fee(student):
    return COURSE_FEES[student["course"]]


def due_amount(student):
    return total_fee(student) - student["paid"]


def get_status(student):
    """Paid (due = 0), Partial (0 < paid < total), Unpaid (paid = 0)."""
    if due_amount(student) == 0:
        return "Paid"
    if student["paid"] > 0:
        return "Partial"
    return "Unpaid"


def find_student(records, roll):
    for r in records:
        if r["roll"] == roll:
            return r
    return None


# ---------------------------------------------------------------- operations
def add_student(records):
    roll = input("Roll: ").strip()
    if not roll:
        print("Roll cannot be empty.")
        return
    if find_student(records, roll):
        print("Roll number already exists.")
        return
    name = input("Name: ").strip()
    if not name or "," in name:
        print("Invalid name.")
        return
    course = input("Course: ").strip()
    # accept any capitalisation of the course name
    matched = next((c for c in COURSE_FEES if c.lower() == course.lower()), None)
    if matched is None:
        print("Invalid course. Choose from: " + ", ".join(COURSE_FEES))
        return

    student = {"roll": roll, "name": name, "course": matched, "paid": 0}
    records.append(student)
    save_records(records)
    print(f"Student added: {roll} | {name} | {matched} | "
          f"Total Fee: {total_fee(student)} | Paid: 0 | "
          f"Due: {due_amount(student)} | Status: {get_status(student)}")


def pay_fee(records):
    roll = input("Roll: ").strip()
    student = find_student(records, roll)
    if student is None:
        print("Student not found.")
        return
    try:
        amount = int(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount. Payment rejected.")
        return

    due = due_amount(student)
    if amount <= 0:
        print("Amount must be greater than zero. Payment rejected.")
    elif amount > due:
        print(f"Amount exceeds due ({due}). Payment rejected.")
    else:
        student["paid"] += amount
        save_records(records)
        print(f"Payment received. Paid: {student['paid']} | "
              f"Due: {due_amount(student)} | Status: {get_status(student)}")


def search_student(records):
    roll = input("Roll: ").strip()
    student = find_student(records, roll)
    if student is None:
        print("Student not found.")
        return
    print(f"{student['roll']} | {student['name']} | {student['course']} | "
          f"Total Fee: {total_fee(student)} | Paid: {student['paid']} | "
          f"Due: {due_amount(student)} | Status: {get_status(student)}")


def pending_dues(records):
    pending = [r for r in records if due_amount(r) > 0]
    if not pending:
        print("No pending dues.")
        return
    print("Students with pending dues:")
    for r in pending:
        print(f"{r['roll']} | {r['name']} | {due_amount(r)}")


# ---------------------------------------------------------------------- main
def main():
    records = load_records()
    while True:
        print("\n===== Student Fee Management System =====")
        print("1. Add Student")
        print("2. Pay Fee")
        print("3. Search by Roll")
        print("4. Pending Dues")
        print("5. Exit")
        choice = input("Menu option: ").strip()

        if choice == "1":
            add_student(records)
        elif choice == "2":
            pay_fee(records)
        elif choice == "3":
            search_student(records)
        elif choice == "4":
            pending_dues(records)
        elif choice == "5":
            save_records(records)
            print("Records saved. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
