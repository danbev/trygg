#!/usr/bin/python3

import sys
import hashlib
import securesystemslib.ecdsa_keys
import json

from pathlib import Path
from ecdsa import SigningKey, VerifyingKey
from ecdsa.util import sigencode_der, sigdecode_der

from securesystemslib import interface
from securesystemslib.interface import *
from in_toto.models.layout import Layout
from in_toto.models.metadata import Metablock

KEYS = securesystemslib.keys

def convert(key_pem):
  public_key_pem = Path(key_pem).read_text()
  public_key = KEYS.import_ecdsakey_from_public_pem(public_key_pem);
  print(json.dumps(public_key));

if __name__ == '__main__':
  convert(sys.argv[1]);
