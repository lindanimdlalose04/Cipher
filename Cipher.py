import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Vigenère Cipher Logic 
def vigenere(text, key, direction=1):
    result = ""
    key = key.upper()
    key_index = 0

    for char in text:
        if char.isalpha():
            shift = (ord(key[key_index % len(key)]) - ord('A')) * direction
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
            result += new_char
            key_index += 1
        else:
            result += char  

    return result

# File Functions 
def import_txt_to(widget):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            widget.delete("1.0", "end")
            widget.insert("1.0", file.read())

def export_txt_from(content):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Success", "File saved successfully!")

#Encryption
def handle_encrypt(input_widget, output_widget, key_entry):
    text = input_widget.get("1.0", "end").strip()
    key = key_entry.get().strip()

    if not key.isalpha():
        messagebox.showerror("Invalid Key", "Key must contain only letters.")
        return

    result = vigenere(text, key, direction=1)
    output_widget.delete("1.0", "end")
    output_widget.insert("1.0", result)

#Decryption
def handle_decrypt(input_widget, output_widget, key_entry):
    text = input_widget.get("1.0", "end").strip()
    key = key_entry.get().strip()

    if not key.isalpha():
        messagebox.showerror("Invalid Key", "Key must contain only letters.")
        return

    result = vigenere(text, key, direction=-1)
    output_widget.delete("1.0", "end")
    output_widget.insert("1.0", result)

# Tabs 
def build_tab(parent, mode="encrypt"):
    is_encrypt = (mode == "encrypt")
    title = "Encrypt" if is_encrypt else "Decrypt"
    action_color = "#007acc" if is_encrypt else "#d9534f"
    button_text = "Encrypt" if is_encrypt else "Decrypt"
    export_text = "Export Encrypted File" if is_encrypt else "Export Decrypted File"

    frame = tk.Frame(parent, bg="#f4f4f4")

    #the custome Key Field
    tk.Label(frame, text="Key (letters only):", bg="#f4f4f4").pack(pady=5)
    key_entry = tk.Entry(frame, width=40)
    key_entry.pack(pady=5)

    #Importing the file
    input_text = tk.Text(frame, height=8, width=80)
    tk.Button(frame, text="Import .txt File", command=lambda: import_txt_to(input_text)).pack(pady=5)
    tk.Label(frame, text="Input Text:", bg="#f4f4f4").pack()
    input_text.pack(pady=5)

    #Encrypt/Decrypt Button
    output_text = tk.Text(frame, height=8, width=80, bg="#ffffff")
    action_func = handle_encrypt if is_encrypt else handle_decrypt
    tk.Button(frame, text=button_text, width=20, bg=action_color, fg="white",
              command=lambda: action_func(input_text, output_text, key_entry)).pack(pady=10)

    #Output and Export
    tk.Label(frame, text="Output Text:", bg="#f4f4f4").pack()
    output_text.pack(pady=5)
    tk.Button(frame, text=export_text, command=lambda: export_txt_from(output_text.get("1.0", "end").strip())).pack(pady=10)

    return frame

#GUI Setup
def main():
    root = tk.Tk()
    root.title("Vigenère Cipher Tool")
    root.geometry("700x600")
    root.configure(bg="#f4f4f4")
    #Tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    #Encrypt and Decrypt Tabs
    notebook.add(build_tab(notebook, mode="encrypt"), text="Encrypt")
    notebook.add(build_tab(notebook, mode="decrypt"), text="Decrypt")

    root.mainloop()

# Run the App
if __name__ == "__main__":
    main()
