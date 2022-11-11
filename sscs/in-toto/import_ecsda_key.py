#!/usr/bin/python3

import sys
from pathlib import Path

import hashlib
import securesystemslib.ecdsa_keys

from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigencode_der, sigdecode_der

from securesystemslib import interface
from securesystemslib.interface import *
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock
import json

KEYS = securesystemslib.keys

def convert(key_pem):
  private_key_pem = Path(key_pem).read_text()
  private_key = KEYS.import_ecdsakey_from_private_pem(private_key_pem);
  print(f"private keyid: {private_key['keyid']}");
  #print(json.dumps(private_key));
  f = open(f"{key_pem}.json", "w")
  f.write(json.dumps(private_key));
  f.close()

  pub_json_dict = {};
  pub_json_dict["keytype"] = private_key["keytype"];
  pub_json_dict["scheme"] = private_key["scheme"];
  pub_json_dict["keyid_hash_algorithms"] = private_key["keyid_hash_algorithms"];
  pub_json_dict["keyval"] = { "public": private_key["keyval"]["public"]};
  #print(pub_json_dict);

  f = open(f"{key_pem}.pub.json", "w")
  f.write(json.dumps(pub_json_dict));
  f.close()

  dict = import_publickeys_from_file([f"{key_pem}.pub.json"], ["ecdsa"]);
  private_key_id = private_key['keyid'];
  public_key_id = dict[private_key_id]["keyid"];
  print(f"public keyid : {public_key_id}");
  if (private_key_id != public_key_id) :
      print("Conversion from pem to json format failed.");
      print("If there has been a change in the order of fields that");
      print("import_publickeys_from_file produces the id generation will not work");
          

if __name__ == '__main__':
  convert(sys.argv[1]);
