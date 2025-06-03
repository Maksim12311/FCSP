import os
import time
import pandas as pd
from information import Student, Course, Professor, Grade

class CourseManager:
    def __init__(self, filename="courses.txt"):
        self.filename = filename
        self.courses = self.load_courses()

    def load_courses(self):
        """Load courses from file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return [line.strip().split(",") for line in f.readlines()]
        return []

    def save_courses(self):
        """Save courses to file."""
        with open(self.filename, "w") as f:
            for course in self.courses:
                f.write(",".join(course) + "\n")

    def add_course(self, course_name, teacher):
        """Add a new course."""
        self.courses.append([course_name, teacher])
        self.save_courses()
        print(f"Course '{course_name}' has been added.")

    def delete_course(self, course_name):
        """Delete course by name."""
        self.courses = [course for course in self.courses if course[0] != course_name]
        self.save_courses()
        print(f"Course '{course_name}' has been deleted.")

    def update_course(self, old_course_name, new_course_name, new_teacher):
        """Update course information."""
        for course in self.courses:
            if course[0] == old_course_name:
                course[0] = new_course_name
                course[1] = new_teacher
                self.save_courses()
                print(f"Course '{old_course_name}' has been updated to '{new_course_name}'.")
                return
        print(f"Course '{old_course_name}' not found.")

    def list_courses(self):
        """Display list of all courses."""
        if not self.courses:
            print("No courses found.")
            return
        print("List of courses:")
        for course in self.courses:
            print(f"Name: {course[0]}, Teacher: {course[1]}")

class Course:
    def __init__(self, code, name, credits, area_of_study):
        self.code = code
        self.name = name
        self.credits = credits
        self.area_of_study = area_of_study

def add_course(code, name, credits, area_of_study):
    """Add a new course to the system"""
    try:
        with open("courses.txt", "a") as f:
            f.write(f"{code},{name},{credits},{area_of_study}\n")
        print(f"Course {name} ({code}) added successfully.")
        return True
    except Exception as e:
        print(f"Error adding course: {str(e)}")
        return False

def enroll_student_in_course(student_name, course_code):
    """Enroll a student in a course"""
    try:
        # Check if student exists
        student_found = False
        with open("students.txt", "r") as f:
            for line in f:
                if line.startswith(student_name):
                    student_found = True
                    break
        
        if not student_found:
            print(f"Student {student_name} not found.")
            return False
            
        # Check if course exists
        course_found = False
        with open("courses.txt", "r") as f:
            for line in f:
                if line.startswith(course_code):
                    course_found = True
                    break
                    
        if not course_found:
            print(f"Course {course_code} not found.")
            return False
            
        # Add enrollment
        with open("enrollments.txt", "a") as f:
            f.write(f"{student_name},{course_code}\n")
        print(f"Successfully enrolled {student_name} in course {course_code}")
        return True
        
    except FileNotFoundError:
        print("Required database files not found.")
        return False

def list_student_courses(student_name):
    """List all courses a student is enrolled in"""
    try:
        # Get student's enrollments
        enrollments = []
        with open("enrollments.txt", "r") as f:
            for line in f:
                name, code = line.strip().split(",")
                if name == student_name:
                    enrollments.append(code)
        
        if not enrollments:
            print(f"No courses found for student {student_name}")
            return []
            
        # Get course details
        courses = []
        with open("courses.txt", "r") as f:
            for line in f:
                code, name, credits, area = line.strip().split(",")
                if code in enrollments:
                    courses.append({
                        'code': code,
                        'name': name,
                        'credits': credits,
                        'area': area
                    })
        
        # Display courses
        print(f"\nCourses for {student_name}:")
        print("-" * 50)
        total_credits = 0
        for course in courses:
            print(f"Course: {course['name']} ({course['code']})")
            print(f"Credits: {course['credits']}")
            print(f"Area: {course['area']}")
            print("-" * 50)
            total_credits += int(course['credits'])
        
        print(f"Total credits: {total_credits}")
        return courses
        
    except FileNotFoundError:
        print("Required database files not found.")
        return []

def get_course_students(course_code):
    """Get all students enrolled in a specific course"""
    try:
        enrolled_students = []
        with open("enrollments.txt", "r") as f:
            for line in f:
                student_name, code = line.strip().split(",")
                if code == course_code:
                    enrolled_students.append(student_name)
        
        if not enrolled_students:
            print(f"No students enrolled in course {course_code}")
            return []
            
        print(f"\nStudents enrolled in {course_code}:")
        print("-" * 30)
        for student in enrolled_students:
            print(student)
        
        return enrolled_students
        
    except FileNotFoundError:
        print("Required database files not found.")
        return []

def analyze_course_performance(course: Course) -> dict:
    """Analyze course performance metrics"""
    if not course.enrolled_students:
        return {
            'enrollment_count': 0,
            'average_gpa': 0.0,
            'completion_rate': 0.0
        }

    # Calculate metrics
    enrollment_count = len(course.enrolled_students)
    gpas = [student.gpa for student in course.enrolled_students]
    average_gpa = sum(gpas) / len(gpas) if gpas else 0.0

    # Calculate completion rate
    students_with_grades = sum(1 for student in course.enrolled_students 
                             if course.code in student.courses)
    completion_rate = students_with_grades / enrollment_count if enrollment_count > 0 else 0.0

    return {
        'enrollment_count': enrollment_count,
        'average_gpa': average_gpa,
        'completion_rate': completion_rate
    }

def generate_performance_report(courses: list[Course], output_file: str = "performance_report.csv") -> bool:
    """Generate a comprehensive performance report"""
    try:
        data = []
        for course in courses:
            performance = analyze_course_performance(course)
            data.append({
                'Course Code': course.code,
                'Course Name': course.name,
                'Enrollment Count': performance['enrollment_count'],
                'Average GPA': performance['average_gpa'],
                'Completion Rate': performance['completion_rate'],
                'Professor': course.professor.full_name if course.professor else 'Unassigned'
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Performance report generated successfully: {output_file}")
        return True
    except Exception as e:
        print(f"Error generating performance report: {str(e)}")
        return False

def visualize_performance(courses: list[Course]) -> None:
    """Show basic course performance data"""
    if not courses:
        print("No courses to analyze")
        return
        
    print("Course Performance Summary")
    print("-" * 40)
    
    for course in courses:
        # Get basic metrics
        students = len(course.enrolled_students)
        gpas = [s.gpa for s in course.enrolled_students if s.gpa > 0]
        avg_gpa = sum(gpas) / len(gpas) if gpas else 0
        
        # Print course info
        print(f"Course: {course.code}")
        print(f"Students: {students}")
        print(f"Average GPA: {avg_gpa:.2f}")
        print("-" * 40)

if __name__ == "__main__":
    print("Course Performance Analysis Module")
    print("Available function:")
    print("- analyze_course_performance(course)")