import click
from rich.console import Console
from library.services.person_service import PersonService

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
def people(ctx):
    """
    Manage people (borrowers) in the library.
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(list_people)

@people.command()
@click.argument('name')
@click.argument('phone_number')
@click.pass_context
def add(ctx, name: str, phone_number: str):
    """
    Adds a new person to the library.
    """
    person_service: PersonService = ctx.obj['person_service']
    try:
        new_person = person_service.add_new_person(name, phone_number)
        console.print(f"[green]Successfully added person: '{new_person.name}'[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)

@people.command(name='list')
@click.pass_context
def list_people(ctx):
    """
    Lists all people in the library.
    """
    person_service: PersonService = ctx.obj['person_service']
    all_people = person_service.get_all_people()

    if not all_people:
        console.print("[yellow]No people registered. Add some first![/yellow]")
        return

    console.print("\n[bold]👥 Registered People[/bold]")
    for person in all_people:
        console.print(f"  [cyan]ID:[/] {person.id} | [cyan]Name:[/] {person.name} | [cyan]Phone:[/] {person.phone_number}")


@people.command()
@click.argument('name')
@click.pass_context
def get(ctx, name: str):
    """
    Retrieves a person by their name.
    """
    person_service: PersonService = ctx.obj['person_service']
    try:
        person = person_service.get_person_by_name(name)
        if person:
            console.print("\n[bold]🔍 Found Person[/bold]")
            console.print(f"  [cyan]ID:[/] {person.id}")
            console.print(f"  [cyan]Name:[/] {person.name}")
            console.print(f"  [cyan]Phone:[/] {person.phone_number}")
        else:
            console.print(f"[yellow]No person found with name '{name}'.[/yellow]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)

@people.command()
@click.argument('old_name')
@click.option('--new-name', '-n', help="The new name for the person.")
@click.option('--new-phone', '-p', help="The new phone number for the person.")
@click.pass_context
def edit(ctx, old_name: str, new_name: str, new_phone: str):
    """
    Edits a person's name and/or phone number.
    """
    person_service: PersonService = ctx.obj['person_service']
    if not new_name and not new_phone:
        console.print("[red]Error: You must provide either a new name or a new phone number.[/red]", err=True)
        return

    try:
        person_service.update_person(old_name, new_name, new_phone)
        console.print(f"[green]Successfully updated details for '{old_name}'.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]", err=True)

@people.command()
@click.argument('query')
@click.pass_context
def search(ctx, query: str):
    """
    Searches for people by name or phone number.
    """
    person_service: PersonService = ctx.obj['person_service']
    results = person_service.search_people(query)

    if not results:
        console.print(f"[yellow]No people found matching '{query}'.[/yellow]")
        return

    console.print(f"\n[bold]🔍 Search Results for '{query}'[/bold]")
    for person in results:
        console.print(f"  [cyan]ID:[/] {person.id} | [cyan]Name:[/] {person.name} | [cyan]Phone:[/] {person.phone_number}")
