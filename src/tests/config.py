# Resources
FILE_SYSTEM = 2 << 1
NETWORK = 2 << 2
DATABASE = 2 << 3

ALL = FILE_SYSTEM | NETWORK | DATABASE
NONE = 0

# Test speed
FULL = NONE     # No resource is mocked
FAST = ALL  # All resources are mocked


def get_config():
    return FAST     # varying


def is_resource_mocked(resource):
    return get_config() & resource


log_names = {FILE_SYSTEM: "FILE_SYSTEM", NETWORK: "NETWORK", DATABASE: "DATABASE"}
