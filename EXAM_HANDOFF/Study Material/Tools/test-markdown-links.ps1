param(
    [string]$Root = (Split-Path -Parent $PSScriptRoot),
    [string]$Report = (Join-Path (Split-Path -Parent $PSScriptRoot) 'Tests and Reports\MARKDOWN_LINK_TEST.csv')
)

$ErrorActionPreference = 'Stop'
$rootPath = (Resolve-Path -LiteralPath $Root).Path
$failures = [System.Collections.Generic.List[object]]::new()
$checked = 0

function ConvertTo-Slug([string]$Heading) {
    $s = $Heading.Trim().ToLowerInvariant()
    $s = [regex]::Replace($s, '<[^>]+>', '')
    $s = [regex]::Replace($s, '[^\p{L}\p{Nd}\s_-]', '')
    $s = [regex]::Replace($s, '\s+', '-')
    return $s
}

function Get-DocumentAnchors([string]$Path) {
    $set = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($line in Get-Content -LiteralPath $Path) {
        if ($line -match '^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$') {
            [void]$set.Add((ConvertTo-Slug $Matches[1]))
        }
        foreach ($match in [regex]::Matches($line, '<a\s+(?:name|id)=["'']([^"'']+)["'']', 'IgnoreCase')) {
            [void]$set.Add($match.Groups[1].Value)
        }
    }
    return $set
}

foreach ($document in Get-ChildItem -LiteralPath $rootPath -Recurse -File -Filter '*.md') {
    $lineNumber = 0
    foreach ($line in Get-Content -LiteralPath $document.FullName) {
        ++$lineNumber
        foreach ($match in [regex]::Matches($line, '(?<!\!)\[[^\]]+\]\(([^)]+)\)')) {
            $rawTarget = $match.Groups[1].Value.Trim()
            if ($rawTarget.StartsWith('<') -and $rawTarget.EndsWith('>')) {
                $rawTarget = $rawTarget.Substring(1, $rawTarget.Length - 2)
            }
            $rawTarget = ($rawTarget -split '\s+["'']', 2)[0]
            if ($rawTarget -match '^(?:https?|mailto|data):') { continue }

            ++$checked
            $parts = $rawTarget -split '#', 2
            $filePart = [uri]::UnescapeDataString($parts[0])
            $fragment = if ($parts.Count -eq 2) { [uri]::UnescapeDataString($parts[1]) } else { '' }
            $targetPath = if ([string]::IsNullOrEmpty($filePart)) {
                $document.FullName
            } elseif ([System.IO.Path]::IsPathRooted($filePart)) {
                $filePart
            } else {
                [System.IO.Path]::GetFullPath((Join-Path $document.DirectoryName $filePart))
            }

            if (-not (Test-Path -LiteralPath $targetPath)) {
                $failures.Add([pscustomobject]@{
                    document = $document.FullName.Substring($rootPath.Length + 1)
                    line = $lineNumber
                    target = $rawTarget
                    reason = 'MISSING_FILE'
                })
                continue
            }

            if ($fragment -and ([System.IO.Path]::GetExtension($targetPath) -ieq '.md')) {
                $anchors = Get-DocumentAnchors $targetPath
                if (-not $anchors.Contains($fragment)) {
                    $failures.Add([pscustomobject]@{
                        document = $document.FullName.Substring($rootPath.Length + 1)
                        line = $lineNumber
                        target = $rawTarget
                        reason = 'MISSING_ANCHOR'
                    })
                }
            }
        }
    }
}

$reportDirectory = Split-Path -Parent $Report
if (-not (Test-Path -LiteralPath $reportDirectory)) {
    New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
}
if ($failures.Count -eq 0) {
    'document,line,target,reason' | Set-Content -LiteralPath $Report -Encoding utf8
} else {
    $failures | Export-Csv -LiteralPath $Report -NoTypeInformation -Encoding utf8
}

Write-Output "Markdown documents: $((Get-ChildItem -LiteralPath $rootPath -Recurse -File -Filter '*.md').Count)"
Write-Output "Local links checked: $checked"
Write-Output "Failures: $($failures.Count)"
Write-Output "Report: $Report"
if ($failures.Count -ne 0) { exit 1 }
