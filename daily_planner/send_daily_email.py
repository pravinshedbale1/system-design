#!/usr/bin/env python3
"""
📅 Daily Study Plan Emailer (v2 — Adaptive)

Sends a clean morning email with:
  1. Today's DSA plan (adaptive — based on actual progress)
  2. Today's System Design plan (adaptive)
  3. Yesterday's progress summary
  4. One motivational line

Runs daily at 6 AM IST via GitHub Actions.
"""

import os, sys, re, hashlib, smtplib, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta, timezone

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

IST = timezone(timedelta(hours=5, minutes=30))

SD_START = datetime(2026, 6, 10, tzinfo=IST).date()
DSA_START = datetime(2026, 6, 10, tzinfo=IST).date()

SD_REPO = os.environ.get("SD_REPO_PATH", ".")
DSA_REPO = os.environ.get("DSA_REPO_PATH", "./dsa")
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")

# ============================================================================
#  SCHEDULE DATA — SYSTEM DESIGN (16 Weeks × 5 Days)
#  Format: (title, phase, {day: [(topic, story), ...]})
# ============================================================================

SD_WEEKS = {
    1: ("The Internet & How Things Talk", "Phase 1", {
        1: [("DNS, HTTP, TCP/IP", "A letter needs an address, a language, and a postal system"),
            ("Client-Server vs P2P", "A restaurant vs a potluck dinner")],
        2: [("REST APIs & HTTP Methods", "A waiter taking your order"),
            ("WebSockets & Long Polling", "A phone call vs checking your mailbox")],
        3: [("Load Balancers", "The hostess at a busy restaurant"),
            ("Reverse Proxies & CDNs", "Branch offices & local warehouses")],
        4: [("Mini-Design: URL Shortener", "Your first system design")],
        5: [("Review + Storytelling Practice", "Narrate the full internet story")],
    }),
    2: ("Data — Where Things Live & Scale", "Phase 1", {
        1: [("SQL vs NoSQL", "A spreadsheet vs a filing cabinet"),
            ("ACID & BASE", "A bank transfer vs a social media like")],
        2: [("Indexing & Query Optimization", "A library without a card catalog"),
            ("Replication", "Photocopies of the Constitution")],
        3: [("Sharding / Partitioning", "Your library outgrew one building"),
            ("CAP Theorem", "The triangle of impossible perfection")],
        4: [("Mini-Design: Pastebin", "Apply all database concepts")],
        5: [("Review + Storytelling", "Tell the story of data at scale")],
    }),
    3: ("Caching, Queues & Not Doing Work", "Phase 1", {
        1: [("Caching Deep Dive", "Your brain doesn't hit the library every time"),
            ("Cache Invalidation", "The hardest problem in CS")],
        2: [("Redis & Memcached", "Swiss Army knife vs a scalpel"),
            ("Message Queues", "A post office that never loses a letter")],
        3: [("Event-Driven Architecture", "Just tell me when it's done"),
            ("Async Processing", "The chef doesn't serve the food")],
        4: [("Mini-Design: Rate Limiter", "A system that protects other systems")],
        5: [("Review + Storytelling", "How caching & queues save the day")],
    }),
    4: ("Consistency, Reliability & Real World", "Phase 1", {
        1: [("Consistency Models", "What does 'up to date' even mean?"),
            ("Consensus Algorithms", "How do 5 servers agree?")],
        2: [("Availability & Fault Tolerance", "The show must go on"),
            ("Distributed Transactions", "2PC — essential and terrible")],
        3: [("Monitoring & Observability", "You can't fix what you can't see"),
            ("Back-of-Envelope Estimation", "The most important 5 minutes")],
        4: [("Design: Key-Value Store", "Your first distributed system")],
        5: [("PHASE 1 CHECKPOINT", "Design any mini-system from scratch")],
    }),
    5: ("Social & Feed Systems", "Phase 2", {
        1: [("Design Twitter/X (1/2)", "From MySQL to a global platform")],
        2: [("Design Twitter/X (2/2)", "Fan-out, celebrity problem, timeline")],
        3: [("Design Instagram (1/2)", "A billion photos")],
        4: [("Design Instagram (2/2)", "Object storage, CDN, feed ranking")],
        5: [("Design Notification System", "Poke a billion users without drowning")],
    }),
    6: ("Messaging & Real-Time", "Phase 2", {
        1: [("Design WhatsApp (1/2)", "End-to-end encrypted global messaging")],
        2: [("Design WhatsApp (2/2)", "WebSockets, ordering, delivery receipts")],
        3: [("Design Slack/Discord (1/2)", "Channels, threads, search, presence")],
        4: [("Design Slack/Discord (2/2)", "Real-time presence, message search")],
        5: [("Design Live Comments/Reactions", "Millions reacting at once")],
    }),
    7: ("Storage & Search", "Phase 2", {
        1: [("Design Google Drive (1/2)", "Planet-scale file sync")],
        2: [("Design Google Drive (2/2)", "Chunking, dedup, sync conflicts")],
        3: [("Design Search Engine (1/2)", "Find one page in a trillion")],
        4: [("Design Search Engine (2/2)", "Inverted index, ranking, sharding")],
        5: [("Design Typeahead/Autocomplete", "Predict before you type")],
    }),
    8: ("Video & Streaming", "Phase 2", {
        1: [("Design YouTube (1/2)", "From upload to Play")],
        2: [("Design YouTube (2/2)", "Transcoding, adaptive bitrate, CDN")],
        3: [("Design Netflix (1/2)", "200M users without buffering")],
        4: [("Design Netflix (2/2)", "Open Connect, personalization")],
        5: [("Design Spotify", "Music that follows you everywhere")],
    }),
    9: ("E-Commerce & Transactions", "Phase 2", {
        1: [("Design Amazon (1/2)", "From browsing to delivery")],
        2: [("Design Amazon (2/2)", "Catalog, inventory, orders")],
        3: [("Design Payment System (1/2)", "Moving money without losing a cent")],
        4: [("Design Payment System (2/2)", "Idempotency, ledger, fraud")],
        5: [("Design Booking System", "Two people can't book the same room")],
    }),
    10: ("Location & Ride-Sharing", "Phase 2", {
        1: [("Design Uber/Lyft (1/2)", "Matching in a moving world")],
        2: [("Design Uber/Lyft (2/2)", "Geohash, real-time location, surge")],
        3: [("Design Google Maps (1/2)", "Routing billions of trips")],
        4: [("Design Google Maps (2/2)", "Dijkstra at scale, live traffic")],
        5: [("PHASE 2 CHECKPOINT", "Full timed mock on unseen system")],
    }),
    11: ("Infrastructure & Platform", "Phase 3", {
        1: [("Distributed Task Scheduler (1/2)", "A billion jobs without missing one")],
        2: [("Distributed Task Scheduler (2/2)", "Failure recovery, exactly-once")],
        3: [("Distributed Cache (1/2)", "Every ms of latency = $ lost")],
        4: [("Distributed Cache (2/2)", "Consistent hashing, eviction, hot keys")],
        5: [("Metrics/Monitoring System", "Watching the watchers")],
    }),
    12: ("Data Pipeline & Analytics", "Phase 3", {
        1: [("Web Crawler (1/2)", "How Google reads the internet")],
        2: [("Web Crawler (2/2)", "URL frontier, dedup, politeness")],
        3: [("Analytics Pipeline (1/2)", "Raw events to insights")],
        4: [("Analytics Pipeline (2/2)", "Stream processing, Lambda/Kappa")],
        5: [("Distributed Logging", "Needle in a haystack of logs")],
    }),
    13: ("Unique/Tricky Systems", "Phase 3", {
        1: [("Ticket Booking (1/2)", "10K people want 100 seats")],
        2: [("Ticket Booking (2/2)", "Waiting room, seat locking")],
        3: [("Collaborative Editor (1/2)", "50 people, one paragraph")],
        4: [("Collaborative Editor (2/2)", "OT vs CRDT, conflict resolution")],
        5: [("URL Shortener at Billion Scale", "Revisit — now you're dangerous")],
    }),
    14: ("Security, Auth & APIs", "Phase 3", {
        1: [("Auth System (1/2)", "Who are you?")],
        2: [("Auth System (2/2)", "JWT, OAuth2, MFA")],
        3: [("API Gateway (1/2)", "Front door to your platform")],
        4: [("API Gateway (2/2)", "Rate limiting, circuit breaking")],
        5: [("Content Moderation", "Keeping the internet safe")],
    }),
    15: ("Mock Interview Marathon", "Phase 3", {
        1: [("Mock 1", "Unseen system, 45 min timed")],
        2: [("Mock 2", "Weak areas focus")],
        3: [("Mock 3", "Curveball system")],
        4: [("Mock 4", "Company-specific style")],
        5: [("Mock 5", "Speed round — 2 systems in 60 min")],
    }),
    16: ("Final Polish", "Phase 3", {
        1: [("Story Compilation", "2-min story for every system")],
        2: [("Building Block Review", "Every block from memory")],
        3: [("Tradeoff Drill", "Why X over Y? × 20 decisions")],
        4: [("Full Simulation", "2 back-to-back interviews")],
        5: [("Light Review + Rest", "Read stories, build confidence")],
    }),
}

