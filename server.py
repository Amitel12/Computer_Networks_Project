import socket
import threading

HOST = "0.0.0.0"  # מאזין לכל הכתובות
PORT = 10000

clients = {}  # מילון: { "שם_משתמש": socket_object }


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    current_username = None

    try:
        # קבלת שם המשתמש
        current_username = conn.recv(1024).decode('utf-8').strip()

        if current_username in clients:
            conn.sendall("Username taken".encode('utf-8'))
            conn.close()
            return

        clients[current_username] = conn
        print(f"[REGISTERED] {current_username}")

        # שלח לכולם עדכון שמישהו הצטרף + רשימת משתמשים חדשה
        broadcast_user_list()

        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')

            # --- טיפול בהודעה פרטית ---
            if message.startswith("@"):
                # פורמט מצופה: @TargetName: Message text
                try:
                    target_name, msg_content = message[1:].split(":", 1)
                    target_name = target_name.strip()
                    send_private_message(current_username, target_name, msg_content)
                except ValueError:
                    pass  # פורמט לא תקין
            else:
                # הודעה רגילה (לכולם - General Chat)
                broadcast(f"{current_username}: {message}", current_username)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if current_username in clients:
            del clients[current_username]
            broadcast_user_list()  # עדכון רשימה אחרי יציאה
        conn.close()


def broadcast_user_list():
    """שולח לכולם את רשימת המחוברים העדכנית בפורמט מיוחד"""
    users = ",".join(clients.keys())
    system_msg = f"USERS_UPDATE:{users}"
    for conn in clients.values():
        try:
            conn.sendall(system_msg.encode('utf-8'))
        except:
            pass


def send_private_message(sender, target, message):
    """שליחת הודעה פרטית"""
    if target in clients:
        target_conn = clients[target]
        formatted_msg = f"(Private) {sender}: {message}"
        try:
            target_conn.sendall(formatted_msg.encode('utf-8'))
        except:
            pass


def broadcast(message, sender_name):
    """שליחה לכולם (צ'אט כללי)"""
    for name, conn in clients.items():
        if name != sender_name:
            try:
                conn.sendall(message.encode('utf-8'))
            except:
                pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()