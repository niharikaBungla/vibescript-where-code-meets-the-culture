// VibeScript Loops Example
// Learn how to use while (lowkey) and for (highkey) loops

// Basic while loop
lit count = 1;
lowkey (count <= 5) lets_go
    spill_the_tea "While count: " + count;
    count = count + 1;
yeet

// For loop (initialize; condition; update)
highkey (lit i = 0; i < 5; i = i + 1) lets_go
    spill_the_tea "For count: " + i;
yeet

// Break statement (and_i_oop)
lowkey (this_slaps) lets_go
    lit random = 42;  // This would be random in a real app
    spill_the_tea "Generated: " + random;
    
    no_cap (random == 42) lets_go
        spill_the_tea "Found the answer!";
        and_i_oop;  // break the loop
    yeet
yeet

// Continue statement (as_if)
highkey (lit i = 0; i < 10; i = i + 1) lets_go
    // Skip even numbers
    no_cap (i % 2 == 0) lets_go
        as_if;  // continue to next iteration
    yeet
    
    spill_the_tea "Odd number: " + i;
yeet

// Nested loops
highkey (lit i = 1; i <= 3; i = i + 1) lets_go
    highkey (lit j = 1; j <= 3; j = j + 1) lets_go
        spill_the_tea i + "," + j;
    yeet
yeet
