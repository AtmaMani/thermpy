"""Build the static site published to GitHub Pages.

Usage: uv run python scripts/build_site.py [output_dir]

Exports every marimo notebook in notebooks/ to <output_dir>/<notebook name>.html.
Notebooks are executed during export, so the output contains their rendered results.
notebooks/index.py is the landing page (index.html). It is a markdown-only notebook
maintained by hand, linking to the other notebooks as "<notebook name>.html".
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks"
INDEX_NOTEBOOK = "index"


def export_notebook(notebook: Path, out_dir: Path) -> Path:
    target = out_dir / f"{notebook.stem}.html"
    command = [
        sys.executable,
        "-m",
        "marimo",
        "export",
        "html",
        str(notebook),
        "-o",
        str(target),
    ]
    if notebook.stem == INDEX_NOTEBOOK:
        command.append("--no-include-code")
    subprocess.run(command, check=True)
    return target


def main() -> None:
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "_site").resolve()
    notebooks = sorted(NOTEBOOK_DIR.glob("*.py"))
    if INDEX_NOTEBOOK not in {nb.stem for nb in notebooks}:
        sys.exit(f"Missing {NOTEBOOK_DIR / 'index.py'}")

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / ".nojekyll").touch()

    for notebook in notebooks:
        print(f"Exporting {notebook.name}")
        export_notebook(notebook, out_dir)

    # Catch links in the hand-written index that point at a missing page.
    index = (NOTEBOOK_DIR / "index.py").read_text(encoding="utf-8")
    for notebook in notebooks:
        if notebook.stem != INDEX_NOTEBOOK and f"{notebook.stem}.html" not in index:
            print(f"Warning: notebooks/index.py does not link to {notebook.stem}.html")
    print(f"Site written to {out_dir}")


if __name__ == "__main__":
    main()
