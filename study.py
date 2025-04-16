import os

class CourseManager:
    def __init__(self, filename="courses.txt"):
        self.filename = filename
        self.courses = self.load_courses()

    def load_courses(self):
        """Загрузка курсов из файла."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return [line.strip().split(",") for line in f.readlines()]
        return []

    def save_courses(self):
        """Сохранение курсов в файл."""
        with open(self.filename, "w") as f:
            for course in self.courses:
                f.write(",".join(course) + "\n")

    def add_course(self, course_name, teacher):
        """Добавление нового курса."""
        self.courses.append([course_name, teacher])
        self.save_courses()
        print(f"Курс '{course_name}' добавлен.")

    def delete_course(self, course_name):
        """Удаление курса по имени."""
        self.courses = [course for course in self.courses if course[0] != course_name]
        self.save_courses()
        print(f"Курс '{course_name}' удален.")

    def update_course(self, old_course_name, new_course_name, new_teacher):
        """Изменение информации о курсе."""
        for course in self.courses:
            if course[0] == old_course_name:
                course[0] = new_course_name
                course[1] = new_teacher
                self.save_courses()
                print(f"Курс '{old_course_name}' обновлен на '{new_course_name}'.")
                return
        print(f"Курс '{old_course_name}' не найден.")

    def list_courses(self):
        """Вывод списка всех курсов."""
        if not self.courses:
            print("Курсы не найдены.")
            return
        print("Список курсов:")
        for course in self.courses:
            print(f"Название: {course[0]}, Преподаватель: {course[1]}")