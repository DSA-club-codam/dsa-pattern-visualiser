# Someone feeds the page an array of a million elements

**The fear:** the browser melts, the laptop fan takes off, the club session ends early.

**How likely:** impossible today. There is no input box; every example is fixed at build time and build.py refuses anything over 20 elements.

**What we would do:** if custom input arrives one day (ADR 005), it gets the same 20-element limit and a friendly message.
