// VibeScript Conditionals Example
// Learn how to use if statements (no_cap/cap)

lit age = 18;

// Basic if statement
no_cap (age >= 18) lets_go
    spill_the_tea "You're an adult!";
yeet

// If-else statement
no_cap (age >= 21) lets_go
    spill_the_tea "You can drink!";
yeet cap lets_go
    spill_the_tea "No drinks for you yet!";
yeet

// Complex conditions
lit score = 85;
no_cap (score >= 90) lets_go
    spill_the_tea "Grade: A";
yeet cap no_cap (score >= 80) lets_go
    spill_the_tea "Grade: B";
yeet cap no_cap (score >= 70) lets_go
    spill_the_tea "Grade: C";
yeet cap lets_go
    spill_the_tea "Grade: F";
yeet

// Boolean variables
mood is_student = this_slaps;
mood has_id = im_dead;

no_cap (is_student == this_slaps) lets_go
    spill_the_tea "Student discount applied!";
yeet

no_cap (has_id == im_dead) lets_go
    spill_the_tea "Please bring your ID";
yeet
