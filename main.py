import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, StringVar, Scrollbar
import customtkinter as ctk  # Assuming this is a custom module you have

# Set the theme (optional)
ctk.set_appearance_mode("Light")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (default), "green", "dark-blue"

class App:
    def __init__(self):
        # Create the welcome window
        self.welcome_window = tk.Tk()
        self.welcome_window.title("Welcome To The Waka-ama Tracker")

        # Welcome label
        welcome_label = tk.Label(self.welcome_window, text="Welcome To The Waka-ama Tracker", font=("Helvetica", 16))
        welcome_label.pack(pady=20)

        # Login button (changed to ctk.CTkButton)
        login_button = ctk.CTkButton(self.welcome_window, text="Login", command=self.open_login_window)
        login_button.pack(pady=10)

        # Start the application loop
        self.welcome_window.mainloop()

    def open_login_window(self):
        # Destroy the welcome window
        self.welcome_window.destroy()

        # Create the main application window
        self.root = ctk.CTk()
        self.root.title("Results")
        self.root.withdraw()  # Hide the main window initially

        # Create the login window
        self.login_window = ctk.CTkToplevel(self.root)
        self.login_window.title("Waka-ama Login")

        # Username label and entry
        self.username_label = ctk.CTkLabel(self.login_window, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_var = StringVar()
        self.username_entry = ctk.CTkEntry(self.login_window, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password label and entry
        self.password_label = ctk.CTkLabel(self.login_window, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_var = StringVar()
        self.password_entry = ctk.CTkEntry(self.login_window, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Login button (changed to ctk.CTkButton)
        self.login_button = ctk.CTkButton(self.login_window, text="Enter", command=self.check_login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Toggle theme button
        self.toggle_theme_button = ctk.CTkButton(self.login_window, text="Toggle Theme", command=self.toggle_theme)
        self.toggle_theme_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Trials for user
        self.trials = 0

        # Username and password (for demonstration)
        self.username = 'admin'
        self.password = 'password'

        # Run the application
        self.root.mainloop()

    def check_login(self):
        if self.username_var.get() == self.username and self.password_var.get() == self.password:
            self.login_window.destroy()
            self.mainwin()
        else:
            self.trials += 1
            if self.trials < 3:
                messagebox.showerror("Error", "Invalid username or password")
            else:
                self.login_button.destroy()
                trial_label = ctk.CTkLabel(self.login_window, text="Too many failed attempts")
                trial_label.grid(row=2, column=0, columnspan=2, pady=10)

    def mainwin(self):
        self.root.deiconify()  # Show the main window

        # Frame for directory selection
        directory_frame = ctk.CTkFrame(self.root)
        directory_frame.pack(pady=10)
        directory_label = ctk.CTkLabel(directory_frame, text="Directory:")
        directory_label.grid(row=0, column=0)
        self.directory_var = StringVar()
        directory_entry = ctk.CTkEntry(directory_frame, textvariable=self.directory_var, width=500)
        directory_entry.grid(row=0, column=1, padx=10)
        browse_button = ctk.CTkButton(directory_frame, text="Search", command=self.browse_directory)
        browse_button.grid(row=0, column=2)

        # Frame for file type filter
        filter_frame = ctk.CTkFrame(self.root)
        filter_frame.pack(pady=10)
        filetype_label = ctk.CTkLabel(filter_frame, text="Filetype:")
        filetype_label.grid(row=0, column=0)
        self.filetype_var = StringVar(value="")
        filetype_entry = ctk.CTkEntry(filter_frame, textvariable=self.filetype_var, width=500)
        filetype_entry.grid(row=0, column=1, padx=10)
        apply_filter_button = ctk.CTkButton(filter_frame, text="Filter", command=self.apply_filter)
        apply_filter_button.grid(row=0, column=2)

        # Frame for race type filter
        race_type_frame = ctk.CTkFrame(self.root)
        race_type_frame.pack(pady=10)
        race_type_label = ctk.CTkLabel(race_type_frame, text="Racetype:")
        race_type_label.grid(row=0, column=0)
        self.race_type_var = StringVar(value="")
        race_type_entry = ctk.CTkEntry(race_type_frame, textvariable=self.race_type_var, width=500)
        race_type_entry.grid(row=0, column=1, padx=10)
        apply_race_filter_button = ctk.CTkButton(race_type_frame, text="Race", command=self.apply_filter)
        apply_race_filter_button.grid(row=0, column=2)

        # Button to check files and assign points
        check_files_button = ctk.CTkButton(self.root, text="Track", command=self.check_files_and_assign_points)
        check_files_button.pack(pady=10)

    def browse_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.directory_var.set(directory_path)
            self.update_file_list(directory_path)

    def update_file_list(self, directory_path):
        pass  # Remove file list updating logic

    def apply_filter(self):
        pass  # Remove file list updating logic

    def assign_points(self, placement):
        points = 9 - placement
        return max(points, 1)  # Ensure minimum points is 1

    def check_files_and_assign_points(self):
        directory_path = self.directory_var.get()
        if not directory_path:
            messagebox.showerror("Error", "No directory selected")
            return

        club_points = {}

        for filename in os.listdir(directory_path):
            if self.filetype_var.get() in filename and self.race_type_var.get() in filename:
                file_path = os.path.join(directory_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                except UnicodeDecodeError:
                    try:
                        with open(file_path, 'r', encoding='latin-1') as file:
                            lines = file.readlines()
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to read file {filename}: {e}")
                        return

                try:
                    for i, line in enumerate(lines[1:9]):  # Only consider lines 2 to 9 (1-indexed)
                        columns = line.split(',')
                        if len(columns) > 5:
                            club_name = columns[5].strip()
                            points = self.assign_points(i + 1)
                            club_points[club_name] = club_points.get(club_name, 0) + points
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process file {filename}: {e}")
                    return

        results_window = Toplevel(self.root)
        results_window.title("Club Points")

        sorted_clubs = sorted(club_points.items(), key=lambda item: item[1], reverse=True)
        scrollbar = Scrollbar(results_window, orient='vertical')
        scrollbar.pack(side='right', fill='y')
        points_text = tk.Text(results_window, wrap='word', yscrollcommand=scrollbar.set)
        points_text.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=points_text.yview)

        for club, points in sorted_clubs:
            points_text.insert('end', f"{club}: {points} points\n")

        points_text.config(state='normal')

    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)

if __name__ == "__main__":
    app = App()
