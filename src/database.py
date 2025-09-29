import sqlite3
from contextlib import closing

DATABASE_URL = "/app/data/astrago.db"


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DATABASE_URL)


def create_table():
    """Creates the 'links' table if it doesn't already exist."""
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    url TEXT NOT NULL
                );
                """
            )
            conn.commit()


def add_link(name: str, url: str) -> bool:
    """Adds a new shortlink to the database.

    Args:
        name: The short name for the link.
        url: The destination URL.

    Returns:
        True if the link was added successfully, False otherwise.
    """
    try:
        with closing(get_db_connection()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("INSERT INTO links (name, url) VALUES (?, ?)", (name, url))
                conn.commit()
        return True
    except sqlite3.IntegrityError:
        # This happens if the name is not unique
        return False


def delete_link(name: str) -> bool:
    """Deletes a shortlink from the database.

    Args:
        name: The short name of the link to delete.

    Returns:
        True if a link was deleted, False otherwise.
    """
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("DELETE FROM links WHERE name = ?", (name,))
            conn.commit()
            return cursor.rowcount > 0


def rename_link(old_name: str, new_name: str) -> bool:
    """Renames a shortlink.

    Args:
        old_name: The current name of the link.
        new_name: The new name for the link.

    Returns:
        True if the link was renamed successfully, False otherwise.
    """
    try:
        with closing(get_db_connection()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("UPDATE links SET name = ? WHERE name = ?", (new_name, old_name))
                conn.commit()
                return cursor.rowcount > 0
    except sqlite3.IntegrityError:
        return False


def get_link(name: str) -> str | None:
    """Retrieves the destination URL for a given shortlink.

    Args:
        name: The short name of the link.

    Returns:
        The destination URL if found, otherwise None.
    """
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT url FROM links WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None


def get_all_links() -> list[dict]:
    """Retrieves all links from the database.

    Returns:
        A list of dictionaries, where each dictionary represents a link.
    """
    with closing(get_db_connection()) as conn:
        conn.row_factory = sqlite3.Row
        with closing(conn.cursor()) as cursor:
            cursor.execute("SELECT id, name, url FROM links ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]


def update_link_url(name: str, new_url: str) -> bool:
    """Updates the URL of an existing shortlink.

    Args:
        name: The name of the link to update.
        new_url: The new destination URL.

    Returns:
        True if the link was updated successfully, False otherwise.
    """
    with closing(get_db_connection()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute("UPDATE links SET url = ? WHERE name = ?", (new_url, name))
            conn.commit()
            return cursor.rowcount > 0
