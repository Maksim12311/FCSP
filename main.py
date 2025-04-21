from .information import add_student, change_information, delete_student, search_students, display_all_students



add_student("Ivan", "Ivanov", "2000-01-01", "IT", "Russia")


change_information("Ivan", "Ivanov", "2000-01-01","Data Science","Russia")


name_search = "Ivan"
area_of_study_search = "IT"
found_students_by_name = search_students(name_search, "name")
print("Результаты поиска по имени:")
for student in found_students_by_name:
    print(student)

found_students_by_area = search_students(area_of_study_search, "area_of_study")
print("\nРезультаты поиска по специальности:")
for student in found_students_by_area:
    print(student)


display_all_students()