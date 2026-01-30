<#
.SYNOPSIS
  Rename files in an assets folder using a CSV mapping.

.DESCRIPTION
  Use this when you have a few screenshots with generic names (image1.png, etc.)
  and you want Chapter-2-style descriptive names without renaming one-by-one.

  CSV format (with headers):

    from,to
    image1.png,slide-00-overview.png
    image2.png,slide-01-title.png

.EXAMPLE
  # Dry run
  .\tools\rename_assets_from_csv.ps1 -Destination "Chapter06/Activities/assets" -MapFile ".\temp\rename-map.csv" -WhatIf

.EXAMPLE
  # Apply
  .\tools\rename_assets_from_csv.ps1 -Destination "Chapter06/Activities/assets" -MapFile ".\temp\rename-map.csv" -Force
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$Destination,

  [Parameter(Mandatory = $true, Position = 1)]
  [string]$MapFile,

  [Parameter(Mandatory = $false)]
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Destination -PathType Container)) {
  throw "Destination folder not found: $Destination"
}

if (-not (Test-Path -LiteralPath $MapFile -PathType Leaf)) {
  throw "Map file not found: $MapFile"
}

$destinationAbs = (Resolve-Path -Path $Destination).Path
$mapAbs = (Resolve-Path -Path $MapFile).Path

$rows = Import-Csv -LiteralPath $mapAbs
if (-not $rows -or $rows.Count -eq 0) {
  throw 'Map file is empty.'
}

# Validate
$tos = @{}
foreach ($row in $rows) {
  if (-not $row.from -or -not $row.to) {
    throw 'Map file must have columns: from,to'
  }

  $fromName = $row.from.Trim()
  $toName = $row.to.Trim()

  if ($tos.ContainsKey($toName)) {
    throw "Duplicate 'to' value in map: $toName"
  }
  $tos[$toName] = $true

  $fromPath = Join-Path -Path $destinationAbs -ChildPath $fromName
  if (-not (Test-Path -LiteralPath $fromPath -PathType Leaf)) {
    throw "Source file not found in destination folder: $fromName"
  }
}

# Do renames using a two-step temp name approach to avoid collisions
$timestamp = Get-Date -Format 'yyyyMMddHHmmssfff'
$temps = @()

foreach ($row in $rows) {
  $fromName = $row.from.Trim()
  $toName = $row.to.Trim()

  $fromPath = Join-Path -Path $destinationAbs -ChildPath $fromName
  $tempName = "__tmp_${timestamp}__$fromName"
  $tempPath = Join-Path -Path $destinationAbs -ChildPath $tempName

  if ($PSCmdlet.ShouldProcess($fromPath, "Rename '$fromName' -> '$tempName'")) {
    Rename-Item -LiteralPath $fromPath -NewName $tempName -Force:$Force
  }

  $temps += [PSCustomObject]@{ tempName = $tempName; toName = $toName }
}

foreach ($t in $temps) {
  $tempPath = Join-Path -Path $destinationAbs -ChildPath $t.tempName
  $toPath = Join-Path -Path $destinationAbs -ChildPath $t.toName

  if ((Test-Path -LiteralPath $toPath) -and (-not $Force)) {
    throw "Target already exists (use -Force to overwrite): $($t.toName)"
  }

  if ($PSCmdlet.ShouldProcess($tempPath, "Rename '$($t.tempName)' -> '$($t.toName)'")) {
    Rename-Item -LiteralPath $tempPath -NewName $t.toName -Force:$Force
  }
}

Write-Host "Renamed $($rows.Count) file(s) in: $destinationAbs" -ForegroundColor Green
