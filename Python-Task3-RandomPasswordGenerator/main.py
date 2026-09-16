import tkinter as tk
from tkinter import messagebox
import string
import secrets

SKY_BLUE = "#87CEEB"
WHITE = "#FFFFFF"
DARK_BLUE = "#00008B"
BLACK = "#000000"

root = tk.Tk()
root.title("PASSFORGE - Smart Password Generator & Security Tool")
root.geometry("900x650")
root.resizable(False, False)
root.configure(bg=SKY_BLUE)

length_var = tk.IntVar(value=12)
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar(value=False)

password_hidden = False
password_history = []


def check_strength(event=None):
    password = password_entry.get()

    if not password:
        strength_label.config(text="Password Strength: --")
        return

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    strength_label.config(
        text="Password Strength: " + strength
    )


def generate_password():
    length = length_var.get()
    characters = ""

    if uppercase_var.get():
        characters += string.ascii_uppercase

    if lowercase_var.get():
        characters += string.ascii_lowercase

    if numbers_var.get():
        characters += string.digits

    if symbols_var.get():
        characters += string.punctuation

    if not characters:
        messagebox.showwarning(
            "Warning",
            "Please select at least one character type."
        )
        return

    if exclude_var.get():
        confusing = "O0Il1"
        characters = "".join(
            c for c in characters
            if c not in confusing
        )

    if not characters:
        messagebox.showwarning(
            "Warning",
            "No characters are available with the selected options."
        )
        return

    password = ""

    for i in range(length):
        password += secrets.choice(characters)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    password_entry.config(show="")

    global password_hidden
    password_hidden = False
    show_button.config(text="Hide")

    password_history.insert(0, password)

    if len(password_history) > 5:
        password_history.pop()

    update_history()
    check_strength()

    status_label.config(
        text="Password generated successfully!"
    )


def show_hide_password():
    global password_hidden

    if password_hidden:
        password_entry.config(show="")
        show_button.config(text="Hide")
        password_hidden = False
    else:
        password_entry.config(show="*")
        show_button.config(text="Show")
        password_hidden = True


def copy_password():
    password = password_entry.get()

    if not password:
        messagebox.showwarning(
            "Warning",
            "Please enter or generate a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    status_label.config(
        text="Password copied successfully!"
    )


def clear_history():
    password_history.clear()
    update_history()


def update_history():
    for widget in history_frame.winfo_children():
        widget.destroy()

    if not password_history:
        label = tk.Label(
            history_frame,
            text="No recent passwords",
            font=("Arial", 10),
            bg=WHITE,
            fg=BLACK
        )
        label.pack(pady=8)
        return

    for password in password_history:
        label = tk.Label(
            history_frame,
            text=password,
            font=("Consolas", 10),
            bg=WHITE,
            fg=BLACK,
            anchor="w"
        )
        label.pack(
            fill="x",
            padx=12,
            pady=2
        )


header_frame = tk.Frame(
    root,
    bg=SKY_BLUE
)

header_frame.pack(
    fill="x",
    pady=(25, 10)
)

title_label = tk.Label(
    header_frame,
    text="🔐 PASSFORGE",
    font=("Arial", 30, "bold"),
    bg=SKY_BLUE,
    fg=DARK_BLUE
)

title_label.pack()

subtitle_label = tk.Label(
    header_frame,
    text="Smart Password Generator & Security Tool",
    font=("Arial", 12),
    bg=SKY_BLUE,
    fg=BLACK
)

subtitle_label.pack(
    pady=(4, 0)
)


settings_frame = tk.Frame(
    root,
    bg=WHITE,
    padx=25,
    pady=15
)

settings_frame.pack(
    padx=50,
    fill="x"
)

settings_title = tk.Label(
    settings_frame,
    text="PASSWORD SETTINGS",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
)

settings_title.pack(
    anchor="w",
    pady=(0, 8)
)


length_row = tk.Frame(
    settings_frame,
    bg=WHITE
)

length_row.pack(
    fill="x",
    pady=3
)

length_text = tk.Label(
    length_row,
    text="Password length (8–32 characters)",
    font=("Arial", 10),
    bg=WHITE,
    fg=BLACK
)

length_text.pack(
    side="left"
)

length_spinbox = tk.Spinbox(
    length_row,
    from_=8,
    to=32,
    textvariable=length_var,
    width=5,
    font=("Arial", 10)
)

length_spinbox.pack(
    side="left",
    padx=15
)


character_label = tk.Label(
    settings_frame,
    text="Character types",
    font=("Arial", 10),
    bg=WHITE,
    fg=BLACK
)

character_label.pack(
    anchor="w",
    pady=(5, 2)
)


character_frame = tk.Frame(
    settings_frame,
    bg=WHITE
)

character_frame.pack(
    anchor="w"
)


