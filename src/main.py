from rich.console import Console
from rich.prompt import Prompt
from irandade.validator import run_meta_validation
from irandade.display import show_concepts, show_measurement_units, show_dimensions, show_indicator, show_series
from irandade.time_lookup import lookup_and_show

console = Console()


def menu_validate():
    console.print("\n[bold]Validate:[/bold]")
    console.print("  1) meta [bold yellow]m[/bold yellow]")
    console.print("  2) data [bold yellow]d[/bold yellow]")
    sub = Prompt.ask("Choice").strip().lower()
    if sub in ("1", "m"):
        run_meta_validation()
    elif sub in ("2", "d"):
        console.print("[yellow]validate data: not implemented[/yellow]")


def menu_show():
    console.print("\n[bold]Show:[/bold]")
    console.print("  1) concept [bold yellow]c[/bold yellow]")
    console.print("  2) measure [bold yellow]m[/bold yellow]")
    console.print("  3) dimension [bold yellow]d[/bold yellow]")
    console.print("  4) indicator [bold yellow]i[/bold yellow]")
    console.print("  5) series [bold yellow]s[/bold yellow]")
    sub = Prompt.ask("Choice").strip().lower()
    if sub in ("1", "c"):
        show_concepts()
    elif sub in ("2", "m"):
        show_measurement_units()
    elif sub in ("3", "d"):
        show_dimensions()
    elif sub in ("4", "i"):
        show_indicator()
    elif sub in ("5", "s"):
        show_series()


def menu_time():
    console.print("\n[bold]Calendar:[/bold]")
    console.print("  1) Gregorian [bold yellow]g[/bold yellow]")
    console.print("  2) Jalali [bold yellow]j[/bold yellow]")
    cal_sub = Prompt.ask("Choice").strip().lower()
    if cal_sub in ("1", "g"):
        calendar = "gregorian"
    elif cal_sub in ("2", "j"):
        calendar = "jalali"
    else:
        console.print("[red]Invalid choice[/red]")
        return

    date_str = Prompt.ask("Enter date [bold](yyyy or yyyy/mm or yyyy/mm/dd)[/bold]").strip()
    parts = date_str.split("/")
    if len(parts) not in (1, 2, 3):
        console.print("[red]Invalid format. Use yyyy or yyyy/mm or yyyy/mm/dd[/red]")
        return
    try:
        nums = [int(p) for p in parts]
    except ValueError:
        console.print("[red]Invalid number in date[/red]")
        return
    lookup_and_show(calendar, *nums)


def main():
    while True:
        console.print("\n[bold]Select an option:[/bold]")
        console.print("  1) validate [bold yellow]v[/bold yellow]")
        console.print("  2) show [bold yellow]s[/bold yellow]")
        console.print("  3) time [bold yellow]t[/bold yellow]")
        console.print("  [bold yellow]q[/bold yellow]uit")
        choice = Prompt.ask("Choice", default="q").strip().lower()

        if choice in ("1", "v"):
            menu_validate()
        elif choice in ("2", "s"):
            menu_show()
        elif choice in ("3", "t"):
            menu_time()
        elif choice in ("q", "quit", "exit"):
            break


if __name__ == "__main__":
    main()
