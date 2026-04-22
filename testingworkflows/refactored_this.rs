fn main() {
    // Preserve original behavior: print header then FizzBuzz sequence 1..=100.
    println!("Fizzbuzz");
    println!();

    for i in 1..=100 {
        let fizz = i % 3 == 0;
        let buzz = i % 5 == 0;

        // Original program printed "FizzBuzz" twice for numbers divisible by both 3 and 5.
        if fizz && buzz {
            println!("FizzBuzz");
            println!("FizzBuzz");
        } else if fizz {
            println!("Fizz");
        } else if buzz {
            println!("Buzz");
        } else {
            println!("{}", i);
        }
    }
}
