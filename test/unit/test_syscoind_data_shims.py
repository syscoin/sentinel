import pytest
import sys
import os
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import syscoinlib
import gobject_json


# old format proposal hex w/multi-dimensional array
@pytest.fixture
def proposal_hex_old():
    return "5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20313534373138333939342c20226e616d65223a20226a61636b2d73706172726f772d6e65772d736869702d7573696e672d737973636f696e222c20227061796d656e745f61646472657373223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b222c20227061796d656e745f616d6f756e74223a2034392c202273746172745f65706f6368223a20313532373730383531382c202274797065223a20312c202275726c223a202268747470733a2f2f776869746570617065722e737973636f696e2e6f7267227d5d5d"


# same proposal data as old, but streamlined format
@pytest.fixture
def proposal_hex_new():
    return "7b22656e645f65706f6368223a20313534373138333939342c20226e616d65223a20226a61636b2d73706172726f772d6e65772d736869702d7573696e672d737973636f696e222c20227061796d656e745f61646472657373223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b222c20227061796d656e745f616d6f756e74223a2034392c202273746172745f65706f6368223a20313532373730383531382c202274797065223a20312c202275726c223a202268747470733a2f2f776869746570617065722e737973636f696e2e6f7267227d"


# old format trigger hex w/multi-dimensional array
@pytest.fixture
def trigger_hex_old():
    return "5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2034333830302c20227061796d656e745f616464726573736573223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b7c54456a4d6e6842356d41507270673752344355435347514e6e4a7150654146425448222c20227061796d656e745f616d6f756e7473223a2022357c33222c202274797065223a20327d5d5d"


# same data as new, but simpler format
@pytest.fixture
def trigger_hex_new():
    return "7b226576656e745f626c6f636b5f686569676874223a2034333830302c20227061796d656e745f616464726573736573223a202254535466654d65577751694344774d53545752616a39777756474e6a5a466676466b7c54456a4d6e6842356d41507270673752344355435347514e6e4a7150654146425448222c20227061796d656e745f616d6f756e7473223a2022357c33222c202274797065223a20327d"


# TODO: remove fixtures below here once test_SHIM_serialise_for_syscoind removed


@pytest.fixture
def sentinel_proposal_hex():
    return '7b22656e645f65706f6368223a20313439313032323830302c20226e616d65223a2022626565722d7265696d62757273656d656e742d37222c20227061796d656e745f61646472657373223a2022795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e74223a20372e30303030303030302c202273746172745f65706f6368223a20313438333235303430302c202274797065223a20312c202275726c223a202268747470733a2f2f6461736863656e7472616c2e636f6d2f626565722d7265696d62757273656d656e742d37227d'


@pytest.fixture
def sentinel_superblock_hex():
    return '7b226576656e745f626c6f636b5f686569676874223a2036323530302c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795443363268755234595145506e39414a486a6e517878726548536267416f617456222c20227061796d656e745f616d6f756e7473223a2022357c33222c202274797065223a20327d'


@pytest.fixture
def syscoind_proposal_hex():
    return '5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20313439313336383430302c20226e616d65223a2022626565722d7265696d62757273656d656e742d39222c20227061796d656e745f61646472657373223a2022795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e74223a2034392e30303030303030302c202273746172745f65706f6368223a20313438333235303430302c202274797065223a20312c202275726c223a202268747470733a2f2f7777772e6461736863656e7472616c2e6f72672f702f626565722d7265696d62757273656d656e742d39227d5d5d'


@pytest.fixture
def syscoind_superblock_hex():
    return '5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2036323530302c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795443363268755234595145506e39414a486a6e517878726548536267416f617456222c20227061796d656e745f616d6f756e7473223a2022357c33222c202274797065223a20327d5d5d'

# ========================================================================


