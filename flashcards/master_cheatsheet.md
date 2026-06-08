# 📝 Master Cheatsheet — System Design Interview

> **The 5-Minute Warmup**: Read this before any system design interview.
> Every building block, every pattern, every tradeoff — in one page.

---

## 🎯 The Interview Framework (RRADS)

```
╔══════════════════════════════════════════════════════════════╗
║  R — Requirements (5 min)                                    ║
║      Functional: "What should the system DO?"                ║
║      Non-functional: "How well? (scale, latency, consistency)"║
║      Estimation: users, QPS, storage, bandwidth              ║
║                                                              ║
║  R — Rough Design (10 min)                                   ║
║      API endpoints + data model + high-level architecture    ║
║      Trace ONE request end-to-end                            ║
║                                                              ║
║  A — Architecture Deep Dive (20 min)                         ║
║      Pick 1-2 interesting components and go DEEP             ║
║      Specific algorithms, data structures, protocols         ║
║                                                              ║
║  D — Design for Scale (5 min)                                ║
║      "Where does this break at 10x?"                         ║
║      Bottlenecks, caching, sharding, async processing        ║
║                                                              ║
║  S — Summary & Tradeoffs (5 min)                             ║
║      "We chose X over Y because..."                          ║
║      Future improvements, monitoring, what we'd do with time ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📊 Back-of-Envelope Numbers You MUST Know

### Latency
```
L1 cache reference ............. 0.5 ns
L2 cache reference ............. 7 ns
RAM reference .................. 100 ns
SSD random read ................ 150 μs
HDD random read ................ 10 ms
Network round trip (same DC) ... 0.5 ms
Network round trip (cross-continent) ... 150 ms
```

### Throughput
```
Read 1 MB from RAM ............. 250 μs
Read 1 MB from SSD ............. 1 ms
Read 1 MB from HDD ............. 20 ms
Transfer 1 MB over 1 Gbps ...... 10 ms
```

### Scale
```
1 million requests/day ......... ~12 QPS
1 billion requests/day ......... ~12,000 QPS
1 byte ......................... 8 bits
1 KB ........................... 1,000 bytes
1 MB ........................... 1,000 KB
1 GB ........................... 1,000 MB
1 TB ........................... 1,000 GB
1 PB ........................... 1,000 TB

100M users, each 1 KB .......... 100 GB
100M users, each 1 MB .......... 100 TB
```

### Quick Estimation Template
```
Daily Active Users (DAU): _____
Actions per user per day: _____
→ Total daily actions: DAU × actions
→ QPS: daily actions / 86,400
→ Peak QPS: QPS × 2-3

Storage per action: _____ bytes
→ Daily storage: total actions × storage per action
→ Yearly storage: daily × 365

Read:Write ratio: _____:1
→ Read QPS: total QPS × (read / total)
→ Write QPS: total QPS × (write / total)
```

---

## 🗄️ Database Selection Quick Guide

```
Need ACID transactions?          → PostgreSQL / MySQL
Need flexible schema?            → MongoDB / DynamoDB
Need blazing fast lookups?       → Redis / Memcached
Need time-series data?           → Cassandra / InfluxDB
Need full-text search?           → Elasticsearch
Need to store files/media?       → S3 / GCS / Azure Blob
Need graph relationships?        → Neo4j
Need a message queue?            → Kafka (streaming) / SQS (tasks)
```

---

## 🔑 Key Tradeoffs to Articulate

| Decision | Option A | Option B | Choose A When... | Choose B When... |
|----------|----------|----------|-----------------|-----------------|
| Consistency | Strong | Eventual | Banking, inventory | Social feed, likes |
| Communication | Sync (REST) | Async (Queue) | Need immediate response | Can process later |
| Scaling | Vertical | Horizontal | Quick fix, DB primary | Long-term, stateless |
| Data storage | SQL | NoSQL | Relationships, ACID | Flexibility, scale |
| Caching | Cache-aside | Write-through | General purpose | Must be consistent |
| Fan-out | On write | On read | Most users have few followers | Celebrity users exist |

---

## 🧠 The "What Happens When..." Responses

```
"What if the server crashes?"
→ Redundancy + failover + health checks

"What if the database is slow?"
→ Cache + read replicas + query optimization + indexing

"What if traffic spikes 10x?"
→ Auto-scaling + load balancer + rate limiter + queue

"What if data is inconsistent?"
→ Choose consistency model based on requirements

"What if the network partitions?"
→ CAP theorem — decide CP or AP based on use case

"What if a payment processes twice?"
→ Idempotency keys + exactly-once semantics
```

---

_This cheatsheet grows as we learn. Glance at it before every mock interview._
