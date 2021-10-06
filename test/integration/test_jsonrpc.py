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
    genesis_hash = u'0000022642db0346b6e01c2a397471f4f12e65d4f4251ec96c1f85367a61a7ab'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000066e1a6b9cfeac8295dce0cc8d9170690a74bc4878cf8a0b412554f5c222'

    creds = SyscoinConfig.get_rpc_creds(config_text, network)
    syscoind = SyscoinDaemon(**creds)
    assert syscoind.rpc_command is not None

    assert hasattr(syscoind, 'rpc_connection')

    # test commands without arguments
    info = syscoind.rpc_command('getblockchaininfo')
    info_keys = [
        'chain',
        'blocks',
        'headers',
        'difficulty'
    ]
    for key in info_keys:
        assert key in info
    assert info['chain'] == ("test" if is_testnet else "main")

    # test commands with args
    assert syscoind.rpc_command('getblockhash', 0) == genesis_hash
