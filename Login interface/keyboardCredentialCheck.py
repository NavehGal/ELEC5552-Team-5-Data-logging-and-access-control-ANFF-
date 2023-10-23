from tkinter import *
import subprocess

wget_command = "wget -r -nH -np -R 'index.html*' http://172.20.10.3/credentialList/"

try:
    subprocess.run(wget_command, shell=True, check=True)
    print("wget command executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing wget command: {e}")


success_screen = None
student_accounts = {}  

# Callback function to return to the login screen
def return_to_login():
    global success_screen
    success_screen.destroy()
    win.deiconify()
    # Clear the values in the input fields
    uname.delete(0, END)
    pwd.delete(0, END)
    write_to_output(0)

# Create the interface after successful login
def create_success_screen(username):
    global success_screen
    success_screen = Toplevel()
    success_screen.title('Success')
    # Get the screen width and height
    screen_width = success_screen.winfo_screenwidth()
    screen_height = success_screen.winfo_screenheight()
    # Calculate the coordinates of the window to center it
    x = (screen_width - 500) // 2
    y = (screen_height - 200) // 2
    success_screen.geometry(f'500x200+{x}+{y}')  # Set the window position to center
    # Create a frame to contain content and buttons
    frame = Frame(success_screen)
    frame.grid(row=0, column=0)
    Label(frame, text='Welcome, ' + username).grid(row=0, column=0, padx=10, pady=10)
    Label(frame, text='Machine Status: Activated').grid(row=1, column=0, padx=10, pady=10)
    # Add a return button
    return_button = Button(frame, text='Return to Login', command=return_to_login)
    return_button.grid(row=2, column=0, padx=10, pady=10)
    # Use columnconfigure and rowconfigure to ensure that the frame is centered within the window
    success_screen.columnconfigure(0, weight=1)
    success_screen.rowconfigure(0, weight=1)

# Create the interface for login failure
def create_failure_screen():
    failure_screen = Toplevel()
    failure_screen.title('Failure')
    failure_screen.geometry('300x100')
    Label(failure_screen, text='Login Failed. Incorrect account or password.').pack()

def read_student_accounts():
    file_path = "/home/pi/credentialList/Account.txt"  # 请替换为实际文件路径
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i in range(0, len(lines), 2):
        account = lines[i].strip()
        password = lines[i + 1].strip()
        student_accounts[account] = password

def login():
    username = uname.get()
    password = pwd.get()

    if username in student_accounts and student_accounts[username] == password:
        print('Login successful')
        win.withdraw()  
        create_success_screen(username)  
        write_to_output(1)
    else:
        print('Login failed')
        create_failure_screen()  
        write_to_output(0)

def write_to_output(value):
    file_path = "/home/pi/isolatorOutput.txt"
    with open(file_path, 'w') as file:
        file.write(str(value))

def add_char(char):
    if uname.focus_get() == uname:
        uname.insert(END, char)
    elif pwd.focus_get() == pwd:
        pwd.insert(END, char)


def delete_char():
    if uname.focus_get() == uname:
        current_text = uname.get()
        if current_text:
            new_text = current_text[:-1]
            uname.delete(0, END)
            uname.insert(0, new_text)
    elif pwd.focus_get() == pwd:
        current_text = pwd.get()
        if current_text:
            new_text = current_text[:-1]
            pwd.delete(0, END)
            pwd.insert(0, new_text)


win = Tk()
win.title('LOGIN')
win.geometry('500x500')
win.resizable(1, 1)

# Toggle the case (uppercase/lowercase) of the letter interface
caps_lock = BooleanVar()
caps_lock.set(False)  # Initial state is lowercase
def toggle_caps_lock():
    caps_lock.set(not caps_lock.get())
    update_keyboard_layout()
# Update the letter case (uppercase/lowercase) status on the keyboard buttons
def update_keyboard_layout():
    for row_buttons in buttons:
        for button in row_buttons:
            char = button["text"]
            if caps_lock.get():
                char = char.upper()
            else:
                char = char.lower()
            button.config(text=char, command=lambda char=char: add_char(char))  # Update button command function


frame1 = Frame(win)
frame1.pack(side=TOP, pady=40)

Label(frame1, text='Account:').grid(row=0, column=0, padx=10, pady=10)
uname = Entry(frame1)
uname.grid(row=0, column=1, padx=10, pady=10)

Label(frame1, text='Password:').grid(row=1, column=0, padx=10, pady=10)
pwd = Entry(frame1, show='*')
pwd.grid(row=1, column=1, padx=10, pady=10)

button_frame = Frame(win)
button_frame.pack(side=TOP, pady=5)

Button(button_frame, text='Enter', command=login, width=10).pack(side=LEFT, padx=5)
Button(button_frame, text='Delete', command=delete_char, width=10).pack(side=LEFT, padx=5)
Button(button_frame, text='Cap Switch', command=toggle_caps_lock, width=10).pack(side=LEFT, padx=5)


keyboard_layout = [
    '1234567890abcdefg',
    'hijklmnopqrstuvwx',
    'yz!@#$%^&*(),.?;:',
]

frame2 = Frame(win)
frame2.pack(side=TOP)

row_frames = []
buttons = []

for row_layout in keyboard_layout:
    row_frame = Frame(frame2)
    row_frame.pack(side=TOP)
    row_frames.append(row_frame)
    row_buttons = []
    buttons.append(row_buttons)

    for char in row_layout:
        button = Button(row_frame, text=char, width=3, height=1, command=lambda char=char: add_char(char))
        button.pack(side=LEFT, padx=2, pady=2)
        row_buttons.append(button)


win.update()
x = (win.winfo_screenwidth() - win.winfo_reqwidth()) // 2
y = (win.winfo_screenheight() - win.winfo_reqheight()) // 2
win.geometry(f'+{x}+{y}')

read_student_accounts() # 3
win.mainloop()
