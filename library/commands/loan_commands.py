import click
from rich.console import Console
from library.services.loan_service import LoanService
from library.services.book_service import BookService
from library.services.person_service import PersonService

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def loans(ctx):
    """
    Manage book loans.
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(list_loans)

@loans.command()
@click.argument('book_id', type=int)
@click.argument('person_id', type=int)
@click.pass_context
def borrow(ctx, book_id: int, person_id: int):
    """
    Lends a book to a person.
    
    Args:
        book_id: The ID of the book to be lent.
        person_id: The ID of the person borrowing the book.
    """
    loan_service: LoanService = ctx.obj['loan_service']
    try:
        loan = loan_service.lend_book(book_id, person_id)
        console.print(f"[green]Successfully lent book (ID: [bold]{loan.book_id}[/bold]) to person (ID: [bold]{loan.person_id}[/bold]).[/green]")
        console.print(f"  [yellow]Loan ID:[/] {loan.id}")
        console.print(f"  [yellow]Due date:[/] {loan.due_date.strftime('%Y-%m-%d')}")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)

@loans.command(name='return')
@click.argument('book_id', type=int)
@click.pass_context
def return_book(ctx, book_id: int):
    """
    Marks a book as returned.
    
    Args:
        book_id: The ID of the book being returned.
    """
    loan_service: LoanService = ctx.obj['loan_service']
    try:
        loan_service.return_book(book_id)
        console.print(f"[green]Successfully returned book with ID [bold]{book_id}[/bold].[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)
    
@loans.command(name='list')
@click.pass_context
def list_loans(ctx):
    """
    Lists all current book loans.
    """
    loan_service: LoanService = ctx.obj['loan_service']
    loans = loan_service.loan_repository.get_all_loans()
    book_service = ctx.obj['book_service']
    person_service = ctx.obj['person_service']

    if not loans:
        console.print("[yellow]No books are currently on loan.[/yellow]")
        return

    console.print("\n[bold]Borrowing records[/bold] 📜")
    for loan in loans:
        book = book_service.get_book_by_id(loan.book_id)
        person = person_service.get_person_by_id(loan.person_id)
        
        book_title = book.title if book else "Unknown Book"
        person_name = person.name if person else "Unknown Person"
        
        console.print(f"  [cyan]Loan ID:[/] {loan.id} | [cyan]Book:[/] {book_title} | [cyan]Borrower:[/] {person_name} | [cyan]Due Date:[/] {loan.due_date.strftime('%Y-%m-%d')}")

@loans.command()
@click.argument('person_id', type=int)
@click.pass_context
def list_by_person(ctx, person_id: int):
    """
    Lists all loans for a specific person.
    
    Args:
        person_id: The ID of the person.
    """
    loan_service: LoanService = ctx.obj['loan_service']
    book_service = ctx.obj['book_service']
    person_service = ctx.obj['person_service']

    person = person_service.get_person_by_id(person_id)
    if not person:
        console.print(f"[red]Error: Person with ID '{person_id}' not found.[/red]", err=True)
        return

    loans = loan_service.loan_repository.get_loans_by_person_id(person_id)
    if not loans:
        console.print(f"[yellow]{person.name} has no books currently on loan.[/yellow]")
        return
    
    console.print(f"\n[bold]Borrowing records for {person.name}[/bold] 📜")
    for loan in loans:
        book = book_service.get_book_by_id(loan.book_id)
        book_title = book.title if book else "Unknown Book"
        
        console.print(f"  [cyan]Loan ID:[/] {loan.id} | [cyan]Book:[/] {book_title} | [cyan]Due Date:[/] {loan.due_date.strftime('%Y-%m-%d')}")