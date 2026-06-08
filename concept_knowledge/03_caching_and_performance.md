# 📖 Caching & Performance — Concept Knowledge

> Caching is the most impactful optimization in system design. 
> "The fastest request is the one you never make."

---

## The Big Story

> _"Your brain doesn't go to the library every time you need to recall a fact.
> It keeps frequently used information in short-term memory. That's exactly what caching is —
> keeping hot data close to where it's needed."_

_To be filled during Week 3 sessions_

---

## Key Insights (Aha! Moments)

_Will be populated as we discuss each concept_

---

## Caching Strategies Comparison

| Strategy | How It Works | Best For | Tradeoff |
|----------|-------------|----------|----------|
| **Cache-Aside** | App checks cache → miss → read DB → fill cache | General purpose | Cache can be stale |
| **Write-Through** | Write to cache AND DB at same time | Strong consistency | Write latency increases |
| **Write-Back** | Write to cache now, DB later (async) | Write-heavy | Risk of data loss |
| **Read-Through** | Cache auto-fetches from DB on miss | Simplicity | Tighter coupling |

---

## The "Where to Cache" Hierarchy

```
Client/Browser Cache (fastest, smallest)
    ↓
CDN Cache (edge locations, static content)
    ↓
Application Cache (Redis/Memcached)
    ↓
Database Cache (query cache, buffer pool)
    ↓
Disk (slowest, largest)
```

---

## Cache Invalidation — "The Hardest Problem"

_To be filled with personal understanding and aha moments_

---

## Interview Tips

1. Always mention caching when discussing read-heavy systems
2. Know the eviction policies: LRU, LFU, TTL — and when to use each
3. Be ready to discuss cache stampede and thundering herd
4. "What happens when your cache goes down?" is a common follow-up

---

## Related Building Blocks
- Redis → Key-Value Store, Distributed Cache
- CDN → Media systems (YouTube, Netflix)
- TTL → Rate Limiter, Session management
