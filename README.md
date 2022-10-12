## Trygg
Trygg, safe in Swedish, is a tool to execute/evaluate policy rules in Rust.
It does so by executing an OPA Policy that has been compiled to wasm.

### Install OPA
This step is only required if one wants to work with the OPA
[policies](./policies) and rebuild wasm modules.

```console
$ cd policies
$ curl -L -o opa https://github.com/open-policy-agent/opa/releases/download/v0.45.0/opa_linux_amd64
$ chmod 744 opa
```

### Polices
The [polices](./polices) directory contains the polices that are used as
examples, there is currently only one policy. This can tested and then built
into a wasm module using the following command:
```console
$ cd policies
$ make test
./opa test . -v
test-license.rego:
data.test_license.test_allow: PASS (391.199µs)
--------------------------------------------------------------------------------
PASS: 1/1

$ make license.wasm 
./opa build -t wasm -e license/allow license.rego
```
The last command will produce a wasm module named `license.wasm` in the
policies directory.

### Running
After building the policy in the previous step we can evaluate the policy
against some [input](./examples/licenses-input.txt):
```console
$ cargo r -q -- --wasm=policies/license.wasm --entry-point=license/allow --input=examples/licenses-input.txt

Evaluating:
policy_name: None
input: [{"name":"MIT Licence"},{"name":"Apache-License 2.0"},{"name":"something"}]
data: {}

Result:
[{"result":true}]
```

This policy called above does not take any as data json file can be specified
using a command line option. 

```console
trygg is a tool to execute OPA policies wasm modules

Usage: trygg [OPTIONS] --wasm <WASM> --entry-point <ENTRY_POINT>

Options:
  -w, --wasm <WASM>                The policy as a wasm module
  -e, --entry-point <ENTRY_POINT>  The entry_point/rule to be executed
  -i, --input <INPUT>              The input file in json format (optional)
  -d, --data <DATA>                The data file in json format (optional)
  -p, --policy-name <POLICY_NAME>  The name of the policy to be run [default: None]
  -h, --help                       Print help information
  -V, --version                    Print version information
```
