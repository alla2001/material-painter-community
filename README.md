# Material Painter community library

Smart materials, material graphs and custom nodes made by [Material Painter](https://github.com/alla2001/material-painter)
users. Everything here shows up inside the app under **Get more assets → Community**,
one click to download.

## Share your creation

1. In Material Painter, save it to the shelf:
   - a **smart material**: right-click a folder in Layers → **Save as smart material**;
   - a **graph**: Material Designer → **Save to shelf**.
2. Right-click it on the shelf → **Share to community…**
3. The app packs it (the file, its thumbnail and any custom nodes it uses) into a
   `.zip` and opens the submission form here. Attach the zip, add a short description
   and submit.

A maintainer checks it and adds it to the library, usually within a few days.

You can also open a pull request directly: add a folder under `items/<id>/` with the
files and an entry in `index.json` (see the format below), or run
`python tools/add_item.py <your.zip>` to do it for you.

## Rules

- **Only share your own work.** Everything here is released as **CC0** (public
  domain), so anyone can use it for anything, like the Poly Haven and ambientCG
  materials in the app.
- No textures or images you don't have the rights to.
- Custom nodes must be plain WGSL node files (no network access, nothing malicious;
  they're reviewed).

## Format

`index.json` lists every item:

```json
{
  "version": 1,
  "items": [
    {
      "id": "lava-crust",
      "name": "Lava Crust",
      "kind": "graph",
      "author": "your-name",
      "description": "Cooling lava with glowing cracks.",
      "tags": ["lava", "rock", "emissive"],
      "path": "items/lava-crust",
      "files": ["lava-crust.mpgraph", "nodes/crackle.wgsl"],
      "thumb": "thumb.png",
      "license": "CC0"
    }
  ]
}
```

- `kind`: `smart` (a `.mpsmart` smart material), `graph` (a `.mpgraph` material
  graph) or `node` (a single `.wgsl` node).
- `files` and `thumb` are relative to `path`. Graphs and nodes are plain text; a
  `.mpsmart` is a zip holding a readable `smart.json`, its images and a thumbnail,
  so everything can be reviewed and used without the app.
