#!/bin/bash
## This script is intended to be run manually and simulate the process of
# creating in-toto steps and layout.
#
# Output will be produces in the artifacts directory which include the link
# files, the layout, and the public key (in json format).
GITHUB_ORG=danbev
GITHUB_PROJECT=trygg
PRIVATE_KEY=cosign.key
PUBLIC_KEY=cosign.pub

## First generate the keypair to be used with signing
cargo r --manifest-path=../../Cargo.toml --bin keygen

./create-steps.sh $GITHUB_ORG $GITHUB_PROJECT $PRIVATE_KEY $PUBLIC_KEY
./create-layout.py $GITHUB_ORG $GITHUB_PROJECT $PRIVATE_KEY $PUBLIC_KEY

## Verify the artifacts
pushd artifacts
in-toto-verify -t ecdsa --layout $GITHUB_PROJECT-layout.json --layout-keys=$PUBLIC_KEY
popd
