# 📖 Message Queues & Async Processing — Concept Knowledge

> "If you can do it later, don't do it now."

---

## The Big Story

> _"Imagine a restaurant where the chef has to personally walk every dish to the table.
> When it's slow, fine. When it's packed? Disaster. The solution? Waiters — they 
> decouple the cooking from the serving. Message queues are those waiters."_

_To be filled during Week 3 sessions_

---

## Key Insights (Aha! Moments)

_Will be populated as we discuss each concept_

---

## Message Queue vs Pub/Sub

| Feature | Message Queue (SQS) | Pub/Sub (Kafka) |
|---------|---------------------|-----------------|
| **Analogy** | Post office — one recipient | Newspaper — all subscribers |
| **Message fate** | Consumed once, deleted | Retained, replayable |
| **Consumers** | One consumer per message | Many consumers per message |
| **Use case** | Task processing, work distribution | Event streaming, analytics |
| **Ordering** | Per-queue (FIFO) | Per-partition |

---

## When to Use Async Processing

_To be filled with personal understanding_

---

## Interview Tips

1. Mention message queues whenever a design has components that don't need to respond in real-time
2. Kafka is the go-to for event streaming; SQS/RabbitMQ for task queues
3. Always mention idempotency when discussing queue consumers
4. Dead letter queues are important for production systems

---

## Related Building Blocks
- Event-Driven Architecture → Microservices decoupling
- Kafka → Analytics pipelines, feed generation
- CQRS → Separating read and write models
