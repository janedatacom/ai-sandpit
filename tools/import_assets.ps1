<#
.SYNOPSIS
  Bulk copy (and optionally rename) image assets into a chapter assets directory.

.DESCRIPTION
  Designed to reduce manual drag/drop for this repo. Copies images from a source
  folder (or list of files) into a destination folder. Supports optional renaming
  to a sequential pattern suitable for slide exports.

.EXAMPLE
  # Copy all PNGs from Downloads into Chapter 6 activity assets (keep names)
  .\tools\import_assets.ps1 -Source "$env:USERPROFILE\Downloads" -Destination "Chapter06/Activities/assets"

.EXAMPLE
  # Copy and rename to slide-00-..., slide-01-..., starting at 0
  .\tools\import_assets.ps1 -Source "$env:USERPROFILE\Downloads\chapter6" -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2

.EXAMPLE
  # Dry run to see what would happen
  .\tools\import_assets.ps1 -Source ".\temp\slides" -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2 -WhatIf
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
  # Folder path or file path(s)
  [Parameter(Mandatory = $true, Position = 0)]
  [string[]]$Source,

  # Destination folder (created if missing)
  [Parameter(Mandatory = $true, Position = 1)]
  [string]$Destination,

  # Optional prefix for renaming. If omitted, original filenames are preserved.
  [Parameter(Mandatory = $false)]
  [string]$Prefix,

  # Starting index for renaming.
  [Parameter(Mandatory = $false)]
  [int]$Start = 1,

  # Number of digits to pad the index with.
  [Parameter(Mandatory = $false)]
  [ValidateRange(1, 6)]
  [int]$Pad = 2,

  # Optional suffix placed after the number (e.g. "overview" => slide-00-overview.png)
  [Parameter(Mandatory = $false)]
  [string]$Suffix,

  # Overwrite destination files if they already exist.
  [Parameter(Mandatory = $false)]
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-AbsPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  return (Resolve-Path -Path $Path).Path
}

$destinationPath = $Destination
if (-not (Test-Path -LiteralPath $destinationPath)) {
  if ($PSCmdlet.ShouldProcess($destinationPath, 'Create directory')) {
    New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null
  }
}
$destinationAbs = Resolve-AbsPath -Path $destinationPath

$extensions = @('.png', '.jpg', '.jpeg', '.gif', '.webp')

$sourceFiles = New-Object System.Collections.Generic.List[string]
foreach ($src in $Source) {
  if (Test-Path -LiteralPath $src -PathType Container) {
    $items = Get-ChildItem -LiteralPath $src -File -Recurse
    foreach ($item in $items) {
      if ($extensions -contains $item.Extension.ToLowerInvariant()) {
        $sourceFiles.Add($item.FullName)
      }
    }
    continue
  }

  if (Test-Path -LiteralPath $src -PathType Leaf) {
    $item = Get-Item -LiteralPath $src
    if ($extensions -contains $item.Extension.ToLowerInvariant()) {
      $sourceFiles.Add($item.FullName)
    }
    continue
  }

  throw "Source path not found: $src"
}

if ($sourceFiles.Count -eq 0) {
  Write-Warning 'No image files found to import.'
  exit 0
}

# Sort by name so the order is stable and predictable.
$sorted = $sourceFiles.ToArray() | Sort-Object

$index = $Start
foreach ($file in $sorted) {
  $item = Get-Item -LiteralPath $file
  $ext = $item.Extension.ToLowerInvariant()

  $destName = $item.Name
  if (-not [string]::IsNullOrWhiteSpace($Prefix)) {
    $num = $index.ToString("D$Pad")
    if ([string]::IsNullOrWhiteSpace($Suffix)) {
      $destName = "$Prefix-$num$ext"
    } else {
      $safeSuffix = $Suffix.Trim()
      $destName = "$Prefix-$num-$safeSuffix$ext"
    }
  }

  $destPath = Join-Path -Path $destinationAbs -ChildPath $destName

  $copyDesc = "Copy '$($item.FullName)' -> '$destPath'"
  if ($PSCmdlet.ShouldProcess($destPath, $copyDesc)) {
    Copy-Item -LiteralPath $item.FullName -Destination $destPath -Force:$Force
  }

  $index++
}

Write-Host "Imported $($sorted.Count) image(s) into: $destinationAbs" -ForegroundColor Green
