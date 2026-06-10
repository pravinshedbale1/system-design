#!/usr/bin/env python3
"""
📅 Daily Study Plan Emailer
Sends a morning email at 6 AM IST with:
  1. Today's DSA + System Design plan
  2. Spaced repetition items due
  3. Latest progress summary
  4. Overall schedule status

Runs via GitHub Actions (daily cron) or locally.
"""

import os
import sys
import re
import hashlib
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# ============================================================================
#  CONFIGURATION
# ============================================================================

IST = timezone(timedelta(hours=5, minutes=30))

SD_START = datetime(2026, 6, 10, tzinfo=IST).date()   # System Design start
DSA_START = datetime(2026, 6, 10, tzinfo=IST).date()   # DSA start

SD_TOTAL_WEEKS = 16
DSA_TOTAL_WEEKS = 17

SD_CONTENT_DAYS = 5   # D1-D5 per week, D6-D7 = buffer
DSA_CONTENT_DAYS = 7  # D1-D7 per week

# Paths (overridden by env vars in GitHub Actions)
SD_REPO = os.environ.get("SD_REPO_PATH", ".")
DSA_REPO = os.environ.get("DSA_REPO_PATH", "./dsa")

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

# ============================================================================
#  SCHEDULE DATA — SYSTEM DESIGN (16 Weeks × 5 Days)
# ============================================================================
# Format: SD_WEEKS[week] = (title, phase_name, {day: [(topic, story), ...]})

