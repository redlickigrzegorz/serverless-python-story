import os
import typing


def build_sqlalchemy_url(database_name: typing.Optional[str] = None) -> str:
    """
    This function returns the database url which is built from environment variables.
    The database name argument allows to change the name of the database (useful for tests).
    """
    try:
        return 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            host=os.environ.get('POSTGRES_HOST', 'database'),
            port=os.environ.get('POSTGRES_PORT', 5432),
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            database=database_name if database_name else os.environ['POSTGRES_DB'],
        )
    except KeyError:
        raise RuntimeError('Database credentials must be specified in environment variables!')
