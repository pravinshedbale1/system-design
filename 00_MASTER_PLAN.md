# 🏗️ SYSTEM DESIGN MASTERY — 16-WEEK MASTER PLAN (112 DAYS)

> **June 10, 2026 → September 29, 2026** | 112 Days | ~40+ Systems Designed
> **Goal**: Walk into any system design interview — Google, Amazon, Meta, Netflix, Uber — and design any system from scratch with confidence, depth, and storytelling that makes interviewers want to hire you on the spot.
>
> ⚠️ _This is NOT a "memorize 20 designs" plan. This is a "understand 8 pillars so deeply that you can design ANYTHING" plan._

---

## 🎭 The Philosophy: Storytelling Over Memorizing

> **A great system design answer is a STORY, not a diagram.**
>
> Imagine you're the CTO explaining to your board why you built the system this way.
> You don't recite textbook definitions. You tell them:
> - "We started with the simplest thing that could work..."
> - "But then we hit this problem at scale..."
> - "So we evolved the architecture to handle..."
> - "And the tradeoff we made was..."
>
> **That's how you'll learn here. Every concept is a story. Every system is a journey.**

---

## How Each Session Works

### 📚 Phase A — The Story (relaxed, conversational)

```
1. 🔄 Quick Recall (5 min)
   └─ "Tell me the story of the last system we designed"
   └─ Focus on WHY decisions were made, not WHAT components exist

2. 🧠 Concept Deep-Dive (if needed)
   └─ New building block? I teach it as a STORY
   └─ "Imagine you're running a restaurant..." → leads to load balancing
   └─ "Your library is growing..." → leads to database sharding
   └─ No abstract theory dumps — every concept is grounded in intuition

3. 🔗 Connect to Previous Knowledge
   └─ "Remember when we built the URL shortener and hit the read bottleneck?"
   └─ "Same problem, but now at 100x scale..."
   └─ Progressive building — each system builds on the last
```

### 🔴 Phase B — Design Interview Simulation (REAL PRESSURE)

> **⚠️ Once we enter Phase B, I become your interviewer. 45 minutes. No mercy.**
> You are sitting across from a Staff Engineer at Google.
> They just said: "Design Twitter." The clock is ticking.

```
4. 🎯 The Problem Drop (the interview begins)
   └─ "Design [System X]" — just like a real interviewer would say it
   └─ ⏱️ TIMER: 45 minutes (some sessions: 35 min for speed practice)
   └─ I give minimal context — YOU must ask the right questions

5. 🗣️ Requirements Gathering (YOU drive this — 5 min)
   └─ Functional requirements: "What should the system DO?"
   └─ Non-functional requirements: "How well should it do it?"
   └─ Scale estimation: users, QPS, storage, bandwidth
   └─ If you skip this → "Hold on, what problem are we actually solving?"
   └─ INTERVIEWER PROBES:
       • "What's more important — consistency or availability?"
       • "How many users are we talking about?"
       • "What's the read:write ratio?"
       • "Do we need real-time or near-real-time?"

6. 🏗️ High-Level Design (10-15 min)
   └─ Start with the simplest architecture that works
   └─ API design: what endpoints exist?
   └─ Data model: what entities, what relationships?
   └─ Core flow: trace a request end-to-end
   └─ I probe: "What happens when a user does X?"
   └─ If you jump to microservices immediately → "Why not a monolith first?"

7. 🔬 Deep Dive (15-20 min)
   └─ I pick 1-2 areas to go deep:
       • "How does the feed generation work exactly?"
       • "Walk me through what happens when 1M people like a post simultaneously"
       • "How do you handle a database failure?"
   └─ I expect: specific algorithms, data structures, protocols
   └─ I push back: "What if that server crashes?" / "What about consistency?"

8. 📏 Scale & Bottleneck Analysis (5 min)
   └─ "Where does this break at 10x scale?"
   └─ "What's your bottleneck?"
   └─ "How would you monitor this system?"

9. ⏱️ TIME CALLED — Design Review
   └─ 🟢 STRONG HIRE / 🟡 HIRE / 🟠 LEAN NO HIRE / 🔴 NO HIRE
   └─ Scoring:
       • Requirements gathering (did you ask the right questions?)
       • API & data model clarity
       • Architecture reasoning (WHY, not just WHAT)
       • Depth on deep-dive topics
       • Scale awareness (numbers, bottlenecks)
       • Tradeoff articulation
       • Communication clarity (did you tell a story?)
```

