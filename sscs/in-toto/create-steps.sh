#!/bin/bash

if [ $# -ne 4 ]
  then
	echo "Usage: create-steps github_org github_project privatekey publickey"
	exit 1
fi

github_org=$1
project_name=$2
private_key_pem=$3
public_key=$4
private_key_json=${private_key_pem}.json
github_url=https://github.com/$github_org/${project_name}.git
workdir=work

## Create a work directory for all artifacts
rm -rf $workdir
mkdir $workdir
cp $private_key_pem $public_key $workdir
pushd $workdir > /dev/null

echo "1) Convert ecdsa pem to securesystemslib/json format"
../private_key_to_securesystemlib_json.py $private_key_pem > $private_key_json
cat $private_key_json | jq

echo "2) Cloning $github_url"
in-toto-run -n clone_project -k $private_key_json -t ecdsa --base-path $project_name --products Cargo.toml Cargo.lock examples README.md rustfmt.toml rust-toolchain.toml src tests -- git clone $github_url

echo "3) Run tests"
cargo test -q --manifest-path=${project_name}/Cargo.toml --no-run
in-toto-run -n run_tests -s -k $private_key_json -t ecdsa -- cargo test --manifest-path ${project_name}/Cargo.toml

echo "4) Copy artifacts"
mkdir -p ../artifacts
# Convert the public key to securesystemslib json format which is the format
# that in-toto expects.
../public_key_to_securesystemlib_json.py $public_key > ../artifacts/$public_key
cp *.link ../artifacts
## TODO: remove this copying, it is just here to help during development
cp $private_key_json ../artifacts

popd > /dev/null

rm -rf $workdir
