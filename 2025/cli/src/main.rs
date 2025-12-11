use std::collections::{HashMap, HashSet};
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

fn char_at<T: AsRef<str>>(rows: &[T], i: isize, j: isize) -> char {
    rows[i as usize].as_ref().chars().nth(j as usize).unwrap()
}

fn day_4_1(input: String) -> i64 {
    let rows: Vec<&str> = input.lines().collect();
    let mut count = 0;
    for i in 0..rows.len() as isize {
        for j in 0..rows[0].len() as isize {
            if char_at(&rows, i, j) == '.' {
                continue;
            }
            let mut adjacent_count = 0;
            for delta_i in -1isize..2 {
                for delta_j in -1isize..2 {
                    let (check_i, check_j) = (i + delta_i, j + delta_j);
                    if (delta_i != 0 || delta_j != 0)
                        && check_i >= 0
                        && check_i < rows.len() as isize
                        && check_j >= 0
                        && check_j < rows[0].len() as isize
                        && char_at(&rows, check_i, check_j) == '@'
                    {
                        adjacent_count += 1;
                    }
                }
            }
            count += (adjacent_count < 4) as i64;
        }
    }
    count
}

fn day_4_2(input: String) -> i64 {
    let mut rows: Vec<String> = input.lines().map(Into::into).collect();
    let mut total_count = 0;
    loop {
        let mut next_rows = Vec::<String>::with_capacity(rows.len());
        let mut count = 0;
        for i in 0..rows.len() as isize {
            next_rows.push(String::with_capacity(rows[0].len()));
            for j in 0..rows[0].len() as isize {
                if char_at(&rows, i, j) == '.' {
                    next_rows[i as usize].push('.');
                    continue;
                }
                let mut adjacent_count = 0;
                for delta_i in -1isize..2 {
                    for delta_j in -1isize..2 {
                        let (check_i, check_j) = (i + delta_i, j + delta_j);
                        if (delta_i != 0 || delta_j != 0)
                            && check_i >= 0
                            && check_i < rows.len() as isize
                            && check_j >= 0
                            && check_j < rows[0].len() as isize
                            && char_at(&rows, check_i, check_j) == '@'
                        {
                            adjacent_count += 1;
                        }
                    }
                }
                count += (adjacent_count < 4) as i64;
                next_rows[i as usize].push(if adjacent_count < 4 { '.' } else { '@' })
            }
        }
        total_count += count;
        if count == 0 {
            return total_count;
        }
        rows = next_rows;
    }
}

fn day_5_1(input: String) -> i64 {
    let mut fresh_count = 0;
    let mut ranges: Vec<(u64, u64)> = Vec::new();
    for line in input.lines() {
        if line == "" {
            continue;
        }
        let bounds: Vec<_> = line.split('-').map(|x| x.parse::<u64>().unwrap()).collect();
        if bounds.len() > 1 {
            ranges.push((bounds[0], bounds[1]));
        } else {
            for (start, end) in &ranges {
                if bounds[0] >= *start && bounds[0] <= *end {
                    fresh_count += 1;
                    break;
                }
            }
        }
    }
    fresh_count
}

fn day_5_2(input: String) -> i64 {
    let mut ranges: Vec<(u64, u64)> = Vec::new();
    for line in input.lines() {
        if line == "" {
            break;
        }
        let bounds: Vec<_> = line.split('-').map(|x| x.parse::<u64>().unwrap()).collect();
        if bounds.len() > 1 {
            ranges.push((bounds[0], bounds[1]));
        }
    }
    ranges.sort_unstable_by_key(|(start, _)| *start);
    let mut i = 0;
    // Would prob be "faster" and simpler logic to use a separate result array instead of splicing
    // in here...but I got this working (hey, it's space-efficient!)
    while i < ranges.len() {
        let mut splice_in = ranges[i];
        let mut splice_end = i + 1;
        while splice_end < ranges.len() && ranges[i].1 >= ranges[splice_end].1 {
            splice_end += 1;
        }
        if splice_end < ranges.len() && ranges[i].1 >= ranges[splice_end].0 {
            splice_in.1 = ranges[splice_end].1;
            splice_end += 1;
        }
        if splice_end > i + 1 || splice_in != ranges[i] {
            ranges.splice(i..splice_end, [splice_in]);
        } else {
            i += 1;
        }
    }
    ranges
        .iter()
        .fold(0, |acc, (start, end)| acc + 1 + end - start) as i64
}

