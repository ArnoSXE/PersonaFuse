from rich.console import Console

def generate(result):
    console = Console()
    console.rule("[bold cyan]PersonaFuse Report[/bold cyan]")
    console.print(f"[bold]Users:[/bold] {result['users'][0]} ↔ {result['users'][1]}")
    console.print(f"[bold]Stylometry Score:[/bold] {result['stylometry']}")
    console.print(f"[bold]Temporal Score:[/bold] {result.get('temporal', 'N/A')}")
    console.print(f"[bold]Final Confidence:[/bold] {result['confidence']}%")
    console.rule()
