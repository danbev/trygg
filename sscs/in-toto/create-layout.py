#!/usr/bin/python3

import sys
from pathlib import Path

import hashlib
import securesystemslib.ecdsa_keys
import json

from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigencode_der, sigdecode_der

from securesystemslib import interface
from securesystemslib.interface import *
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock

KEYS = securesystemslib.keys

def process(github_org, github_project, private_key_file, public_key_file):
  print(f"Processing https://github.com/{github_org}/{github_project}.git")

  private_key_pem = Path(private_key_file).read_text();
  public_key_pem = Path(public_key_file).read_text();

  private_key = KEYS.import_ecdsakey_from_private_pem(private_key_pem);
  public_key = KEYS.import_ecdsakey_from_public_pem(public_key_pem);

  layout = Layout.read({
      "_type": "layout",
      "keys": {
          public_key["keyid"]: public_key,
      },
      "steps": [{
          "name": "clone_project",
          "expected_materials": [],
          "expected_products": [
              ["CREATE", github_project],
              ["ALLOW", f"{github_project}/*"],
          ],
          "pubkeys": [public_key["keyid"]],
          "expected_command": [
              "git",
              "clone",
              f"https://github.com/{github_org}/{github_project}.git"
          ],
          "threshold": 1,
        },{
          "name": "run_tests",
          "expected_materials": [
              ["MATCH", f"{github_project}/*", "WITH", "PRODUCTS", "FROM", "clone_project"],
              ["ALLOW", "Cargo.toml"],
              ["DISALLOW", "*"],
          ],
          "expected_products": [
              ["ALLOW", "Cargo.lock"],
              ["ALLOW", "cosign.pub"],
              ["ALLOW", "sscs-layout.json"],
              ["DISALLOW", "*"]],
          "pubkeys": [public_key["keyid"]],
          "expected_command": [],
          "threshold": 1,
        }],
      "inspect": [{
          "name": "cargo-fetch",
          "expected_materials": [
              ["MATCH", f"{github_project}/*", "WITH", "PRODUCTS", "FROM", "clone_project"],
              ["ALLOW", f"{github_project}/target"],
              ["ALLOW", "cosign.pub"],
              ["ALLOW", "sscs-layout.json"],
              ["DISALLOW", "*"],
          ],
          "expected_products": [
              ["MATCH", f"{github_project}/Cargo.toml", "WITH", "PRODUCTS", "FROM", "clone_project"],
              ["MATCH", "*", "WITH", "PRODUCTS", "FROM", "clone_project"],
              ["ALLOW", f"{github_project}/target"],
              ["ALLOW", public_key_file],
              ["ALLOW", "sscs-layout.json"],
          ],
          "run": [
              "git",
              "clone",
              f"https://github.com/{github_org}/{github_project}.git"
          ],
        }],
  })

  metadata = Metablock(signed=layout)

  print(f"Creating artifiacts/{github_project}-layout.json file")
  metadata.sign(private_key)
  metadata.dump(f"artifacts/{github_project}-layout.json")

if __name__ == '__main__':
  process(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
