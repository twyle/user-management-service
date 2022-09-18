"""Provide commands for starting the application, creating the database and seeding the database."""
from api import create_app
from flask.cli import FlaskGroup
from dotenv import load_dotenv
from api.helpers.helpers import seed_db_, create_db_

load_dotenv()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("create_db")
def create_db():
    """Create the database and all the tables."""
    create_db_()


@cli.command("seed_db")
def seed_db():
    """Seed the database."""

    seed_db_()


if __name__ == "__main__":
    cli()