### 📦 Phase C — Debrief & Story Extraction (relaxed again)

```
10. 📖 The Story We'd Tell in an Interview
    └─ I help you craft the "elevator pitch" version
    └─ "If someone asks you to design X, here's the 2-minute story..."

11. 🧩 Building Block Extraction
    └─ "This system taught us about [caching/sharding/event sourcing]..."
    └─ Link to building_blocks/ knowledge base

12. 📝 State Update
    └─ Update CONVERSATION_STATE.md
    └─ Update the system's design document
    └─ Add to spaced repetition
```

### 🎭 Interview Pressure Rules (NON-NEGOTIABLE)

```
• I do NOT give away the architecture — ever. I nudge, I probe, I wait.
• If you're stuck, I give at most 2 hints. After that: "Let's simplify — what's the MVP?"
• I track hints given per design and note them in the session log.
• I use intentional silence — if you stop talking, I wait before prompting.
• I ask follow-up questions that a real interviewer would:
    - "Why not use X instead?"
    - "What happens during a network partition?"
    - "How do you handle the thundering herd?"
    - "What's the consistency model here?"
• I give a HIRE/NO-HIRE rating after every design — this is your feedback loop.
• The goal is NOT to make you feel bad — it's to build the muscle memory
  so the real interview feels EASY by comparison.
```

---

## ⚙️ Daily Structure

| Activity | Time | Description |
|----------|------|-------------|
| **Story Recall** | 5-10 min | Retell the story of a previously designed system |
| **Concept/Building Block** | 20-30 min | Learn a new concept through stories and analogies |
| **Design Session** | 45-60 min | Full system design with interview simulation |
| **Reflection & Notes** | 10 min | Update state, extract patterns, craft the story |

---

# 🟢 PHASE 1 — THE FOUNDATION: Building Blocks That Make Everything Work (Weeks 1-4)

> **Goal**: Master the 8 pillars of system design so deeply that you can explain each one
> as a story at a dinner party. No system design question can surprise you because you understand
> the BUILDING BLOCKS, not just the blueprints.
>
> **The Analogy**: Before you can design a skyscraper, you need to understand concrete, steel,
> plumbing, electricity, and elevators. That's what Phase 1 is.

---

## Week 1: The Internet & How Things Talk (June 10 – June 16)

### The Story Arc
> *"You type google.com and press Enter. What happens next is one of the most beautiful
> engineering stories ever told. By the end of this week, you'll be able to narrate every
> millisecond of that journey — and that story alone can impress in an interview."*

### Day-by-Day Progression

| Day | Topic | The Story | What You'll Be Able to Explain |
|-----|-------|-----------|-------------------------------|
| D1 | **DNS, HTTP, TCP/IP** | "A letter needs an address, a language, and a postal system" | How a URL becomes a web page. Why TCP, not UDP for web. |
| D1 | **Client-Server vs P2P** | "A restaurant vs a potluck dinner" | When to use each, real-world examples |
| D2 | **REST APIs & HTTP Methods** | "A waiter taking your order" | Design a clean API for any feature in 5 minutes |
| D2 | **WebSockets & Long Polling** | "A phone call vs checking your mailbox" | When real-time is needed, how to implement it |
| D3 | **Load Balancers** | "The hostess at a busy restaurant" | Round robin, least connections, consistent hashing, L4 vs L7 |
| D3 | **Reverse Proxies & CDNs** | "Branch offices & local warehouses" | Why Netflix doesn't serve video from one building |
| D4 | **🔨 Mini-Design: URL Shortener** | Your FIRST system design — simple, but teaches everything | End-to-end design with all Week 1 concepts |
| D5 | **Review + Storytelling Practice** | Tell the story of how the internet works | Practice narrating DNS→TCP→HTTP→LB→Server flow |

