from pyprofiling import profile
from OpenDrive import start_client

profile(start_client.main, globals(), "OpenDrive", "ClientSide_main")
