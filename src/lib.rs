use policy_evaluator::burrego::Evaluator;

pub fn evaluate(wasm: &Vec<u8>, entry_point: &String, input: &String, data: &String) {
    let input: serde_json::Value =
        serde_json::from_str(&input).expect("input json does not have correct format.");
    let data: serde_json::Value =
        serde_json::from_str(&data).expect("data json does not have correct format.");

    println!("Evaluating:");
    println!("input: {}", input);
    println!("data: {}", data);
    let mut evaluator = Evaluator::new(wasm, Default::default()).unwrap();
    let entrypoint_id = evaluator.entrypoint_id(entry_point).unwrap();
    let ret = evaluator.evaluate(entrypoint_id, &input, &data).unwrap();
    println!("Result:");
    print!("{}", ret);
}

#[cfg(test)]
mod tests {
    #[test]
    fn process_test() {
        println!("implement test...");
        assert_eq!(1, 1);
    }
}
