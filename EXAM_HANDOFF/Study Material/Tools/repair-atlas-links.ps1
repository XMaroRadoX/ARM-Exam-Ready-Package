param([string]$Root = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
$rootPath = (Resolve-Path -LiteralPath $Root).Path
$atlas = Join-Path $rootPath 'Exam Atlas and Code Patterns\ARM_EXAM_ATLAS'
$templates = Join-Path $rootPath 'Exam Atlas and Code Patterns\CODE_TEMPLATES'
$solutions = Join-Path $rootPath 'Solved Exams'
$changedFiles = 0
$changedLinks = 0

function Get-RelativeLink([string]$FromDirectory, [string]$ToPath) {
    $from = [uri](([System.IO.Path]::GetFullPath($FromDirectory).TrimEnd('\') + '\'))
    $to = [uri][System.IO.Path]::GetFullPath($ToPath)
    return [uri]::UnescapeDataString($from.MakeRelativeUri($to).ToString())
}

foreach ($document in Get-ChildItem -LiteralPath $atlas -Recurse -File -Filter '*.md') {
    $original = Get-Content -LiteralPath $document.FullName -Raw
    $updated = [regex]::Replace($original, '(?<!\!)\[([^\]]+)\]\(([^)]+)\)', {
        param($match)
        $label = $match.Groups[1].Value
        $target = $match.Groups[2].Value
        $destination = $null

        if ($target -match 'deliverables/selected_arm_kit/templates/(.+)$') {
            $suffix = $Matches[1] -replace '/', '\'
            $destination = Join-Path $templates $suffix
        } elseif ($target -match 'deliverables/solved_exam_examples/([^/]+)/Source/exam/(.+)$') {
            $project = $Matches[1]
            $file = $Matches[2] -replace '/', '\'
            $destination = Join-Path (Join-Path (Join-Path $solutions $project) 'Answer Source') $file
        }

        if ($null -eq $destination) { return $match.Value }
        if (-not (Test-Path -LiteralPath $destination)) {
            throw "Cannot repair missing destination: $destination (from $($document.FullName))"
        }
        ++$script:changedLinks
        $relative = Get-RelativeLink $document.DirectoryName $destination
        return "[$label]($relative)"
    })

    if ($updated -cne $original) {
        [System.IO.File]::WriteAllText($document.FullName, $updated,
            [System.Text.UTF8Encoding]::new($false))
        ++$changedFiles
    }
}

Write-Output "Atlas Markdown files changed: $changedFiles"
Write-Output "Links repaired: $changedLinks"