### Building Blocks Unlocked
- [ ] Networking fundamentals (DNS, TCP, HTTP)
- [ ] API design (REST, WebSocket)
- [ ] Load balancing strategies
- [ ] CDN & caching at the edge
- [ ] **First system designed: URL Shortener** ✨

---

## Week 2: Data — Where Things Live & How They Scale (June 17 – June 23)

### The Story Arc
> *"Every system is just 'take data in, store it, give it back.' The question is:
> HOW do you store a billion things and find any one of them in milliseconds?
> This week, you'll understand the answer so well that databases will feel intuitive, not scary."*

### Day-by-Day Progression

| Day | Topic | The Story | What You'll Be Able to Explain |
|-----|-------|-----------|-------------------------------|
| D1 | **SQL vs NoSQL** | "A spreadsheet vs a filing cabinet" | When to use relational vs document vs key-value vs column |
| D1 | **ACID & BASE** | "A bank transfer vs a social media like" | Why some things need transactions and others don't |
| D2 | **Indexing & Query Optimization** | "A library without a card catalog is useless" | B-trees, hash indexes, covering indexes, explain plans |
| D2 | **Replication** | "Making photocopies of your only copy of the Constitution" | Leader-follower, leader-leader, quorum reads/writes |
| D3 | **Sharding / Partitioning** | "Your library outgrew one building — time to open branches" | Hash vs range sharding, hot spots, resharding, consistent hashing |
| D3 | **CAP Theorem** | "The triangle of impossible perfection" | Real-world tradeoffs: CP vs AP systems, when to choose each |
| D4 | **🔨 Mini-Design: Pastebin / Notes Service** | Apply all database concepts to a real system | Schema design, replication strategy, sharding key selection |
| D5 | **Review + Storytelling Practice** | Tell the story of data at scale | Practice narrating "small DB → replicated → sharded" evolution |

### Building Blocks Unlocked
- [ ] SQL vs NoSQL decision framework
- [ ] ACID transactions & BASE eventual consistency
- [ ] Database indexing strategies
- [ ] Replication patterns (sync, async, quorum)
- [ ] Sharding strategies & consistent hashing
- [ ] CAP theorem practical application
- [ ] **System designed: Pastebin** ✨

---

## Week 3: Caching, Queues & The Art of Not Doing Work (June 24 – June 30)

### The Story Arc
> *"The fastest way to do something is to not do it at all. That's what caching is.
> And when you MUST do something, but not right now? That's what queues are.
> These two ideas alone can take a system from 'crashing under load' to 'effortlessly handling millions.'"*

### Day-by-Day Progression

| Day | Topic | The Story | What You'll Be Able to Explain |
|-----|-------|-----------|-------------------------------|
| D1 | **Caching Deep Dive** | "Your brain doesn't go to the library every time you need a fact" | Cache-aside, write-through, write-back, eviction (LRU/LFU) |
| D1 | **Cache Invalidation** | "The hardest problem in CS — and how we live with it" | TTL, event-based invalidation, cache stampede, thundering herd |
| D2 | **Redis & Memcached** | "The difference between a Swiss Army knife and a scalpel" | When to use each, data structures in Redis, persistence options |
| D2 | **Message Queues** | "A post office that never loses a letter" | Kafka vs RabbitMQ vs SQS — when, why, tradeoffs |
| D3 | **Event-Driven Architecture** | "Instead of asking 'is it ready yet?', just tell me when it's done" | Pub/sub, event sourcing, CQRS — the story of decoupling |
| D3 | **Async Processing** | "The chef doesn't serve the food — the waiter does" | Worker pools, job queues, idempotency, retry strategies |
| D4 | **🔨 Mini-Design: Rate Limiter** | A system that protects other systems | Token bucket, sliding window, distributed rate limiting |
| D5 | **Review + Storytelling Practice** | Tell the story of "how caching & queues save the day" | Practice narrating a system evolution with caching layers |

### Building Blocks Unlocked
- [ ] Caching strategies & eviction policies
- [ ] Cache invalidation patterns
- [ ] Message queues & event-driven architecture
- [ ] Async processing & worker patterns
- [ ] **System designed: Rate Limiter** ✨

