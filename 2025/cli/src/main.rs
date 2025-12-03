use std::env;
use std::fs::read_to_string;
use std::io::{self};

fn day_1_1(input: String) -> i64 {
    let mut curr: i64 = 50;
    let mut zeroCount = 0;
    for line in input.lines() {
        let inc = line[1..].parse::<i64>().expect("i64 to come after L or R");
        let direction = line.chars().nth(0).expect("all lines to start w/ L or R");
        if direction == 'L' {
            curr = (curr - inc).rem_euclid(100);
        } else {
            curr = (curr + inc).rem_euclid(100);
        }
        println!("rotated {line} to point at {curr}");
        if curr == 0 {
            zeroCount += 1;
        }
    }
    zeroCount
}

fn day_1_2(input: String) -> i64 {
    let mut curr: i64 = 50;
    let mut zeroCount = 0;
    for line in input.lines() {
        let inc = line[1..].parse::<i64>().expect("i64 to come after L or R");
        let direction = line.chars().nth(0).expect("all lines to start w/ L or R");
        let next = if direction == 'L' {
            curr - inc
        } else {
            curr + inc
        };
        // We either will land at 0, or crossed over it going negative -- count 1 extra
        if next <= 0 && curr != 0 {
            zeroCount += 1
        }
        zeroCount += next.abs() / 100;
        curr = (next).rem_euclid(100);
        println!("rotated {line} to point at {curr} -- zeroCount {zeroCount}");
    }
    zeroCount
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 || args.len() > 4 {
        return Err(io::Error::other(format!(
            "wrong number of input args: {} - {args:?}",
            args.len()
        )));
    }
    let day_num = &args[1].parse::<u64>().unwrap();
    let part_num = &args[2].parse::<u64>().unwrap();
    let is_example = args.len() > 3 && &args[3] == "example";
    let input = read_to_string(format!(
        "/Users/Lucas/Documents/advent_of_code/2025/day{day_num}{}.txt",
        if is_example { "_example" } else { "" },
    ))?;
    match (day_num, part_num) {
        (1, 1) => {
            let res = day_1_1(input);
            println!("Day 1.1 output: {res}");
        }
        (1, 2) => {
            let res = day_1_2(input);
            println!("Day 1.2 output: {res}");
        }
        (_, _) => {
            todo!("haven't implemented day {day_num} part {part_num}")
        }
    }
    Ok(())
}
