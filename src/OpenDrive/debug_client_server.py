from multiprocessing import Process
import networking as net

import OpenDrive.client_side.net_start
import OpenDrive.server_side.net_start
from OpenDrive.client_side.authentication import register_user_device_cli


def debug_client_routine():
    client_net = OpenDrive.client_side.net_start
    client_net.connect()
    register_user_device_cli()
    client_net.close_connection()


def debug_server_routine():
    server_net = OpenDrive.server_side.net_start
    server_net.start()
    net.ClientManager().mainloop()


if __name__ == '__main__':
    server_process = Process(target=debug_server_routine)
    server_process.start()

    debug_client_routine()

    server_process.kill()