---

## Week 4: Consistency, Reliability & The Real World (July 1 – July 7)

### The Story Arc
> *"Systems don't fail — they partially fail. A server doesn't just 'stop working.'
> The network gets slow. The disk fills up. One replica has stale data.
> This week, you learn to design systems that SURVIVE the chaos of the real world."*

### Day-by-Day Progression

| Day | Topic | The Story | What You'll Be Able to Explain |
|-----|-------|-----------|-------------------------------|
| D1 | **Consistency Models** | "What does 'up to date' even mean?" | Strong, eventual, causal, read-your-writes, linearizability |
| D1 | **Consensus Algorithms** | "How do 5 servers agree on anything? (Spoiler: it's hard)" | Raft/Paxos intuition, leader election, split-brain |
| D2 | **Availability & Fault Tolerance** | "The show must go on — even when things break" | Redundancy, failover, health checks, circuit breakers |
| D2 | **Distributed Transactions** | "Two-phase commit and why it's both essential and terrible" | 2PC, Saga pattern, compensating transactions |
| D3 | **Monitoring & Observability** | "You can't fix what you can't see" | Metrics, logs, traces (the three pillars), SLOs/SLAs |
| D3 | **Back-of-Envelope Estimation** | "The most important 5 minutes of any design interview" | Powers of 2, latency numbers, QPS/storage/bandwidth estimation |
| D4 | **🔨 Design: Key-Value Store** | Your first "real" distributed system | Consistent hashing, replication, conflict resolution (vector clocks) |
| D5 | **🎯 PHASE 1 CHECKPOINT** | Design any mini-system using all building blocks | Full timed design + storytelling assessment |

### Building Blocks Unlocked
- [ ] Consistency models & consensus
- [ ] Fault tolerance patterns
- [ ] Distributed transaction strategies
- [ ] Monitoring & observability
- [ ] Back-of-envelope estimation
- [ ] **System designed: Distributed Key-Value Store** ✨

---

# 🟡 PHASE 2 — THE CLASSICS: Systems Everyone Must Know (Weeks 5-10)

> **Goal**: Design the 12-15 most commonly asked systems with depth and confidence.
> Each system is a STORY — with a beginning (requirements), middle (evolution), and end (tradeoffs).
>
> **The Analogy**: Phase 1 gave you the ingredients. Phase 2 teaches you the recipes.
> But more importantly, it teaches you WHY each recipe works — so you can improvise.

---

## Week 5: Social & Feed Systems (July 8 – July 14)

### The Story Arc
> *"You open Instagram. In 0.3 seconds, you see a feed of posts from people you follow —
> personalized, ranked, with photos loaded. Behind that 0.3 seconds is one of the most
> complex engineering systems ever built. Let's build it."*

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design Twitter/X** | "From a single MySQL table to a global real-time platform" |
| | | Fan-out on write vs fan-out on read, celebrity problem, timeline service |
| D3-D4 | **Design Instagram/Photo Sharing** | "Storing, serving, and recommending a billion photos" |
| | | Object storage, CDN, feed ranking, content moderation pipeline |
| D5 | **Design a Notification System** | "How to poke a billion users without drowning" |
| | | Push vs pull, priority queues, rate limiting, cross-platform delivery |

### Patterns to Extract
- Fan-out strategies (write-heavy vs read-heavy)
- Feed generation (pre-computed vs on-the-fly)
- Media storage & CDN distribution
- Notification delivery pipelines

---

## Week 6: Messaging & Real-Time Systems (July 15 – July 21)

### The Story Arc
> *"WhatsApp handles 100 billion messages a day with just 50 engineers.
> How? Because real-time messaging is a solved problem — if you understand the patterns.
> This week, you'll understand them so well that designing any real-time system becomes trivial."*

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design WhatsApp/Chat System** | "From IRC to end-to-end encrypted global messaging" |
| | | WebSocket management, message ordering, delivery receipts, group chat, E2E encryption |
| D3-D4 | **Design Slack/Discord** | "Chat, but with channels, threads, search, and presence" |
| | | Channel architecture, real-time presence, message search (Elasticsearch), workspace isolation |
| D5 | **Design a Live Comments/Reactions System** | "Millions watching the same event, all reacting at once" |
| | | Real-time fanout, approximate counting, eventual consistency for reactions |

