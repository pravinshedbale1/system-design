# 📐 System Design Templates

> These are reusable frameworks and templates for common system design patterns.
> Use them as starting points, not as copy-paste solutions.

---

## Template 1: Back-of-Envelope Estimation

```
System: _____________________
Timeframe: ___________________

USERS & TRAFFIC
├── Total users: ___
├── Daily Active Users (DAU): ___
├── Actions per user/day: ___
├── Total requests/day: DAU × actions = ___
├── QPS: total / 86,400 = ___
├── Peak QPS: QPS × 3 = ___
└── Read:Write ratio: ___:1

STORAGE
├── Data per action: ___ bytes
├── Daily new data: total actions × bytes = ___
├── Monthly: daily × 30 = ___
├── Yearly: daily × 365 = ___
├── 5-year projection: yearly × 5 = ___
└── With replication (3x): 5-year × 3 = ___

BANDWIDTH
├── Incoming (write): write QPS × data size = ___
├── Outgoing (read): read QPS × data size = ___
└── Total: incoming + outgoing = ___

MEMORY (for caching)
├── Cache 20% of daily data
├── Daily data = ___
└── Cache size: daily × 0.2 = ___
```

---

## Template 2: API Design Framework

```
# Resource: [Entity Name]

## Create
POST /api/v1/{resources}
Request Body: { ... }
Response: 201 Created + { id, ...created entity }

## Read (single)
GET /api/v1/{resources}/{id}
Response: 200 OK + { ...entity }

## Read (list)
GET /api/v1/{resources}?page=1&limit=20&sort=created_at&filter=...
Response: 200 OK + { data: [...], pagination: { page, limit, total } }

## Update
PUT /api/v1/{resources}/{id}
Request Body: { ...full entity }
Response: 200 OK + { ...updated entity }

## Partial Update
PATCH /api/v1/{resources}/{id}
Request Body: { ...fields to update }
Response: 200 OK + { ...updated entity }

## Delete
DELETE /api/v1/{resources}/{id}
Response: 204 No Content
```

---

## Template 3: Data Model Design

```
1. Identify entities (nouns in the requirements)
2. Identify relationships (verbs between entities)
3. Choose storage per entity:
   - Structured + relationships → SQL
   - Flexible documents → NoSQL
   - Key-value lookups → Redis/DynamoDB
   - Binary files → Object Storage (S3)
4. Define schema for each entity
5. Identify hot paths (most queried)
6. Add indexes for hot paths
7. Plan for sharding key if data > 1 TB
```

---

## Template 4: System Design Interview Structure (45 min)

```
[0:00 - 5:00]  REQUIREMENTS
├── Ask 3-5 clarifying questions
├── List functional requirements (3-5 core features)
├── List non-functional requirements (scale, latency, consistency)
└── Quick estimation (DAU, QPS, storage)

[5:00 - 10:00]  API DESIGN
├── Define core API endpoints
├── Request/response shapes
└── Authentication approach

[10:00 - 15:00]  DATA MODEL
├── Entity relationship
├── Choose database type(s)
├── Schema design
└── Sharding strategy (if applicable)

[15:00 - 25:00]  HIGH-LEVEL ARCHITECTURE
├── Draw core components
├── Trace ONE request end-to-end
├── Explain data flow
└── Identify key services

[25:00 - 40:00]  DEEP DIVE
├── Interviewer picks 1-2 areas
├── Specific algorithms / data structures
├── Handle edge cases and failures
└── Scale analysis

[40:00 - 45:00]  WRAP UP
├── Summarize key tradeoffs
├── What would you improve with more time?
├── Monitoring & alerting strategy
└── Answer remaining questions
```

---

## Template 5: Tradeoff Articulation

```
"We have two options here:

Option A: [description]
  ✅ Advantage: ...
  ❌ Disadvantage: ...

Option B: [description]  
  ✅ Advantage: ...
  ❌ Disadvantage: ...

I'd go with [Option X] because [reason tied to our requirements].
However, if [condition changes], we'd switch to [Option Y]."
```

---

_Templates will be refined and expanded as we progress._
