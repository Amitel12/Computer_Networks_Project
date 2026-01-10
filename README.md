# 📡 TCP/IP Networking Project: Encapsulation & Chat Application

This repository contains a comprehensive networking project divided into two main parts:
1.  **Network Encapsulation Analysis:** A simulation of the TCP/IP stack using Python and Wireshark.
2.  **TCP Chat System:** A fully functional, multi-threaded GUI chat application supporting private messaging and real-time status updates.

---

## 📂 Project Structure
├── Part 1 - Encapsulation/
│   ├── Project_Part1.ipynb       # Jupyter Notebook for packet crafting simulation
│   └── group02_http_input.csv    # Input data for the simulation
│
├── Part 2 - Chat Application/
│   ├── server.py                 # Multi-threaded TCP Server
│   └── client.py                 # GUI Client (Tkinter)
│
└── README.md

Libraries: socket, threading, tkinter, scapy, pandas

1️⃣ Part 1: Encapsulation Simulation & Analysis
In this section, we manually craft TCP/IP packets based on application data (HTTP messages) to demonstrate how encapsulation works in the network stack.
Features
Reads application messages from a CSV file (group02_http_input.csv).
Uses Scapy (or raw sockets) to encapsulate data into TCP segments and IP packets.
Sends packets over the local network interface (Loopback).
Traffic is analyzed using Wireshark to verify headers, ports, and payloads.
2️⃣ Part 2: TCP Chat Application (GUI)
A robust client-server chat application designed with a modern, dark-themed GUI. It demonstrates socket programming, threading, and protocol design.

Key Features
Real-time Communication: Uses TCP sockets for reliable message delivery.

Multi-User Support: The server handles multiple clients simultaneously using threads.

Private Messaging (Unicast): Click on a user's name to switch to a private conversation.

Status Indicators:

🟢 Green Dot: User is online.
<img width="940" height="300" alt="image" src="https://github.com/user-attachments/assets/81817f88-4163-4537-b11a-a9b16fe0b29b" />

🔴 Red Dot: User has disconnected.
<img width="940" height="287" alt="image" src="https://github.com/user-attachments/assets/0c4c4f1c-8ebe-460d-ba26-c8a40823073e" />

Unread Counters: Visual notification (N) next to users who sent messages while you were in a different chat room.
<img width="392" height="238" alt="image" src="https://github.com/user-attachments/assets/09b5eccc-bd6d-4f1d-83a5-bdbb09e185a2" />

History Management: Chat history is saved separately for every user and the General Chat.
