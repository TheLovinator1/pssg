import os
from pathlib import Path

import mistune
import typer
from rich import print
from rich.progress import track

app = typer.Typer()

CONTENT_DIR: Path = Path(os.getenv("CONTENT_DIR", "content"))


def generate_html_from_markdown(markdown_file: Path, output_file: Path) -> Path:
    """Generate HTML from Markdown file."""
    with Path.open(markdown_file) as f:
        markdown: str = f.read()

    html: str = mistune.html(markdown)  # type: ignore  # noqa: PGH003
    if not html:
        msg = "Markdown file is empty."
        raise ValueError(msg)

    with Path.open(output_file, "w") as f:
        f.write(html)

    print(f"[green]Generated[/green] HTML file: {output_file}")
    return output_file


@app.command(name="build", help="Build static site.")
def build() -> None:
    """Build static site."""
    for file in track(CONTENT_DIR.glob("*.md"), description="Processing..."):
        output_file: Path = Path("public") / (file.stem + ".html")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # TODO: Only generate HTML if Markdown file has changed. Check timestamp?
        generate_html_from_markdown(file, output_file)


if __name__ == "__main__":
    app()