fn day_6_1(input: String) -> i64 {
    let mut problems: Vec<Vec<_>> = Vec::new();
    let mut sum = 0;
    for line in input.lines() {
        line.split_whitespace()
            .enumerate()
            .for_each(|(idx, token)| {
                let num = token.parse::<i64>();
                if problems.len() <= idx {
                    problems.push(vec![num.unwrap()])
                } else if let Ok(num) = num {
                    problems[idx].push(num)
                } else {
                    sum += if token == "+" {
                        problems[idx].iter().sum::<i64>()
                    } else {
                        problems[idx].iter().product()
                    }
                }
            })
    }
    sum
}

fn day_6_2(input: String) -> i64 {
    // This processing is ugly, but []-indexing into Vec<chars> >>> `&str.chars().nth().unwrap()`
    let lines: Vec<Vec<char>> = input.lines().map(|l| l.chars().collect()).collect();
    let mut curr_problem = vec![];
    let mut curr_problem_start = 0usize;
    let mut sum = 0;
    for i in 0..lines[0].len() {
        let mut curr_value = 0;
        for j in 0..lines.len() - 1 {
            if let Some(val) = lines[j][i].to_digit(10) {
                curr_value = curr_value * 10 + val as i64
            }
        }
        if curr_value > 0 {
            curr_problem.push(curr_value);
        }
        // i == lines[0].len() - 1 to include the last problem
        if curr_value == 0 || i == lines[0].len() - 1 {
            sum += if lines[lines.len() - 1][curr_problem_start] == '+' {
                curr_problem.iter().sum::<i64>()
            } else {
                curr_problem.iter().product()
            };
            curr_problem_start = i + 1;
            curr_problem = vec![];
        }
    }
    sum
}

fn day_7_1(input: String) -> i64 {
    let lines: Vec<Vec<char>> = input.lines().map(|x| x.chars().collect()).collect();
    let mut beams = HashSet::from([input.find('S').unwrap()]);
    let mut count = 0;
    for line in &lines[1..] {
        let mut next_beams = HashSet::new();
        for beam in beams {
            if line[beam] == '^' {
                count += 1;
                if beam + 1 < line.len() {
                    next_beams.insert(beam + 1);
                }
                if beam >= 1 {
                    next_beams.insert(beam - 1);
                }
            } else {
                next_beams.insert(beam);
            }
        }
        beams = next_beams.clone()
    }
    count
}

fn day_7_2_helper(
    y: usize,
    x: usize,
    input: &Vec<Vec<char>>,
    cache: &mut HashMap<(usize, usize), i64>,
) -> i64 {
    if y >= input.len() || x >= input[0].len() {
        return 0;
    }
    if let Some(val) = cache.get(&(x, y)) {
        return *val;
    }
    if input[y][x] == '^' {
        let right = day_7_2_helper(y, x + 1, input, cache);
        let left = day_7_2_helper(y, x - 1, input, cache);
        cache.insert((x + 1, y), right);
        cache.insert((x - 1, y), left);
        return left + right + 1;
    }
    day_7_2_helper(y + 1, x, input, cache)
}

fn day_7_2(input: String) -> i64 {
    let mut cache = HashMap::new();
    let lines: Vec<Vec<char>> = input.lines().map(|x| x.chars().collect()).collect();
    day_7_2_helper(0, input.find('S').unwrap(), &lines, &mut cache) + 1
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
        (4, 1) => {
            let res = day_4_1(input);
            println!("Day 4.1 output: {res}");
        }
        (4, 2) => {
            let res = day_4_2(input);
            println!("Day 4.2 output: {res}");
        }
        (5, 1) => {
            let res = day_5_1(input);
            println!("Day 5.1 output: {res}");
        }
        (5, 2) => {
            let res = day_5_2(input);
            println!("Day 5.2 output: {res}");
        }
        (6, 1) => {
            let res = day_6_1(input);
            println!("Day 6.1 output: {res}");
        }
        (6, 2) => {
            let res = day_6_2(input);
            println!("Day 6.2 output: {res}");
        }
        (7, 1) => {
            let res = day_7_1(input);
            println!("Day 7.1 output: {res}");
        }
        (7, 2) => {
            let res = day_7_2(input);
            println!("Day 7.2 output: {res}");
        }
        (_, _) => {
            todo!("haven't implemented day {day_num} part {part_num}")
        }
    }
    Ok(())
}
