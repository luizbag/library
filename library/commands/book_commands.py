import click
import csv
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
    book_service: BookService = ctx.obj['book_service']
    all_books = book_service.get_all_books()

    if not all_books:
        console.print("[yellow]No books found. Add some first![/yellow]")
        return

    console.print("\n[bold]📚 Library Books[/bold]")
    for book in all_books:
        status = "[green]Available[/green]" if book.is_available else "[red]On Loan[/red]"
        console.print(f"  [cyan]ID:[/] {book.id} | [cyan]Title:[/] {book.title} | [cyan]Author:[/] {book.author} | [cyan]ISBN:[/] {book.isbn} | [cyan]Status:[/] {status}")


@books.command()
@click.argument('query')
@click.pass_context
def search(ctx, query: str):
    """
    Searches for books by title or author.
    """
    book_service: BookService = ctx.obj['book_service']
    results = book_service.search_books(query)

    if not results:
        console.print(f"[yellow]No books found matching '{query}'.[/yellow]")
        return

    console.print(f"\n[bold]🔍 Search Results for '{query}'[/bold]")
    for book in results:
        status = "[green]Available[/green]" if book.is_available else "[red]On Loan[/red]"
        console.print(f"  [cyan]ID:[/] {book.id} | [cyan]Title:[/] {book.title} | [cyan]Author:[/] {book.author} | [cyan]ISBN:[/] {book.isbn} | [cyan]Status:[/] {status}")

@books.command()
@click.argument('isbn')
@click.pass_context
def get(ctx, isbn: str):
    """
    Retrieves a book by its ISBN.
    """
    book_service: BookService = ctx.obj['book_service']
    book = book_service.get_book_by_isbn(isbn)

    if book:
        status = "Available" if book.is_available else "On Loan"
        console.print("\n[bold]🔍 Found Book[/bold]")
        console.print(f"  [cyan]ID:[/] {book.id}")
        console.print(f"  [cyan]Title:[/] {book.title}")
        console.print(f"  [cyan]Author:[/] {book.author}")
        console.print(f"  [cyan]ISBN:[/] {book.isbn}")
        console.print(f"  [cyan]Status:[/] {status}")
    else:
        console.print(f"[yellow]No book found with ISBN '{isbn}'.[/yellow]")

@books.command()
@click.argument('csv_file', type=click.Path(exists=True))
@click.pass_context
def import_csv(ctx, csv_file: str):
    """
    Imports books from a CSV file.
    CSV file must have headers: title, author, isbn
    """
    book_service = ctx.obj["book_service"]
    imported_count=0
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        console.print(f"[bold]Importing books from '{csv_file}'...[/bold]")
        
        for row in reader:
            try:
                title = row['title']
                author = row['author']
                isbn = row['isbn']
                
                book_service.add_new_book(title, author, isbn)
                imported_count += 1
                console.print(f"[green]✔[/green] Added '{title}' by {author} with ISBN {isbn}")
            
            except KeyError:
                console.print("[red]Error: Invalid CSV format. Missing one of the required headers (title, author, isbn).[/red]", err=True)
                return
            except ValueError as e:
                console.print(f"[yellow]✖[/yellow] Skipped '{title}': [red]{e}[/red]", err=True)
            except Exception as e:
                console.print(f"[red]An unexpected error occurred: {e}[/red]", err=True)
    
    console.print(f"\n[bold green]Import complete! Successfully imported {imported_count} book(s).[/bold green]")

