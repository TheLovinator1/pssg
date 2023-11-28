from pathlib import Path

import mistune
from loguru import logger


def generate_html_from_markdown(markdown_file: Path, output_file: Path) -> Path:
    """Generate HTML from Markdown file.

    Args:
        markdown_file: Path to Markdown file.
        output_file: Path to output HTML file.

    Returns:
        Path: Path to output HTML file.
    """
    # TODO: Only generate HTML if Markdown file has changed. Check timestamp?
    with Path.open(markdown_file) as f:
        markdown: str = f.read()
    html: str = mistune.html(markdown)  # type: ignore  # noqa: PGH003
    if not html:
        msg = "Markdown file is empty."
        raise ValueError(msg)

    with Path.open(output_file, "w") as f:
        f.write(html)

    logger.debug(f"Generated HTML file: {output_file}")
    return output_file


if __name__ == "__main__":
    content_dir = Path("content")
    for file in content_dir.glob("*.md"):
        output_file: Path = Path("public") / (file.stem + ".html")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        generate_html_from_markdown(file, output_file)
