// VibeScript Functions Example
// Learn how to define and use functions (rizz_up/slay)

// Simple function without parameters
rizz_up greet() lets_go
    spill_the_tea "Hello from a function!";
yeet

// Call the function
greet();

// Function with parameters
rizz_up add_numbers(a, b) lets_go
    lit result = a + b;
    spill_the_tea "Sum: " + result;
    slay result;
yeet

// Call function with parameters
lit sum = add_numbers(5, 3);
spill_the_tea "Returned value: " + sum;

// Function with conditional logic
rizz_up check_age(age) lets_go
    no_cap (age >= 18) lets_go
        slay "adult";
    yeet cap lets_go
        slay "minor";
    yeet
yeet

tea status = check_age(25);
spill_the_tea "Status: " + status;

// Recursive function (factorial)
rizz_up factorial(n) lets_go
    no_cap (n <= 1) lets_go
        slay 1;
    yeet cap lets_go
        slay n * factorial(n - 1);
    yeet
yeet

lit fact = factorial(5);
spill_the_tea "5! = " + fact;
