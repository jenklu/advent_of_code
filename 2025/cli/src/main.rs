use std::env;
use std::fs::read_to_string;
use std::io::{self};

fn day_1_1(input: String) -> i64 {
    let mut curr: i64 = 50;
    let mut zero_count = 0;
    for line in input.lines() {
        let inc = line[1..].parse::<i64>().expect("i64 to come after L or R");
        let direction = line.chars().nth(0).expect("all lines to start w/ L or R");
        if direction == 'L' {
            curr = (curr - inc).rem_euclid(100);
        } else {
            curr = (curr + inc).rem_euclid(100);
        }
        //println!("rotated {line} to point at {curr}");
        if curr == 0 {
            zero_count += 1;
        }
    }
    zero_count
}

fn day_1_2(input: String) -> i64 {
    let mut curr: i64 = 50;
    let mut zero_count = 0;
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
            zero_count += 1
        }
        zero_count += next.abs() / 100;
        curr = (next).rem_euclid(100);
        //println!("rotated {line} to point at {curr} -- zero_count {zero_count}");
    }
    zero_count
}

// Something like --
// invalid count = 0
// foreach range:
//   curr_start = lowest even-digit number above range_start
//   curr = curr_start
//   while curr < range_end {
//     delta = digits[(len(start) / 2)..].parse::<i64>(
//     curr_end  = curr + 10 * delta
//     curr += delta
//     if curr <  range_end {
//
//   }
fn day_2_1(input: String) -> i64 {
    let ranges = input.split(",");
    let mut count: usize = 0;
    for range in ranges {
        let (start, end) = range.split_once("-").expect("range had more than 1 -");
        let end_val: usize = end.parse().unwrap();
        let mut curr: usize = start.parse().unwrap();
        while curr <= end_val {
            let num_digits = (curr).ilog10() + 1;
            let first_half = curr / 10usize.pow(num_digits / 2);
            let second_half = curr % 10usize.pow(num_digits / 2);
            count += if first_half == second_half { curr } else { 0 };
            curr += 1;
        }
    }
    count.try_into().unwrap()
}

fn is_invalid(input: String) -> bool {
    let sz = input.len();
    'outer: for i in 1..((sz / 2) + 1) {
        if sz % i != 0 {
            continue;
        };
        for j in (i..sz).step_by(i) {
            if input[..i] != input[j..j + i] {
                continue 'outer;
            }
        }
        return true;
    }
    false
}
fn day_2_2(input: String) -> i64 {
    let ranges = input.split(",");
    let mut count: usize = 0;
    for range in ranges {
        let (start, end) = range.split_once("-").expect("range had more than 1 -");
        let end_val: usize = end.parse().unwrap();
        let mut curr: usize = start.parse().unwrap();
        while curr <= end_val {
            count += if is_invalid(curr.to_string()) {
                //println!("range: {start}-{end} invalid: {curr}");
                curr
            } else {
                0
            };
            curr += 1;
        }
    }
    count.try_into().unwrap()
}

fn day_3_1(input: String) -> i64 {
    let mut total_joltage: i64 = 0;
    for line in input.lines() {
        let digits: Vec<_> = line
            .chars()
            .map(|c| c.to_digit(10).unwrap() as i64)
            .collect();
        let (idx, first_digit) = digits[..(digits.len() - 1)]
            .iter()
            .enumerate()
            // We do this b/c of the semantics `If several elements are equally minimum, the first
            // element is returned`, whereas max_by_key has the opposite
            .min_by_key(|x| -x.1)
            .unwrap();
        let second_digit = digits[idx + 1..].iter().max().unwrap();
        total_joltage += first_digit * 10 + second_digit;
    }
    total_joltage
}

fn day_3_2_helper(digits: &[i64], num_digits: u32) -> i64 {
    if num_digits == 0 {
        return 0;
    }
    // + 1 accounts for looking at the _last_ digit -- think about when num_digits = 1
    let (idx, first_digit) = digits[..(digits.len() + 1 - num_digits as usize)]
        .iter()
        .enumerate()
        // We do this b/c of the semantics `If several elements are equally minimum, the first
        // element is returned`, whereas max_by_key has the opposite
        .min_by_key(|x| -x.1)
        .unwrap();
    return first_digit * 10i64.pow(num_digits - 1)
        + day_3_2_helper(&digits[idx + 1..], num_digits - 1);
}

fn day_3_2(input: String) -> i64 {
    let mut total_joltage: i64 = 0;
    for line in input.lines() {
        let digits: Vec<_> = line
            .chars()
            .map(|c| c.to_digit(10).unwrap() as i64)
            .collect();
        total_joltage += day_3_2_helper(&digits, 12);
    }
    total_joltage
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
        (2, 1) => {
            let res = day_2_1(input);
            println!("Day 2.1 output: {res}");
        }
        (2, 2) => {
            let res = day_2_2(input);
            println!("Day 2.2 output: {res}");
        }
        (3, 1) => {
            let res = day_3_1(input);
            println!("Day 3.1 output: {res}");
        }
        (3, 2) => {
            let res = day_3_2(input);
            println!("Day 3.2 output: {res}");
        }
        (_, _) => {
            todo!("haven't implemented day {day_num} part {part_num}")
        }
    }
    Ok(())
}
