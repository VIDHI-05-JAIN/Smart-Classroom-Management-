import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class SmartClassroomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Classroom System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#121212")

        # Dark color scheme
        self.bg_color = "#121212"
        self.bg_color_light = "#1e1e1e"
        self.btn_color = "#e94560"
        self.btn_text_color = "#ffffff"
        self.entry_bg_color = "#1e1e1e"
        self.text_color = "#ffffff"

        self.users = {}
        self.load_data()

        self.setup_gradient_background()
        self.create_initial_screen()

    def setup_gradient_background(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=700, bg=self.bg_color)
        self.canvas.pack(fill="both", expand=True)

    def create_initial_screen(self):
        self.initial_frame = tk.Frame(self.canvas, bg=self.bg_color_light, relief=tk.RAISED)
        self.initial_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        label_title = tk.Label(self.initial_frame, text="Welcome to Smart Classroom", font=('Helvetica', 24, 'bold'),
                               bg=self.bg_color_light, fg=self.text_color)
        label_title.pack(pady=20)

        btn_login = tk.Button(self.initial_frame, text="Login", bg=self.btn_color, fg=self.btn_text_color,
                              font=('Arial', 12, 'bold'), command=self.create_login_screen)
        btn_login.pack(pady=10)

        btn_register = tk.Button(self.initial_frame, text="Register", bg=self.btn_color, fg=self.btn_text_color,
                                 font=('Arial', 12, 'bold'), command=self.create_register_screen)
        btn_register.pack(pady=10)

    def create_register_screen(self):
        self.initial_frame.destroy()
        self.register_frame = tk.Frame(self.canvas, bg=self.bg_color_light, relief=tk.RAISED)
        self.register_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        label_title = tk.Label(self.register_frame, text="Register for Smart Classroom", font=('Helvetica', 24, 'bold'),
                               bg=self.bg_color_light, fg=self.text_color)
        label_title.pack(pady=20)

        label_user = tk.Label(self.register_frame, text="Username:", font=('Arial', 14), bg=self.bg_color_light, fg=self.text_color)
        label_user.pack(anchor=tk.W, padx=20)
        self.entry_register_user = tk.Entry(self.register_frame, width=30, bg=self.entry_bg_color, fg=self.text_color)
        self.entry_register_user.pack(pady=10)

        label_pass = tk.Label(self.register_frame, text="Password:", font=('Arial', 14), bg=self.bg_color_light, fg=self.text_color)
        label_pass.pack(anchor=tk.W, padx=20)
        self.entry_register_pass = tk.Entry(self.register_frame, width=30, bg=self.entry_bg_color, fg=self.text_color, show="*")
        self.entry_register_pass.pack(pady=10)

        label_role = tk.Label(self.register_frame, text="Role (student/teacher):", font=('Arial', 14), bg=self.bg_color_light, fg=self.text_color)
        label_role.pack(anchor=tk.W, padx=20)
        self.entry_register_role = tk.Entry(self.register_frame, width=30, bg=self.entry_bg_color, fg=self.text_color)
        self.entry_register_role.pack(pady=10)

        btn_register = tk.Button(self.register_frame, text="Register", bg=self.btn_color, fg=self.btn_text_color,
                                 font=('Arial', 12, 'bold'), command=self.register_user)
        btn_register.pack(pady=20)

        btn_back = tk.Button(self.register_frame, text="Back", bg=self.btn_color, fg=self.btn_text_color,
                             font=('Arial', 12, 'bold'), command=self.create_initial_screen)
        btn_back.pack(pady=10)

    def register_user(self):
        username = self.entry_register_user.get()
        password = self.entry_register_pass.get()
        role = self.entry_register_role.get().lower()

        if username and password and role in ['student', 'teacher']:
            if username not in self.users:
                self.users[username] = {
                    'password': password,
                    'role': role,
                    'attendance': [],
                    'assignments': [],
                    'assignment_submissions': {}
                }
                self.save_data()
                messagebox.showinfo("Success", "Registration Successful!")
                self.register_frame.destroy()
                self.create_login_screen()
            else:
                messagebox.showwarning("Input Error", "Username already exists!")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields correctly!")

    def create_login_screen(self):
        self.initial_frame.destroy()
        self.login_frame = tk.Frame(self.canvas, bg=self.bg_color_light, relief=tk.RAISED)
        self.login_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        label_title = tk.Label(self.login_frame, text="Login to Smart Classroom", font=('Helvetica', 24, 'bold'),
                               bg=self.bg_color_light, fg=self.text_color)
        label_title.pack(pady=20)

        label_user = tk.Label(self.login_frame, text="Username:", font=('Arial', 14), bg=self.bg_color_light, fg=self.text_color)
        label_user.pack(anchor=tk.W, padx=20)
        self.entry_user = tk.Entry(self.login_frame, width=30, bg=self.entry_bg_color, fg=self.text_color)
        self.entry_user.pack(pady=10)

        label_pass = tk.Label(self.login_frame, text="Password:", font=('Arial', 14), bg=self.bg_color_light, fg=self.text_color)
        label_pass.pack(anchor=tk.W, padx=20)
        self.entry_pass = tk.Entry(self.login_frame, width=30, bg=self.entry_bg_color, fg=self.text_color, show="*")
        self.entry_pass.pack(pady=10)

        btn_login = tk.Button(self.login_frame, text="Login", bg=self.btn_color, fg=self.btn_text_color,
                              font=('Arial', 12, 'bold'), command=self.check_login)
        btn_login.pack(pady=20)

        btn_back = tk.Button(self.login_frame, text="Back", bg=self.btn_color, fg=self.btn_text_color,
                             font=('Arial', 12, 'bold'), command=self.create_initial_screen)
        btn_back.pack(pady=10)

    def check_login(self):
        entered_username = self.entry_user.get()
        entered_password = self.entry_pass.get()

        if entered_username in self.users and self.users[entered_username]['password'] == entered_password:
            messagebox.showinfo("Login Successful", f"Welcome, {entered_username}!")
            self.login_frame.destroy()
            self.create_dashboard(entered_username)
        else:
            messagebox.showwarning("Login Error", "Invalid username or password!")

    def create_dashboard(self, username):
        self.dashboard_frame = tk.Frame(self.canvas, bg=self.bg_color_light, relief=tk.RAISED)
        self.dashboard_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        user_role = self.users[username]['role']
        
        label_title = tk.Label(self.dashboard_frame, text="Dashboard", font=('Helvetica', 24, 'bold'),
                               bg=self.bg_color_light, fg=self.text_color)
        label_title.pack(pady=20)

        if user_role == 'teacher':
            btn_manage_attendance = tk.Button(self.dashboard_frame, text="Manage Attendance", command=self.manage_attendance, bg=self.btn_color, fg=self.btn_text_color)
            btn_manage_attendance.pack(pady=10)

            btn_create_assignment = tk.Button(self.dashboard_frame, text="Create Assignment", command=self.create_assignment, bg=self.btn_color, fg=self.btn_text_color)
            btn_create_assignment.pack(pady=10)

            btn_view_assignments = tk.Button(self.dashboard_frame, text="View Assignments", command=self.view_assignments, bg=self.btn_color, fg=self.btn_text_color)
            btn_view_assignments.pack(pady=10)

        elif user_role == 'student':
            btn_view_attendance = tk.Button(self.dashboard_frame, text="View Attendance", command=lambda: self.view_attendance(username), bg=self.btn_color, fg=self.btn_text_color)
            btn_view_attendance.pack(pady=10)

            btn_submit_assignment = tk.Button(self.dashboard_frame, text="Submit Assignment", command=self.submit_assignment, bg=self.btn_color, fg=self.btn_text_color)
            btn_submit_assignment.pack(pady=10)

            btn_view_submissions = tk.Button(self.dashboard_frame, text="View Submissions", command=lambda: self.view_submissions(username), bg=self.btn_color, fg=self.btn_text_color)
            btn_view_submissions.pack(pady=10)

        btn_logout = tk.Button(self.dashboard_frame, text="Logout", command=self.logout, bg=self.btn_color, fg=self.btn_text_color)
        btn_logout.pack(pady=20)

    def manage_attendance(self):
        attendance_frame = tk.Toplevel(self.root)
        attendance_frame.title("Manage Attendance")
        attendance_frame.geometry("300x200")
        attendance_frame.configure(bg=self.bg_color)

        label_title = tk.Label(attendance_frame, text="Mark Attendance", font=('Helvetica', 16, 'bold'), bg=self.bg_color, fg=self.text_color)
        label_title.pack(pady=10)

        label_student = tk.Label(attendance_frame, text="Student Username:", bg=self.bg_color, fg=self.text_color)
        label_student.pack(pady=5)
        entry_student = tk.Entry(attendance_frame, bg=self.entry_bg_color, fg=self.text_color)
        entry_student.pack(pady=5)

        def mark_attendance():
            student_username = entry_student.get()
            if student_username in self.users:
                date_today = datetime.now().date()
                self.users[student_username]['attendance'].append(str(date_today))
                self.save_data()
                messagebox.showinfo("Success", f"Attendance marked for {student_username}!")
                attendance_frame.destroy()
            else:
                messagebox.showwarning("Error", "Student not found!")

        btn_mark = tk.Button(attendance_frame, text="Mark Attendance", command=mark_attendance, bg=self.btn_color, fg=self.btn_text_color)
        btn_mark.pack(pady=10)

    def create_assignment(self):
        assignment_frame = tk.Toplevel(self.root)
        assignment_frame.title("Create Assignment")
        assignment_frame.geometry("300x300")
        assignment_frame.configure(bg=self.bg_color)

        label_title = tk.Label(assignment_frame, text="Create Assignment", font=('Helvetica', 16, 'bold'), bg=self.bg_color, fg=self.text_color)
        label_title.pack(pady=10)

        label_assignment = tk.Label(assignment_frame, text="Assignment Title:", bg=self.bg_color, fg=self.text_color)
        label_assignment.pack(pady=5)
        entry_assignment_title = tk.Entry(assignment_frame, bg=self.entry_bg_color, fg=self.text_color)
        entry_assignment_title.pack(pady=5)

        label_assignment_desc = tk.Label(assignment_frame, text="Assignment Description:", bg=self.bg_color, fg=self.text_color)
        label_assignment_desc.pack(pady=5)
        text_assignment_desc = tk.Text(assignment_frame, height=5, bg=self.entry_bg_color, fg=self.text_color)
        text_assignment_desc.pack(pady=5)

        def submit_assignment():
            title = entry_assignment_title.get()
            description = text_assignment_desc.get("1.0", tk.END).strip()
            if title and description:
                self.users[username]['assignments'].append({
                    'title': title,
                    'description': description
                })
                self.save_data()
                messagebox.showinfo("Success", "Assignment Created!")
                assignment_frame.destroy()
            else:
                messagebox.showwarning("Error", "Please fill all fields!")

        btn_submit = tk.Button(assignment_frame, text="Create Assignment", command=submit_assignment, bg=self.btn_color, fg=self.btn_text_color)
        btn_submit.pack(pady=10)

    def view_assignments(self):
        view_assignments_frame = tk.Toplevel(self.root)
        view_assignments_frame.title("View Assignments")
        view_assignments_frame.geometry("400x400")
        view_assignments_frame.configure(bg=self.bg_color)

        label_title = tk.Label(view_assignments_frame, text="Assignments", font=('Helvetica', 16, 'bold'), bg=self.bg_color, fg=self.text_color)
        label_title.pack(pady=10)

        for assignment in self.users[username]['assignments']:
            label_assignment = tk.Label(view_assignments_frame, text=f"{assignment['title']}: {assignment['description']}",
                                         bg=self.bg_color, fg=self.text_color)
            label_assignment.pack(pady=5)

    def view_attendance(self, username):
        attendance_frame = tk.Toplevel(self.root)
        attendance_frame.title("View Attendance")
        attendance_frame.geometry("300x400")
        attendance_frame.configure(bg=self.bg_color)

        label_title = tk.Label(attendance_frame, text="Your Attendance", font=('Helvetica', 16, 'bold'), bg=self.bg_color, fg=self.text_color)
        label_title.pack(pady=10)

        attendance_list = self.users[username]['attendance']
        if attendance_list:
            for date in attendance_list:
                label_date = tk.Label(attendance_frame, text=date, bg=self.bg_color, fg=self.text_color)
                label_date.pack(pady=5)
        else:
            label_no_attendance = tk.Label(attendance_frame, text="No attendance marked.", bg=self.bg_color, fg=self.text_color)
            label_no_attendance.pack(pady=5)

    def submit_assignment(self):
        submit_frame = tk.Toplevel(self.root)
        submit_frame.title("Submit Assignment")
        submit_frame.geometry("300x300")
        submit_frame.configure(bg=self.bg_color)

        label_title = tk.Label(submit_frame, text="Submit Assignment", font=('Helvetica', 16, 'bold'), bg=self.bg_color, fg=self.text_color)
        label_title.pack(pady=10)

        label_assignment = tk.Label(submit_frame, text="Assignment Title:", bg=self.bg_color, fg=self.text_color)
        label_assignment.pack(pady=5)
        entry_assignment_title = tk.Entry(submit_frame, bg=self.entry_bg_color, fg=self.text_color)
        entry_assignment_title.pack(pady=5)

        def upload_file():
            file_path = filedialog.askopenfilename()
            if file_path:
                self.users[username]['assignment_submissions'][entry_assignment_title.get()] = file_path
                self.save_data()
                messagebox.showinfo("Success", "Assignment Submitted!")
                submit_frame.destroy()

        btn_upload = tk.Button(submit_frame, text="Upload Assignment", command=upload_file, bg=self.btn_color, fg=self.btn_text_color)
        btn_upload.pack(pady=10)

    def view_submissions(self, username):
        submissions_frame = tk.Toplevel(self.root)
        submissions_frame.title("View Submissions")
        submissions_frame.geometry("300x400")
        submissions_frame.configure(bg=self.bg_color)

        label_title = tk.Label(submissions_frame, text="Your Submissions", font=('Helvetica', 16, 'bold'), bg=self.bg_color, fg=self.text_color)
        label_title.pack(pady=10)

        submissions = self.users[username]['assignment_submissions']
        if submissions:
            for title, path in submissions.items():
                label_submission = tk.Label(submissions_frame, text=f"{title}: {path}", bg=self.bg_color, fg=self.text_color)
                label_submission.pack(pady=5)
        else:
            label_no_submission = tk.Label(submissions_frame, text="No submissions made.", bg=self.bg_color, fg=self.text_color)
            label_no_submission.pack(pady=5)

    def logout(self):
        self.dashboard_frame.destroy()
        self.create_initial_screen()

    def load_data(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                self.users = json.load(f)

    def save_data(self):
        with open("users.json", "w") as f:
            json.dump(self.users, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartClassroomApp(root)
    root.mainloop()
