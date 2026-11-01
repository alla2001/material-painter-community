"""Adds a submission (the .zip made by Material Painter's Share to community)
to the library: unpacks it under items/<id>/ and adds its entry to index.json.

    python tools/add_item.py submission.zip [--author NAME] [--description TEXT] [--tags a,b]

The zip holds one folder <id>/ with info.json, the .mpgraph, thumb.png and
nodes/*.wgsl. Review the graph and any .wgsl nodes before committing.
"""
import argparse
import json
import pathlib
import shutil
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = {".mpgraph", ".wgsl", ".png", ".json"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zip")
    ap.add_argument("--author")
    ap.add_argument("--description")
    ap.add_argument("--tags")
    args = ap.parse_args()

    with zipfile.ZipFile(args.zip) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        info_name = next((n for n in names if n.endswith("info.json")), None)
        if not info_name:
            sys.exit("no info.json in the zip")
        info = json.loads(z.read(info_name))
        item_id = info["id"]
        prefix = info_name[: -len("info.json")]
        dest = ROOT / "items" / item_id
        if dest.exists():
            shutil.rmtree(dest)
        for n in names:
            rel = pathlib.PurePosixPath(n[len(prefix):])
            # Only the expected file types, and nothing that escapes the folder.
            if rel.suffix not in ALLOWED or ".." in rel.parts or rel.is_absolute():
                print(f"skipping {n}")
                continue
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(n))

    if args.author:
        info["author"] = args.author
    if args.description:
        info["description"] = args.description
    if args.tags:
        info["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
    info["path"] = f"items/{item_id}"

    index_path = ROOT / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    index["items"] = [i for i in index["items"] if i["id"] != item_id] + [info]
    index["items"].sort(key=lambda i: i["name"].lower())
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (dest / "info.json").unlink(missing_ok=True)
    print(f"added {info['name']} ({item_id}) with files: {info['files']}")
    print("Review the .wgsl and .mpgraph files, then commit and push.")


if __name__ == "__main__":
    main()
