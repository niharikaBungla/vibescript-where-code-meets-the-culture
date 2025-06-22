// VibeScript Conditionals Example
// Learn how to use if-else statements (no_cap/cap)

// Basic if statement
lit score = 85;

no_cap (score >= 80) lets_go
    spill_the_tea "You're doing amazing!";
yeet

// If-else statement
lit temperature = 15;

no_cap (temperature > 25) lets_go
    spill_the_tea "It's hot outside!";
yeet
cap lets_go
    spill_the_tea "It's cool outside!";
yeet

// Nested conditionals
mood is_weekend = this_slaps;
lit time = 10;

no_cap (is_weekend) lets_go
    no_cap (time < 12) lets_go
        spill_the_tea "It's weekend morning!";
    yeet
    cap lets_go
        spill_the_tea "It's weekend afternoon/evening!";
    yeet
yeet
cap lets_go
    spill_the_tea "It's a weekday.";
yeet

// Logical operators
lit age = 20;
mood has_id = this_slaps;

no_cap (age >= 21 && has_id) lets_go
    spill_the_tea "You can enter the venue.";
yeet
cap lets_go
    spill_the_tea "Sorry, you can't enter.";
yeet
