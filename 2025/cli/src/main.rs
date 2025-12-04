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
// fn day_2_1(input: String) -> i64 {
//     let ranges = input.split(",");
//     let mut count = 0;
//     for range in ranges {
//         let (start, end) = range.split_once("-").expect("range had more than 1 -");
//         let end_val: usize = end.parse().unwrap();
//         let mut curr: usize = start.parse().unwrap();
//         while curr < end_val {
//             let curr_str = curr.to_string();
//             let half_len: u32 = (curr_str.len() / 2).try_into().unwrap();
//             let first_half = curr / (10usize.pow(half_len));
//             let next: usize = 10usize.pow(curr_str.len().try_into().unwrap());
//             println!("curr: {curr}");
//             if curr_str.len() % 2 == 0 {
//                 count += if next < end_val {
//                     println!("adding {}", next / 10 - first_half);
//                     next / 10 - first_half
//                 } else {
//                     let end_first_half = end_val / (10usize.pow(half_len));
//                     let maybe_last_double = end_first_half * 10usize.pow(half_len) + end_first_half;
//                     let maybe_add_one = if end_val >= maybe_last_double { 1 } else { 0 };
//                     println!("adding {}", end_first_half - first_half + maybe_add_one);
//                     end_first_half - first_half + maybe_add_one
//                 }
//             };
//             curr = next;
//         }
//     }
//     count.try_into().unwrap()
// }
fn day_2_1(input: String) -> i64 {
    let ranges = input.split(",");
    let mut count = 0;
    for range in ranges {
        let (start, end) = range.split_once("-").expect("range had more than 1 -");
        let end_val: usize = end.parse().unwrap();
        let mut curr: usize = start.parse().unwrap();
        while curr < end_val {
            let curr_str: String = curr.to_string();
            let next: usize = 10usize.pow(curr_str.len().try_into().unwrap());
            if curr_str.len() % 2 == 1 {
                curr = next;
                continue;
            }

            let half_len: u32 = (curr_str.len() / 2).try_into().unwrap();
            let first_half = curr / (10usize.pow(half_len));
            let next_double = first_half * 10usize.pow(half_len) + first_half;
            if next_double > end_val {
                break;
            } else if next_double >= curr {
                println!("next_double {next_double}");
                count += next_double;
            }
            curr = (first_half + 1) * 10usize.pow(half_len);
        }
    }
    count.try_into().unwrap()
}

fn day_2_2(input: String) -> i64 {
    todo!()
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
            println!("Day 2.1 output: {res}");
        }
        (_, _) => {
            todo!("haven't implemented day {day_num} part {part_num}")
        }
    }
    Ok(())
}
