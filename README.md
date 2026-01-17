# 📡 TCP/IP Networking Project: Encapsulation & Chat Application

This repository contains a comprehensive networking project divided into two main parts:
1. Network Encapsulation Analysis: A simulation of the TCP/IP stack using Python and Wireshark.
2. TCP Chat System: A fully functional, multi-threaded GUI chat application supporting private messaging, real-time status updates, and session persistence.

---

## 📂 Project Structure

<img width="682" height="175" alt="image" src="https://github.com/user-attachments/assets/ce0dd6ae-78a4-4159-a88f-1e098cb8c780" />

Libraries: socket, threading, tkinter, scapy, pandas

---

## 1️⃣ Part 1: Encapsulation Simulation & Analysis
In this section, we manually craft TCP/IP packets based on application data (HTTP messages) to demonstrate how encapsulation works in the network stack.

### Features
* Data Injection: Reads application messages from a CSV file (group02_http_input.csv).
* Manual Stack Construction: Uses Scapy to encapsulate raw data into TCP segments and IP packets.
* Network Transmission: Sends packets over the local network interface (Loopback).
* Deep Packet Inspection: Traffic is analyzed using Wireshark to verify headers, checksums, ports, and payloads.

---

## 2️⃣ Part 2: TCP Chat Application (GUI)
A robust client-server chat application designed with a modern, dark-themed GUI. It demonstrates advanced socket programming, concurrent threading, and custom protocol design.

### Key Features
* Real-time Communication: Uses TCP sockets for reliable, ordered message delivery.
* Multi-User Architecture: The server manages multiple clients simultaneously using unique threads for each connection.
* Private Messaging (Unicast): Direct messaging support. Simply click a user's name in the sidebar to switch from General Chat to a private room.
* General Chat (Broadcast): Default room for global communication across all connected users.

### Identity & Connection Management
* Duplicate Name Protection: The server prevents multiple logins with the same username. If a name is already active, the client receives a "Username Taken" error and is denied access.
* Reconnection Logic: The system recognizes returning users. If a user disconnects and joins again, they are greeted with a "Reconnected" status, and the server broadcasts their return to the chat.
* Thread-Safe Registration: The server utilizes atomic checks to ensure that two users cannot claim the same name even if they attempt to connect at the exact same millisecond.
* Graceful Disconnection: The server handles client departures by cleaning up active sockets and notifying other participants instantly.

### Visual Status & UI
* Dynamic Sidebar:
    * 🟢 Green Dot: User is currently online and active.
    * ⚪ Grey Dot: User has disconnected but remains in the known users list.
* Unread Message Counters: Visual notifications (N) appear next to usernames when messages are received in a background chat room.
* User History Persistence: Chat history is locally cached during the session and separated between the General Chat and individual private conversations.

---

## 🚀 How to Run (Step-by-Step)

### 🪟 Windows Instructions
1. **Prerequisites**: Ensure Python 3.x is installed. Install required libraries:
   `pip install scapy pandas`
2. **Step 1: Start the Server**:
   - Open Command Prompt or PowerShell in the project folder.
   - Run the command: `python server.py`
   - **Expected Output**: `Server running on 0.0.0.0:10000...`
   - ⚠️ **Note**: Do not close this window! Closing it will stop the entire chat system.
3. **Step 2: Launch Clients**:
   - Open a new terminal window for each user.
   - Run: `python client.py`
   - In the login screen: Enter the **Server's IPv4 Address** (e.g., 192.168.x.x).
   - *(Note: Use `127.0.0.1` only if the server and client are on the same machine for testing).*

### 🍎 macOS Instructions
1. **Prerequisites**: Ensure Python 3.x is installed. Install libraries:
   `pip3 install scapy pandas`
2. **Step 1: Start the Server**:
   - Open Terminal in the project folder.
   - Run: `python3 server.py`
   - ⚠️ **Note**: Keep this Terminal tab open at all times.
3. **Step 2: Launch Clients**:
   - Open a new Terminal tab (`Cmd + T`) for each user.
   - Run: `python3 client.py`
   - Enter the **Server's IPv4 Address** and your username.

### 🐧 Linux Instructions
1. **Prerequisites**: Install Python3 and Tkinter (often required separately on Linux):
   `sudo apt update && sudo apt install python3-tk`
   `pip3 install scapy pandas`
2. **Step 1: Start the Server**:
   - Open Terminal.
   - Run: `python3 server.py`
3. **Step 2: Launch Clients**:
   - Run: `python3 client.py`
   - Enter the **Server's IPv4 Address** in the login field.
4. **Permissions**: Part 1 (Scapy) requires root privileges to send raw packets:
   `sudo python3 encapsulation_script.py`

---

## 🛠️ Troubleshooting

* **Finding the Server IP**:
    - **Windows**: Run `ipconfig` in CMD. Look for `IPv4 Address`.
    - **macOS/Linux**: Run `ifconfig` or `ip a` in Terminal. Look for `inet` under your active interface (e.g., `en0` or `eth0`).
* **"Address already in use" Error**:
    - This happens if a previous instance of the server is still running. Close all terminals and wait 5 seconds before restarting.
* **Connection Refused**:
    - Ensure the Server is running **before** you launch the Client.
    - Check that the Client is using the correct IPv4 address of the host machine.
* **Firewall Issues**:
    - Ensure your firewall allows Python to communicate over Port 10000. On Linux, you may need: `sudo ufw allow 10000/tcp`.

---

## 💬 Usage Tips
* **Private Chat**: Click a name in the sidebar. The header will change from `# General Chat` to `@ Username`.
* **Notifications**: If you see a number in parentheses, e.g., `Omer (2)`, it means you have unread messages.
* **Reconnection**: Log back in with the same name to see the "Reconnected" status in action.
  
---
## 👥 Authors
* **Amit Almaliach**
* **Amir Macktin**