### Patterns to Extract
- WebSocket connection management at scale
- Message ordering & delivery guarantees
- Presence systems (online/offline/typing)
- Real-time fanout to millions of connections

---

## Week 7: Storage & Search Systems (July 22 – July 28)

### The Story Arc
> *"Google Search returns results in 0.2 seconds from an index of the ENTIRE internet.
> Dropbox syncs your files across every device without losing a byte.
> These aren't magic — they're engineering. And they share surprisingly similar patterns."*

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design Google Drive/Dropbox** | "From a shared folder to planet-scale file sync" |
| | | File chunking, deduplication, sync conflicts, metadata vs blob storage |
| D3-D4 | **Design a Search Engine (Web Search / Elasticsearch)** | "How do you find one page in a trillion?" |
| | | Inverted index, crawling, ranking (PageRank intuition), query parsing, sharded search |
| D5 | **Design a Typeahead/Autocomplete** | "Predicting what you'll type before you type it" |
| | | Trie, prefix matching, ranking by popularity, personalization, edge caching |

### Patterns to Extract
- File chunking & content-addressable storage
- Inverted indexes for full-text search
- Ranking algorithms & relevance scoring
- Trie-based prefix matching

---

## Week 8: Video & Streaming Systems (July 29 – August 4)

### The Story Arc
> *"Netflix accounts for 15% of all internet bandwidth. YouTube serves a billion hours of video daily.
> Behind every 'Play' button is an orchestra of encoding, CDN routing, adaptive bitrate, and recommendation.
> This week, you become the conductor."*

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design YouTube** | "From upload to 'Play' — the journey of a video" |
| | | Upload pipeline, transcoding, adaptive bitrate, CDN, recommendation engine |
| D3-D4 | **Design Netflix** | "Streaming to 200M users simultaneously without buffering" |
| | | Content delivery architecture, Open Connect, personalization, A/B testing at scale |
| D5 | **Design Spotify / Audio Streaming** | "Music that follows you everywhere" |
| | | Audio encoding, offline sync, collaborative playlists, discovery algorithm |

### Patterns to Extract
- Media processing pipelines (transcoding, chunking)
- Adaptive bitrate streaming (HLS/DASH)
- CDN architecture for media delivery
- Recommendation systems (collaborative filtering, content-based)

---

## Week 9: E-Commerce & Transactional Systems (August 5 – August 11)

### The Story Arc
> *"On Prime Day, Amazon processes 100,000 orders per SECOND. Every order must be consistent —
> you can't sell the same item twice, charge the wrong amount, or lose a payment.
> This is where consistency meets scale, and it's one of the hardest problems in engineering."*

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design Amazon / E-Commerce Platform** | "From browsing to delivery — the commerce machine" |
| | | Product catalog, inventory management, cart service, order processing, payment handling |
| D3-D4 | **Design a Payment System (Stripe/PayPal)** | "Moving money without losing a cent" |
| | | Idempotency, exactly-once processing, ledger design, fraud detection, PCI compliance |
| D5 | **Design a Booking System (Airbnb/Hotels)** | "Two people can't book the same room" |
| | | Double-booking prevention, optimistic locking, search with geo-filtering |

### Patterns to Extract
- Inventory management with distributed locks
- Idempotent payment processing
- Saga pattern for multi-step transactions
- Geo-spatial search & indexing

---

## Week 10: Location & Ride-Sharing Systems (August 12 – August 18)