tk.Checkbutton(
    character_frame,
    text="Uppercase A-Z",
    variable=uppercase_var,
    bg=WHITE,
    fg=BLACK,
    activebackground=WHITE
).grid(
    row=0,
    column=0,
    sticky="w"
)


tk.Checkbutton(
    character_frame,
    text="Lowercase a-z",
    variable=lowercase_var,
    bg=WHITE,
    fg=BLACK,
    activebackground=WHITE
).grid(
    row=0,
    column=1,
    sticky="w",
    padx=15
)


tk.Checkbutton(
    character_frame,
    text="Numbers 0-9",
    variable=numbers_var,
    bg=WHITE,
    fg=BLACK,
    activebackground=WHITE
).grid(
    row=1,
    column=0,
    sticky="w"
)


tk.Checkbutton(
    character_frame,
    text="Symbols !@#$",
    variable=symbols_var,
    bg=WHITE,
    fg=BLACK,
    activebackground=WHITE
).grid(
    row=1,
    column=1,
    sticky="w",
    padx=15
)


tk.Checkbutton(
    settings_frame,
    text="Exclude confusing characters (O, 0, I, l, 1)",
    variable=exclude_var,
    bg=WHITE,
    fg=BLACK,
    activebackground=WHITE
).pack(
    anchor="w",
    pady=(4, 0)
)


password_frame = tk.Frame(
    root,
    bg=WHITE,
    padx=25,
    pady=15
)

password_frame.pack(
    padx=50,
    pady=10,
    fill="x"
)


password_title = tk.Label(
    password_frame,
    text="YOUR SECURE PASSWORD",
    font=("Arial", 13, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
)

password_title.pack(
    anchor="w",
    pady=(0, 8)
)


entry_frame = tk.Frame(
    password_frame,
    bg=WHITE
)

entry_frame.pack(
    fill="x"
)


password_entry = tk.Entry(
    entry_frame,
    font=("Consolas", 13),
    bg=WHITE,
    fg=BLACK,
    relief="solid",
    bd=1,
    show=""
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=7
)


show_button = tk.Button(
    entry_frame,
    text="Hide",
    command=show_hide_password,
    bg=SKY_BLUE,
    fg=BLACK,
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=15,
    pady=7
)

show_button.pack(
    side="right",
    padx=(8, 0)
)


strength_label = tk.Label(
    password_frame,
    text="Password Strength: --",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=BLACK
)

strength_label.pack(
    anchor="e",
    pady=(5, 2)
)


status_label = tk.Label(
    password_frame,
    text="",
    font=("Arial", 9),
    bg=WHITE,
    fg=BLACK
)

status_label.pack(
    anchor="e"
)


button_frame = tk.Frame(
    root,
    bg=SKY_BLUE
)

button_frame.pack(
    padx=50,
    fill="x"
)


generate_button = tk.Button(
    button_frame,
    text="⚡  GENERATE PASSWORD",
    command=generate_password,
    bg=DARK_BLUE,
    fg=WHITE,
    font=("Arial", 11, "bold"),
    relief="flat",
    pady=10
)

generate_button.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)


copy_button = tk.Button(
    button_frame,
    text="COPY",
    command=copy_password,
    bg=SKY_BLUE,
    fg=BLACK,
    font=("Arial", 10, "bold"),
    relief="flat",
    pady=10
)

copy_button.pack(
    side="right",
    padx=(5, 0)
)


recent_frame = tk.Frame(
    root,
    bg=WHITE,
    padx=15,
    pady=10
)

recent_frame.pack(
    padx=50,
    pady=10,
    fill="x"
)



recent_header = tk.Frame(
    recent_frame,
    bg=WHITE
)

recent_header.pack(
    fill="x"
)


recent_title = tk.Label(
    recent_header,
    text="RECENT PASSWORDS",
    font=("Arial", 12, "bold"),
    bg=WHITE,
    fg=DARK_BLUE
)

recent_title.pack(
    side="left"
)


clear_button = tk.Button(
    recent_header,
    text="Clear",
    command=clear_history,
    bg=SKY_BLUE,
    fg=BLACK,
    font=("Arial", 9, "bold"),
    relief="flat",
    padx=10
)

clear_button.pack(
    side="right"
)


history_frame = tk.Frame(
    recent_frame,
    bg=WHITE,
    height=55
)

history_frame.pack(
    fill="x",
    pady=(5, 0)
)

history_frame.pack_propagate(False)


footer_label = tk.Label(
    root,
    text="Secure password generation using Python",
    font=("Arial", 9),
    bg=SKY_BLUE,
    fg=BLACK
)

footer_label.pack(
    pady=5
)


password_entry.bind(
    "<KeyRelease>",
    check_strength
)

update_history()

root.mainloop()
