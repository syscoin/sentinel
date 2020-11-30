import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from syscoin_config import SyscoinConfig


@pytest.fixture
def syscoin_conf(**kwargs):
    defaults = {
        'rpcuser': 'syscoinrpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    syscoin_config = syscoin_conf()
    creds = SyscoinConfig.get_rpc_creds(syscoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'syscoinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    syscoin_config = syscoin_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = SyscoinConfig.get_rpc_creds(syscoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'syscoinrpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', syscoin_conf(), re.M)
    creds = SyscoinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'syscoinrpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 18370


def test_slurp_config_file():
    import tempfile

    syscoin_config = """# basic settings
#testnet=1 # TESTNET
server=1
printtoconsole=1
"""

    expected_stripped_config = """server=1
printtoconsole=1
"""

    with tempfile.NamedTemporaryFile(mode='w') as temp:
        temp.write(syscoin_config)
        temp.flush()
        conf = SyscoinConfig.slurp_config_file(temp.name)
        assert conf == expected_stripped_config