def test_SHIM_serialise_for_syscoind(sentinel_proposal_hex, sentinel_superblock_hex):
    assert syscoinlib.SHIM_serialise_for_syscoind(sentinel_proposal_hex) == '5b5b2270726f706f73616c222c207b22656e645f65706f6368223a20313439313032323830302c20226e616d65223a2022626565722d7265696d62757273656d656e742d37222c20227061796d656e745f61646472657373223a2022795965384b77796155753559737753596d4233713372797838585455753979375569222c20227061796d656e745f616d6f756e74223a20372e30303030303030302c202273746172745f65706f6368223a20313438333235303430302c202274797065223a20312c202275726c223a202268747470733a2f2f6461736863656e7472616c2e636f6d2f626565722d7265696d62757273656d656e742d37227d5d5d'
    assert syscoinlib.SHIM_serialise_for_syscoind(sentinel_superblock_hex) == '5b5b2274726967676572222c207b226576656e745f626c6f636b5f686569676874223a2036323530302c20227061796d656e745f616464726573736573223a2022795965384b77796155753559737753596d42337133727978385854557539793755697c795443363268755234595145506e39414a486a6e517878726548536267416f617456222c20227061796d656e745f616d6f756e7473223a2022357c33222c202274797065223a20327d5d5d'


def test_valid_json():
    import binascii

    # test some valid JSON
    assert gobject_json.valid_json("{}") is True
    assert gobject_json.valid_json("null") is True
    assert gobject_json.valid_json("true") is True
    assert gobject_json.valid_json("false") is True
    assert gobject_json.valid_json("\"rubbish\"") is True
    assert gobject_json.valid_json(
        binascii.unhexlify(proposal_hex_old())
    ) is True
    assert gobject_json.valid_json(
        binascii.unhexlify(proposal_hex_new())
    ) is True
    assert gobject_json.valid_json(
        binascii.unhexlify(trigger_hex_new())
    ) is True
    assert gobject_json.valid_json(
        binascii.unhexlify(trigger_hex_old())
    ) is True

    # test some invalid/bad/not JSON
    assert gobject_json.valid_json("False") is False
    assert gobject_json.valid_json("True") is False
    assert gobject_json.valid_json("Null") is False
    assert gobject_json.valid_json("NULL") is False
    assert gobject_json.valid_json("nil") is False
    assert gobject_json.valid_json("rubbish") is False
    assert gobject_json.valid_json("{{}") is False
    assert gobject_json.valid_json("") is False

    poorly_formatted = trigger_hex_old() + "7d"
    assert gobject_json.valid_json(
        binascii.unhexlify(poorly_formatted)
    ) is False


def test_extract_object():
    from decimal import Decimal
    import binascii

    # jack sparrow needs a new ship - same expected proposal data for both new &
    # old formats
    expected = {
        'type': 1,
        'name': 'jack-sparrow-new-ship-using-syscoin',
        'url': 'https://whitepaper.syscoin.org',
        'start_epoch': 1527708518,
        'end_epoch': 1547183994,
        'payment_address': 'TSTfeMeWwQiCDwMSTWRaj9wwVGNjZFfvFk',
        'payment_amount': Decimal('49'),
    }

    # test proposal old format
    json_str = binascii.unhexlify(proposal_hex_old()).decode('utf-8')
    assert gobject_json.extract_object(json_str) == expected

    # test proposal new format
    json_str = binascii.unhexlify(proposal_hex_new()).decode('utf-8')
    assert gobject_json.extract_object(json_str) == expected

    # same expected trigger data for both new & old formats
    expected = {
        'type': 2,
        'event_block_height': 43800,
        'payment_addresses': 'TSTfeMeWwQiCDwMSTWRaj9wwVGNjZFfvFk|TEjMnhB5mAPrpg7R4CUCSGQNnJqPeAFBTH',
        'payment_amounts': '5|3',
    }

    # test trigger old format
    json_str = binascii.unhexlify(trigger_hex_old()).decode('utf-8')
    assert gobject_json.extract_object(json_str) == expected

    # test trigger new format
    json_str = binascii.unhexlify(trigger_hex_new()).decode('utf-8')
    assert gobject_json.extract_object(json_str) == expected
