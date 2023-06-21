from lighthouseweb3 import Lighthouse
import pytest
import io
import os
import re


def parse_env():
    """parse .env file"""
    try:
        with open(".env", "r") as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith("#") or not line:
                    continue
                if "=" not in line:
                    print(f"Invalid line: {line}")
                    continue
                key, value = map(str.strip, line.split("=", 1))
                if not re.match(r'^[A-Z_][A-Z0-9_]*$', key):
                    print(f"Invalid key: {key}")
                    continue
                os.environ[key] = value
    except FileNotFoundError:
        print("No .env file found")
        print("Defaulting to preset environment variables...")
    except IOError as e:
        print(f"Error reading .env file: {e}")


def proposed_hex():
    return "5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20313534373138333939342c20226e616d65223a20226a61636b2d73706172726f772d6e65772d73686970222c20227061796d656e745f61646472657373223a2022795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e74223a2034392c202273746172745f65706f6368223a20313532313432393139342c202274797065223a20312c202275726c223a202268747470733a2f2f7777772e6461736863656e7472616c2e6f72672f626c61636b2d706561726c227d5d5d"


def proposed_hash():
    return "9081934f7cf5379b339fdae8ec5c9259bb25333443c9fa6b39852056e9084815"


parse_env()
def test_uploadBlob_for_string():
    """test Hex string  function"""
    l = Lighthouse(os.environ.get("LIGHTHOUSE_TOKEN"))
    res = l.uploadBlob(
        io.BytesIO(proposed_hex().encode("utf-8")), "generate_random_string.txt",proposed_hash())
    filehash= res.get("data").get("Hash")
    assert type(res.get("data")) is type({})
    assert len(res.get("data").get("Hash"))>=46

    tagData = l.getTagged(proposed_hash())
    assert filehash == tagData.get("data").get("cid")