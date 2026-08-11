import typer
app = typer.Typer()

@app.command()
def learn(url: str) -> None:
    typer.echo(f"Learning from {url}")



if __name__ == "__main__":
    app()
