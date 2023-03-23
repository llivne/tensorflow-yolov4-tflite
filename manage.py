import os

from flask.cli import FlaskGroup
from server import app


cli = FlaskGroup(app)


if __name__ == "__main__":
    if os.environ.get('FLASK_APP') is None:
        os.environ["FLASK_APP"] = "server/__init__.py"

    cli()
