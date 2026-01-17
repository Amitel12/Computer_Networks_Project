import socket
import threading
import tkinter as tk
from tkinter import messagebox
import ctypes

# הגדרות ברירת מחדל
DEFAULT_IP = "192.168.1.120"
DEFAULT_PORT = 10000

# --- צבעים ועיצוב ---
BG_COLOR = "#1e1f22"
SIDEBAR_COLOR = "#2b2d31"
TEXT_COLOR = "#dbdee1"
ACCENT_COLOR = "#5865F2"
ENTRY_BG = "#383a40"
ONLINE_COLOR = "#23a559"  # ירוק
OFFLINE_COLOR = "#80848e"  # אפור
HOVER_COLOR = "#35373c"  # צבע רקע כשעוברים עם העכבר


class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x650")
        self.root.title("Chat Login")
        self.root.configure(bg=BG_COLOR)

        # השחרת כותרת (Windows)
        try:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                ctypes.windll.user32.GetParent(self.root.winfo_id()),
                20, ctypes.byref(ctypes.c_int(2)), 4)
        except:
            pass

        self.sock = None
        self.username = ""
        self.current_chat_room = "General Chat"
        self.running = False

        # --- ניהול מידע ---
        self.history = {"General Chat": []}
        self.known_users = set()
        self.online_users = set()
        self.unread_counts = {}

        # --- מסך התחברות ---
        self.login_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(self.login_frame, text="WELCOME", bg=BG_COLOR, fg="white", font=("Segoe UI", 20, "bold")).pack(pady=20)

        tk.Label(self.login_frame, text="Server IP:", bg=BG_COLOR, fg="#b9bbbe").pack(anchor="w")
        self.entry_ip = tk.Entry(self.login_frame, bg=ENTRY_BG, fg="white", font=("Segoe UI", 12), bd=0,
                                 insertbackground="white")
        self.entry_ip.insert(0, DEFAULT_IP)
        self.entry_ip.pack(fill=tk.X, ipady=5, pady=(0, 10))

        tk.Label(self.login_frame, text="Username:", bg=BG_COLOR, fg="#b9bbbe").pack(anchor="w")
        self.entry_user = tk.Entry(self.login_frame, bg=ENTRY_BG, fg="white", font=("Segoe UI", 12), bd=0,
                                   insertbackground="white")
        self.entry_user.pack(fill=tk.X, ipady=5, pady=(0, 20))
        self.entry_user.bind("<Return>", self.connect_to_server)

        self.btn_connect = tk.Button(self.login_frame, text="Join Chat", command=self.connect_to_server,
                                     bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 11, "bold"), bd=0, cursor="hand2")
        self.btn_connect.pack(fill=tk.X, ipady=8)

        self.main_chat_layout = tk.Frame(self.root, bg=BG_COLOR)

    def connect_to_server(self, event=None):
        ip = self.entry_ip.get()
        user = self.entry_user.get()

        if not user:
            messagebox.showwarning("Missing Info", "Please enter a username.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(3)
            self.sock.connect((ip, DEFAULT_PORT))

            self.sock.sendall(user.encode('utf-8'))
            response = self.sock.recv(1024).decode('utf-8')

            if response == "Username taken":
                messagebox.showerror("Login Error", f"The username '{user}' is already taken.")
                self.sock.close()
                return

            self.sock.settimeout(None)
            self.username = user
            self.setup_chat_ui()

            if "Welcome back" in response:
                self.save_to_history("General Chat", "System", response, False)

        except Exception as e:
            messagebox.showerror("Connection Failed", f"Could not connect to {ip}:{DEFAULT_PORT}")
            return
    def setup_chat_ui(self):
        self.login_frame.destroy()
        self.main_chat_layout.pack(fill=tk.BOTH, expand=True)
        self.root.title(f"Dark Chat - {self.username}")
        self.running = True

        # --- צד שמאל: רשימת משתמשים (עכשיו עם Text Widget במקום Listbox) ---
        sidebar = tk.Frame(self.main_chat_layout, bg=SIDEBAR_COLOR, width=240)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="CHATS", bg=SIDEBAR_COLOR, fg="#80848e", font=("Segoe UI", 9, "bold")).pack(pady=15,
                                                                                                           padx=15,
                                                                                                           anchor="w")

        # שינוי: שימוש ב-Text במקום Listbox כדי לאפשר צבעים מרובים בשורה אחת
        self.users_sidebar = tk.Text(sidebar, bg=SIDEBAR_COLOR, fg=TEXT_COLOR, bd=0,
                                     font=("Segoe UI", 11), state="disabled", cursor="hand2",
                                     padx=10, pady=5)
        self.users_sidebar.pack(fill=tk.BOTH, expand=True)

        # הגדרת תגיות לצבעים
        self.users_sidebar.tag_config("online_dot", foreground=ONLINE_COLOR)  # ירוק לנקודה
        self.users_sidebar.tag_config("offline_dot", foreground=OFFLINE_COLOR)  # אפור לנקודה
        self.users_sidebar.tag_config("username_text", foreground=TEXT_COLOR)  # לבן לשם
        self.users_sidebar.tag_config("selected_bg", background="#3f4148")  # רקע כשבוחרים

        # אירוע לחיצה על הרשימה
        self.users_sidebar.bind("<Button-1>", self.on_sidebar_click)

        # --- צד ימין: הצ'אט ---
        chat_area = tk.Frame(self.main_chat_layout, bg=BG_COLOR)
        chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        input_frame = tk.Frame(chat_area, bg=BG_COLOR)
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        self.entry_msg = tk.Entry(input_frame, bg=ENTRY_BG, fg="white", bd=0, font=("Segoe UI", 11),
                                  insertbackground="white")
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=(0, 10))
        self.entry_msg.bind("<Return>", self.send_message)

        btn_send = tk.Button(input_frame, text="Send", bg=ACCENT_COLOR, fg="white", bd=0,
                             command=self.send_message, font=("Segoe UI", 10, "bold"))
        btn_send.pack(side=tk.RIGHT, ipadx=15, ipady=6)

        self.header_label = tk.Label(chat_area, text="# General Chat", bg=BG_COLOR, fg="white",
                                     font=("Segoe UI", 14, "bold"))
        self.header_label.pack(side=tk.TOP, fill=tk.X, pady=15, padx=20, anchor="w")

        tk.Frame(chat_area, bg="#2b2d31", height=1).pack(fill=tk.X, padx=20)

        self.text_display = tk.Text(chat_area, bg="#313338", fg=TEXT_COLOR, bd=0, font=("Segoe UI", 10),
                                    state="disabled", padx=15, pady=15)
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=(10, 0))

        threading.Thread(target=self.receive_loop, daemon=True).start()

        # רענון ראשוני
        self.render_users_list()

    def on_sidebar_click(self, event):
        """מטפל בלחיצה על רשימת המשתמשים החדשה"""

        try:
            index = self.users_sidebar.index(f"@{event.x},{event.y}")
            line_content = self.users_sidebar.get(index + " linestart", index + " lineend").strip()

            if not line_content: return  # לחיצה על שורה ריקה

            # ניקוי השם (הורדת הנקודה והמספרים)
            # הפורמט הוא: "● Name (1)" או "● Name"
            clean_name = line_content.replace("● ", "")
            clean_name = clean_name.split(" (")[0]  # מוריד את ה-(You) או מספרי הודעות

            if "General Chat" in clean_name:
                clean_name = "General Chat"

            # עדכון החדר
            self.current_chat_room = clean_name
            self.unread_counts[clean_name] = 0  # איפוס מונה

            self.render_users_list()  # ציור מחדש (כדי לעדכן את הרקע הנבחר)

            # עדכון כותרת
            if clean_name == "General Chat":
                self.header_label.config(text="# General Chat", fg=ONLINE_COLOR)
            else:
                status_color = ONLINE_COLOR if clean_name in self.online_users else OFFLINE_COLOR
                self.header_label.config(text=f"@ {clean_name}", fg=status_color)

            self.refresh_chat_display()

        except Exception as e:
            pass

    def render_users_list(self):
        """מצייר את הרשימה עם נקודות צבעוניות אמיתיות"""
        self.users_sidebar.config(state="normal")
        self.users_sidebar.delete("1.0", tk.END)  # ניקוי

        # --- פונקציית עזר להוספת שורה ---
        def add_line(name, is_online, unread, is_special=False):
            # בחירת צבע הנקודה
            dot_tag = "online_dot" if is_online else "offline_dot"

            # האם השורה הזו נבחרה כרגע?
            bg_tag = "selected_bg" if name == self.current_chat_room else ""

            # טקסט להצגה
            display_name = name
            if name == self.username: display_name += " (You)"
            if unread > 0: display_name += f" ({unread})"

            # ציור הנקודה (העיגול)
            self.users_sidebar.insert(tk.END, "● ", (dot_tag, bg_tag))
            # ציור השם
            self.users_sidebar.insert(tk.END, display_name + "\n", ("username_text", bg_tag))

        # --- הוספת General Chat ---
        gen_unread = self.unread_counts.get("General Chat", 0)
        add_line("General Chat", True, gen_unread, True)

        # --- הוספת שאר המשתמשים ---
        sorted_users = sorted(list(self.known_users))
        for user in sorted_users:
            if user == self.username or not user: continue

            is_online = user in self.online_users
            unread = self.unread_counts.get(user, 0)
            add_line(user, is_online, unread)

        self.users_sidebar.config(state="disabled")

    # --- שאר הפונקציות נשארו ללא שינוי מהותי ---
    def refresh_chat_display(self):
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)

        if self.current_chat_room in self.history:
            for packet in self.history[self.current_chat_room]:
                self.insert_msg_to_screen(packet[0], packet[1], packet[2])

        self.text_display.see(tk.END)
        self.text_display.config(state='disabled')

    def insert_msg_to_screen(self, sender, msg, is_me):
        name_color = "#4fc3f7" if is_me else "#a0e686"
        if sender == "System": name_color = "#ed4245"

        self.text_display.insert(tk.END, f"{sender}: ", ("name_tag",))
        self.text_display.insert(tk.END, f"{msg}\n\n", ("msg_tag",))
        self.text_display.tag_config("name_tag", foreground=name_color, font=("Segoe UI", 10, "bold"))
        self.text_display.tag_config("msg_tag", foreground=TEXT_COLOR)

    def send_message(self, event=None):
        msg = self.entry_msg.get()
        if not msg: return

        try:
            if self.current_chat_room != "General Chat":
                if self.current_chat_room not in self.online_users:
                    self.save_to_history(self.current_chat_room, "System", "User is offline.", False)
                    self.refresh_chat_display()
                    self.entry_msg.delete(0, tk.END)
                    return

                full_msg = f"@{self.current_chat_room}:{msg}"
                self.sock.sendall(full_msg.encode())
                self.save_to_history(self.current_chat_room, "Me", msg, True)
            else:
                self.sock.sendall(msg.encode())
                self.save_to_history("General Chat", self.username, msg, True)

            self.entry_msg.delete(0, tk.END)
            self.refresh_chat_display()
        except:
            pass

    def receive_loop(self):
        while self.running:
            try:
                data = self.sock.recv(1024).decode('utf-8')
                if not data: break

                if data.startswith("USERS_UPDATE:"):
                    raw_users = data.split(":", 1)[1]
                    new_online_list = set(raw_users.split(",")) if raw_users else set()
                    self.process_user_update(new_online_list)
                else:
                    self.handle_incoming_message(data)
            except:
                break

        if self.running:
            self.root.after(0, lambda: messagebox.showerror("Disconnected", "Server closed connection"))
            self.root.destroy()

    def process_user_update(self, new_online_list):
        disconnected_users = self.online_users - new_online_list
        for user in disconnected_users:
            if user != self.username and user:
                self.save_to_history(user, "System", "--- User disconnected ---", False)
                if self.current_chat_room == user:
                    self.root.after(0, self.refresh_chat_display)

        self.online_users = new_online_list
        self.known_users.update(new_online_list)
        if self.username in self.online_users: self.online_users.remove(self.username)
        self.root.after(0, self.render_users_list)

    def handle_incoming_message(self, data):
        sender = "System"
        content = data
        room_name = "General Chat"

        if "(Private)" in data:
            try:
                clean_data = data.replace("(Private) ", "")
                sender, content = clean_data.split(": ", 1)
                room_name = sender
            except:
                pass
        elif ": " in data:
            sender, content = data.split(": ", 1)
            if sender == self.username: return
        else:
            content = data

        self.save_to_history(room_name, sender, content, False)

        if self.current_chat_room == room_name:
            self.root.after(0, self.refresh_chat_display)
        else:
            self.unread_counts[room_name] = self.unread_counts.get(room_name, 0) + 1
            self.root.after(0, self.render_users_list)

    def save_to_history(self, room, sender, msg, is_me):
        if room not in self.history: self.history[room] = []
        self.history[room].append((sender, msg, is_me))


if __name__ == "__main__":
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()