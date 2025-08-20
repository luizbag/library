import click
from .data.database_manager import DatabaseManager
from .data.book_repository import BookRepository
from .data.person_repository import PersonRepository
from .services.book_service import BookService
from .services.person_service import PersonService

# Import the command groups
from .commands.book_commands import books
from .commands.person_commands import people

@click.group()
@click.option('--db-path', default=None, help='Path to the database file.')
@click.pass_context
def cli(ctx, db_path: str):
    """
    A command-line application to manage your personal library.
    """
    ctx.ensure_object(dict)
    
    # Initialize the DatabaseManager (it's a singleton)
    db_manager = DatabaseManager(db_path=db_path)
    
    # Initialize all repositories
    book_repo = BookRepository(db_manager)
    # loan_repo = LoanRepository(db_manager)
    person_repo = PersonRepository(db_manager)
    
    # Initialize all services with their repositories
    book_service = BookService(book_repo)
    # loan_service = LoanService(loan_repo)
    person_service = PersonService(person_repo)
    
    # Store shared objects in the context for subcommands to access
    ctx.obj['db_manager'] = db_manager
    ctx.obj['book_service'] = book_service
    ctx.obj['person_service'] = person_service
    # Store other services here
    
    # Register the close method to be called when the CLI command finishes
    ctx.call_on_close(db_manager.close_connection)

# Add the command groups to the main CLI group
cli.add_command(books)
cli.add_command(people)
# cli.add_command(loans)