### The Story Arc
> *"You tap 'Request Ride' on Uber. In 3 seconds, a driver 2 minutes away accepts.
> Behind that tap: real-time location tracking of millions of drivers, a matching algorithm running
> in milliseconds, dynamic pricing computed from supply/demand, and an ETA model predicting traffic.
> Let's build it."*

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design Uber/Lyft** | "Matching riders to drivers in a moving world" |
| | | Geo-spatial indexing (geohash/quadtree), real-time location, matching, surge pricing, ETA |
| D3-D4 | **Design Google Maps** | "Routing billions of trips across the planet" |
| | | Graph storage, Dijkstra/A* at scale, live traffic, map tile rendering, offline maps |
| D5 | **🎯 PHASE 2 CHECKPOINT** | Full timed mock: design an unseen system | 
| | | Use all patterns from Weeks 5-10 | 

### Patterns to Extract
- Geo-spatial indexing (geohash, quadtree, R-tree)
- Real-time location tracking at scale
- Graph-based routing algorithms
- Dynamic pricing & supply-demand modeling

---

# 🔴 PHASE 3 — THE DEEP CUTS: Advanced Systems & Interview Mastery (Weeks 11-16)

> **Goal**: Handle ANY system design question — including ones you've never seen before.
> Master advanced patterns, handle ambiguity, and develop the storytelling instinct that
> makes interviewers say "This person thinks like a senior engineer."
>
> **The Analogy**: Phase 1 = ingredients. Phase 2 = classic recipes. Phase 3 = becoming a chef
> who can improvise any dish from any cuisine.

---

## Week 11: Infrastructure & Platform Systems (August 19 – August 25)

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design a Distributed Task Scheduler (Cron at scale)** | "Running a billion jobs without missing one" |
| | | Job distribution, failure recovery, exactly-once execution, priority queues |
| D3-D4 | **Design a Distributed Cache (Redis Cluster)** | "Every millisecond of latency = $ lost" |
| | | Consistent hashing, replication, eviction, cache warming, hot key handling |
| D5 | **Design a Metrics/Monitoring System (Datadog/Prometheus)** | "Watching the watchers" |
| | | Time-series data, roll-ups, alerting, dashboards, push vs pull collection |

---

## Week 12: Data Pipeline & Analytics Systems (August 26 – September 1)

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design a Web Crawler** | "How Google reads the entire internet" |
| | | Politeness, URL frontier, deduplication, distributed crawling, robots.txt |
| D3-D4 | **Design a Data Analytics Pipeline (like Kafka + Spark)** | "From raw events to business insights" |
| | | Event ingestion, stream processing, batch processing, Lambda/Kappa architecture |
| D5 | **Design a Distributed Logging System (ELK Stack)** | "Finding a needle in a haystack of logs" |
| | | Log collection, indexing, search, retention, sampling strategies |

---

## Week 13: Unique/Tricky Systems (September 2 – September 8)

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design a Ticket Booking System (Ticketmaster)** | "10,000 people want the same 100 seats" |
| | | Virtual waiting room, seat locking, inventory under extreme contention |
| D3-D4 | **Design a Collaborative Editor (Google Docs)** | "50 people editing the same paragraph" |
| | | OT vs CRDT, operational transforms, conflict resolution, cursor presence |
| D5 | **Design a URL Shortener at Billion Scale** | "Revisiting our first design — but now you're dangerous" |
| | | Compare your Week 1 design to what you'd build now |

---

## Week 14: Security, Auth & API Systems (September 9 – September 15)

| Day | System | The Story |
|-----|--------|-----------|
| D1-D2 | **Design an Authentication System (OAuth/SSO)** | "Who are you, and how do I know you're not lying?" |
| | | JWT, OAuth2 flows, session management, MFA, token refresh |
| D3-D4 | **Design an API Gateway** | "The front door to your entire platform" |
| | | Rate limiting, auth, routing, request transformation, circuit breaking |
| D5 | **Design a Content Moderation System** | "Keeping the internet safe at scale" |
| | | ML pipeline, human review queue, appeals process, real-time vs async moderation |

---

## Week 15: Mock Interview Marathon (September 16 – September 22)

| Day | Focus |
|-----|-------|
| D1 | **Mock 1**: Unseen system — 45 min timed, full interview simulation |
| D2 | **Mock 2**: Focus on weak areas identified in state file |
| D3 | **Mock 3**: "Curveball" system — something unusual (Design a multiplayer game server, Design a voting system) |
| D4 | **Mock 4**: Company-specific style (Google: focus on scale; Meta: focus on social; Amazon: focus on customer) |
| D5 | **Mock 5**: Speed round — design 2 systems in 60 minutes (high-level only) |

