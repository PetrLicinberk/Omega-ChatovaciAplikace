import src.server.server as s
from src.server import config
import src.server.db_connection as db

def main():
    config.get_config().read('config/server.ini')
    ip = config.get_str('server', 'ip', '127.0.0.1')
    port = config.get_int('server', 'port', 65525)
    timeout = config.get_int('server', 'timeout', 100)

    db_conn = db.get_instance()
    db_conn.address = config.get_str('database', 'ip', '127.0.0.1')
    db_conn.user = config.get_str('database', 'user', 'app')
    db_conn.password = config.get_str('database', 'password', '')
    db_conn.name = config.get_str('database', 'db_name', 'chat')
    server = s.Server(ip, port, timeout)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
if __name__ == '__main__':
    main()