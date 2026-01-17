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
1. Prerequisites: Ensure Python 3.x is installed. Install required libraries via terminal:
   pip install scapy pandas
2. Start the Server:
   - Open Command Prompt or PowerShell.
   - Navigate to the project folder.
   - Run: python server.py
3. Launch Clients:
   - Open a new Command Prompt for each user.
   - Run: python client.py
   - In the GUI: Enter Server's IPv4 as the Server IP and choose a username.

### 🍎 macOS Instructions
1. Prerequisites: Ensure Python 3.x is installed (usually via brew install python). Install libraries:
   pip3 install scapy pandas
2. Start the Server:
   - Open Terminal.
   - Navigate to the project folder.
   - Run: python3 server.py
3. Launch Clients:
   - Open a new Terminal tab (Cmd + T) for each user.
   - Run: python3 client.py
   - Note: You may need to grant Terminal "Accessibility" permissions if the GUI doesn't appear immediately.
4. Permissions: If using Scapy (Part 1), run with sudo:
   sudo python3 encapsulation_script.py

---

## 💬 Usage Tips
* Private Chat: Click a name in the sidebar. The header will change from # General Chat to @ Username.
* Notifications: If you see a number in parentheses, e.g., Omer (2), it means you have 2 unread private messages from that user.
* Testing Reconnection: Close a client window and log back in with the same name; the chat will announce your return.
