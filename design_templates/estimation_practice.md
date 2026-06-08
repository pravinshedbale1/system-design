# 📊 Estimation Practice — Back-of-Envelope Calculations

> The first 5 minutes of a system design interview are about ESTIMATION.
> Get these right, and you set the foundation for the entire design.
> Get them wrong, and your entire architecture is built on quicksand.

---

## 🧮 Numbers You Must Memorize

### Powers of 2
```
2^10 = 1 Thousand       = 1 KB
2^20 = 1 Million         = 1 MB
2^30 = 1 Billion         = 1 GB
2^40 = 1 Trillion        = 1 TB
2^50 = 1 Quadrillion     = 1 PB
```

### Latency Numbers Every Developer Should Know
```
L1 cache reference ................... 0.5 ns
Branch mispredict .................... 5 ns
L2 cache reference ................... 7 ns
Mutex lock/unlock .................... 100 ns
Main memory reference ................ 100 ns
Compress 1KB with Zippy .............. 10,000 ns = 10 μs
Send 2KB over 1 Gbps network ........ 20,000 ns = 20 μs
Read 1 MB sequentially from memory ... 250,000 ns = 250 μs
Round trip within same datacenter .... 500,000 ns = 500 μs = 0.5 ms
Disk seek ............................ 10,000,000 ns = 10 ms
Read 1 MB sequentially from disk ..... 30,000,000 ns = 30 ms
Send packet CA → Netherlands → CA .... 150,000,000 ns = 150 ms
```

### Quick Conversion Tricks
```
1 day = 86,400 seconds ≈ 100,000 seconds (for estimation)
1 day = 24 × 60 × 60 = 86,400

1 million requests/day = ~12 QPS
10 million requests/day = ~120 QPS
100 million requests/day = ~1,200 QPS
1 billion requests/day = ~12,000 QPS

1 QPS for a year = ~32 million requests
```

---

## 📝 Practice Estimations

### Example 1: Twitter
```
GIVEN:
- 300M monthly active users
- 50% daily active → 150M DAU
- Each user tweets 2/day, reads 100 tweets/day
- Average tweet: 140 chars + metadata = 300 bytes
- 30% tweets have media (average 200KB image)

CALCULATE:
Write QPS: 150M × 2 / 86400 ≈ 3,500 QPS
Read QPS: 150M × 100 / 86400 ≈ 175,000 QPS
Read:Write ratio ≈ 50:1

Storage (text/day): 150M × 2 × 300B = 90GB/day
Storage (media/day): 150M × 2 × 0.3 × 200KB = 18TB/day
Storage (5 years): ~33 PB (with media)

Bandwidth (incoming): 3,500 × 300B ≈ 1 MB/s (text only)
Bandwidth (outgoing): 175,000 × 300B ≈ 50 MB/s (text only)
```

### Example 2: URL Shortener
```
GIVEN:
- 100M new URLs/month
- 10:1 read:write ratio
- URL stored for 5 years

CALCULATE:
Write QPS: 100M / (30 × 86400) ≈ 40 QPS
Read QPS: 40 × 10 = 400 QPS
Peak: 400 × 3 = 1,200 QPS

Total URLs (5 years): 100M × 12 × 5 = 6 billion
Storage per URL: ~500 bytes (short URL + long URL + metadata)
Total storage: 6B × 500B = 3 TB

Cache: 20% of daily reads × data size
Daily reads: 400 × 86,400 = ~35M
Cache: 35M × 0.2 × 500B = 3.5 GB → fits in memory!
```

---

## 🏋️ Estimation Exercises (to be done together)

| # | System | Key Metrics to Estimate | Status |
|---|--------|------------------------|--------|
| 1 | Instagram | Posts/day, image storage, feed QPS | Not done |
| 2 | WhatsApp | Messages/day, connection count, storage | Not done |
| 3 | YouTube | Video upload size, streaming bandwidth, storage | Not done |
| 4 | Google Search | Queries/day, index size, crawl rate | Not done |
| 5 | Uber | Rides/day, location updates/sec, matching QPS | Not done |

---

_Practice estimations will be added as we work through each system._
