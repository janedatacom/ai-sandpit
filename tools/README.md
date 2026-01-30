# Tools

## import_assets.ps1

Bulk copy screenshots/slide exports into an `assets` folder.

Examples:

- Copy (keep filenames):

  `./tools/import_assets.ps1 -Source "$env:USERPROFILE\Downloads\chapter6" -Destination "Chapter06/Activities/assets"`

- Copy + auto-rename (sequential):

  `./tools/import_assets.ps1 -Source "$env:USERPROFILE\Downloads\chapter6" -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2`

- Dry run:

  `./tools/import_assets.ps1 -Source ".\temp\slides" -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2 -WhatIf`

## rename_assets.ps1

Rename generic pasted filenames like `image.png`, `image (1).png`, etc. into sequential names like `slide-00.png`, `slide-01.png`.

Examples:

- Rename anything in the folder that is not already `slide-XX.*`:

  `./tools/rename_assets.ps1 -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2`

- Rename only default `image*.png` style files:

  `./tools/rename_assets.ps1 -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2 -OnlyDefaultNames`

- Dry run:

  `./tools/rename_assets.ps1 -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2 -WhatIf`

## rename_assets_from_csv.ps1

Rename files using a simple CSV mapping (best when you want Chapter-2-style descriptive names).

1) Create a CSV (example: `.\temp\rename-map.csv`):

`from,to`

`image1.png,slide-00-overview.png`

`image2.png,slide-01-title.png`

2) Preview:

`./tools/rename_assets_from_csv.ps1 -Destination "Chapter06/Activities/assets" -MapFile ".\temp\rename-map.csv" -WhatIf`

3) Apply:

`./tools/rename_assets_from_csv.ps1 -Destination "Chapter06/Activities/assets" -MapFile ".\temp\rename-map.csv" -Force`
