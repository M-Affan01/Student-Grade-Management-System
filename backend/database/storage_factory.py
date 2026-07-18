"""
Storage Factory Module
=======================
Factory pattern for creating the appropriate storage backend.
Uses JSON file storage by default, with MySQL available when requested.


create_storage(storage_type, config):
    Factory function that creates and returns the appropriate storage backend.
"""


import os
from database.json_storage import JSONStorage


# Storage type constants
STORAGE_TYPE_JSON = "json"
STORAGE_TYPE_MYSQL = "mysql"


def create_storage(storage_type=None, config=None):
    """Factory function to create the appropriate storage backend.

    Determines which storage to use based on the provided type or the
    STORAGE_TYPE environment variable. Uses JSON by default. When MySQL is
    explicitly requested, falls back to JSON if MySQL is unavailable.

    Args:
        storage_type (str or None): The storage backend to create.
            Accepted values: 'mysql', 'json', or None (uses env var).
            If None, reads from STORAGE_TYPE env var, defaults to 'json'.
        config (dict or None): Configuration options for the storage backend.
            For MySQL: host, user, password, database, port.
            For JSON: filepath.
            Defaults to empty dict if None.

    Returns:
        JSONStorage or MySQLStorage: The initialized storage backend.

    Example:
        >>> storage = create_storage("json", {"filepath": "data/test.json"})
        >>> storage = create_storage("mysql")  # explicitly uses MySQL
        >>> storage = create_storage()  # defaults to JSON
    """
    if config is None:
        config = {}

    if storage_type is None:
        storage_type = os.environ.get("STORAGE_TYPE", STORAGE_TYPE_JSON)

    storage_type = storage_type.strip().lower()

    if storage_type == STORAGE_TYPE_MYSQL:
        try:
            from database.mysql_storage import MySQLStorage
            storage = MySQLStorage(
                host=config.get("host", "localhost"),
                user=config.get("user", "root"),
                password=config.get("password", ""),
                database=config.get("database", "student_grade_db"),
                port=config.get("port", 3306)
            )
            if storage.is_connected():
                print("Using MySQL storage")
                return storage
            else:
                print("MySQL not available, falling back to JSON storage")
        except Exception as e:
            print(f"MySQL error: {e}, falling back to JSON storage")

    filepath = config.get("filepath", "data/students.json")
    storage = JSONStorage(filepath=filepath)
    print(f"Using JSON storage: {filepath}")
    return storage
