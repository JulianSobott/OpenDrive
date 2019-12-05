"""
:module: OpenDrive.client_side.program_state
:synopsis: Global program states
:author: Julian Sobott

"""

#: Requests should only be made when this is True
is_authenticated_at_server = False

def set_authenticated_at_server(value: bool):
    global is_authenticated_at_server
    is_authenticated_at_server = value

def wait_till_authenticated_at_server():
    pass

