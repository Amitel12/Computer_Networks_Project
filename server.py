import socket
import threading

HOST = "0.0.0.0"
PORT = 10000

# מילון של משתמשים מחוברים כרגע: { "username": socket_object }
active_clients = {}
# סט של שמות משתמש שנרשמו אי פעם במערכת (כדי לזהות Reconnect)
registered_users = set()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    current_username = None

    try:
        # קבלת שם המשתמש מהלקוח
        data = conn.recv(1024)
        if not data:
            conn.close()
            return

        current_username = data.decode('utf-8').strip()

        # 1. בדיקה אם השם תפוס (מחובר כרגע)
        if current_username in active_clients:
            conn.sendall("Username taken".encode('utf-8'))
            print(f"[REJECTED] {current_username} - Name already online.")
            current_username = None  # איפוס כדי למנוע מחיקה ב-finally
            conn.close()
            return

        # 2. אישור חיבור - שליחת הודעת "OK" או הודעת ברוך הבא ללקוח
        # זה עוזר ללקוח לדעת שהשם אושר לפני שהוא עובר למסך הצאט
        if current_username in registered_users:
            welcome_back_msg = f"Welcome back, {current_username}!"
            conn.sendall(welcome_back_msg.encode('utf-8'))
            broadcast(f"System: {current_username} reconnected.", "System")
        else:
            registered_users.add(current_username)
            conn.sendall("Welcome!".encode('utf-8'))
            broadcast(f"System: {current_username} joined the chat.", "System")

        # 3. הוספה למילון המחוברים
        active_clients[current_username] = conn
        print(f"[REGISTERED] {current_username}")

        # 4. עדכון רשימת המשתמשים לכולם (כולל למצטרף החדש)
        broadcast_user_list()

        # 5. לולאת קבלת הודעות
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')

            # טיפול בהודעה פרטית
            if message.startswith("@"):
                try:
                    target_name, msg_content = message[1:].split(":", 1)
                    send_private_message(current_username, target_name.strip(), msg_content)
                except ValueError:
                    pass
            else:
                # הודעה לכולם
                broadcast(f"{current_username}: {message}", current_username)

    except Exception as e:
        print(f"[ERROR] with {current_username}: {e}")
    finally:
        # ניקוי בזמן התנתקות
        if current_username and current_username in active_clients:
            del active_clients[current_username]
            print(f"[DISCONNECTED] {current_username}")
            # שליחת רשימה מעודכנת אחרי שמישהו יצא
            broadcast_user_list()
        conn.close()


def broadcast_user_list():
    """שולח לכל המחוברים את רשימת השמות העדכנית"""
    users = ",".join(active_clients.keys())
    system_msg = f"USERS_UPDATE:{users}"
    for name, conn in active_clients.items():
        try:
            conn.sendall(system_msg.encode('utf-8'))
        except Exception as e:
            print(f"[BROADCAST ERROR] Could not send list to {name}")


def send_private_message(sender, target, message):
    """שליחת הודעה פרטית למשתמש ספציפי"""
    if target in active_clients:
        target_conn = active_clients[target]
        formatted_msg = f"(Private) {sender}: {message}"
        try:
            target_conn.sendall(formatted_msg.encode('utf-8'))
        except:
            pass
    else:
        # אופציונלי: שליחת הודעה חזרה לשולח שהיעד לא מחובר
        if sender in active_clients:
            active_clients[sender].sendall(f"System: User {target} is not online.".encode('utf-8'))


def broadcast(message, sender_name):

    for name, conn in active_clients.items():
        if name != sender_name:
            try:
                conn.sendall(message.encode('utf-8'))
            except:
                pass


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # פתרון לבעיית "Address already in use"
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()