# ============================================================================
#  SCHEDULE DATA — DSA (17 Weeks × 7 Days)
#  Format: (title, phase, {day: [(name, diff, pattern), ...] or "string"})
# ============================================================================

DSA_WEEKS = {
    1: ("Arrays & Hashing", "Phase 1", {
        1: [("Two Sum (#1)", "Easy", "HashMap complement"), ("Contains Duplicate (#217)", "Easy", "HashSet")],
        2: [("Valid Anagram (#242)", "Easy", "Frequency int[26]"), ("Two Sum II (#167)", "Med", "Two pointers sorted")],
        3: [("Group Anagrams (#49)", "Med", "HashMap grouping"), ("Top K Frequent (#347)", "Med", "Bucket sort")],
        4: [("Product Except Self (#238)", "Med", "Prefix/Suffix"), ("Longest Consecutive (#128)", "Med", "HashSet sequence")],
        5: [("Encode/Decode Strings (#271)", "Med", "Length-prefix"), ("Valid Sudoku (#36)", "Med", "HashSet per row/col/box")],
        6: [("Subarray Sum = K (#560)", "Med", "Prefix sum + HashMap")],
        7: "Weekly Challenge: 2 unseen problems",
    }),
    2: ("Two Pointers & Sorting", "Phase 1", {
        1: [("Valid Palindrome (#125)", "Easy", "Two pointers inward"), ("Two Sum II (#167)", "Med", "Two pointers sorted")],
        2: [("3Sum (#15)", "Med", "Sort + fix + 2ptr"), ("Container With Most Water (#11)", "Med", "Greedy 2ptr")],
        3: [("Trapping Rain Water (#42)", "Hard", "Two pointers / prefix max"), ("Move Zeroes (#283)", "Easy", "Write pointer")],
        4: [("Sort Colors (#75)", "Med", "Dutch National Flag"), ("Remove Duplicates (#26)", "Easy", "Slow/fast pointer")],
        5: [("4Sum (#18)", "Med", "Sort + fix two + 2ptr"), ("Boats to Save People (#881)", "Med", "Greedy 2ptr")],
        6: "Review + re-solve struggles",
        7: "Weekly Challenge: 2 unseen problems",
    }),
    3: ("Sliding Window", "Phase 1", {
        1: [("Max Sum Subarray Size K", "Easy", "Fixed window"), ("Longest Substring No Repeat (#3)", "Med", "Variable + HashSet")],
        2: [("Min Size Subarray Sum (#209)", "Med", "Variable shrink"), ("Permutation in String (#567)", "Med", "Fixed + freq match")],
        3: [("Min Window Substring (#76)", "Hard", "Variable + freq"), ("Longest Repeating Char Replace (#424)", "Med", "Variable + max freq")],
        4: [("Fruit Into Baskets (#904)", "Med", "At most K distinct"), ("Max Consecutive Ones III (#1004)", "Med", "At most K zeros")],
        5: [("Subarrays K Different (#992)", "Hard", "AtMost(K)-AtMost(K-1)"), ("Sliding Window Max (#239)", "Hard", "Monotonic deque")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge: 2 unseen problems",
    }),
    4: ("Stack & Queue", "Phase 1", {
        1: [("Valid Parentheses (#20)", "Easy", "Stack matching"), ("Min Stack (#155)", "Med", "Auxiliary stack")],
        2: [("Evaluate RPN (#150)", "Med", "Stack eval"), ("Daily Temperatures (#739)", "Med", "Monotonic stack")],
        3: [("Next Greater Element (#496)", "Easy", "Monotonic + HashMap"), ("Largest Rectangle Histogram (#84)", "Hard", "Monotonic stack")],
        4: [("Car Fleet (#853)", "Med", "Stack + sorting"), ("Queue using Stacks (#232)", "Easy", "Two stacks")],
        5: [("Asteroid Collision (#735)", "Med", "Stack simulation"), ("Maximal Rectangle (#85)", "Hard", "Histogram + stack")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    5: ("Linked List", "Phase 1", {
        1: [("Reverse Linked List (#206)", "Easy", "3-pointer"), ("Merge Two Sorted (#21)", "Easy", "Dummy node")],
        2: [("Linked List Cycle (#141)", "Easy", "Floyd's"), ("Cycle II (#142)", "Med", "Floyd's phase 2")],
        3: [("Remove Nth From End (#19)", "Med", "Gap pointers"), ("Reorder List (#143)", "Med", "Mid+reverse+merge")],
        4: [("Merge K Sorted (#23)", "Hard", "Min-heap"), ("Copy Random Pointer (#138)", "Med", "HashMap clone")],
        5: [("LRU Cache (#146)", "Med", "HashMap + DLL"), ("Add Two Numbers (#2)", "Med", "Carry arithmetic")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    6: ("Binary Search", "Phase 1", {
        1: [("Binary Search (#704)", "Easy", "Classic lo/hi/mid"), ("Search Insert (#35)", "Easy", "Lower bound")],
        2: [("Search Rotated (#33)", "Med", "Modified BS"), ("Find Min Rotated (#153)", "Med", "BS for pivot")],
        3: [("Koko Eating Bananas (#875)", "Med", "BS on answer"), ("Search 2D Matrix (#74)", "Med", "Flatten to 1D")],
        4: [("Time Based KV Store (#981)", "Med", "BS on timestamps"), ("Find Peak (#162)", "Med", "BS on unsorted")],
        5: [("Median Two Sorted (#4)", "Hard", "BS on partition"), ("Split Array Largest (#410)", "Hard", "BS on answer")],
        6: "PHASE 1 CHECKPOINT: 5 mixed timed problems",
        7: "Review all Phase 1 patterns",
    }),
    7: ("Trees — DFS", "Phase 2", {
        1: [("Invert Tree (#226)", "Easy", "Recursive DFS"), ("Max Depth (#104)", "Easy", "DFS")],
        2: [("Same Tree (#100)", "Easy", "Compare recursively"), ("Subtree (#572)", "Med", "Compare trees")],
        3: [("Diameter (#543)", "Easy", "Height+diameter"), ("Balanced Tree (#110)", "Easy", "Height DFS")],
        4: [("LCA (#236)", "Med", "Recursive LCA"), ("Path Sum (#112)", "Easy", "Root-to-leaf")],
        5: [("Max Path Sum (#124)", "Hard", "Global max DFS"), ("Good Nodes (#1448)", "Med", "DFS+max tracking")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    8: ("Trees — BFS + BST", "Phase 2", {
        1: [("Level Order (#102)", "Med", "BFS queue"), ("Right Side View (#199)", "Med", "BFS last per level")],
        2: [("Zigzag Level (#103)", "Med", "BFS + direction"), ("Avg of Levels (#637)", "Easy", "BFS average")],
        3: [("Validate BST (#98)", "Med", "Inorder = sorted"), ("Kth Smallest BST (#230)", "Med", "Inorder")],
        4: [("Serialize BT (#297)", "Hard", "Serialization"), ("Construct BT (#105)", "Med", "Divide & conquer")],
        5: [("BST Iterator (#173)", "Med", "Controlled inorder"), ("LCA of BST (#235)", "Med", "BST property")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    9: ("Heap / Priority Queue", "Phase 2", {
        1: [("Kth Largest (#215)", "Med", "Heap/QuickSelect"), ("Last Stone Weight (#1046)", "Easy", "Max heap")],
        2: [("K Closest Points (#973)", "Med", "Min-heap size K"), ("Top K Frequent revisit (#347)", "Med", "Heap vs Bucket")],
        3: [("Find Median Stream (#295)", "Hard", "Two-heap")],
        4: [("Merge K Sorted revisit (#23)", "Hard", "K-way merge"), ("Task Scheduler (#621)", "Med", "Greedy+heap")],
        5: [("Reorganize String (#767)", "Med", "Greedy heap"), ("K Closest Sorted (#658)", "Med", "BS + 2ptr")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    10: ("Backtracking", "Phase 2", {
        1: [("Subsets (#78)", "Med", "Include/exclude"), ("Subsets II (#90)", "Med", "Skip duplicates")],
        2: [("Permutations (#46)", "Med", "Swap-based"), ("Permutations II (#47)", "Med", "used[] array")],
        3: [("Combination Sum (#39)", "Med", "Unbounded"), ("Combination Sum II (#40)", "Med", "Bounded+dedup")],
        4: [("Word Search (#79)", "Med", "Grid backtrack"), ("Palindrome Partition (#131)", "Med", "String partition")],
        5: [("N-Queens (#51)", "Hard", "Constraint satisfaction"), ("Sudoku Solver (#37)", "Hard", "Constraint")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    11: ("Graphs — BFS/DFS", "Phase 2", {
        1: [("Number of Islands (#200)", "Med", "Grid DFS"), ("Clone Graph (#133)", "Med", "DFS+clone")],
        2: [("Pacific Atlantic (#417)", "Med", "Multi-source DFS"), ("Surrounded Regions (#130)", "Med", "Border DFS")],
        3: [("Course Schedule (#207)", "Med", "Topo sort Kahn's"), ("Course Schedule II (#210)", "Med", "Topo sort DFS")],
        4: [("Word Ladder (#127)", "Hard", "BFS shortest"), ("Rotting Oranges (#994)", "Med", "Multi-source BFS")],
        5: [("Accounts Merge (#721)", "Med", "Union-Find"), ("Graph Valid Tree (#261)", "Med", "Union-Find/DFS")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    12: ("Advanced Graphs", "Phase 2", {
        1: [("Network Delay (#743)", "Med", "Dijkstra"), ("Cheapest Flights (#787)", "Med", "Bellman-Ford")],
        2: [("Swim in Rising Water (#778)", "Hard", "BS+BFS"), ("Path Min Effort (#1631)", "Med", "Dijkstra variant")],
        3: [("Redundant Connection (#684)", "Med", "Union-Find"), ("Min Cost Connect (#1135)", "Med", "MST Kruskal")],
        4: [("Alien Dictionary (#269)", "Hard", "Topo sort chars"), ("Longest Increasing Path (#329)", "Hard", "DFS+memo")],
        5: [("Critical Connections (#1192)", "Hard", "Tarjan's bridges")],
        6: "PHASE 2 CHECKPOINT: 5 mixed timed problems",
        7: "Review Phase 1+2 patterns",
    }),
    13: ("DP — 1D", "Phase 3", {
        1: [("Climbing Stairs (#70)", "Easy", "Fibonacci DP"), ("House Robber (#198)", "Med", "Linear DP")],
        2: [("House Robber II (#213)", "Med", "Circular DP"), ("Decode Ways (#91)", "Med", "Counting DP")],
        3: [("Coin Change (#322)", "Med", "Min unbounded"), ("Coin Change 2 (#518)", "Med", "Count ways")],
        4: [("LIS (#300)", "Med", "LIS pattern"), ("Word Break (#139)", "Med", "Substring DP")],
        5: [("Max Product Subarray (#152)", "Med", "Track min/max"), ("Partition Equal Subset (#416)", "Med", "0/1 knapsack")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    14: ("DP — 2D & Strings", "Phase 3", {
        1: [("Unique Paths (#62)", "Med", "Grid DP"), ("Min Path Sum (#64)", "Med", "Grid DP")],
        2: [("LCS (#1143)", "Med", "Two-string DP"), ("Edit Distance (#72)", "Hard", "Two-string DP")],
        3: [("Longest Palindromic Sub (#5)", "Med", "Expand center"), ("Palindromic Substrings (#647)", "Med", "Expand center")],
        4: [("Interleaving String (#97)", "Hard", "2-string adv"), ("Distinct Subsequences (#115)", "Hard", "2-string DP")],
        5: [("Burst Balloons (#312)", "Hard", "Interval DP"), ("Regex Matching (#10)", "Hard", "String match DP")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    15: ("Tries, Intervals & Greedy", "Phase 3", {
        1: [("Implement Trie (#208)", "Med", "Trie"), ("Word Search II (#212)", "Hard", "Trie+DFS")],
        2: [("Add/Search Words (#211)", "Med", "Trie wildcards"), ("Longest Word Dict (#720)", "Med", "Trie+BFS")],
        3: [("Merge Intervals (#56)", "Med", "Sort+merge"), ("Insert Interval (#57)", "Med", "Interval insert")],
        4: [("Non-overlapping (#435)", "Med", "Greedy interval"), ("Meeting Rooms II (#253)", "Med", "Sweep line")],
        5: [("Jump Game (#55)", "Med", "Greedy"), ("Jump Game II (#45)", "Med", "Greedy BFS"), ("Gas Station (#134)", "Med", "Greedy")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    16: ("Advanced Mixed", "Phase 3", {
        1: [("LFU Cache (#460)", "Hard", "Complex DS"), ("LRU Cache revisit (#146)", "Med", "HashMap+DLL")],
        2: [("Skyline Problem (#218)", "Hard", "Sweep+heap"), ("Trapping Rain Water revisit (#42)", "Hard", "2ptr")],
        3: [("Word Ladder II (#126)", "Hard", "BFS+backtrack"), ("Longest Valid Parens (#32)", "Hard", "Stack/DP")],
        4: [("Maximal Rectangle (#85)", "Hard", "Histogram+stack"), ("Largest Rectangle revisit (#84)", "Hard", "Monotonic stack")],
        5: [("Company-tagged hards", "Hard", "Mixed — 2-3 problems")],
        6: "Review + spaced repetition",
        7: "Weekly Challenge",
    }),
    17: ("Mock Interview Marathon", "Phase 3", {
        1: "Mock 1: 2 problems, 45 min each, any pattern",
        2: "Mock 2: 2 problems, focus on weak patterns",
        3: "Mock 3: 2 hard problems, full simulation",
        4: "Mock 4: Company-tagged (Google/Amazon/Meta)",
        5: "Mock 5: Speed — 4 mediums in 60 min",
        6: "Mock 6: Full interview day — 2 rounds back-to-back",
        7: "Final review: entire pattern index from memory",
    }),
}

QUOTES = [
    "Consistency beats intensity. Show up every day.",
    "First, solve the problem. Then, write the code.",
    "Every expert was once a beginner.",
    "Small daily improvements → staggering long-term results.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Hard choices, easy life. Easy choices, hard life.",
    "Discipline is choosing between what you want now and what you want most.",
    "Strive for progress, not perfection.",
    "You don't have to be great to start, but you have to start to be great.",
    "The best time was yesterday. The next best time is now.",
    "It's not about being the best. It's about being better than yesterday.",
    "Stay hungry. Stay foolish.",
    "What you do every day matters more than what you do once in a while.",
    "Don't count the days. Make the days count.",
]

# ============================================================================
#  HELPERS
# ============================================================================

def today_ist():
    return datetime.now(IST).date()

def compute_position(start, today):
    delta = (today - start).days
    if delta < 0:
        return None, None, delta
    return delta // 7 + 1, delta % 7 + 1, delta

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, PermissionError):
        return ""

# ============================================================================
#  ADAPTIVE PARSERS — read actual progress from CONVERSATION_STATE.md
# ============================================================================

def parse_current_position(content):
    """Extract current position fields as dict."""
    state = {}
    m = re.search(r'## 📍 Current Position\s*\n\s*\|.*\|\s*\n\s*\|[-\s|]+\|\s*\n((?:\|.*\n)*)', content)
    if m:
        for line in m.group(1).strip().split('\n'):
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                key = re.sub(r'\*\*', '', parts[0]).strip()
                state[key] = re.sub(r'\*\*', '', parts[1]).strip()
    return state


def parse_next_plan(content):
    """Extract the Next Session Plan section as clean text lines."""
    m = re.search(r'## ⏭️ Next Session Plan\s*\n(.*?)(?=\n---|\n## |\Z)', content, re.DOTALL)
    if not m:
        return None
    raw = m.group(1).strip()
    lines = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line or line.startswith('**Focus**') or line.startswith('-'):
            if line.startswith('- '):
                lines.append(line)
            continue
        if line.startswith('**'):
            # Header like **Topic**: ... or **Plan**:
            clean = re.sub(r'\*\*', '', line).strip()
            if clean.endswith(':'):
                continue  # skip bare headers like "Plan:"
            lines.append(clean)
        elif line.startswith(('1.', '2.', '3.', '4.', '5.')):
            lines.append(line)
    return lines if lines else None


def parse_latest_session(content):
    """Extract the most recent session entry."""
    sessions = re.findall(
        r'### Session #(\d+)\s*—\s*(.+?)\s*—\s*(.+?)\n(.*?)(?=### Session #|\n---|\Z)',
        content, re.DOTALL
    )
    if not sessions:
        return None
    last = sessions[-1]
    # Pull out problem results
    results = re.findall(r'- (.+?(?:LC #\d+).+?)(?:\n|$)', last[3])
    return {
        'num': last[0],
        'date': last[1].strip(),
        'topic': last[2].strip(),
        'results': [r.strip()[:120] for r in results[:5]],
    }


def parse_spaced_rep_due(content, today):
    """Find items due today or overdue from review_schedule.md."""
    due = []
    current_box = ""
    for line in content.split('\n'):
        if '## ' in line and 'Box' in line:
            bm = re.search(r'Box (\d)', line)
            current_box = f"Box {bm.group(1)}" if bm else ""
        if '|' in line and 'LC #' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 4:
                problem = parts[0]
                pattern = parts[1]
                # Search for date in last columns
                for part in reversed(parts):
                    dm = re.search(r'(June|July|Aug|Sep|Oct)\w*\s+(\d+)', part)
                    if dm:
                        month_map = {'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10}
                        mn = dm.group(1)[:3]
                        m = month_map.get(mn, 0)
                        if m:
                            try:
                                rd = datetime(2026, m, int(dm.group(2))).date()
                                if rd <= today:
                                    due.append((problem, pattern, current_box, rd < today))
                            except ValueError:
                                pass
                        break
    return due


def get_adaptive_plan(state, next_plan, cal_week, cal_day, weeks, total_weeks, content_days):
    """
    Returns (week_title, phase, content, status_note).
    Uses next_plan (from CONVERSATION_STATE) if available, else falls back to calendar.
    """
    # If no state data at all, use calendar
    if not state and not next_plan:
        return _calendar_lookup(cal_week, cal_day, weeks, total_weeks, content_days)

    # If we have a next plan from CONVERSATION_STATE, use it (adaptive)
    if next_plan:
        # Try to determine actual week from state
        actual_week_str = state.get('Current Week', '')
        actual_week = None
        wm = re.search(r'Week (\d+)', actual_week_str)
        if wm:
            actual_week = int(wm.group(1))

        w = weeks.get(actual_week or cal_week)
        title = w[0] if w else f"Week {actual_week or cal_week}"
        phase = w[1] if w else ""

        # Determine if behind/ahead
        note = ""
        if cal_week and actual_week and cal_week <= total_weeks:
            if actual_week < cal_week:
                note = f"⚠️ Behind schedule (Week {actual_week} vs expected Week {cal_week})"
            elif actual_week > cal_week:
                note = f"🚀 Ahead of schedule"

        return title, phase, next_plan, note

    # State exists but no next plan — use calendar
    return _calendar_lookup(cal_week, cal_day, weeks, total_weeks, content_days)


def _calendar_lookup(week, day, weeks, total_weeks, content_days):
    if not week or week > total_weeks:
        return None, None, None, "Plan complete ✅"
    w = weeks.get(week)
    if not w:
        return None, None, None, ""
    title, phase, days = w
    if day > content_days:
        return title, phase, "Rest day — review the week's material", ""
    content = days.get(day)
    return title, phase, content, ""


# ============================================================================
#  EMAIL GENERATOR — Clean, concise, no fluff
# ============================================================================

def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def generate_email(today, dsa_data, sd_data, dsa_session, sd_session, due_reviews):
    """Generate a clean, minimal email."""

    date_str = today.strftime('%A, %b %d')

    # --- Build DSA section ---
    dsa_week_title, dsa_phase, dsa_content, dsa_note = dsa_data
    dsa_html = _build_section(
        "DSA", dsa_week_title, dsa_phase, dsa_content, dsa_note,
        "#b45309", due_reviews
    )

    # --- Build SD section ---
    sd_week_title, sd_phase, sd_content, sd_note = sd_data
    sd_html = _build_section(
        "System Design", sd_week_title, sd_phase, sd_content, sd_note,
        "#1d4ed8", None
    )

    # --- Yesterday's progress ---
    yesterday_html = _build_yesterday(dsa_session, sd_session)

    # --- Quote ---
    qidx = int(hashlib.md5(date_str.encode()).hexdigest(), 16) % len(QUOTES)

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f9fafb;font-family:-apple-system,BlinkMacSystemFont,
'Segoe UI',Roboto,sans-serif;color:#1f2937;line-height:1.6;">
<div style="max-width:560px;margin:0 auto;padding:24px 16px;">

<h1 style="font-size:20px;font-weight:700;margin:0 0 24px 0;color:#111827;">
📅 {date_str}</h1>

{dsa_html}
{sd_html}
{yesterday_html}

<p style="text-align:center;color:#9ca3af;font-size:13px;margin:32px 0 0 0;
          padding-top:16px;border-top:1px solid #e5e7eb;">
{_esc(QUOTES[qidx])}</p>

</div></body></html>"""

    return html


def _build_section(label, week_title, phase, content, note, accent, due_reviews=None):
    """Build one plan section (DSA or SD)."""
    if not week_title and not content:
        return f"""<div style="margin:0 0 28px 0;">
<h2 style="font-size:16px;color:{accent};margin:0 0 8px 0;">{label}</h2>
<p style="color:#6b7280;margin:0;">Plan complete ✅</p>
</div>"""

    # Header
    header = f"{week_title}"
    if phase:
        header += f" · {phase}"

    # Status note (behind/ahead)
    note_html = ""
    if note:
        nc = "#dc2626" if "Behind" in note else "#059669"
        note_html = f'<p style="color:{nc};font-size:13px;font-weight:600;margin:4px 0 0 0;">{_esc(note)}</p>'

    # Spaced rep due (only for DSA)
    rep_html = ""
    if due_reviews:
        items = []
        for prob, pat, box, overdue in due_reviews:
            tag = " (OVERDUE)" if overdue else ""
            items.append(f"Recall: {_esc(prob)}{tag}")
        rep_html = "".join(f'<li style="color:#92400e;font-size:14px;margin:2px 0;">⏰ {i}</li>' for i in items)

    # Content
    content_html = ""
    if isinstance(content, str):
        # Simple string (review day, challenge day, rest day)
        content_html = f'<p style="color:#4b5563;font-size:14px;margin:8px 0;">{_esc(content)}</p>'
    elif isinstance(content, list):
        items_html = ""
        for item in content:
            if isinstance(item, tuple):
                if len(item) == 3:
                    # DSA problem: (name, difficulty, pattern)
                    name, diff, pat = item
                    dc = {"Easy":"#059669","Med":"#d97706","Hard":"#dc2626","":"#6b7280"}.get(diff,"#6b7280")
                    items_html += (f'<li style="font-size:14px;margin:4px 0;color:#1f2937;">'
                                   f'{_esc(name)} '
                                   f'<span style="color:{dc};font-size:12px;font-weight:600;">{diff}</span>'
                                   f'<br><span style="color:#6b7280;font-size:12px;">{_esc(pat)}</span></li>')
                elif len(item) == 2:
                    # SD topic: (name, story)
                    name, story = item
                    items_html += (f'<li style="font-size:14px;margin:4px 0;color:#1f2937;">'
                                   f'{_esc(name)}'
                                   f'<br><span style="color:#6b7280;font-size:12px;font-style:italic;">'
                                   f'"{_esc(story)}"</span></li>')
            elif isinstance(item, str):
                # Line from Next Session Plan (adaptive)
                clean = re.sub(r'\*\*', '', item)
                clean = re.sub(r'^[\d]+\.\s*', '', clean)
                clean = re.sub(r'^[⏰🧠🆕📖🔗]\s*', '', clean)
                clean = re.sub(r'^- ', '', clean)
                items_html += f'<li style="font-size:14px;margin:3px 0;color:#374151;">{_esc(clean.strip())}</li>'
        content_html = f'<ul style="margin:8px 0;padding-left:20px;list-style:disc;">{rep_html}{items_html}</ul>'
    elif content is None:
        content_html = '<p style="color:#6b7280;font-size:14px;">No content scheduled.</p>'

    if rep_html and not content_html.startswith('<ul'):
        content_html = f'<ul style="margin:8px 0;padding-left:20px;list-style:disc;">{rep_html}</ul>{content_html}'

    return f"""<div style="margin:0 0 28px 0;">
<h2 style="font-size:16px;color:{accent};margin:0 0 2px 0;">{label}</h2>
<p style="color:#6b7280;font-size:13px;margin:0;">{_esc(header)}</p>
{note_html}
{content_html}
</div>"""


def _build_yesterday(dsa_session, sd_session):
    """Build yesterday's progress section."""
    if not dsa_session and not sd_session:
        return """<div style="margin:0 0 28px 0;padding-top:20px;border-top:1px solid #e5e7eb;">
<h2 style="font-size:16px;color:#4b5563;margin:0 0 8px 0;">Yesterday</h2>
<p style="color:#9ca3af;font-size:14px;margin:0;">No sessions recorded yet.</p>
</div>"""

    parts = []

    if dsa_session:
        s = dsa_session
        summary = f"<strong>DSA Session #{s['num']}</strong> — {_esc(s['date'])} — {_esc(s['topic'])}"
        if s['results']:
            results = "".join(f"<li style='font-size:13px;color:#4b5563;margin:2px 0;'>{_esc(r)}</li>"
                              for r in s['results'])
            summary += f"<ul style='margin:4px 0 0 0;padding-left:18px;'>{results}</ul>"
        parts.append(summary)

    if sd_session:
        s = sd_session
        parts.append(f"<strong>System Design Session #{s['num']}</strong> — {_esc(s['date'])} — {_esc(s['topic'])}")

    if not sd_session:
        parts.append("<span style='color:#9ca3af;'>System Design: No session yet</span>")
    if not dsa_session:
        parts.append("<span style='color:#9ca3af;'>DSA: No session yet</span>")

    inner = "".join(f"<p style='font-size:14px;margin:6px 0;color:#1f2937;'>{p}</p>" for p in parts)

    return f"""<div style="margin:0 0 28px 0;padding-top:20px;border-top:1px solid #e5e7eb;">
<h2 style="font-size:16px;color:#4b5563;margin:0 0 8px 0;">Yesterday</h2>
{inner}
</div>"""


# ============================================================================
#  SENDER
# ============================================================================

def send_email(subject, html):
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        log.error("GMAIL_ADDRESS and GMAIL_APP_PASSWORD required")
        sys.exit(1)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = f"Study Plan <{GMAIL_ADDRESS}>"
    msg['To'] = GMAIL_ADDRESS
    msg.attach(MIMEText(html, 'html'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            s.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, msg.as_string())
        log.info(f"✅ Email sent to {GMAIL_ADDRESS}")
    except Exception as e:
        log.error(f"❌ Failed: {e}")
        sys.exit(1)


# ============================================================================
#  MAIN
# ============================================================================

def main():
    dry_run = "--dry-run" in sys.argv
    today = today_ist()
    log.info(f"📅 {today.strftime('%A, %B %d, %Y')}")

    # Calendar positions
    sd_week, sd_day, _ = compute_position(SD_START, today)
    dsa_week, dsa_day, _ = compute_position(DSA_START, today)

    # Read state files
    sd_state_raw = read_file(os.path.join(SD_REPO, "CONVERSATION_STATE.md"))
    dsa_state_raw = read_file(os.path.join(DSA_REPO, "CONVERSATION_STATE.md"))

    sd_state = parse_current_position(sd_state_raw)
    dsa_state = parse_current_position(dsa_state_raw)

    sd_next = parse_next_plan(sd_state_raw)
    dsa_next = parse_next_plan(dsa_state_raw)

    # Adaptive plans
    sd_data = get_adaptive_plan(sd_state, sd_next, sd_week, sd_day, SD_WEEKS, 16, 5)
    dsa_data = get_adaptive_plan(dsa_state, dsa_next, dsa_week, dsa_day, DSA_WEEKS, 17, 7)

    # Latest sessions (yesterday's progress)
    sd_session = parse_latest_session(sd_state_raw)
    dsa_session = parse_latest_session(dsa_state_raw)

    # Spaced rep
    review_raw = read_file(os.path.join(DSA_REPO, "spaced_repetition", "review_schedule.md"))
    due = parse_spaced_rep_due(review_raw, today)

    # Generate
    html = generate_email(today, dsa_data, sd_data, dsa_session, sd_session, due)

    subject = f"📅 {today.strftime('%b %d')} — Study Plan"

    if dry_run:
        preview = os.path.join(SD_REPO, "daily_planner", "preview.html")
        with open(preview, 'w') as f:
            f.write(html)
        log.info(f"Preview: {preview}")
    else:
        send_email(subject, html)

    log.info("Done")


if __name__ == "__main__":
    main()
