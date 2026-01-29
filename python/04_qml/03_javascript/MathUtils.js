// MathUtils.js - JavaScript helper module for mathematical operations
// This file demonstrates importing JavaScript functions in QML

// Calculate factorial of a number
function factorial(n) {
    if (n < 0) return null;
    if (n === 0 || n === 1) return 1;
    
    let result = 1;
    for (let i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

// Calculate the nth Fibonacci number
function fibonacci(n) {
    if (n < 0) return null;
    if (n === 0) return 0;
    if (n === 1) return 1;
    
    let a = 0, b = 1;
    for (let i = 2; i <= n; i++) {
        let temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// Calculate sum of an array of numbers
function sum(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) return 0;
    
    let total = 0;
    for (let i = 0; i < numbers.length; i++) {
        total += parseFloat(numbers[i]) || 0;
    }
    return total;
}

// Calculate average of an array of numbers
function average(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) return 0;
    return sum(numbers) / numbers.length;
}

// Check if a number is prime
function isPrime(n) {
    if (n < 2) return false;
    if (n === 2) return true;
    if (n % 2 === 0) return false;
    
    for (let i = 3; i <= Math.sqrt(n); i += 2) {
        if (n % i === 0) return false;
    }
    return true;
}

// Generate a random integer between min and max (inclusive)
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// Convert degrees to radians
function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

// Calculate power
function power(base, exponent) {
    return Math.pow(base, exponent);
}
