# 📖 Data Storage & Modeling — Concept Knowledge

> This file captures your understanding of databases, storage, indexing, replication, and sharding.
> Every concept is learned through stories and real system examples.

---

## The Big Story

> _"Every system is just 'take data in, store it, give it back.' 
> The question that changes everything is: HOW MUCH data, HOW FAST, and HOW CORRECT?"_

_To be filled during Week 2 sessions_

---

## Key Insights (Aha! Moments)

_Will be populated as we discuss each concept_

<!--
Expected insights:
- "SQL is for when relationships matter. NoSQL is for when speed and flexibility matter."
- "Sharding is inevitable — the question is WHEN and on WHAT key"
- "Replication gives you availability AND read performance — but at the cost of consistency"
- "CAP theorem isn't about choosing 2 of 3 — it's about what to sacrifice DURING a partition"
- "Indexes are a space-time tradeoff — faster reads, slower writes"
-->

---

## SQL vs NoSQL Decision Framework

| Choose SQL When... | Choose NoSQL When... |
|-------------------|---------------------|
| Data has clear relationships | Schema is flexible or evolving |
| Need ACID transactions | Need horizontal scaling |
| Complex queries with JOINs | Simple key→value or document lookups |
| Data integrity is critical | High write throughput needed |
| Schema is stable | Geographic distribution needed |

---

## The Database Scaling Story (Progressive)

```
Stage 1: Single Server
└─ "Everything on one machine. Simple. Works up to ~10K users."

Stage 2: Read Replicas  
└─ "One writer, many readers. Like having one author but many copies of the book."
└─ Works up to ~100K users.

Stage 3: Caching Layer
└─ "Don't even go to the library — check your bookshelf first."
└─ Reduces DB load by 80-90%.

Stage 4: Vertical Scaling
└─ "Get a bigger machine. Buys time, but has limits."

Stage 5: Sharding
└─ "Split the library into branches. Each branch holds different books."
└─ Horizontal scaling — theoretically infinite.
└─ But JOINs across shards are painful.

Stage 6: Multi-Region
└─ "Open libraries in every country."
└─ Latency drops, but consistency gets harder.
```

---

## Common Mistakes

_Will be populated as we identify mistakes_

---

## Interview Tips

1. Always start with a simple schema, then evolve it
2. Mention your sharding key and explain WHY you chose it
3. Discuss read:write ratio — it determines your replication strategy
4. Know when to denormalize (hint: when JOINs become bottleneck)

---

## Related Building Blocks
- Replication → Consistency models
- Sharding → Consistent hashing
- Indexing → Search systems (inverted index)
- Object Storage → Media/file systems (YouTube, Dropbox)
