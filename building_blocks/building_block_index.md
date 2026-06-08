# 🧩 BUILDING BLOCK INDEX — "The 8 Pillars + Components"

> This is your **system design cheat sheet**. Before every design, scan this.
> Every building block is a STORY you can tell.
> As we cover new concepts, this grows. By Week 16, this is your ultimate weapon.

---

## 🔗 Pillar 1: Networking & Communication

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 1 | **DNS** | "The internet's phone book — name to IP" | Every system (it's always there) |
| 2 | **HTTP/HTTPS** | "The language browsers and servers speak" | Web APIs, REST services |
| 3 | **TCP vs UDP** | "Reliable mail vs fast shouting" | TCP for data integrity, UDP for streaming |
| 4 | **REST APIs** | "A waiter with a menu — ordered, predictable" | 90% of service communication |
| 5 | **GraphQL** | "Order exactly what you want — no more, no less" | Mobile apps, complex nested data |
| 6 | **gRPC** | "High-speed internal phone line between services" | Service-to-service, low latency |
| 7 | **WebSockets** | "An open phone call — both sides can talk anytime" | Chat, live updates, gaming |
| 8 | **Long Polling** | "Checking your mailbox every 30 seconds" | When WebSocket is overkill |
| 9 | **Server-Sent Events** | "A radio broadcast — server talks, clients listen" | Live feeds, notifications |

---

## 🗄️ Pillar 2: Data Storage & Modeling

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 10 | **Relational DB (SQL)** | "A perfectly organized spreadsheet with rules" | Structured data, relationships, transactions |
| 11 | **Document DB (MongoDB)** | "A filing cabinet of flexible folders" | Varied schemas, rapid iteration |
| 12 | **Key-Value Store (Redis)** | "A dictionary — look up anything by its name instantly" | Caching, sessions, counters |
| 13 | **Wide-Column (Cassandra)** | "A spreadsheet where each row can have different columns" | Time-series, IoT, write-heavy |
| 14 | **Graph DB (Neo4j)** | "A web of relationships — who knows whom" | Social networks, recommendations |
| 15 | **Object Storage (S3)** | "A warehouse for files — infinite, cheap, durable" | Images, videos, backups |
| 16 | **B-Tree Index** | "A library card catalog — find any book fast" | Range queries, ordered data |
| 17 | **Hash Index** | "A dictionary index — exact word, instant lookup" | Exact match queries |
| 18 | **Inverted Index** | "Google's trick — find docs by the words they contain" | Full-text search |

---

## ⚡ Pillar 3: Caching & Performance

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 19 | **Cache-Aside** | "Check the shelf first, go to warehouse if missing" | Most common caching pattern |
| 20 | **Write-Through** | "Update the shelf AND warehouse at the same time" | When reads must be fresh |
| 21 | **Write-Back** | "Update the shelf now, warehouse later" | Write-heavy, tolerance for staleness |
| 22 | **CDN** | "Local warehouses in every city" | Static content, media, global users |
| 23 | **LRU Eviction** | "Remove the thing you haven't used the longest" | General-purpose cache eviction |
| 24 | **TTL** | "This milk expires in 24 hours" | Simple time-based invalidation |

---

## 📬 Pillar 4: Message Queues & Async Processing

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 25 | **Message Queue (SQS)** | "A post office — guaranteed delivery, one at a time" | Task processing, decoupling |
| 26 | **Pub/Sub (Kafka)** | "A newspaper — publish once, everyone subscribed gets it" | Event streaming, analytics |
| 27 | **Event Sourcing** | "Recording every chess move, not just the final board" | Audit trails, financial systems |
| 28 | **CQRS** | "Separate the reading desk from the writing desk" | Different read/write patterns |
| 29 | **Dead Letter Queue** | "The undeliverable mail pile" | Handling failed message processing |

---

## 🔒 Pillar 5: Consistency & Reliability

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 30 | **Strong Consistency** | "Everyone sees the same thing at the same time" | Banking, inventory |
| 31 | **Eventual Consistency** | "Everyone will agree... eventually" | Social feeds, likes, comments |
| 32 | **Leader-Follower Replication** | "One boss writes, everyone else copies" | Read-heavy workloads |
| 33 | **Quorum** | "Majority rules — 3 out of 5 agree" | Distributed consensus |
| 34 | **Circuit Breaker** | "Stop calling a dead service — give it time to recover" | Microservice resilience |
| 35 | **Retry with Backoff** | "Try again, but wait longer each time" | Transient failures |
| 36 | **Idempotency** | "Doing the same thing twice has the same effect as once" | Payment processing, APIs |

---

## 📈 Pillar 6: Scalability & Partitioning

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 37 | **Horizontal Scaling** | "Add more waiters, not a faster waiter" | Stateless services |
| 38 | **Vertical Scaling** | "Get a bigger server" | Quick fix, DB primary |
| 39 | **Consistent Hashing** | "A circular table — add/remove seats without reshuffling everyone" | Distributed caching, sharding |
| 40 | **Hash Sharding** | "Assign data to servers by hash of key" | Even distribution |
| 41 | **Range Sharding** | "A-M goes to server 1, N-Z goes to server 2" | Range queries needed |
| 42 | **Load Balancer** | "The hostess at a restaurant" | Distributing traffic |
| 43 | **Rate Limiter** | "The bouncer at the door" | Protecting services from abuse |

---

## 🛡️ Pillar 7: Security & Access Control

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 44 | **JWT** | "A stamped wristband — carry your identity with you" | Stateless authentication |
| 45 | **OAuth 2.0** | "Let Google vouch for you at my door" | Third-party login |
| 46 | **API Keys** | "Your building access card" | Service-to-service auth |
| 47 | **TLS/SSL** | "Sealed envelope vs postcard" | All production traffic |
| 48 | **Encryption at Rest** | "Locked filing cabinet" | Sensitive data storage |

---

## 👁️ Pillar 8: Monitoring & Observability

| # | Building Block | The One-Line Story | When to Use |
|---|---------------|-------------------|-------------|
| 49 | **Metrics** | "The dashboard gauges in your car" | Performance tracking |
| 50 | **Logs** | "The flight recorder / black box" | Debugging, auditing |
| 51 | **Traces** | "Following one request through the maze" | Distributed debugging |
| 52 | **Health Checks** | "Taking the patient's pulse" | Service availability |
| 53 | **Alerting** | "The smoke detector" | Incident response |

---

## 🧠 The Decision Framework

```
What kind of data?
├── Structured + relationships → SQL (Postgres, MySQL)
├── Flexible documents → MongoDB, DynamoDB  
├── Simple key→value → Redis, Memcached
├── Time-series → Cassandra, InfluxDB
├── Graph (relationships ARE the data) → Neo4j
├── Files/media → S3, GCS
└── Full-text search → Elasticsearch

How do services communicate?
├── Client → Server (web/mobile) → REST or GraphQL
├── Server → Server (internal) → gRPC or REST
├── Need real-time? → WebSocket or SSE
├── Need async? → Message Queue (Kafka/SQS)
└── Need broadcast? → Pub/Sub

How to handle scale?
├── More requests → Load Balancer + horizontal scaling
├── More data → Shard the database  
├── More reads → Add read replicas + cache
├── More writes → Message queue + async processing
└── Global users → CDN + multi-region deployment

How to stay reliable?
├── Service might fail → Circuit breaker + retry
├── Data might be lost → Replication + backups
├── Payment might double-charge → Idempotency
├── Too many requests → Rate limiter
└── Need to debug → Metrics + logs + traces
```

---

_This index grows as we learn. Every new building block gets added here during our sessions._
