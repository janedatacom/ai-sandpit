# Slide Generator (Azure OpenAI)

This folder includes a small script that uses your Azure OpenAI deployment to generate:

- `slides.json` (structured slide content)
- `slides.pptx` (rendered PowerPoint)

## Setup (no admin required)

From the repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r Chapter03\Activities\slidegen_requirements.txt
```

## Configure Azure OpenAI

### Option A (recommended): use a local `.env`

1) Copy the template:

```powershell
Copy-Item Chapter03\Activities\.env.example Chapter03\Activities\.env
```

2) Edit `Chapter03/Activities/.env` and fill in values.

Note: `generate_slides.py` will also load `Chapter03/Activities/assets/.env` if you accidentally put it there.

This repo already ignores `.env` in `.gitignore`, so it won’t be checked in.

### Option B: set environment variables in PowerShell

Set these environment variables (PowerShell):

```powershell
$env:AZURE_OPENAI_ENDPOINT = "https://<your-resource-name>.openai.azure.com"
$env:AZURE_OPENAI_API_KEY = "<your-key>"
$env:AZURE_OPENAI_DEPLOYMENT = "<your-deployment-name>"
$env:AZURE_OPENAI_API_VERSION = "<your-api-version>"
```

## Run

```powershell
.\.venv\Scripts\python Chapter03\Activities\generate_slides.py
```

Outputs:

- `Chapter03/Activities/slides.json`
- `Chapter03/Activities/slides.pptx`

## Notes

- The generator reads `CHAPTER03_ACTIVITY01.md` by default.
- If a slide’s `suggested_asset_filename` exists under `Chapter03/Activities/assets`, the PPTX generator will embed that image as a full-slide background.
- You can override paths and Azure settings with CLI flags; run:

```powershell
.\.venv\Scripts\python Chapter03\Activities\generate_slides.py -h
```