---

## Week 16: Final Polish & Interview Readiness (September 23 – September 29)

| Day | Focus |
|-----|-------|
| D1 | **Story Compilation**: Write the 2-minute story for every system you've designed |
| D2 | **Building Block Review**: Walk through every building block from memory |
| D3 | **Tradeoff Drill**: "Why did you choose X over Y?" for 20 key decisions |
| D4 | **Full Simulation**: 2 back-to-back system design interviews (45 min each) |
| D5 | **Light Review**: Read stories, rest, build confidence |

---

## 📊 Milestone Checkpoints

| Date | Milestone | Success Criteria |
|------|-----------|-----------------|
| Jun 16 (W1) | Networking & APIs solid | Can narrate DNS→HTTP→Server flow, design a URL shortener |
| Jun 23 (W2) | Data layer mastered | Can explain SQL vs NoSQL, sharding, replication as stories |
| Jun 30 (W3) | Caching & queues intuitive | Can explain when/why to add cache, design rate limiter |
| Jul 7 (W4) | **Phase 1 complete** | All building blocks as stories, back-of-envelope fluent |
| Jul 28 (W7) | Core systems designed | Can design Twitter, WhatsApp, Dropbox from scratch |
| Aug 18 (W10) | **Phase 2 complete** | 12+ systems designed, can handle any classic question |
| Sep 8 (W13) | Advanced systems done | Can handle curveballs (Google Docs, Ticketmaster) |
| **Sep 29 (W16)** | **🎯 INTERVIEW READY** | **Design any system with stories, depth, and confidence** |

---

## 📚 The 8 Pillars of System Design (Your Mental Framework)

> Every system design answer touches some combination of these pillars.
> Master these, and you can design ANYTHING.

| # | Pillar | The One-Line Story |
|---|--------|--------------------|
| 1 | **Networking & Communication** | "How do things talk to each other?" |
| 2 | **Data Storage & Modeling** | "Where does stuff live, and how do you find it?" |
| 3 | **Caching & Performance** | "How do you make it fast?" |
| 4 | **Message Queues & Async** | "How do you handle work that can wait?" |
| 5 | **Consistency & Reliability** | "How do you keep things correct when everything's on fire?" |
| 6 | **Scalability & Partitioning** | "How do you serve a billion users?" |
| 7 | **Security & Access Control** | "How do you keep the bad guys out?" |
| 8 | **Monitoring & Observability** | "How do you know it's working?" |

---

## 🔄 Spaced Repetition for System Design

> Unlike DSA (which tests recall of algorithms), system design tests your ability to TELL A STORY.
> So spaced repetition here is about re-narrating the story, not re-solving a problem.

| Box | Review After | What to Do |
|-----|-------------|-----------|
| **Box 1** (New) | 2 days | Re-tell the 2-minute story of the system |
| **Box 2** (Learning) | 5 days | Re-design from scratch (high-level only, 10 min) |
| **Box 3** (Reviewing) | 2 weeks | Full design under time pressure (30 min) |
| **Box 4** (Familiar) | 1 month | Quick story + "what would you change?" |
| **Box 5** (Mastered) | Before interviews | Skim story, check for new insights |

**Rule**: If you can't narrate the story or forget key tradeoffs → back to Box 1.

---

## 🎯 The Interview Day Checklist

> Before you walk into any system design interview, you should be able to:

- [ ] Estimate QPS, storage, and bandwidth in your head (2 min)
- [ ] Start with requirements that impress the interviewer (3 min)
- [ ] Draw a clean high-level architecture on a whiteboard (5 min)
- [ ] Dive deep into any component with specific details (15 min)
- [ ] Articulate tradeoffs with "We could do X, but Y is better because..." language
- [ ] Tell the STORY of the system — beginning, middle, end
- [ ] Handle curveballs: "What if we need to support 100x more users tomorrow?"
- [ ] Name specific technologies and justify WHY (not just "use Redis")
