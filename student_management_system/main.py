# from student_management import load_data,add_student,search_student,update_details,delete_student
from student_management import *

#Display the menu options

def display_menu():
    print("==============Student Management System=================")
    print("Enter the option number only")
    print("1. Add Student")
    print("2. Search Student by ID")
    print("3. Update Student details")
    print("4. Delete Students")
    print("5. View Students")
    print("6. Course Statistics")
    print("7. Exit")


def main():
    students_db = load_data() 

    while True:
        display_menu()
        choice = int(input("Enter the choice : "))

        if choice == 1:
            add_student(students_db)
        elif choice == 2:
            search_student(students_db)
        elif choice == 3:
            update_details(students_db)
        elif choice == 4:
            delete_student(students_db)
        elif choice == 5:
            view_students(students_db)
        elif choice == 6:
            course_statistics(students_db)
        elif choice == 6:
            break
        else:
            print('Invalid input')


if __name__ == '__main__':
    main()