import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.align import Align
from service import InventoryService

console = Console()
service = InventoryService()

def show_header():
    console.print(Align.center(
        Panel.fit(" Food Inventory Manager ", border_style="magenta", width=60)
    ))

def show_menu():
    # Left-aligned menu options, no spacing
    menu_text = (
        "[bold cyan]1.[/] View Inventory Items\n"
        "[bold cyan]2.[/] Add New Item Manually\n"
        "[bold cyan]3.[/] Update Item\n"
        "[bold cyan]4.[/] Delete Item\n"
        "[bold cyan]5.[/] Search Product on OpenFoodFacts\n"
        "[bold cyan]6.[/] Exit"
    )
    console.print(Panel(menu_text, title="[green]Main Menu[/]", border_style="magenta", width=60, padding=(0,1)))

def display_items(items):
    if not items:
        console.print(Align.center("[yellow]No items in your inventory yet![/]"))
        return

    table = Table(title="Inventory Items", border_style="magenta")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Price", justify="right", style="yellow")
    table.add_column("Quantity", justify="center", style="magenta")

    for item in items:
        table.add_row(str(item["id"]), item["name"], f"${item['price']:.2f}", str(item["quantity"]))

    console.print(Align.center(table))

def user_add_item():
    console.print(Align.center(Panel("✨ Add a New Item ✨", border_style="cyan", width=50)))
    name = Prompt.ask("Enter item name")
    price = float(Prompt.ask("Enter item price (use 0 if unknown)"))
    quantity = int(Prompt.ask("Enter item quantity"))
    added = service.add_item({"name": name, "price": price, "quantity": quantity})
    console.print(Align.center(f"[green]Item added successfully:[/] {added}"))

def user_update_item():
    console.print(Align.center(Panel("Update an Item ", border_style="cyan", width=50)))
    item_id = int(Prompt.ask("Enter the ID of the item to update"))
    item = service.get_item(item_id)
    if item:
        console.print(f"Current Name: {item['name']}, Price: ${item['price']:.2f}, Quantity: {item['quantity']}")
        name = Prompt.ask("Enter new name (leave blank to keep current)", default=item['name'])
        price_input = Prompt.ask("Enter new price (leave blank to keep current)", default=str(item['price']))
        quantity_input = Prompt.ask("Enter new quantity (leave blank to keep current)", default=str(item['quantity']))
        updated = service.update_item(item_id, {
            "name": name,
            "price": float(price_input),
            "quantity": int(quantity_input)
        })
        console.print(Align.center(f"[green]Item updated successfully:[/] {updated}"))
    else:
        console.print(Align.center(f"[red]Item {item_id} not found[/]"))

def user_delete_item():
    console.print(Align.center(Panel("Delete an Item", border_style="red", width=50)))

    items = service.get_items()
    if not items:
        console.print(Align.center("[yellow]No items available to delete[/]"))
        return

    display_items(items)

    try:
        item_id = int(Prompt.ask("Enter the ID of the item to delete"))
    except ValueError:
        console.print(Align.center("[red]Invalid input! Please enter a valid number for ID[/]"))
        return

    if service.delete_item(item_id):
        console.print(Align.center(f"[green]Item {item_id} deleted successfully[/]"))
    else:
        console.print(Align.center(f"[red]Item with ID {item_id} not found in inventory[/]"))

def user_search_product():
    console.print(Align.center(Panel("🔎 Search Product on OpenFoodFacts 🔎", border_style="yellow", width=60)))
    query = Prompt.ask("Enter product name (e.g., 'Almond Milk')")
    product = service.fetch_product(query)

    if product and "error" not in product:
        ingredients = product.get("ingredients", "No ingredient info (might not be a food item)")
        panel_text = (
            f"[bold green]Name:[/] {product.get('name', 'Unknown')}\n"
            f"[bold blue]Brand:[/] {product.get('brand', 'Unknown')}\n"
            f"[bold yellow]Ingredients:[/] {ingredients}"
        )
        console.print(Align.center(Panel(panel_text, border_style="yellow", width=70)))

        save = Prompt.ask("Would you like to add this product to your inventory? (yes/no)").lower()
        if save == "yes":
            added = service.add_item({
                "name": product.get("name", "Unknown"),
                "price": 0,
                "quantity": 1
            })
            console.print(Align.center(f"[green] Added to inventory:[/] {added}"))
        else:
            console.print(Align.center("[cyan] Product not added to inventory[/]"))
    else:
        console.print(Align.center("[red]Product not found on OpenFoodFacts[/]"))

#looping
while True:
    console.clear()
    show_header()
    show_menu()
    choice = Prompt.ask("Select an option (1-6)")

    if choice == "1":
        display_items(service.get_items())
    elif choice == "2":
        user_add_item()
    elif choice == "3":
        user_update_item()
    elif choice == "4":
        user_delete_item()
    elif choice == "5":
        user_search_product()
    elif choice == "6":
        console.print(Align.center("[cyan]Exiting Inventory Manager... Goodbye![/]"))
        break
    else:
        console.print(Align.center("[red]Invalid choice, please enter a number from 1 to 6[/]"))

    input("\nPress Enter to continue...")