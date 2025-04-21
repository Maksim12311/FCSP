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