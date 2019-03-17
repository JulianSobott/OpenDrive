import OpenDrive.client_side.net_start
import OpenDrive.server_side.net_start

if __name__ == '__main__':
    OpenDrive.client_side.net_start.connect()
    OpenDrive.server_side.net_start.start()
