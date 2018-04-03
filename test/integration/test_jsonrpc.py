import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from syscoind import SyscoinDaemon
from syscoin_config import SyscoinConfig


def test_syscoind():
    config_text = SyscoinConfig.slurp_config_file(config.syscoin_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'0000006086e066c3e9df26340d6324982c031e1e8d37f66c2f4cb5d76a3db7da'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000d070aa618e6549464d948b37e92df680312a38e22f4c14fa9e0c3ab494f'

    creds = SyscoinConfig.get_rpc_creds(config_text, network)
    syscoind = SyscoinDaemon(**creds)
    assert syscoind.rpc_command is not None

    assert hasattr(syscoind, 'rpc_connection')

    # Syscoin testnet block 0 hash == 00000790e2439c71e102414f0c42b1107ac1fd661b802577f502cc0720d86e73
    # test commands without arguments
    info = syscoind.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert syscoind.rpc_command('getblockhash', 0) == genesis_hash
