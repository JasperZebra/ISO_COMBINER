import os
import threading
import subprocess
import random
import string
import tkinter as tk
from tkinter import filedialog, ttk
from file_reader import get_version, get_instructions

class ISOCombiner:
    def __init__(self, root):
        self.root = root
        self.version = get_version()
        self.root.title(f"ISO Combiner{self.version}")
        self.root.geometry("600x505")
        self.file_paths = []

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 14))

        self.instructions_box = tk.Text(self.root, height=6)
        instructions = get_instructions()
        self.instructions_box.insert(tk.END, instructions)
        self.instructions_box.configure(state="disabled", bg=self.root.cget("bg"), bd=0,  font=("Arial", 10))
        self.instructions_box.pack(side=tk.TOP, padx=10, pady=10)

        self.frame = ttk.Frame(self.root)
        self.frame.pack(side=tk.BOTTOM, fill="y", expand=True)

        self.listbox = tk.Listbox(self.frame, width=60)
        self.listbox.pack(side=tk.TOP)

        self.browse_button = ttk.Button(
            self.frame, text="Browse", command=self.browse_files
        )
        self.browse_button.pack(side=tk.TOP, pady=12)

        self.combine_button = ttk.Button(
            self.frame, text="Combine", command=self.combine_files
        )
        self.combine_button.pack(side=tk.TOP, pady=12)

        self.clear_button = ttk.Button(
            self.frame, text="Clear", command=self.clear_files
        )
        self.clear_button.pack(side=tk.TOP, pady=12)

        self.loading_label = ttk.Label(self.frame, text="Loading...", font=("Arial", 15))
        self.progress = None


    def browse_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select ISO files", filetypes=(("ISO files", "*.iso"),)
        )
        for file_path in file_paths:
            if file_path not in self.file_paths:
                self.file_paths.append(file_path)
                self.listbox.insert(tk.END, file_path)

    def combine_files(self):
        if len(self.file_paths) >= 2:
            output_path = filedialog.asksaveasfilename(
                title="Save Combined ISO",
                filetypes=(("ISO files", "*.iso"),),
                defaultextension=".iso",
            )
            if output_path:
                self.loading_label.pack(side=tk.BOTTOM, pady=20)
                self.browse_button.configure(state=tk.DISABLED)
                self.combine_button.configure(state=tk.DISABLED)
                self.clear_button.configure(state=tk.DISABLED)

                # Generate a random string for the temporary file name
                temp_file_name = ''.join(random.choices(string.ascii_lowercase, k=8))
                temp_file_path = os.path.join(os.path.dirname(output_path), f"{temp_file_name}.tmp")

                command = self.build_copy_command(temp_file_path)
                thread = threading.Thread(target=self.execute_command, args=(command,))
                thread.start()

                self.root.after(100, self.check_progress, thread, temp_file_path, output_path)
        else:
            tk.messagebox.showerror(
                "Error", "Please select at least two ISO files."
            )

    def execute_command(self, command):
        current_dir = os.getcwd()
        source_dir = os.path.dirname(self.file_paths[0])
        os.chdir(source_dir)
        subprocess.run(command, shell=True)
        os.chdir(current_dir)

    def check_progress(self, thread, temp_file_path, output_path):
        if thread.is_alive():
            self.root.after(100, self.check_progress, thread, temp_file_path, output_path)
        else:
            self.loading_label.pack_forget()
            self.combine_button.configure(state=tk.NORMAL)
            self.clear_button.configure(state=tk.NORMAL)
            
            # Rename the temporary file to the final output file
            os.rename(temp_file_path, output_path)

            tk.messagebox.showinfo(
                "Success", "ISO files combined successfully!"
            )
            self.reset_state()

    def clear_files(self):
        self.file_paths.clear()
        self.listbox.delete(0, tk.END)

    def build_copy_command(self, temp_file_path):
        command = f'copy /b "{self.file_paths[0]}"'
        for file in self.file_paths[1:]:
            command += f' /b + "{file}"'
        command += f' /b "{temp_file_path}" /b'
        return command
    
    def reset_state(self):
        self.clear_files()
        self.browse_button.configure(state="normal")
        self.combine_button.configure(state="normal")
        self.clear_button.configure(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    ISOCombiner(root)
    root.mainloop()
