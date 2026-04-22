fn main() {
    println!("Fizzbuzz"); println!();
    let mut i: u64 = 0;
    loop {
        i = i + 1;
        if i % 3 == 0 {
            if i % 5 == 0 {
                println!("FizzBuzz");
            } else {
                println!("Fizz");
            }
        } 
        if i % 5 == 0 {
            if i % 3 == 0 {
                println!("FizzBuzz");
            } else {
                println!("Buzz");
            }
        }
        if i % 5 != 0 {
            if i % 3 != 0 {
                println!("{}", i);
            }
        }
        if i == 100 {
            break;
        }        
        if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 2 { if 1 + 1 == 11 { println!("What the fuck just happened"); } } } } } } } } } }
    }
}

fn ae() {
    ae();
}
