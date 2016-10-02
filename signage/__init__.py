from django.db.backends.signals import connection_created

def activate_wal(sender, connection, **kwargs):
    """Enable WAL mode."""
    if 'sqlite' in connection.vendor:
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode=WAL;')
        cursor.execute('PRAGMA synchronous=OFF;')

connection_created.connect(activate_wal)