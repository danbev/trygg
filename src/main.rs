use clap::Parser;

use lib::evaluate;
use std::fs;

#[derive(Parser, Debug)]
#[command(author,
    version,
    long_about = None)]
/// trygg is a tool to execute OPA policies wasm modules.
struct Args {
    #[arg(short, long, help = "The policy as a wasm module")]
    wasm: String,

    #[arg(short, long, help = "The entry_point/rule to be executed")]
    entry_point: String,

    #[arg(short, long, help = "The input file in json format (optional)")]
    input: Option<String>,

    #[arg(short, long, help = "The data file in json format (optional)")]
    data: Option<String>,
}

fn main() {
    let args = Args::parse();

    let wasm = fs::read(args.wasm).unwrap();
    let input = args
        .input
        .map_or(String::from("{}"), |p| fs::read_to_string(p).unwrap());
    let data = args
        .data
        .map_or(String::from("{}"), |p| fs::read_to_string(p).unwrap());
    evaluate(&wasm, &args.entry_point, &input, &data);
}
