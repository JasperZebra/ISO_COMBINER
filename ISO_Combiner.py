import os
import threading
import subprocess
import random
import string
import tkinter as tk
from tkinter import filedialog, ttk
from copy import deepcopy
from collections import defaultdict
from file_reader import get_version, get_instructions_text, get_game_name_to_file_paths_map, create_unique_filename

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

        # Create a Notebook widget
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create a frame for the main application
        self.frame = ttk.Frame(notebook)
        self.frame.pack(side=tk.BOTTOM, fill="y", expand=True)
        notebook.add(self.frame, text="Application")

        # Instructions Tab
        instructions_frame = ttk.Frame(notebook)
        instructions_frame.pack(fill=tk.BOTH, expand=True)
        notebook.add(instructions_frame, text="Instructions")

        instructions_text = get_instructions_text()
        instructions_textbox = tk.Text(instructions_frame, wrap="word", height=10, font=("Arial", 12))
        instructions_textbox.pack(fill=tk.BOTH, expand=True, padx=10)

        instructions_textbox.insert("1.0", instructions_text)
        instructions_textbox.configure(state="disabled")

        # Add a message at the bottom indicating to scroll down
        scroll_message = tk.Label(instructions_frame, text="Scroll down to see more", anchor="center", fg="black")
        scroll_message.pack(fill=tk.X, pady=5)

        self.intro_label = ttk.Label(self.frame, \
                                     text="Welcome to ISO Combiner! \n See Instructions tab for details and instructions.", \
                                     justify="center")
        self.intro_label.pack(side=tk.TOP, padx=10, pady=10)        

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

        self.loading_label = ttk.Label(self.frame, font=("Arial", 15))
        
        self.logger = defaultdict(str)
        self.num_games_complete = 0
        MAX_CONCURRENT_EXECUTIONS = 1
        self.semaphore = threading.Semaphore(MAX_CONCURRENT_EXECUTIONS)
        self.good_to_continue = True

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select ISO files", filetypes=(("ISO files", "*.iso"),)
        )
        for file_path in file_paths:
            if file_path not in self.file_paths:
                self.file_paths.append(file_path)
                self.listbox.insert(tk.END, file_path)
        self.group_by_game()

    def group_by_game(self):
        print("grouping games by name")
        file_path_copy = deepcopy(self.file_paths)
        self.game_name_to_files = get_game_name_to_file_paths_map(file_path_copy)
        self.num_games = len(self.game_name_to_files.keys())

    def combine_files(self):
        if not self.file_paths:
            return
        self.threads = []
        for game, paths in self.game_name_to_files.items():
            print(f"processing game {game}")
            if not paths:
                continue
            if len(paths) >= 2:
                # Generate a random string for the temporary file name
                output_dir = os.path.dirname(paths[0])
                temp_file_name = ''.join(random.choices(string.ascii_lowercase, k=8))
                temp_file_path = os.path.join(output_dir, f"{temp_file_name}.tmp")

                command = self.build_copy_command(paths, temp_file_path)         
                thread = threading.Thread(target=self.execute_command, args=(command, output_dir, game))
                self.threads.append(thread)
                print("starting thread")
                thread.start()

                self.root.after(500, self.check_progress, thread, temp_file_path, output_dir, game)
            else:
                self.logger[f"Only one .iso file selected for game {game}. No changes made to file {paths[0]}."] = "SUCCESS"
                self.num_games_complete += 1

        self.root.after(100, self.end_process)

    def enable_loading_settings(self):
        print("enabling load settings")
        self.loading_label.configure(text=f"Processing {self.num_games_complete + 1} of {self.num_games}")
        self.loading_label.pack(side=tk.BOTTOM, pady=20)
        self.browse_button.configure(state=tk.DISABLED)
        self.combine_button.configure(state=tk.DISABLED)
        self.clear_button.configure(state=tk.DISABLED)

    def build_copy_command(self, paths, temp_file_path):
        command = f'copy /b "{paths[0]}"'
        for file in paths[1:]:
            command += f' /b + "{file}"'
        command += f' /b "{temp_file_path}" /b'
        return command

    def execute_command(self, command, source_dir, game):
        print("executing command")
        self.semaphore.acquire()
        if not self.good_to_continue:
            self.cancel_and_exit_gracefully()
            return
        self.enable_loading_settings()
        try:
            current_dir = os.getcwd()
            os.chdir(source_dir)
            result = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True,shell=True,encoding='utf-8')
            output = result.stdout.strip()
            os.chdir(current_dir)
        except subprocess.CalledProcessError as e:
            # format error message
            error_message = e.output.strip() if e.output else str(e)
            prefix = f"Error occured while combining ISOs for game {game}: "
            error_message_as_list = error_message.split("\n")
            error_message_as_list[0] = prefix
            error_message = "".join(line for line in error_message_as_list)
            self.logger[str(error_message)] = "FAILED"
            self.cancel_and_exit_gracefully()

    def cancel_and_exit_gracefully(self):
        print("cancelling")
        self.good_to_continue = False    
        self.semaphore.release()

    def check_progress(self, thread, temp_file_path, output_dir, game):
        if thread.is_alive() and self.good_to_continue:
            self.root.after(100, self.check_progress, thread, temp_file_path, output_dir, game)
        elif not thread.is_alive() and self.good_to_continue:
            self.rename_tmp_file(output_dir, game, temp_file_path)

    def rename_tmp_file(self, output_dir, game, temp_file_path):
        try:
            # Rename the temporary file to the final output file
            DEFAULT_SUFFIX = ".COMBINED.iso" 
            combined_file_path = os.path.join(output_dir, game + DEFAULT_SUFFIX)
            final_file_path = create_unique_filename(combined_file_path)
            os.rename(temp_file_path, final_file_path)
            self.logger[f"Game {game} combined succesfully at {final_file_path}"] = "SUCCESS"
            self.num_games_complete += 1
            self.semaphore.release()
        except Exception as e:
            prefix = f"Error occured while combining ISOs for game {game}: "
            error_message = prefix + str(e)
            self.logger[error_message] = "FAILED"
            self.cancel_and_exit_gracefully()

    def end_process(self):
        if self.good_to_continue and not self.are_all_games_done():
            self.root.after(5000, self.end_process)
            return
        if not self.good_to_continue:
            self.cancel_and_exit_gracefully()
        self.loading_label.pack_forget()
        print("done")
        if self.logger:
            print("dummping logs")
            final_message = "SUMMARY: \n"
            count = 1
            for log, log_status in self.logger.items():
                final_message += f"{count}. {log_status}: {log}\n"
                count += 1
            status = "SUCCESS" if self.good_to_continue else "FAILED"
            tk.messagebox.showinfo(
                    status, final_message
                )
        self.reset_state()
            
    def are_all_games_done(self):
        return self.num_games_complete == self.num_games
    
    def reset_state(self):
        self.clear_files()
        self.browse_button.configure(state=tk.NORMAL)
        self.combine_button.configure(state=tk.NORMAL)
        self.clear_button.configure(state=tk.NORMAL)

    def clear_files(self):
        self.file_paths = []
        self.game_name_to_files.clear()
        self.logger = defaultdict(str)
        self.good_to_continue = True
        self.num_games = self.num_games_complete = 0
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    ISOCombiner(root)
    root.mainloop()
