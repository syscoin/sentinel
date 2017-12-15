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
    genesis_hash = u'00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000080db17ee560bd9e8ece89d981820589a80455be965197d90e8a2641edbb'

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
