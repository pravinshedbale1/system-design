# 🧩 Tradeoff Library — "Why X Over Y?"

> In system design interviews, the TRADEOFF ARTICULATION is what separates a hire from a strong hire.
> Every decision you make has a cost. This library documents every tradeoff we encounter,
> organized by category, with the storytelling language to use in interviews.

---

## How to Articulate a Tradeoff

> **The Formula**: "We could do [Option A], which gives us [benefit], but at the cost of [downside].
> Alternatively, [Option B] gives us [different benefit] but sacrifices [different thing].
> Given our requirements for [key requirement], I'd go with [choice] because [reason]."

---

## 🗄️ Data Storage Tradeoffs

### SQL vs NoSQL
```
SQL:    ✅ ACID, relationships, complex queries, mature tooling
        ❌ Harder to scale horizontally, rigid schema
NoSQL:  ✅ Flexible schema, horizontal scaling, high write throughput
        ❌ No JOINs (usually), eventual consistency, query limitations

TELL IN INTERVIEW:
"For a system with clear entity relationships and transactional requirements — 
like a payment system — I'd choose PostgreSQL. But for something like a chat 
system with high write volume and flexible message formats, MongoDB or 
Cassandra makes more sense."
```

### Replication: Sync vs Async
```
Sync:   ✅ Strong consistency, no stale reads
        ❌ Higher latency, reduced availability during failures
Async:  ✅ Lower latency, higher availability
        ❌ Stale reads possible, data loss risk on failure

TELL IN INTERVIEW:
"For a banking system, I'd use synchronous replication — a customer can't 
see different balances on different devices. For a social media feed, 
async is fine — it's okay if a like takes a second to propagate."
```

### Normalization vs Denormalization
```
Normalized:    ✅ No data duplication, easier updates, data integrity
               ❌ More JOINs, slower reads at scale
Denormalized:  ✅ Faster reads, fewer JOINs, simpler queries
               ❌ Data duplication, harder updates, potential inconsistency

TELL IN INTERVIEW:
"I'd start normalized for data integrity, then denormalize specific 
read-heavy paths as we identify bottlenecks. Premature denormalization 
is a common trap."
```

---

## ⚡ Performance Tradeoffs

### Cache Consistency vs Speed
```
Strong cache consistency: ✅ Always fresh data | ❌ Slower, more complex
Eventual cache consistency: ✅ Faster, simpler | ❌ Stale data possible

TELL IN INTERVIEW:
"For product prices on an e-commerce site, I'd use cache-aside with a short 
TTL (30s) — slightly stale prices are okay. For inventory counts? 
Write-through to ensure the cache and DB always agree."
```

### Fan-out on Write vs Fan-out on Read
```
On Write: ✅ Fast reads (pre-computed) | ❌ Slow writes, storage heavy, celebrity problem
On Read:  ✅ Fast writes, less storage  | ❌ Slow reads (compute at read time)

TELL IN INTERVIEW:
"For most users, fan-out on write is great — pre-compute the feed when 
someone posts. But for celebrities with 50M followers, fan-out on read 
makes more sense — you don't want to write to 50M feeds on every tweet. 
That's the hybrid approach Twitter uses."
```

---

## 🔗 Communication Tradeoffs

### REST vs gRPC vs GraphQL
```
REST:    ✅ Simple, widely supported, HTTP caching | ❌ Over/under-fetching
gRPC:    ✅ Fast (binary), streaming, type-safe     | ❌ Not browser-friendly
GraphQL: ✅ Exact data needed, one endpoint        | ❌ Complex, caching harder

TELL IN INTERVIEW:
"REST for public APIs — it's the lingua franca. gRPC for internal 
service-to-service calls where latency matters. GraphQL for mobile 
apps that need to minimize data transfer."
```

### Sync vs Async Processing
```
Sync:  ✅ Simple, immediate response | ❌ Blocks the caller, slower
Async: ✅ Fast response, decoupled    | ❌ Complex, eventual consistency

TELL IN INTERVIEW:
"I'd process the payment synchronously — the user needs to know immediately 
if it succeeded. But sending the confirmation email? That goes to a queue. 
The user doesn't need to wait for an email to be sent."
```

---

## 📈 Scalability Tradeoffs

### Vertical vs Horizontal Scaling
```
Vertical: ✅ Simple, no code changes | ❌ Has limits, single point of failure
Horizontal: ✅ Theoretically infinite, redundancy | ❌ Complex, state management

TELL IN INTERVIEW:
"I'd start vertical for the database — scale up to the biggest machine 
available. For application servers, horizontal from day one — they're 
stateless, so adding more is straightforward."
```

---

## 🔒 Consistency Tradeoffs

### Strong vs Eventual Consistency
```
Strong:   ✅ Always correct, simple mental model | ❌ Slower, less available
Eventual: ✅ Fast, highly available, partition-tolerant | ❌ Stale data window

TELL IN INTERVIEW:
"The real question is: what's the COST of inconsistency? If a user sees 
a stale follower count for 2 seconds, nobody notices. If their bank 
balance is wrong for 2 seconds, that's a lawsuit."
```

---

_This library grows with every design session. Every tradeoff we discuss gets documented here._
