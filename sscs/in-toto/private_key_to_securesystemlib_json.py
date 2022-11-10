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
  print(json.dumps(private_key));

if __name__ == '__main__':
  convert(sys.argv[1]);
