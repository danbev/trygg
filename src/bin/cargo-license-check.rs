use clap::Parser;

use lib::evaluate;
use std::fs;

#[derive(Parser, Debug)]
#[command(author,
    version,
    long_about = None)]
/// cargo-license-check is a tool that checks license of dependencies according to...
struct Args {
    #[arg(short, long, help = "The input file in json format (optional)")]
    input: Option<String>,

    #[arg(short, long, help = "The data file in json format (optional)")]
    data: Option<String>,
}

fn main() {
    let args = Args::parse();

    let wasm = fs::read("policies/license.wasm").unwrap();
    let entry_point = String::from("license/allow");
    let input = args
        .input
        .map_or(String::from("{}"), |p| fs::read_to_string(p).unwrap());
    let data = args
        .data
        .map_or(String::from("{}"), |p| fs::read_to_string(p).unwrap());
    let policy_name = String::from("license-check");
    evaluate(&wasm, &entry_point, &input, &data, policy_name);
}
