# 📖 Networking & Communication — Concept Knowledge

> This file is populated through our conversations. Each section captures what YOU understood, 
> not textbook definitions. Every concept is a story.

---

## The Big Story

> _"Imagine you want to send a letter to a friend in another city. You need three things:
> their address (DNS), a language you both speak (HTTP), and a postal system that guarantees 
> delivery (TCP). That's the internet."_

_To be filled during Session #1_

---

## Key Insights (Aha! Moments)

_Will be populated as we discuss each concept_

<!-- 
Expected insights:
- "DNS is just a phone book — I type a name, it gives me a number"
- "TCP is like certified mail — slow but guaranteed. UDP is like shouting across the room"
- "HTTP is stateless — the waiter doesn't remember you between visits"
- "A load balancer is the hostess — she decides which waiter serves you"
- "WebSocket is a phone call. HTTP is texting."
-->

---

## When to Use What

| Protocol/Tech | Use When... | Don't Use When... |
|--------------|------------|-------------------|
| HTTP/REST | Standard request-response, CRUD APIs | Need real-time bidirectional |
| WebSocket | Real-time, bidirectional (chat, gaming) | Simple request-response |
| Long Polling | Need "real-time-ish" but can't use WebSocket | True real-time needed |
| SSE | Server→Client streaming (live feeds) | Client needs to send data too |
| gRPC | Internal service-to-service, performance-critical | Browser clients (limited support) |
| GraphQL | Complex nested data, mobile apps (save bandwidth) | Simple CRUD, internal services |

---

## Common Mistakes (Your Struggle Log)

_Will be populated as we identify mistakes_

---

## Interview Tips

1. Always mention DNS resolution when tracing a request end-to-end
2. Know the difference between L4 (TCP) and L7 (HTTP) load balancing
3. Understand when to use REST vs gRPC vs WebSocket — it's a common interview question
4. Be able to explain "what happens when you type google.com" in 2 minutes

---

## Related Building Blocks
- DNS → URL Shortener (custom domain routing)
- Load Balancer → Every system at scale
- WebSocket → Chat systems, real-time collaboration
- CDN → Any system serving static content or media
