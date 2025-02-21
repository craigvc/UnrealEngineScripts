import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import json
import platform
import shlex  # Import for safely handling shell arguments

CONFIG_FILE = "config.json"

INSTRUCTIONS = """
Instructions:
1. Select your Unreal Engine root folder (e.g., I:/5.5).
2. Choose the .uplugin file of the plugin you want to build.
3. Select the target output folder where the packaged plugin will be stored.
4. Choose the target platform from the dropdown.
5. Check any optional flags if needed.
6. Click 'Build Plugin' to start the process.
"""

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config():
    config = {
        "ue_root": ue_root_var.get(),
        "source_plugin": source_var.get(),
        "target_folder": target_var.get(),
        "target_platform": platform_var.get()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def update_engine_version(plugin_path, ue_version):
    try:
        if not os.path.exists(plugin_path):
            messagebox.showerror("Error", "Plugin file does not exist.")
            return
        with open(plugin_path, "r") as file:
            data = json.load(file)
        
        if "EngineVersion" in data:
            data["EngineVersion"] = ue_version
        
        with open(plugin_path, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update engine version: {e}")

def run_command():
    ue_root = ue_root_var.get().strip()
    source_plugin = source_var.get().strip()
    target_folder = target_var.get().strip()
    target_platform = platform_var.get().strip()
    additional_flags = []

    if clean_var.get():
        additional_flags.append("-Clean")
    if no_compile_var.get():
        additional_flags.append("-NoCompile")
    if verbose_var.get():
        additional_flags.append("-Verbose")

    if not ue_root or not source_plugin or not target_folder or not target_platform:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return

    uat_script = "RunUAT.bat" if platform.system() == "Windows" else "RunUAT.sh"
    uat_path = os.path.join(ue_root, "Engine", "Build", "BatchFiles", uat_script)

    if platform.system() != "Windows":
        subprocess.run(["chmod", "+x", uat_path], check=False)

    # Properly format command to avoid double quotes
    command = [
        uat_path,
        "BuildPlugin",
        f"-Plugin={shlex.quote(source_plugin)}",
        f"-Package={shlex.quote(target_folder)}",
        f"-TargetPlatforms={shlex.quote(target_platform)}",
        *additional_flags
    ]

    save_config()
    update_engine_version(source_plugin, os.path.basename(ue_root))
    output_text.delete(1.0, tk.END)

    def execute():
        output_text.insert(tk.END, f"Executing: {' '.join(command)}\n")
        output_text.see(tk.END)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False, cwd=os.path.dirname(uat_path))
        for line in process.stdout:
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
        for line in process.stderr:
            output_text.insert(tk.END, line, "error")
            output_text.see(tk.END)
        process.wait()

    threading.Thread(target=execute, daemon=True).start()

def browse_ue_root():
    folder_path = filedialog.askdirectory()
    if folder_path:
        ue_root_var.set(folder_path)

def browse_source():
    file_path = filedialog.askopenfilename(filetypes=[("Unreal Plugin", "*.uplugin")])
    if file_path:
        source_var.set(file_path)

def browse_target():
    folder_path = filedialog.askdirectory()
    if folder_path:
        target_var.set(folder_path)

# GUI Setup
root = tk.Tk()
root.title("Unreal Plugin Builder")
config = load_config()

ue_root_var = tk.StringVar(value=config.get("ue_root", ""))
source_var = tk.StringVar(value=config.get("source_plugin", ""))
target_var = tk.StringVar(value=config.get("target_folder", ""))
platform_var = tk.StringVar(value=config.get("target_platform", "Win64"))
clean_var = tk.BooleanVar()
no_compile_var = tk.BooleanVar()
verbose_var = tk.BooleanVar()

platform_options = ["Win64", "Mac", "Linux", "Android", "IOS"]

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text=INSTRUCTIONS, justify="left", padx=10, pady=10).grid(row=0, column=0, columnspan=3)

tk.Label(frame, text="Unreal Engine Root:").grid(row=1, column=0, sticky="w")
tk.Entry(frame, textvariable=ue_root_var, width=50).grid(row=1, column=1)
tk.Button(frame, text="Browse", command=browse_ue_root).grid(row=1, column=2)

tk.Label(frame, text="Source Plugin:").grid(row=2, column=0, sticky="w")
tk.Entry(frame, textvariable=source_var, width=50).grid(row=2, column=1)
tk.Button(frame, text="Browse", command=browse_source).grid(row=2, column=2)

tk.Label(frame, text="Target Folder:").grid(row=3, column=0, sticky="w")
tk.Entry(frame, textvariable=target_var, width=50).grid(row=3, column=1)
tk.Button(frame, text="Browse", command=browse_target).grid(row=3, column=2)

tk.Label(frame, text="Target Platform:").grid(row=4, column=0, sticky="w")
platform_menu = ttk.Combobox(frame, textvariable=platform_var, values=platform_options, state="readonly")
platform_menu.grid(row=4, column=1)
platform_menu.current(0)

tk.Checkbutton(frame, text="Clean", variable=clean_var).grid(row=5, column=0, sticky="w")
tk.Checkbutton(frame, text="No Compile", variable=no_compile_var).grid(row=5, column=1, sticky="w")
tk.Checkbutton(frame, text="Verbose Output", variable=verbose_var).grid(row=5, column=2, sticky="w")

tk.Button(frame, text="Build Plugin", command=run_command).grid(row=6, column=1, pady=10)

output_text = tk.Text(frame, height=10, width=80)
output_text.grid(row=7, column=0, columnspan=3)
output_text.tag_configure("error", foreground="red")

root.mainloop()
