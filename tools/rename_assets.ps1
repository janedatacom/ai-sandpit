<#
.SYNOPSIS
  Rename default-named pasted images (e.g. image.png) to a sequential slide naming scheme.

.DESCRIPTION
  When copying/pasting screenshots into an assets folder, Windows/PowerPoint tools often
  create generic names like image.png, image (1).png, etc. This script renames those
  files to the next available sequence like slide-00.png, slide-01.png, ...

  It only renames files that do NOT already match the target pattern.

.EXAMPLE
  # Rename image*.png in Chapter 6 activity assets to slide-00.png, slide-01.png, ...
  .\tools\rename_assets.ps1 -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2

.EXAMPLE
  # Preview changes only
  .\tools\rename_assets.ps1 -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2 -WhatIf

.EXAMPLE
  # Rename based on 'image' base name only
  .\tools\rename_assets.ps1 -Destination "Chapter06/Activities/assets" -Prefix "slide" -Start 0 -Pad 2 -OnlyDefaultNames
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
  # Assets folder to rename files in
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$Destination,

  # Prefix used for renamed files (e.g., 'slide' -> slide-00.png)
  [Parameter(Mandatory = $false)]
  [string]$Prefix = 'slide',

  # Minimum index to start at if the folder has no existing matching files
  [Parameter(Mandatory = $false)]
  [int]$Start = 0,

  # Digits for zero-padding
  [Parameter(Mandatory = $false)]
  [ValidateRange(1, 6)]
  [int]$Pad = 2,

  # If set, only rename files that start with 'image' (image.png, image (1).png, ...)
  [Parameter(Mandatory = $false)]
  [switch]$OnlyDefaultNames,

  # Overwrite destination files if they already exist (not recommended unless you know what you're doing)
  [Parameter(Mandatory = $false)]
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Destination -PathType Container)) {
  throw "Destination folder not found: $Destination"
}

$destinationAbs = (Resolve-Path -Path $Destination).Path

# Existing files already in the target pattern: slide-00.png
$pattern = "^" + [regex]::Escape($Prefix) + "-(\d{" + $Pad + "})\.(png|jpg|jpeg|gif|webp)$"

$images = Get-ChildItem -LiteralPath $destinationAbs -File |
  Where-Object {
    @('.png', '.jpg', '.jpeg', '.gif', '.webp') -contains $_.Extension.ToLowerInvariant()
  }

$existingIndexes = @()
foreach ($img in $images) {
  $m = [regex]::Match($img.Name, $pattern, 'IgnoreCase')
  if ($m.Success) {
    $existingIndexes += [int]$m.Groups[1].Value
  }
}

$nextIndex = $Start
if ($existingIndexes.Count -gt 0) {
  $nextIndex = ([int]($existingIndexes | Measure-Object -Maximum).Maximum) + 1
}

# Candidates: files that are NOT already in the target pattern
$candidates = $images | Where-Object {
  -not [regex]::IsMatch($_.Name, $pattern, 'IgnoreCase')
}

if ($OnlyDefaultNames) {
  $candidates = $candidates | Where-Object {
    $_.BaseName -match '^image(\s*\(\d+\))?$'
  }
}

# Rename in chronological order so it's predictable based on drop/paste order
$candidates = $candidates | Sort-Object LastWriteTime, Name

if (-not $candidates -or $candidates.Count -eq 0) {
  Write-Host "No files to rename in: $destinationAbs" -ForegroundColor Yellow
  exit 0
}

foreach ($file in $candidates) {
  $num = $nextIndex.ToString("D$Pad")
  $ext = $file.Extension.ToLowerInvariant()
  $newName = "$Prefix-$num$ext"
  $targetPath = Join-Path -Path $destinationAbs -ChildPath $newName

  $desc = "Rename '$($file.Name)' -> '$newName'"
  if ($PSCmdlet.ShouldProcess($targetPath, $desc)) {
    Rename-Item -LiteralPath $file.FullName -NewName $newName -Force:$Force
  }

  $nextIndex++
}

Write-Host "Renamed $($candidates.Count) file(s) in: $destinationAbs" -ForegroundColor Green
