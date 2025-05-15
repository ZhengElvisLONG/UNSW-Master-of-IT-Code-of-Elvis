COMP3331/9331 Discussion Forum
Zheng LONG

System Architecture
-----------------
I broke down the program into these main components:

Server side:
- Authentication: This part checks usernames/passwords against credentials.txt and keeps track of who's logged in. Nothing fancy but it works.
- Thread management: Handles creating threads, listing them, and deleting them. I made sure only the person who created a thread can delete it - seemed fair.
- Message handling: For posting, editing and deleting messages. Again, you can only mess with your own messages.
- File transfers: This was tricky! Had to use TCP connections for this part since files can be big and UDP would be a nightmare.
- UDP reliability: This gave me headaches... had to implement sequence numbers, ACKs and retransmission timers.

Client side:
- Command interface: Just parses what users type and formats it for the server
- Network stuff: Deals with both protocols (UDP/TCP)
- Display: Shows responses in a readable way

Data Structurs
--------------
Dictionaries were my best friend for this assignment. I probably overused them but their just so convenient:

```python
# For users
users = {"yoda": "wise@!man", "vader": "sithlord**"}
active_users = {"yoda": ("192.168.1.5", 45678)}

# For forum content
threads = {
  "jedi_training": {
    "creator": "yoda",
    "messages": [
      {"id": 1, "author": "yoda", "content": "Do or do not"},
      {"id": 2, "author": "luke", "content": "I'll try"}
    ],
    "files": ["lightsaber_manual.txt"]
  }
}
```

Thread safety was a pain - had to use locks everywhere to make sure things didn't break when multiple people used the forum at once. I probably over-engineered this part a bit. At one point I had deadlocks happening because I wasn't acquiring locks in a consistent order. Took forever to debug that one.

Communication Protocol
--------------------
Nothing too complicated here, just basic command/response stuff:

Commands are formatted like: `COMMAND [ARGUMENTS]`  
Examples:
- `CRT jedi_training` (create thread)
- `MSG jedi_training May the force be with you` (post message)
- `RDT jedi_training` (read thread)

The UDP reliability part was where I spent most of my time. Had to:
- Add sequence #s to packets (4 bytes at the start)
- Make the reciever send back ACKs
- Retransmit after 500ms if no ACK
- Double the timeout on repeated failures (exponential backoff)

I originally tried a sliding window approach but it was getting too complex, so I simplified to stop-and-wait which worked fine for this assignment.

For file transfers, I did:
1. Client asks to transfer via UDP
2. Server says "connect to port XXXX" 
3. Client makes TCP connection & sends JSON with file info
4. Data gets sent in chunks (1KB)
5. Connection closes when done

Design Decisions
--------------
Had to make some choices:

UDP vs. TCP for commands:
I went with UDP + my own reliability layer for commands. Its a bit faster for small messages, and I wanted to try implementing the reliability stuff myself. For files, obviously TCP makes more sense - wasn't about to implement large file transfer over UDP!

Concurrency:
Used threads + locks. Not the most scalable but WAY easier than async programming. I tried using asyncio at first but got confused with all the callbacks and switched to threading.

Storage:
Everything's just in memory. If server restarts, all data is gone. Not ideal but the assignment didn't require persistance. In-memory is super fast anyway.

Limitations & Improvements
------------------------
My implementation definitely has some issues:

Problems:
- Passwords stored as plaintext (I know, I know...)
- Can't resume interupted file transfers
- Everything's lost if server crashes
- Probably won't scale past ~1000 users

What I'd fix with more time:
- At minimum hash the passwords
- Use SQLite or something for persistance
- Add resume capability for file transfers
- Maybe make a web frontend

Testing
------
I tested a few different ways:

Basic testing:
Ran through all the commands in sequence to make sure they worked. Created threads, posted stuff, edited and deleted messages, etc..

Concurrent testing:
Got a few clients going at once to test thread safety. Found a nasty race condition where two users editing messages at the same time could cause message IDs to get messed up.

Network testing:
Wrote a script to randomly drop packets and tested my reliability code. Works ok up to about 30% packet loss, then gets really slow (as expected).
