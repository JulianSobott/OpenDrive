import signal
from multiprocessing import Process
import networking as net
import os

import OpenDrive.client_side.net_start
import OpenDrive.server_side.net_start


def debug_client_routine():
    client_net = OpenDrive.client_side.net_start
    client_net.connect()

    client_net.close_connection()


def debug_server_routine():
    server_net = OpenDrive.server_side.net_start
    server_net.start()
    net.ClientManager().mainloop()


if __name__ == '__main__':
    client_process = Process(target=debug_client_routine)
    client_process.start()
    server_process = Process(target=debug_server_routine)
    server_process.start()
    client_process.join()
    server_process.kill()

