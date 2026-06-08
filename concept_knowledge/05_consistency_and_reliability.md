# 📖 Consistency & Reliability — Concept Knowledge

> "Systems don't fail — they partially fail. The question is: what do you do about it?"

---

## The Big Story

> _"Imagine 5 copies of a bank ledger, held by 5 different clerks in 5 different cities.
> A customer deposits money with Clerk A. When does Clerk E know about it? Immediately?
> Eventually? Only when asked? THAT is the consistency problem."_

_To be filled during Week 4 sessions_

---

## Key Insights (Aha! Moments)

_Will be populated as we discuss each concept_

---

## Consistency Models Spectrum

```
STRONGEST ←————————————————————————————→ WEAKEST (but fastest)

Linearizable → Sequential → Causal → Read-your-writes → Eventual
     ↓              ↓          ↓            ↓                ↓
"Everyone sees   "Same     "Cause     "You see your     "Everyone
 the same thing   order,    before     own writes"      agrees...
 at the same      maybe     effect"                     eventually"
 time"            delayed"
```

---

## CAP Theorem — The Real Story

_To be filled with personal understanding_

---

## Fault Tolerance Patterns

| Pattern | Analogy | When to Use |
|---------|---------|-------------|
| **Redundancy** | "Spare tire in the trunk" | Always |
| **Failover** | "Backup pilot" | Leader-follower systems |
| **Circuit Breaker** | "Tripping a fuse before the house burns" | Calling external services |
| **Retry + Backoff** | "Try knocking again, but wait longer each time" | Transient failures |
| **Bulkhead** | "Watertight compartments in a ship" | Isolating service failures |

---

## Interview Tips

1. When discussing consistency, always frame it as a TRADEOFF, not a binary choice
2. Know the practical difference: CP system (banking) vs AP system (social media likes)
3. Saga pattern is the go-to for distributed transactions — know when to use it vs 2PC
4. "How does your system handle a network partition?" — always have an answer

---

## Related Building Blocks
- CAP Theorem → Every distributed system design
- Saga Pattern → E-commerce, payment systems
- Consensus → Leader election, distributed locks
