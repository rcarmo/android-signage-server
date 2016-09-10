from django.db.backends.signals import connection_created

def activate_wal(sender, connection, **kwargs):
    """Enable WAL mode."""
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute('PRAGMA journal_mode=WAL;')

connection_created.connect(activate_wal)