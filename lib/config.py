"""
    Set up defaults and read sentinel.conf
"""
import sys
import os
import re
import datetime
from syscoin_config import SyscoinConfig
from poda_payload import PoDAPayload

default_sentinel_config = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '../sentinel.conf')
)
sentinel_config_file = os.environ.get('SENTINEL_CONFIG', default_sentinel_config)
sentinel_cfg = SyscoinConfig.tokenize(sentinel_config_file)
sentinel_version = "1.5.0"


std_print = print

def print(*args, **kwargs):
    std_print(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), *args, **kwargs)

# event handler for SENTINEL_DEBUG not registered yet, so simulate it
def printdbg(*args, **kwargs):
    if os.environ.get('SENTINEL_DEBUG', None):
        std_print(datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"), *args, **kwargs)


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
        printdbg("No .env file found")
        printdbg("Defaulting to preset environment variables...")
    except IOError as e:
        print(f"Error reading .env file: {e}")


def get_syscoin_conf():
    if sys.platform == 'win32':
        syscoin_conf = os.path.join(os.getenv('APPDATA'), "Syscoin/syscoin.conf")
    else:
        home = os.environ.get('HOME')

        syscoin_conf = os.path.join(home, ".syscoin/syscoin.conf")
        if sys.platform == 'darwin':
            syscoin_conf = os.path.join(home, "Library/Application Support/Syscoin/syscoin.conf")

    syscoin_conf = sentinel_cfg.get('syscoin_conf', syscoin_conf)

    return syscoin_conf


def get_network():
    envNetwork = os.environ.get('NETWORK', '')
    if envNetwork != '':
        return envNetwork
    return sentinel_cfg.get('network', 'mainnet')

def get_poda_db_account_id():
    return os.environ.get('PODA_DB_ACCOUNT_ID', '')

def get_poda_db_key_id():
    return os.environ.get('PODA_DB_KEY_ID', '')

def get_poda_db_access_key():
    return os.environ.get('PODA_DB_ACCESS_KEY', '')

def get_lighthouse_token():
    return os.environ.get('LIGHTHOUSE_TOKEN', '')

def get_rpchost():
    return sentinel_cfg.get('rpchost', '127.0.0.1')


def sqlite_test_db_name(sqlite_file_path):
    (root, ext) = os.path.splitext(sqlite_file_path)
    test_sqlite_file_path = root + '_test' + ext
    return test_sqlite_file_path


def get_db_conn():
    import peewee
    env = os.environ.get('SENTINEL_ENV', 'production')

    # default values should be used unless you need a different config for development
    db_host = sentinel_cfg.get('db_host', '127.0.0.1')
    db_port = sentinel_cfg.get('db_port', None)
    db_name = sentinel_cfg.get('db_name', 'sentinel')
    db_user = sentinel_cfg.get('db_user', 'sentinel')
    db_password = sentinel_cfg.get('db_password', 'sentinel')
    db_charset = sentinel_cfg.get('db_charset', 'utf8mb4')
    db_driver = sentinel_cfg.get('db_driver', 'sqlite')

    if (env == 'test'):
        if db_driver == 'sqlite':
            db_name = sqlite_test_db_name(db_name)
        else:
            db_name = "%s_test" % db_name

    peewee_drivers = {
        'mysql': peewee.MySQLDatabase,
        'postgres': peewee.PostgresqlDatabase,
        'sqlite': peewee.SqliteDatabase,
    }
    driver = peewee_drivers.get(db_driver)

    dbpfn = 'passwd' if db_driver == 'mysql' else 'password'
    db_conn = {
        'host': db_host,
        'user': db_user,
        dbpfn: db_password,
    }
    if db_port:
        db_conn['port'] = int(db_port)

    if driver == peewee.SqliteDatabase:
        db_conn = {}

    db = driver(db_name, **db_conn)

    return db

parse_env()
syscoin_conf = get_syscoin_conf()
network = get_network()
rpc_host = get_rpchost()
db = get_db_conn()
poda_db_account_id = get_poda_db_account_id()
poda_db_key_id = get_poda_db_key_id()
poda_db_access_key = get_poda_db_access_key()
lh_token =get_lighthouse_token()
if lh_token == '':
    printdbg("Lighthouse token not set.")
else :
    printdbg("Lighthouse token found.")
poda_payload = PoDAPayload(poda_db_account_id, poda_db_key_id, poda_db_access_key,lh_token)
