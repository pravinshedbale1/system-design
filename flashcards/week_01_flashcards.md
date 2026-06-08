# 📝 Week 1 Flashcards — Networking & Communication

> Revisit these before each session. Each card is a story you should be able to tell.

---

## Card 1: DNS Resolution
```
🔍 TRIGGER: "How does a URL become a web page?"
💡 STORY:   "DNS is the internet's phone book. You type google.com, 
            DNS converts it to 142.250.80.46. Without DNS, you'd need 
            to memorize IP addresses like phone numbers before speed dial."
🧠 DETAIL:  Browser cache → OS cache → ISP resolver → root → TLD → authoritative
⏱️ SPEED:   Cached: <1ms | Full resolution: 20-120ms
⚠️ INTERVIEW: "What if the DNS server goes down?" → Caching + multiple resolvers
```

---

## Card 2: TCP vs UDP
```
🔍 TRIGGER: "Why TCP for web, UDP for video calls?"
💡 STORY:   "TCP is certified mail — slow but guaranteed. Three-way handshake, 
            acknowledgments, retransmission. UDP is shouting across a room — 
            fast but some words get lost. You don't resend a video frame from 
            2 seconds ago — it's already irrelevant."
🧠 KEY:     TCP = reliability. UDP = speed. Choose based on what matters more.
⚠️ EDGE:    HTTP/3 (QUIC) uses UDP with reliability built on top — best of both.
```

---

## Card 3: REST API Design
```
🔍 TRIGGER: "Design the API for [any system]"
💡 STORY:   "REST is a waiter with a menu. You say 'GET /users/123' and they 
            bring you user 123. You say 'POST /users' with a body, and they 
            create a new user. The menu (API) is the contract."
🧠 VERBS:   GET (read), POST (create), PUT (replace), PATCH (update), DELETE
📝 RULES:   Nouns for resources (/users), not verbs (/getUser)
             Plural (/users/123 not /user/123)
             Versioning: /v1/users
⚠️ EDGE:    Pagination, filtering, rate limiting headers
```

---

## Card 4: WebSocket vs HTTP
```
🔍 TRIGGER: "How do you build real-time features?"
💡 STORY:   "HTTP is texting — you send a message, wait for a reply. 
            WebSocket is a phone call — once connected, both sides can 
            talk freely at any time. Use HTTP for 'ask and answer.' 
            Use WebSocket for 'we need to keep talking.'"
🧠 WHEN:    Chat, live scores, collaborative editing, gaming
⚠️ COST:    Each WebSocket = persistent connection = server memory. 
            1M users × 1 WebSocket = 1M open connections.
```

---

## Card 5: Load Balancer
```
🔍 TRIGGER: "How do you handle millions of requests?"
💡 STORY:   "A load balancer is the hostess at a restaurant. When you 
            walk in, she doesn't send everyone to the same waiter — 
            she distributes customers across all available waiters."
🧠 ALGORITHMS:
   Round Robin — take turns (simple, fair)
   Least Connections — send to the least busy waiter
   IP Hash — same customer, same waiter (session affinity)
   Weighted — better waiters get more customers
📝 L4 vs L7: 
   L4 (TCP level) — fast, simple, can't see HTTP content
   L7 (HTTP level) — smart, can route by URL/header, slower
```

---

## Card 6: CDN
```
🔍 TRIGGER: "How does Netflix serve video to billions?"
💡 STORY:   "Netflix doesn't serve videos from one building. They have 
            'branch offices' (PoPs) in every major city. When you press 
            Play, you're streaming from the nearest branch — not HQ."
🧠 KEY:     Cache static content at edge locations close to users
📝 WHEN:    Images, CSS, JS, videos, any static content
⚠️ INTERVIEW: "What about cache invalidation?" → TTL + purge API
```

---

## 🧠 Week 1 Summary Mantra
```
╔════════════════════════════════════════════════════════════╗
║  How do things FIND each other?     → DNS                  ║
║  How do they TALK?                  → HTTP/REST             ║
║  How do they TALK in real-time?     → WebSocket             ║
║  How do you DISTRIBUTE the load?    → Load Balancer         ║
║  How do you serve things FAST?      → CDN                   ║
║                                                            ║
║  🎯 INTERVIEW SUPERPOWER: Trace a request end-to-end!     ║
║  Client → DNS → CDN/LB → Server → DB → Response           ║
╚════════════════════════════════════════════════════════════╝
```

---

_Cards for Week 2+ will be created as we progress._
