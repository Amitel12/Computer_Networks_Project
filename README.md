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

### Identity & Connection Management
* Duplicate Name Protection: The server prevents multiple logins with the same username. If a name is already active, the client receives a "Username Taken" error and is denied access.
* Reconnection Logic: The system recognizes returning users. If a user disconnects and joins again, they are greeted with a "Reconnected" status, and the server broadcasts their return to the chat.
* Thread-Safe Registration: The server handles incoming connections concurrently, ensuring that name checks and registrations are handled safely even during simultaneous login attempts.

### Visual Status & UI
* Dynamic Sidebar:
    * 🟢 Green Dot: User is currently online and active.
    * ⚪ Grey Dot: User has disconnected but remains in the known users list.
* Unread Message Counters: Visual notifications (N) appear next to usernames when messages are received in a background chat room.
* History Management: Chat history is locally cached and separated between the General Chat and individual private conversations.

---

## 🚀 How to Run

* Step 1: Start the Server
    * Open a terminal or command prompt.
    * Run the command: python server.py.
    * The server will begin listening on 0.0.0.0:10000.

* Step 2: Launch the Clients
    * Open a new terminal for each user you want to add.
    * Run the command: python client.py.
    * Enter the Server IP (e.g., 127.0.0.1 for local testing) and choose a unique username.

* Step 3: Start Chatting
    * Send messages in the General Chat to broadcast to everyone.
    * Click on any user in the CHATS sidebar to start a private conversation.