SD_WEEKS = {
    1: ("The Internet & How Things Talk", "Phase 1 — Building Blocks", {
        1: [("DNS, HTTP, TCP/IP", "A letter needs an address, a language, and a postal system"),
            ("Client-Server vs P2P", "A restaurant vs a potluck dinner")],
        2: [("REST APIs & HTTP Methods", "A waiter taking your order"),
            ("WebSockets & Long Polling", "A phone call vs checking your mailbox")],
        3: [("Load Balancers", "The hostess at a busy restaurant"),
            ("Reverse Proxies & CDNs", "Branch offices & local warehouses")],
        4: [("🔨 Mini-Design: URL Shortener", "Your FIRST system design — simple, but teaches everything")],
        5: [("Review + Storytelling Practice", "Tell the story of how the internet works")],
    }),
    2: ("Data — Where Things Live & How They Scale", "Phase 1 — Building Blocks", {
        1: [("SQL vs NoSQL", "A spreadsheet vs a filing cabinet"),
            ("ACID & BASE", "A bank transfer vs a social media like")],
        2: [("Indexing & Query Optimization", "A library without a card catalog is useless"),
            ("Replication", "Making photocopies of your only copy of the Constitution")],
        3: [("Sharding / Partitioning", "Your library outgrew one building — time to open branches"),
            ("CAP Theorem", "The triangle of impossible perfection")],
        4: [("🔨 Mini-Design: Pastebin / Notes Service", "Apply all database concepts to a real system")],
        5: [("Review + Storytelling Practice", "Tell the story of data at scale")],
    }),
    3: ("Caching, Queues & The Art of Not Doing Work", "Phase 1 — Building Blocks", {
        1: [("Caching Deep Dive", "Your brain doesn't go to the library every time you need a fact"),
            ("Cache Invalidation", "The hardest problem in CS — and how we live with it")],
        2: [("Redis & Memcached", "The difference between a Swiss Army knife and a scalpel"),
            ("Message Queues", "A post office that never loses a letter")],
        3: [("Event-Driven Architecture", "Instead of asking 'is it ready yet?', just tell me when it's done"),
            ("Async Processing", "The chef doesn't serve the food — the waiter does")],
        4: [("🔨 Mini-Design: Rate Limiter", "A system that protects other systems")],
        5: [("Review + Storytelling Practice", "Tell the story of how caching & queues save the day")],
    }),
    4: ("Consistency, Reliability & The Real World", "Phase 1 — Building Blocks", {
        1: [("Consistency Models", "What does 'up to date' even mean?"),
            ("Consensus Algorithms", "How do 5 servers agree on anything? (Spoiler: it's hard)")],
        2: [("Availability & Fault Tolerance", "The show must go on — even when things break"),
            ("Distributed Transactions", "Two-phase commit and why it's both essential and terrible")],
        3: [("Monitoring & Observability", "You can't fix what you can't see"),
            ("Back-of-Envelope Estimation", "The most important 5 minutes of any design interview")],
        4: [("🔨 Design: Key-Value Store", "Your first 'real' distributed system")],
        5: [("🎯 PHASE 1 CHECKPOINT", "Design any mini-system using all building blocks")],
    }),
    5: ("Social & Feed Systems", "Phase 2 — The Classics", {
        1: [("Design Twitter/X (Day 1/2)", "From a single MySQL table to a global real-time platform")],
        2: [("Design Twitter/X (Day 2/2)", "Fan-out on write vs read, celebrity problem, timeline service")],
        3: [("Design Instagram/Photo Sharing (Day 1/2)", "Storing, serving, and recommending a billion photos")],
        4: [("Design Instagram/Photo Sharing (Day 2/2)", "Object storage, CDN, feed ranking, content moderation")],
        5: [("Design a Notification System", "How to poke a billion users without drowning")],
    }),
    6: ("Messaging & Real-Time Systems", "Phase 2 — The Classics", {
        1: [("Design WhatsApp/Chat System (Day 1/2)", "From IRC to end-to-end encrypted global messaging")],
        2: [("Design WhatsApp/Chat System (Day 2/2)", "WebSocket management, message ordering, delivery receipts")],
        3: [("Design Slack/Discord (Day 1/2)", "Chat, but with channels, threads, search, and presence")],
        4: [("Design Slack/Discord (Day 2/2)", "Channel architecture, real-time presence, message search")],
        5: [("Design Live Comments/Reactions", "Millions watching the same event, all reacting at once")],
    }),
    7: ("Storage & Search Systems", "Phase 2 — The Classics", {
        1: [("Design Google Drive/Dropbox (Day 1/2)", "From a shared folder to planet-scale file sync")],
        2: [("Design Google Drive/Dropbox (Day 2/2)", "File chunking, deduplication, sync conflicts")],
        3: [("Design a Search Engine (Day 1/2)", "How do you find one page in a trillion?")],
        4: [("Design a Search Engine (Day 2/2)", "Inverted index, crawling, ranking, sharded search")],
        5: [("Design Typeahead/Autocomplete", "Predicting what you'll type before you type it")],
    }),
    8: ("Video & Streaming Systems", "Phase 2 — The Classics", {
        1: [("Design YouTube (Day 1/2)", "From upload to 'Play' — the journey of a video")],
        2: [("Design YouTube (Day 2/2)", "Upload pipeline, transcoding, adaptive bitrate, CDN")],
        3: [("Design Netflix (Day 1/2)", "Streaming to 200M users simultaneously without buffering")],
        4: [("Design Netflix (Day 2/2)", "Content delivery, Open Connect, personalization, A/B testing")],
        5: [("Design Spotify / Audio Streaming", "Music that follows you everywhere")],
    }),
    9: ("E-Commerce & Transactional Systems", "Phase 2 — The Classics", {
        1: [("Design Amazon / E-Commerce (Day 1/2)", "From browsing to delivery — the commerce machine")],
        2: [("Design Amazon / E-Commerce (Day 2/2)", "Product catalog, inventory, cart, order processing")],
        3: [("Design a Payment System (Day 1/2)", "Moving money without losing a cent")],
        4: [("Design a Payment System (Day 2/2)", "Idempotency, exactly-once, ledger design, fraud detection")],
        5: [("Design a Booking System (Airbnb)", "Two people can't book the same room")],
    }),
    10: ("Location & Ride-Sharing Systems", "Phase 2 — The Classics", {
        1: [("Design Uber/Lyft (Day 1/2)", "Matching riders to drivers in a moving world")],
        2: [("Design Uber/Lyft (Day 2/2)", "Geo-spatial indexing, real-time location, matching, surge pricing")],
        3: [("Design Google Maps (Day 1/2)", "Routing billions of trips across the planet")],
        4: [("Design Google Maps (Day 2/2)", "Graph storage, Dijkstra/A* at scale, live traffic, map tiles")],
        5: [("🎯 PHASE 2 CHECKPOINT", "Full timed mock: design an unseen system")],
    }),
    11: ("Infrastructure & Platform Systems", "Phase 3 — Deep Cuts", {
        1: [("Distributed Task Scheduler (Day 1/2)", "Running a billion jobs without missing one")],
        2: [("Distributed Task Scheduler (Day 2/2)", "Job distribution, failure recovery, exactly-once execution")],
        3: [("Distributed Cache / Redis Cluster (Day 1/2)", "Every millisecond of latency = $ lost")],
        4: [("Distributed Cache / Redis Cluster (Day 2/2)", "Consistent hashing, replication, eviction, hot keys")],
        5: [("Design Metrics/Monitoring System", "Watching the watchers")],
    }),
    12: ("Data Pipeline & Analytics Systems", "Phase 3 — Deep Cuts", {
        1: [("Design a Web Crawler (Day 1/2)", "How Google reads the entire internet")],
        2: [("Design a Web Crawler (Day 2/2)", "Politeness, URL frontier, deduplication, distributed crawling")],
        3: [("Design Data Analytics Pipeline (Day 1/2)", "From raw events to business insights")],
        4: [("Design Data Analytics Pipeline (Day 2/2)", "Event ingestion, stream processing, Lambda/Kappa")],
        5: [("Design Distributed Logging System", "Finding a needle in a haystack of logs")],
    }),
    13: ("Unique/Tricky Systems", "Phase 3 — Deep Cuts", {
        1: [("Design Ticket Booking System (Day 1/2)", "10,000 people want the same 100 seats")],
        2: [("Design Ticket Booking System (Day 2/2)", "Virtual waiting room, seat locking, extreme contention")],
        3: [("Design Collaborative Editor (Day 1/2)", "50 people editing the same paragraph")],
        4: [("Design Collaborative Editor (Day 2/2)", "OT vs CRDT, operational transforms, conflict resolution")],
        5: [("Design URL Shortener at Billion Scale", "Revisiting your first design — but now you're dangerous")],
    }),
    14: ("Security, Auth & API Systems", "Phase 3 — Deep Cuts", {
        1: [("Design Authentication System (Day 1/2)", "Who are you, and how do I know you're not lying?")],
        2: [("Design Authentication System (Day 2/2)", "JWT, OAuth2, session management, MFA, token refresh")],
        3: [("Design an API Gateway (Day 1/2)", "The front door to your entire platform")],
        4: [("Design an API Gateway (Day 2/2)", "Rate limiting, auth, routing, circuit breaking")],
        5: [("Design Content Moderation System", "Keeping the internet safe at scale")],
    }),
    15: ("Mock Interview Marathon", "Phase 3 — Deep Cuts", {
        1: [("Mock 1: Unseen system", "45 min timed, full interview simulation")],
        2: [("Mock 2: Weak areas focus", "Focus on areas identified in state file")],
        3: [("Mock 3: Curveball system", "Something unusual — multiplayer game server, voting system")],
        4: [("Mock 4: Company-specific style", "Google: scale, Meta: social, Amazon: customer")],
        5: [("Mock 5: Speed round", "Design 2 systems in 60 minutes (high-level only)")],
    }),
    16: ("Final Polish & Interview Readiness", "Phase 3 — Deep Cuts", {
        1: [("Story Compilation", "Write the 2-minute story for every system designed")],
        2: [("Building Block Review", "Walk through every building block from memory")],
        3: [("Tradeoff Drill", "'Why did you choose X over Y?' for 20 key decisions")],
        4: [("Full Simulation", "2 back-to-back system design interviews (45 min each)")],
        5: [("Light Review + Rest", "Read stories, rest, build confidence")],
    }),
}

# ============================================================================
#  SCHEDULE DATA — DSA (17 Weeks × 7 Days)
# ============================================================================
# Format: DSA_WEEKS[week] = (title, phase_name, {day: [(name, difficulty, pattern), ...]})
# Special days: use string instead of list for review/challenge days

