import typer

app = typer.Typer()
validate_app = typer.Typer()
show_app = typer.Typer()

app.add_typer(validate_app, name="validate", help="Validate data files")
app.add_typer(show_app, name="show", help="Display seed data")


@validate_app.callback()
def validate_callback():
    pass


@validate_app.command("meta")
def validate_meta():
    """Validate all meta data against JSON schemas"""
    from irandade.validator import run_meta_validation
    success = run_meta_validation()
    raise typer.Exit(code=0 if success else 1)


@validate_app.command("data")
def validate_data():
    """Placeholder — no basic data validation implemented yet"""
    typer.echo("validate data: not implemented")


@show_app.callback()
def show_callback():
    pass


@show_app.command("concept")
def show_concept():
    """Display concepts in a table"""
    from irandade.display import show_concepts
    show_concepts()


@show_app.command("measure")
def show_measurement():
    """Display measurement units in a table"""
    from irandade.display import show_measurement_units
    show_measurement_units()


@show_app.command("dimension")
def show_dimension():
    """Display dimension classes and values in tables"""
    from irandade.display import show_dimensions
    show_dimensions()


@show_app.command("indicator")
def show_indicator_cmd():
    """Display indicators in a table"""
    from irandade.display import show_indicator
    show_indicator()


@show_app.command("series")
def show_series_cmd():
    """Display series in a table"""
    from irandade.display import show_series
    show_series()


app.add_typer(validate_app, name="v", hidden=True)
app.add_typer(show_app, name="s", hidden=True)
