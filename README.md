# MultiClients-Chat
MultiClients Chat created using python
Simple socket program to communication between server and clients.

Libraries I used: socket, threading, sys, time

first run `` python server.py `` in order to create a server

then run`` python client.py `` for each client

#### server commands:
``!help``

``!list - listing all running clients``

``!kick {nickname} - kick specific client``

``!exit - close all clients``
<br>
#### client commands:
``!exit - client exits from the server``
<br><br>

### TODO list:
- [x] handling more errors
- [ ] create a log file
- [x] close sockets correctly
- [ ] add type annotations
- [ ] fix ``getnickname()`` - add test if nickname is already in use
- [x] make clients a dict and not a list