DSA_WEEKS = {
    1: ("Arrays & Hashing", "Phase 1 — Foundation", {
        1: [("Two Sum (LC #1)", "Easy", "HashMap complement"),
            ("Contains Duplicate (LC #217)", "Easy", "HashSet membership")],
        2: [("Valid Anagram (LC #242)", "Easy", "Frequency array int[26]"),
            ("Two Sum II (LC #167)", "Medium", "Two pointers on sorted")],
        3: [("Group Anagrams (LC #49)", "Medium", "HashMap grouping"),
            ("Top K Frequent Elements (LC #347)", "Medium", "Freq count + Bucket sort")],
        4: [("Product of Array Except Self (LC #238)", "Medium", "Prefix/Suffix product"),
            ("Longest Consecutive Sequence (LC #128)", "Medium", "HashSet + sequence start")],
        5: [("Encode and Decode Strings (LC #271)", "Medium", "Length-prefix delimiter"),
            ("Valid Sudoku (LC #36)", "Medium", "HashSet per row/col/box")],
        6: [("Subarray Sum Equals K (LC #560)", "Medium", "Prefix sum + HashMap"),
            ("📖 Review + weak problem re-solve", "", "")],
        7: "🔥 Weekly Challenge: Solve 2 unseen problems using only W1 patterns",
    }),
    2: ("Two Pointers & Sorting", "Phase 1 — Foundation", {
        1: [("Valid Palindrome (LC #125)", "Easy", "Two pointers inward"),
            ("Two Sum II (LC #167)", "Medium", "Sorted + two pointers")],
        2: [("3Sum (LC #15)", "Medium", "Sort + fix one + two pointers"),
            ("Container With Most Water (LC #11)", "Medium", "Greedy two pointers")],
        3: [("Trapping Rain Water (LC #42)", "Hard", "Two pointers / prefix max"),
            ("Move Zeroes (LC #283)", "Easy", "Partition / write pointer")],
        4: [("Sort Colors (LC #75)", "Medium", "Dutch National Flag"),
            ("Remove Duplicates from Sorted Array (LC #26)", "Easy", "Slow/fast write pointer")],
        5: [("4Sum (LC #18)", "Medium", "Sort + fix two + two pointers"),
            ("Boats to Save People (LC #881)", "Medium", "Sort + greedy two pointers")],
        6: "📖 Review + re-solve W1-W2 struggles",
        7: "🔥 Weekly Challenge: 2 unseen two-pointer problems",
    }),
    3: ("Sliding Window", "Phase 1 — Foundation", {
        1: [("Maximum Sum Subarray of Size K", "Easy", "Fixed window"),
            ("Longest Substring Without Repeating (LC #3)", "Medium", "Variable window + HashSet")],
        2: [("Minimum Size Subarray Sum (LC #209)", "Medium", "Variable window shrink"),
            ("Permutation in String (LC #567)", "Medium", "Fixed window + freq match")],
        3: [("Minimum Window Substring (LC #76)", "Hard", "Variable window + freq"),
            ("Longest Repeating Char Replacement (LC #424)", "Medium", "Variable window + max freq")],
        4: [("Fruit Into Baskets (LC #904)", "Medium", "At most K distinct"),
            ("Max Consecutive Ones III (LC #1004)", "Medium", "Variable window — at most K zeros")],
        5: [("Subarrays with K Different Integers (LC #992)", "Hard", "AtMost(K) - AtMost(K-1)"),
            ("Sliding Window Maximum (LC #239)", "Hard", "Monotonic deque")],
        6: "📖 Review + W1-W2 spaced repetition",
        7: "🔥 Weekly Challenge: 2 unseen sliding window problems",
    }),
    4: ("Stack & Queue", "Phase 1 — Foundation", {
        1: [("Valid Parentheses (LC #20)", "Easy", "Stack for matching"),
            ("Min Stack (LC #155)", "Medium", "Auxiliary stack for min")],
        2: [("Evaluate Reverse Polish Notation (LC #150)", "Medium", "Stack for expression eval"),
            ("Daily Temperatures (LC #739)", "Medium", "Monotonic decreasing stack")],
        3: [("Next Greater Element I (LC #496)", "Easy", "Monotonic stack + HashMap"),
            ("Largest Rectangle in Histogram (LC #84)", "Hard", "Monotonic increasing stack")],
        4: [("Car Fleet (LC #853)", "Medium", "Stack + sorting"),
            ("Implement Queue using Stacks (LC #232)", "Easy", "Two stacks")],
        5: [("Asteroid Collision (LC #735)", "Medium", "Stack simulation"),
            ("Maximal Rectangle (LC #85)", "Hard", "Histogram per row + monotonic stack")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    5: ("Linked List", "Phase 1 — Foundation", {
        1: [("Reverse Linked List (LC #206)", "Easy", "Iterative 3-pointer"),
            ("Merge Two Sorted Lists (LC #21)", "Easy", "Dummy node + merge")],
        2: [("Linked List Cycle (LC #141)", "Easy", "Fast/slow pointers (Floyd's)"),
            ("Linked List Cycle II (LC #142)", "Medium", "Floyd's + phase 2")],
        3: [("Remove Nth Node From End (LC #19)", "Medium", "Two pointers with gap"),
            ("Reorder List (LC #143)", "Medium", "Find mid + reverse + merge")],
        4: [("Merge K Sorted Lists (LC #23)", "Hard", "Min-heap / divide & conquer"),
            ("Copy List with Random Pointer (LC #138)", "Medium", "HashMap clone / interleave")],
        5: [("LRU Cache (LC #146)", "Medium", "HashMap + Doubly Linked List"),
            ("Add Two Numbers (LC #2)", "Medium", "Carry arithmetic")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    6: ("Binary Search", "Phase 1 — Foundation", {
        1: [("Binary Search (LC #704)", "Easy", "Classic template: lo, hi, mid"),
            ("Search Insert Position (LC #35)", "Easy", "Lower bound")],
        2: [("Search in Rotated Sorted Array (LC #33)", "Medium", "Modified binary search"),
            ("Find Min in Rotated Sorted (LC #153)", "Medium", "Binary search for pivot")],
        3: [("Koko Eating Bananas (LC #875)", "Medium", "Binary search on answer"),
            ("Search a 2D Matrix (LC #74)", "Medium", "Flatten to 1D binary search")],
        4: [("Time Based Key-Value Store (LC #981)", "Medium", "Binary search on timestamps"),
            ("Find Peak Element (LC #162)", "Medium", "Binary search on unsorted")],
        5: [("Median of Two Sorted Arrays (LC #4)", "Hard", "Binary search on partition"),
            ("Split Array Largest Sum (LC #410)", "Hard", "Binary search on answer")],
        6: "🎯 PHASE 1 CHECKPOINT: Solve 5 mixed unseen problems (timed)",
        7: "📖 Review all Phase 1 patterns + update confidence",
    }),
    7: ("Binary Trees — DFS", "Phase 2 — Advanced Patterns", {
        1: [("Invert Binary Tree (LC #226)", "Easy", "Recursive DFS"),
            ("Maximum Depth (LC #104)", "Easy", "Recursive DFS")],
        2: [("Same Tree (LC #100)", "Easy", "Compare trees recursively"),
            ("Subtree of Another Tree (LC #572)", "Medium", "Compare trees recursively")],
        3: [("Diameter of Binary Tree (LC #543)", "Easy", "Height + diameter relationship"),
            ("Balanced Binary Tree (LC #110)", "Easy", "Height-based DFS")],
        4: [("Lowest Common Ancestor (LC #236)", "Medium", "Recursive LCA"),
            ("Path Sum (LC #112)", "Easy", "Root-to-leaf DFS")],
        5: [("Binary Tree Max Path Sum (LC #124)", "Hard", "Global max with DFS"),
            ("Count Good Nodes (LC #1448)", "Medium", "DFS with max tracking")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    8: ("Binary Trees — BFS + BST", "Phase 2 — Advanced Patterns", {
        1: [("Level Order Traversal (LC #102)", "Medium", "BFS with queue"),
            ("Right Side View (LC #199)", "Medium", "BFS — last node per level")],
        2: [("Zigzag Level Order (LC #103)", "Medium", "BFS with direction flag"),
            ("Average of Levels (LC #637)", "Easy", "BFS + average")],
        3: [("Validate BST (LC #98)", "Medium", "Inorder = sorted"),
            ("Kth Smallest in BST (LC #230)", "Medium", "Inorder traversal")],
        4: [("Serialize/Deserialize BT (LC #297)", "Hard", "Tree serialization"),
            ("Construct BT from Preorder+Inorder (LC #105)", "Medium", "Divide & conquer")],
        5: [("BST Iterator (LC #173)", "Medium", "Controlled inorder"),
            ("LCA of BST (LC #235)", "Medium", "BST property")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    9: ("Heap / Priority Queue", "Phase 2 — Advanced Patterns", {
        1: [("Kth Largest Element (LC #215)", "Medium", "Max heap / QuickSelect"),
            ("Last Stone Weight (LC #1046)", "Easy", "Max heap")],
        2: [("K Closest Points (LC #973)", "Medium", "Min-heap of size K"),
            ("Top K Frequent (LC #347 revisit)", "Medium", "Heap vs Bucket sort")],
        3: [("Find Median from Data Stream (LC #295)", "Hard", "Two-heap pattern")],
        4: [("Merge K Sorted Lists (LC #23 revisit)", "Hard", "K-way merge with heap"),
            ("Task Scheduler (LC #621)", "Medium", "Greedy + heap")],
        5: [("Reorganize String (LC #767)", "Medium", "Greedy with heap"),
            ("K Closest in Sorted Array (LC #658)", "Medium", "Binary search + two pointers")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    10: ("Backtracking", "Phase 2 — Advanced Patterns", {
        1: [("Subsets (LC #78)", "Medium", "Include/exclude"),
            ("Subsets II (LC #90)", "Medium", "Skip duplicates")],
        2: [("Permutations (LC #46)", "Medium", "Swap-based"),
            ("Permutations II (LC #47)", "Medium", "used[] array")],
        3: [("Combination Sum (LC #39)", "Medium", "Unbounded combinations"),
            ("Combination Sum II (LC #40)", "Medium", "Bounded + skip duplicates")],
        4: [("Word Search (LC #79)", "Medium", "Grid backtracking"),
            ("Palindrome Partitioning (LC #131)", "Medium", "String partition")],
        5: [("N-Queens (LC #51)", "Hard", "Constraint satisfaction"),
            ("Sudoku Solver (LC #37)", "Hard", "Constraint satisfaction")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    11: ("Graphs — BFS/DFS", "Phase 2 — Advanced Patterns", {
        1: [("Number of Islands (LC #200)", "Medium", "Grid DFS"),
            ("Clone Graph (LC #133)", "Medium", "Graph DFS + clone")],
        2: [("Pacific Atlantic Water Flow (LC #417)", "Medium", "Multi-source BFS/DFS"),
            ("Surrounded Regions (LC #130)", "Medium", "Border DFS")],
        3: [("Course Schedule (LC #207)", "Medium", "Topological sort (Kahn's)"),
            ("Course Schedule II (LC #210)", "Medium", "Topological sort (DFS)")],
        4: [("Word Ladder (LC #127)", "Hard", "BFS shortest path"),
            ("Rotting Oranges (LC #994)", "Medium", "Multi-source BFS")],
        5: [("Accounts Merge (LC #721)", "Medium", "Union-Find"),
            ("Graph Valid Tree (LC #261)", "Medium", "Union-Find / DFS")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    12: ("Advanced Graphs + Union-Find", "Phase 2 — Advanced Patterns", {
        1: [("Network Delay Time (LC #743)", "Medium", "Dijkstra"),
            ("Cheapest Flights (LC #787)", "Medium", "Bellman-Ford")],
        2: [("Swim in Rising Water (LC #778)", "Hard", "Binary search + BFS"),
            ("Path with Min Effort (LC #1631)", "Medium", "Dijkstra variant")],
        3: [("Redundant Connection (LC #684)", "Medium", "Union-Find"),
            ("Min Cost to Connect (LC #1135)", "Medium", "MST / Kruskal")],
        4: [("Alien Dictionary (LC #269)", "Hard", "Topo sort on chars"),
            ("Longest Increasing Path (LC #329)", "Hard", "DFS + memoization")],
        5: [("Critical Connections (LC #1192)", "Hard", "Tarjan's (bridges)")],
        6: "🎯 PHASE 2 CHECKPOINT: Solve 5 mixed tree/graph/heap problems (timed)",
        7: "📖 Full review of Phase 1 + 2 patterns",
    }),
    13: ("Dynamic Programming — 1D", "Phase 3 — DP & Hard Patterns", {
        1: [("Climbing Stairs (LC #70)", "Easy", "Fibonacci-style DP"),
            ("House Robber (LC #198)", "Medium", "Linear DP")],
        2: [("House Robber II (LC #213)", "Medium", "Circular DP"),
            ("Decode Ways (LC #91)", "Medium", "Counting DP")],
        3: [("Coin Change (LC #322)", "Medium", "Min coins — unbounded"),
            ("Coin Change 2 (LC #518)", "Medium", "Count ways — unbounded")],
        4: [("Longest Increasing Subsequence (LC #300)", "Medium", "LIS pattern"),
            ("Word Break (LC #139)", "Medium", "Substring DP")],
        5: [("Maximum Product Subarray (LC #152)", "Medium", "Track min/max"),
            ("Partition Equal Subset Sum (LC #416)", "Medium", "0/1 knapsack")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    14: ("Dynamic Programming — 2D & Strings", "Phase 3 — DP & Hard Patterns", {
        1: [("Unique Paths (LC #62)", "Medium", "Grid DP"),
            ("Minimum Path Sum (LC #64)", "Medium", "Grid DP")],
        2: [("Longest Common Subsequence (LC #1143)", "Medium", "Two-string DP"),
            ("Edit Distance (LC #72)", "Hard", "Two-string DP")],
        3: [("Longest Palindromic Substring (LC #5)", "Medium", "Expand around center / DP"),
            ("Palindromic Substrings (LC #647)", "Medium", "Expand around center")],
        4: [("Interleaving String (LC #97)", "Hard", "Two-string DP advanced"),
            ("Distinct Subsequences (LC #115)", "Hard", "Two-string DP")],
        5: [("Burst Balloons (LC #312)", "Hard", "Interval DP"),
            ("Regular Expression Matching (LC #10)", "Hard", "String matching DP")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    15: ("Tries, Intervals & Greedy", "Phase 3 — DP & Hard Patterns", {
        1: [("Implement Trie (LC #208)", "Medium", "Trie implementation"),
            ("Word Search II (LC #212)", "Hard", "Trie + DFS")],
        2: [("Design Add/Search Words (LC #211)", "Medium", "Trie with wildcards"),
            ("Longest Word in Dict (LC #720)", "Medium", "Trie + BFS")],
        3: [("Merge Intervals (LC #56)", "Medium", "Sort + merge"),
            ("Insert Interval (LC #57)", "Medium", "Interval insertion")],
        4: [("Non-overlapping Intervals (LC #435)", "Medium", "Greedy interval"),
            ("Meeting Rooms II (LC #253)", "Medium", "Sweep line")],
        5: [("Jump Game (LC #55)", "Medium", "Greedy"),
            ("Jump Game II (LC #45)", "Medium", "Greedy BFS"),
            ("Gas Station (LC #134)", "Medium", "Greedy proof")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    16: ("Advanced Mixed Problems", "Phase 3 — DP & Hard Patterns", {
        1: [("LFU Cache (LC #460)", "Hard", "Complex data structure"),
            ("LRU Cache (LC #146 revisit)", "Medium", "HashMap + DLL")],
        2: [("Skyline Problem (LC #218)", "Hard", "Sweep line + heap"),
            ("Trapping Rain Water (LC #42 revisit)", "Hard", "Two pointers")],
        3: [("Word Ladder II (LC #126)", "Hard", "BFS + backtrack"),
            ("Longest Valid Parentheses (LC #32)", "Hard", "Stack / DP")],
        4: [("Maximal Rectangle (LC #85)", "Hard", "Histogram + stack"),
            ("Largest Rectangle (LC #84 revisit)", "Hard", "Monotonic stack")],
        5: [("Company-tagged hard problems", "Hard", "Mixed patterns — 2-3 problems")],
        6: "📖 Review + spaced repetition",
        7: "🔥 Weekly Challenge",
    }),
    17: ("Mock Interview Marathon + Final Polish", "Phase 3 — DP & Hard Patterns", {
        1: "Mock 1: 2 problems (45 min each) — any pattern, timed, explain aloud",
        2: "Mock 2: 2 problems — focus on weak patterns from state file",
        3: "Mock 3: 2 hard problems — full interview simulation with edge cases",
        4: "Mock 4: Company-tagged problems (Google/Amazon/Meta style)",
        5: "Mock 5: Speed round — 4 mediums in 60 minutes",
        6: "Mock 6: Full interview day simulation — 2 coding rounds back to back",
        7: "📖 Final review: walk through entire pattern index from memory",
    }),
}

# ============================================================================
#  MOTIVATIONAL QUOTES
# ============================================================================

QUOTES = [
    "The only way to do great work is to love what you do. — Steve Jobs",
    "It's not that I'm so smart, it's just that I stay with problems longer. — Einstein",
    "First, solve the problem. Then, write the code. — John Johnson",
    "Consistency beats intensity. Show up every day.",
    "Every expert was once a beginner. Keep going. 💪",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Small daily improvements → staggering long-term results.",
    "You don't have to be great to start, but you have to start to be great.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Dream big. Start small. Act now.",
    "Hard choices, easy life. Easy choices, hard life.",
    "Discipline is choosing between what you want now and what you want most.",
    "Code is like humor. When you have to explain it, it's bad. — Cory House",
    "Strive for progress, not perfection.",
]

# ============================================================================
#  DATE & POSITION HELPERS
# ============================================================================

def today_ist():
    """Get today's date in IST."""
    return datetime.now(IST).date()


def compute_position(start_date, today):
    """Compute (week, day_in_week, total_days_elapsed)."""
    delta = (today - start_date).days
    if delta < 0:
        return None, None, delta
    week = delta // 7 + 1
    day = delta % 7 + 1
    return week, day, delta


def get_sd_today(week, day):
    """Get System Design content for today."""
    if not week or week > SD_TOTAL_WEEKS:
        return None, None, None
    w = SD_WEEKS.get(week)
    if not w:
        return None, None, None
    title, phase, days = w
    if day > SD_CONTENT_DAYS:
        return title, phase, "buffer"
    content = days.get(day)
    return title, phase, content


def get_dsa_today(week, day):
    """Get DSA content for today."""
    if not week or week > DSA_TOTAL_WEEKS:
        return None, None, None
    w = DSA_WEEKS.get(week)
    if not w:
        return None, None, None
    title, phase, days = w
    content = days.get(day)
    return title, phase, content


# ============================================================================
#  MARKDOWN PARSERS (for CONVERSATION_STATE.md)
# ============================================================================

def parse_state_table(content):
    """Parse the Current Position table from CONVERSATION_STATE.md."""
    state = {}
    match = re.search(
        r'## 📍 Current Position\s*\n\s*\|.*\|\s*\n\s*\|[-\s|]+\|\s*\n((?:\|.*\n)*)',
        content
    )
    if match:
        for line in match.group(1).strip().split('\n'):
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]
            if len(parts) >= 2:
                key = re.sub(r'\*\*', '', parts[0]).strip()
                val = re.sub(r'\*\*', '', parts[1]).strip()
                state[key] = val
    return state


def parse_latest_session(content):
    """Extract the latest session entry."""
    pattern = r'### Session #(\d+)\s*—\s*(.+?)\s*—\s*(.+?)\n(.*?)(?=### Session #|\n---|\Z)'
    sessions = re.findall(pattern, content, re.DOTALL)
    if not sessions:
        return None
    last = sessions[-1]
    # Extract key info from session content
    problems = re.findall(r'- (.+?LC #\d+.+?)(?:\n|$)', last[3])
    return {
        'number': last[0],
        'date': last[1].strip(),
        'topic': last[2].strip(),
        'problems': problems[:5],  # Limit to 5
    }


def parse_review_due(content, today):
    """Parse spaced repetition section for due items."""
    due = []
    # Look for the "Spaced Repetition — Due Today" or review schedule sections
    # Parse box sections in review_schedule.md
    lines = content.split('\n')
    current_box = ""
    for line in lines:
        if 'Box 1' in line and '##' in line:
            current_box = "Box 1 (Daily)"
        elif 'Box 2' in line and '##' in line:
            current_box = "Box 2 (3-Day)"
        elif 'Box 3' in line and '##' in line:
            current_box = "Box 3 (Weekly)"
        elif 'Box 4' in line and '##' in line:
            current_box = "Box 4 (Bi-Weekly)"
        elif 'Box 5' in line and '##' in line:
            current_box = "Box 5 (Monthly)"

        if '|' in line and 'LC #' in line:
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]
            if len(parts) >= 4:
                problem = parts[0]
                pattern = parts[1] if len(parts) > 1 else ""
                # Try to find a date that could be "Next Review"
                for part in reversed(parts):
                    date_match = re.search(
                        r'(June|July|August|September|October)\s+(\d+)', part
                    )
                    if date_match:
                        month_map = {
                            'June': 6, 'July': 7, 'August': 8,
                            'September': 9, 'October': 10
                        }
                        m = month_map.get(date_match.group(1), 0)
                        d = int(date_match.group(2))
                        if m:
                            try:
                                review_date = datetime(2026, m, d).date()
                                if review_date <= today:
                                    due.append({
                                        'problem': problem,
                                        'pattern': pattern,
                                        'box': current_box,
                                        'due': review_date.strftime('%b %d'),
                                        'overdue': review_date < today,
                                    })
                            except ValueError:
                                pass
                        break
    return due


def read_file_safe(path):
    """Read a file, return empty string if not found."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, PermissionError):
        return ""


# ============================================================================
#  HTML EMAIL GENERATOR
# ============================================================================

def generate_email_html(today, sd_week, sd_day, dsa_week, dsa_day,
                        sd_title, sd_phase, sd_content,
                        dsa_title, dsa_phase, dsa_content,
                        sd_state, dsa_state, dsa_last_session,
                        sd_last_session, due_reviews):
    """Generate a beautiful dark-themed HTML email."""

    date_str = today.strftime('%A, %B %d, %Y')

    # --- Spaced Repetition Section ---
    review_html = ""
    if due_reviews:
        rows = ""
        for item in due_reviews:
            badge = (' <span style="background:#e74c3c;color:#fff;padding:1px 6px;'
                     'border-radius:3px;font-size:10px;font-weight:600;">OVERDUE</span>'
                     if item['overdue'] else '')
            rows += f"""<tr>
                <td style="padding:8px 12px;border-bottom:1px solid #2d2d44;color:#e0e0e0;font-size:14px;">
                    {item['problem']}{badge}</td>
                <td style="padding:8px 12px;border-bottom:1px solid #2d2d44;color:#9ca3af;font-size:13px;">
                    {item['pattern']}</td>
                <td style="padding:8px 12px;border-bottom:1px solid #2d2d44;color:#9ca3af;font-size:13px;">
                    {item['box']}</td>
            </tr>"""
        review_html = f"""
        <div style="margin:20px 0;background:linear-gradient(135deg,#1a1a2e,#1e2340);
                     border-radius:10px;padding:20px;border:1px solid #2d2d44;">
            <h3 style="margin:0 0 14px 0;color:#f39c12;font-size:16px;">
                ⏰ Spaced Repetition Due Today</h3>
            <table style="width:100%;border-collapse:collapse;">
                <tr>
                    <th style="text-align:left;padding:8px 12px;border-bottom:2px solid #3d3d5c;
                               color:#6b7280;font-size:12px;text-transform:uppercase;">Problem</th>
                    <th style="text-align:left;padding:8px 12px;border-bottom:2px solid #3d3d5c;
                               color:#6b7280;font-size:12px;text-transform:uppercase;">Pattern</th>
                    <th style="text-align:left;padding:8px 12px;border-bottom:2px solid #3d3d5c;
                               color:#6b7280;font-size:12px;text-transform:uppercase;">Box</th>
                </tr>
                {rows}
            </table>
        </div>"""

    # --- System Design Section ---
    sd_html = ""
    if sd_week and sd_week <= SD_TOTAL_WEEKS:
        if sd_content == "buffer":
            inner = """<p style="color:#8b949e;font-size:14px;margin:12px 0;">
                📚 Buffer Day — Review and consolidate this week's learning.
                Re-tell stories from the week, update notes, rest your brain.</p>"""
        elif sd_content is None:
            inner = '<p style="color:#8b949e;font-size:14px;">No content scheduled.</p>'
        elif isinstance(sd_content, list):
            topics = ""
            for name, story in sd_content:
                topics += f"""
                <div style="margin:10px 0;padding:12px;background:#0d1117;border-radius:8px;
                            border-left:3px solid #58a6ff;">
                    <strong style="color:#58a6ff;font-size:14px;">{name}</strong><br>
                    <em style="color:#8b949e;font-size:13px;">"{story}"</em>
                </div>"""
            inner = topics
        else:
            inner = f'<p style="color:#8b949e;">{sd_content}</p>'

        sd_html = f"""
        <div style="margin:20px 0;background:linear-gradient(135deg,#0d1117,#161b22);
                     border-radius:10px;padding:20px;border:1px solid #30363d;">
            <h2 style="margin:0 0 4px 0;color:#58a6ff;font-size:18px;">
                🏗️ System Design</h2>
            <p style="margin:0 0 16px 0;color:#8b949e;font-size:13px;">
                Week {sd_week} / {SD_TOTAL_WEEKS} &nbsp;•&nbsp; Day {sd_day}
                &nbsp;•&nbsp; {sd_title or ''}</p>
            <p style="margin:0 0 8px 0;color:#6b7280;font-size:11px;
                       text-transform:uppercase;letter-spacing:1px;">
                {sd_phase or ''}</p>
            {inner}
        </div>"""
    elif sd_week and sd_week > SD_TOTAL_WEEKS:
        sd_html = """
        <div style="margin:20px 0;background:#0d1117;border-radius:10px;padding:20px;
                     border:1px solid #30363d;">
            <h2 style="margin:0;color:#58a6ff;">🏗️ System Design — ✅ Plan Complete!</h2>
            <p style="color:#8b949e;">You've completed the 16-week system design plan. 🎉</p>
        </div>"""

    # --- DSA Section ---
    dsa_html = ""
    if dsa_week and dsa_week <= DSA_TOTAL_WEEKS:
        if isinstance(dsa_content, str):
            # Special day (review, challenge, mock, checkpoint)
            inner = f"""<div style="margin:10px 0;padding:14px;background:#0d1117;
                                    border-radius:8px;border-left:3px solid #f39c12;">
                <strong style="color:#f39c12;font-size:14px;">{dsa_content}</strong>
            </div>"""
        elif isinstance(dsa_content, list):
            problems = ""
            for item in dsa_content:
                if len(item) >= 3:
                    name, diff, pattern = item[0], item[1], item[2]
                    dc = {'Easy': '#10b981', 'Medium': '#f59e0b',
                          'Hard': '#ef4444', '': '#6b7280'}.get(diff, '#6b7280')
                    diff_badge = (f'<span style="color:{dc};font-size:11px;font-weight:600;'
                                  f'margin-left:8px;">{diff}</span>' if diff else '')
                    pat = (f'<br><span style="color:#6b7280;font-size:12px;">'
                           f'Pattern: {pattern}</span>' if pattern else '')
                    problems += f"""
                    <div style="margin:8px 0;padding:12px;background:#0d1117;
                                border-radius:8px;border-left:3px solid {dc};">
                        <strong style="color:#e5e7eb;font-size:14px;">{name}</strong>
                        {diff_badge}{pat}
                    </div>"""
                else:
                    problems += f"""
                    <div style="margin:8px 0;padding:12px;background:#0d1117;
                                border-radius:8px;border-left:3px solid #6b7280;">
                        <span style="color:#e5e7eb;font-size:14px;">{item[0]}</span>
                    </div>"""
            inner = problems
        else:
            inner = '<p style="color:#8b949e;">No content scheduled.</p>'

        dsa_html = f"""
        <div style="margin:20px 0;background:linear-gradient(135deg,#0d1117,#1a1520);
                     border-radius:10px;padding:20px;border:1px solid #30363d;">
            <h2 style="margin:0 0 4px 0;color:#f39c12;font-size:18px;">💻 DSA</h2>
            <p style="margin:0 0 16px 0;color:#8b949e;font-size:13px;">
                Week {dsa_week} / {DSA_TOTAL_WEEKS} &nbsp;•&nbsp; Day {dsa_day}
                &nbsp;•&nbsp; {dsa_title or ''}</p>
            <p style="margin:0 0 8px 0;color:#6b7280;font-size:11px;
                       text-transform:uppercase;letter-spacing:1px;">
                {dsa_phase or ''}</p>
            {inner}
        </div>"""
    elif dsa_week and dsa_week > DSA_TOTAL_WEEKS:
        dsa_html = """
        <div style="margin:20px 0;background:#0d1117;border-radius:10px;padding:20px;
                     border:1px solid #30363d;">
            <h2 style="margin:0;color:#f39c12;">💻 DSA — ✅ Plan Complete!</h2>
            <p style="color:#8b949e;">You've completed the 17-week DSA plan. 🎉</p>
        </div>"""

    # --- Latest Progress Section ---
    progress_parts = []
    if dsa_last_session:
        problems_str = ""
        if dsa_last_session.get('problems'):
            problems_str = "<br>".join(
                f'<span style="color:#d1d5db;font-size:12px;">• {p[:80]}</span>'
                for p in dsa_last_session['problems'][:3]
            )
        progress_parts.append(f"""
        <div style="margin:8px 0;padding:12px;background:#0d1117;border-radius:8px;">
            <strong style="color:#f39c12;font-size:13px;">
                💻 DSA Session #{dsa_last_session['number']}</strong>
            <span style="color:#6b7280;font-size:12px;"> — {dsa_last_session['date']}</span>
            <br><span style="color:#9ca3af;font-size:13px;">{dsa_last_session['topic']}</span>
            {f'<br>{problems_str}' if problems_str else ''}
        </div>""")

    if sd_last_session:
        progress_parts.append(f"""
        <div style="margin:8px 0;padding:12px;background:#0d1117;border-radius:8px;">
            <strong style="color:#58a6ff;font-size:13px;">
                🏗️ SD Session #{sd_last_session['number']}</strong>
            <span style="color:#6b7280;font-size:12px;"> — {sd_last_session['date']}</span>
            <br><span style="color:#9ca3af;font-size:13px;">{sd_last_session['topic']}</span>
        </div>""")

    progress_html = ""
    if progress_parts:
        progress_html = f"""
        <div style="margin:20px 0;background:linear-gradient(135deg,#1a1520,#161b22);
                     border-radius:10px;padding:20px;border:1px solid #30363d;">
            <h3 style="margin:0 0 12px 0;color:#a78bfa;font-size:16px;">
                📋 Latest Progress</h3>
            {"".join(progress_parts)}
        </div>"""

    # --- Overall Stats ---
    sd_sessions = sd_state.get('Session Count', '0')
    sd_systems = sd_state.get('Systems Designed', '0')
    dsa_sessions = dsa_state.get('Session Count', '0')
    dsa_problems = dsa_state.get('Total Problems Solved', '0')

    sd_pct = min(100, round(((sd_week or 1) - 1) / SD_TOTAL_WEEKS * 100)) if sd_week else 0
    dsa_pct = min(100, round(((dsa_week or 1) - 1) / DSA_TOTAL_WEEKS * 100)) if dsa_week else 0

    stats_html = f"""
    <div style="margin:20px 0;background:linear-gradient(135deg,#161b22,#1a1a2e);
                 border-radius:10px;padding:20px;border:1px solid #30363d;">
        <h3 style="margin:0 0 16px 0;color:#a78bfa;font-size:16px;">📊 Overall Progress</h3>
        <table style="width:100%;border-collapse:collapse;">
            <tr>
                <td style="padding:10px 8px;color:#58a6ff;font-weight:700;font-size:14px;width:140px;">
                    🏗️ System Design</td>
                <td style="padding:10px 8px;">
                    <div style="background:#1e1e3a;border-radius:10px;height:18px;overflow:hidden;">
                        <div style="background:linear-gradient(90deg,#3b82f6,#60a5fa);
                                    height:100%;width:{sd_pct}%;border-radius:10px;
                                    min-width:2px;"></div>
                    </div>
                </td>
                <td style="padding:10px 8px;color:#9ca3af;font-size:12px;white-space:nowrap;width:100px;">
                    W{sd_week or 0}/{SD_TOTAL_WEEKS} • {sd_sessions}s • {sd_systems}sys</td>
            </tr>
            <tr>
                <td style="padding:10px 8px;color:#f39c12;font-weight:700;font-size:14px;">
                    💻 DSA</td>
                <td style="padding:10px 8px;">
                    <div style="background:#1e1e3a;border-radius:10px;height:18px;overflow:hidden;">
                        <div style="background:linear-gradient(90deg,#f59e0b,#fbbf24);
                                    height:100%;width:{dsa_pct}%;border-radius:10px;
                                    min-width:2px;"></div>
                    </div>
                </td>
                <td style="padding:10px 8px;color:#9ca3af;font-size:12px;white-space:nowrap;">
                    W{dsa_week or 0}/{DSA_TOTAL_WEEKS} • {dsa_sessions}s • {dsa_problems}p</td>
            </tr>
        </table>
    </div>"""

    # --- Motivational Quote ---
    qidx = int(hashlib.md5(date_str.encode()).hexdigest(), 16) % len(QUOTES)
    quote = QUOTES[qidx]

    # --- Full Email ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Daily Study Plan — {date_str}</title></head>
<body style="margin:0;padding:0;background:#0a0a14;
             font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
<div style="max-width:620px;margin:0 auto;padding:20px;">

    <!-- Header -->
    <div style="text-align:center;padding:28px 20px;
                background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
                border-radius:14px;margin-bottom:4px;border:1px solid #30363d;">
        <h1 style="margin:0;color:#f0f0f0;font-size:22px;font-weight:700;letter-spacing:-0.5px;">
            📅 Daily Study Plan</h1>
        <p style="margin:10px 0 0 0;color:#8b949e;font-size:15px;">{date_str}</p>
    </div>

    {review_html}
    {sd_html}
    {dsa_html}
    {progress_html}
    {stats_html}

    <!-- Quote -->
    <div style="margin:20px 0;text-align:center;padding:16px 20px;
                border-top:1px solid #1e1e3a;">
        <p style="color:#4b5563;font-style:italic;margin:0;font-size:13px;">💡 {quote}</p>
    </div>

    <!-- Footer -->
    <div style="text-align:center;padding:8px;color:#374151;font-size:10px;">
        Auto-generated by Daily Study Planner &nbsp;•&nbsp; GitHub Actions<br>
        <span style="color:#4b5563;">Data from last git push. Push your progress to keep emails accurate.</span>
    </div>
</div>
</body></html>"""

    return html


# ============================================================================
#  EMAIL SENDER
# ============================================================================

def send_email(subject, html_body):
    """Send HTML email via Gmail SMTP."""
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        log.error("❌ GMAIL_ADDRESS and GMAIL_APP_PASSWORD env vars required")
        sys.exit(1)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Study Planner <{GMAIL_ADDRESS}>"
    msg['To'] = GMAIL_ADDRESS
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, msg.as_string())
        log.info(f"✅ Email sent to {GMAIL_ADDRESS}")
    except smtplib.SMTPAuthenticationError:
        log.error("❌ Gmail authentication failed. Check GMAIL_ADDRESS and GMAIL_APP_PASSWORD.")
        sys.exit(1)
    except Exception as e:
        log.error(f"❌ Failed to send email: {e}")
        sys.exit(1)


# ============================================================================
#  MAIN
# ============================================================================

def main():
    dry_run = "--dry-run" in sys.argv

    today = today_ist()
    log.info(f"📅 Generating daily plan for {today.strftime('%A, %B %d, %Y')}")

    # Compute schedule positions
    sd_week, sd_day, _ = compute_position(SD_START, today)
    dsa_week, dsa_day, _ = compute_position(DSA_START, today)
    log.info(f"🏗️  System Design: Week {sd_week}, Day {sd_day}")
    log.info(f"💻 DSA:            Week {dsa_week}, Day {dsa_day}")

    # Get today's content
    sd_title, sd_phase, sd_content = get_sd_today(sd_week, sd_day)
    dsa_title, dsa_phase, dsa_content = get_dsa_today(dsa_week, dsa_day)

    # Parse conversation states
    sd_state_content = read_file_safe(os.path.join(SD_REPO, "CONVERSATION_STATE.md"))
    dsa_state_content = read_file_safe(os.path.join(DSA_REPO, "CONVERSATION_STATE.md"))

    sd_state = parse_state_table(sd_state_content)
    dsa_state = parse_state_table(dsa_state_content)

    sd_last = parse_latest_session(sd_state_content)
    dsa_last = parse_latest_session(dsa_state_content)

    # Parse spaced repetition due items
    review_content = read_file_safe(
        os.path.join(DSA_REPO, "spaced_repetition", "review_schedule.md")
    )
    due_reviews = parse_review_due(review_content, today)

    # Generate email
    html = generate_email_html(
        today, sd_week, sd_day, dsa_week, dsa_day,
        sd_title, sd_phase, sd_content,
        dsa_title, dsa_phase, dsa_content,
        sd_state, dsa_state, dsa_last, sd_last, due_reviews,
    )

    # Build subject line
    sd_tag = f"SD W{sd_week}D{sd_day}" if sd_week and sd_week <= SD_TOTAL_WEEKS else "SD ✅"
    dsa_tag = f"DSA W{dsa_week}D{dsa_day}" if dsa_week and dsa_week <= DSA_TOTAL_WEEKS else "DSA ✅"
    subject = f"📅 {today.strftime('%b %d')} | {sd_tag} | {dsa_tag} | Daily Study Plan"

    if dry_run:
        log.info("🔍 Dry run — printing HTML to stdout:\n")
        print(html)
        # Also save to file for preview
        preview_path = os.path.join(SD_REPO, "daily_planner", "preview.html")
        with open(preview_path, 'w') as f:
            f.write(html)
        log.info(f"\n📄 Preview saved to {preview_path}")
    else:
        send_email(subject, html)

    log.info("✅ Done!")


if __name__ == "__main__":
    main()
