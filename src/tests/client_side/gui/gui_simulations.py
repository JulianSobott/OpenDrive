from OpenDrive.client_side.gui import main
from OpenDrive.client_side.gui import screens


def start_from_zero():
    main.main(screens.REGISTRATION)


if __name__ == '__main__':
    start_from_zero()