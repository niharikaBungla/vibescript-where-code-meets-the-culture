// VibeScript Functions Example
// Learn how to define and call functions (rizz_up)

// Basic function definition
rizz_up greet() lets_go
    spill_the_tea "Hey there!";
yeet

// Call the function
greet();

// Function with parameters
rizz_up say_hello(name) lets_go
    spill_the_tea "Hello, " + name + "!";
yeet

// Call function with argument
say_hello("VibeScript");

// Function with return value (slay)
rizz_up add(a, b) lets_go
    slay a + b;
yeet

// Use the return value
lit result = add(5, 3);
spill_the_tea "5 + 3 = " + result;

// Function with conditional return
rizz_up get_grade(score) lets_go
    no_cap (score >= 90) lets_go
        slay "A";
    yeet
    no_cap (score >= 80) lets_go
        slay "B";
    yeet
    no_cap (score >= 70) lets_go
        slay "C";
    yeet
    no_cap (score >= 60) lets_go
        slay "D";
    yeet
    slay "F";
yeet

// Call function with different values
spill_the_tea "Score 95: " + get_grade(95);
spill_the_tea "Score 85: " + get_grade(85);
spill_the_tea "Score 55: " + get_grade(55);

// Function that calls another function
rizz_up calculate_and_display(a, b) lets_go
    lit sum = add(a, b);
    spill_the_tea "The sum of " + a + " and " + b + " is " + sum;
yeet

// Call combined function
calculate_and_display(10, 20);
