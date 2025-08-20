import click
from rich.console import Console

from ..services.book_service import BookService

# Initialize the rich console for nice output formatting
console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def books(ctx):
    """
    Manage books in the library.
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(list_books)


@books.command()
@click.argument('title')
@click.argument('author')
@click.argument('isbn')
@click.pass_context
def add(ctx, title: str, author: str, isbn: str):
    """
    Adds a new book to the library.
    """
    book_service = ctx.obj['book_service']
    try:
        new_book = book_service.add_new_book(title, author, isbn)
        console.print(f"[green]Successfully added book: '{new_book.title}' by {new_book.author}.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)


@books.command(name='list')
@click.pass_context
def list_books(ctx):
    """
    Lists all books in the library.
    """
    book_service = ctx.obj['book_service']
    all_books = book_service.get_all_books()

    if not all_books:
        console.print("[yellow]The library is empty. Add some books first![/yellow]")
        return

    console.print("\n[bold]📚 Your Library[/bold]")
    for book in all_books:
        status_color = "green" if book.is_available else "yellow"
        availability = "Available" if book.is_available else "Borrowed"
        console.print(f"  [cyan]Title:[/] {book.title} | [cyan]Author:[/] {book.author} | [cyan]ISBN:[/] {book.isbn} | [cyan]Status:[/] [{status_color}]{availability}[/]")

@books.command()
@click.argument('search_term')
@click.pass_context
def search(ctx, search_term: str):
    """
    Searches for books by title.
    """
    book_service = ctx.obj['book_service']
    try:
        found_books = book_service.search_books_by_title(search_term)
        if not found_books:
            console.print(f"[yellow]No books found with the title '{search_term}'.[/yellow]")
            return

        console.print(f"\n[bold]🔍 Found Books for '{search_term}'[/bold]")
        for book in found_books:
            status_color = "green" if book.is_available else "yellow"
            availability = "Available" if book.is_available else "Borrowed"
            console.print(f"  [cyan]Title:[/] {book.title} | [cyan]Author:[/] {book.author} | [cyan]ISBN:[/] {book.isbn} | [cyan]Status:[/] [{status_color}]{availability}[/]")
            
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)

# my_books/cli_commands/books.py
# ... (rest of the file) ...

@books.command()
@click.argument('isbn')
@click.pass_context
def isbn(ctx, isbn: str):
    """
    Retrieves a book by its ISBN.
    """
    book_service = ctx.obj['book_service']
    try:
        book = book_service.get_book_by_isbn(isbn)
        if book:
            status_color = "green" if book.is_available else "yellow"
            availability = "Available" if book.is_available else "Borrowed"
            console.print("\n[bold]🔍 Found Book[/bold]")
            console.print(f"  [cyan]Title:[/] {book.title}")
            console.print(f"  [cyan]Author:[/] {book.author}")
            console.print(f"  [cyan]ISBN:[/] {book.isbn}")
            console.print(f"  [cyan]Status:[/] [{status_color}]{availability}[/]")
        else:
            console.print(f"[yellow]No book found with ISBN '{isbn}'.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)