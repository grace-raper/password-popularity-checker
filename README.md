# Count-Min Sketch Password Popularity Checker

## Overview

This project implements a Count-Min Sketch (CMS) data structure for efficiently tracking password frequency and popularity. CMS is a probabilistic data structure that provides space-efficient frequency counting, making it ideal for large-scale password analysis where exact counts aren't critical but relative popularity matters.

## Why Count-Min Sketch for Password Popularity?

Password popularity checking helps identify commonly used passwords that should be avoided. Traditional hash tables become impractical when dealing with massive datasets of compromised passwords like those in breach databases.

### Key Advantages with Example:

Consider analyzing the 3.2 billion passwords from the RockYou breach dataset. A traditional hash table storing each unique password would require approximately 50GB of memory. A Count-Min Sketch with dimensions 1,000,000 × 10 uses only 40MB - a 99.92% space reduction.

**Memory Efficiency**: CMS uses a fixed-size array regardless of input size. A 1000×10 structure uses just 40KB and can handle millions of passwords.

**Privacy Preservation**: Passwords aren't stored - only frequency counters are maintained. After processing "password123" a million times, the original string is never retained.

**Scalability**: Handles billions of password entries with consistent O(1) performance. Adding the billionth password takes the same time as adding the first.

**Real-time Updates**: New password breaches can be incrementally added without rebuilding the entire structure.

## Drawbacks

**Overestimation Error**: CMS can only overestimate frequency, never underestimate. If "mypassword" appears 1,000 times but hashes collide with popular passwords, it might report 5,000 occurrences. For security applications, this creates false alarms where rare passwords are flagged as common.

**Parameter Selection**: Choosing the right table size and number of hash functions is crucial. Too small (100×5) causes excessive collisions making every password appear popular. Too large (1,000,000×50) wastes memory. The optimal configuration depends on dataset size, acceptable error rate, and memory constraints.

## Other Applications

**Network Traffic Analysis**: Monitor packet frequencies and detect DDoS attacks. When analyzing 10 million packets per second, CMS can identify the top 1% of IP addresses using constant memory.

**Web Analytics**: Track page views across millions of URLs. A news website can identify trending articles using 1MB of memory instead of storing counters for every URL.

**Fraud Detection**: Identify suspicious transaction patterns by tracking account numbers or amounts without storing detailed histories.

## Implementation Details

This implementation uses a 2D numpy array of size `m × k` (default: 1000 × 10) creating 10,000 integer counters using approximately 40KB of memory. It uses MurmurHash3 with different seeds for each hash function, and the key insight is taking the minimum across all hash positions - this provides the conservative estimate that makes CMS work for the "heavy hitters" problem.

When you add a password, it gets hashed 10 times and increments 10 different counters. When you query a password, it returns the minimum of those 10 counters. This minimum operation filters out most collision effects while guaranteeing the estimate is at least as large as the true count.

## Future Improvements

**Accuracy**: Implement conservative update strategies and hierarchical CMS structures for different frequency ranges.

**Performance**: Add parallel processing for hash computation and batch operations for multiple passwords.

**Features**: Add time-decay for recent trends, weighted updates for different breach sources, and confidence intervals on estimates.

**Security**: Use cryptographic hash functions, implement differential privacy, and add rate limiting.

## Usage Example

```python
# Initialize CMS for password tracking
cms = CountMinSketch(size=10000, number=15)

# Add passwords from breach data
cms.add("123456", 1000000)  # Very common password
cms.add("password", 500000)

# Check password popularity
popularity = cms.getCount("123456")  # Returns >= 1000000
if popularity > 100000:
    print("This password is too common - choose another!")
```

## Conclusion

Count-Min Sketch provides an elegant solution for password popularity checking that balances accuracy, performance, and privacy. The benefits of constant space usage and fast operations make it ideal for large-scale password security applications where identifying clearly problematic passwords is more important than perfect accuracy.
