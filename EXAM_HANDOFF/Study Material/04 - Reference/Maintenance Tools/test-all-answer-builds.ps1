param(
  [string]$Uv4 = 'C:\Users\marwa\AppData\Local\Keil_v5\UV4\UV4.exe',
  [string]$Only = ''
)

$ErrorActionPreference = 'Stop'
$handoff = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$template = Join-Path $handoff 'ARM_Exam_Project'
$answersRoot = Join-Path $handoff 'Study Material\03 - Solved Exams'
$reportRoot = Join-Path $handoff 'Study Material\04 - Reference\Tests and Reports\Solved Answer Builds'
New-Item -ItemType Directory -Force -Path $reportRoot | Out-Null

$temporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('arm-exam-build-' + [Guid]::NewGuid().ToString('N'))
$resolvedTempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath())
$resolvedTemporaryRoot = [System.IO.Path]::GetFullPath($temporaryRoot)
if (-not $resolvedTemporaryRoot.StartsWith($resolvedTempBase, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Temporary build root escaped the operating-system temporary directory: $resolvedTemporaryRoot"
}
New-Item -ItemType Directory -Force -Path $resolvedTemporaryRoot | Out-Null

$results = @()
try {
  $projects = Get-ChildItem -Directory -LiteralPath $answersRoot | Where-Object {
    Test-Path -LiteralPath (Join-Path $_.FullName 'Answer Source\assembly.s')
  } | Sort-Object Name
  if ($Only) {
    $selectedNames = $Only.Split(',',[System.StringSplitOptions]::RemoveEmptyEntries)
    $projects = $projects | Where-Object { $selectedNames -contains $_.Name }
  }

  foreach ($project in $projects) {
    $work = Join-Path $resolvedTemporaryRoot $project.Name
    Copy-Item -LiteralPath $template -Destination $work -Recurse
    $source = Join-Path $project.FullName 'Answer Source'
    Copy-Item -LiteralPath (Join-Path $source 'assembly.s') -Destination (Join-Path $work 'Answer\assembly.s') -Force
    Copy-Item -LiteralPath (Join-Path $source 'main.c') -Destination (Join-Path $work 'Answer\main.c') -Force

    # Generated objects from the template must never satisfy a historical build.
    foreach ($generatedName in @('Build','Listings')) {
      $generated = [System.IO.Path]::GetFullPath((Join-Path $work $generatedName))
      $verifiedWork = [System.IO.Path]::GetFullPath($work)
      if ($generated.StartsWith($verifiedWork + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $generated)) {
        Remove-Item -LiteralPath $generated -Recurse -Force
      }
    }

    # A historical answer that defines a handler owns that exact vector.
    $answerText = (Get-Content -Raw -LiteralPath (Join-Path $work 'Answer\main.c')) + "`n" +
                  (Get-Content -Raw -LiteralPath (Join-Path $work 'Answer\assembly.s'))
    $configPath = Join-Path $work 'Source\platform\exam_config.h'
    $configText = Get-Content -Raw -LiteralPath $configPath
    $owners = @('TIMER0','TIMER1','TIMER2','TIMER3','RIT','SYSTICK','ADC','EINT0','EINT1','EINT2','SVC')
    foreach ($owner in $owners) {
      $handler = if ($owner -eq 'SYSTICK') { 'SysTick_Handler' } elseif ($owner -eq 'SVC') { 'SVC_Handler' } else { $owner + '_IRQHandler' }
      if ($answerText -match ('\b' + [regex]::Escape($handler) + '\b')) {
        $configText = $configText -replace ('(#define EXAM_OWN_' + $owner + '_HANDLER) 0'), '$1 1'
      }
    }
    Set-Content -LiteralPath $configPath -Value $configText -Encoding UTF8

    $log = Join-Path $reportRoot ($project.Name + '.log')
    $uvproj = Join-Path $work 'ARM_Exam_Template.uvprojx'
    $process = Start-Process -FilePath $Uv4 -ArgumentList @('-b', "`"$uvproj`"", '-j0', '-o', "`"$log`"") -WindowStyle Hidden -Wait -PassThru
    $text = if (Test-Path -LiteralPath $log) { Get-Content -Raw -LiteralPath $log } else { '' }
    $errors = if ($text -match '(\d+) Error\(s\)') { [int]$Matches[1] } else { -1 }
    $warnings = if ($text -match '(\d+) Warning\(s\)') { [int]$Matches[1] } else { -1 }
    $results += [pscustomobject]@{
      project = $project.Name
      exit_code = $process.ExitCode
      errors = $errors
      warnings = $warnings
      status = if ($process.ExitCode -eq 0 -and $errors -eq 0 -and $warnings -eq 0) { 'ARM_COMPILE_LINK_PASS' } else { 'BUILD_FAIL' }
      log = ('Study Material/04 - Reference/Tests and Reports/Solved Answer Builds/' + $project.Name + '.log')
    }
    Write-Output ("{0}: exit={1} errors={2} warnings={3}" -f $project.Name,$process.ExitCode,$errors,$warnings)
  }
  $results | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath (Join-Path $reportRoot 'SUMMARY.csv')
}
finally {
  $verified = [System.IO.Path]::GetFullPath($resolvedTemporaryRoot)
  if ($verified.StartsWith($resolvedTempBase, [System.StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $verified)) {
    Remove-Item -LiteralPath $verified -Recurse -Force
  }
}

if (($results | Where-Object status -ne 'ARM_COMPILE_LINK_PASS').Count -ne 0) { exit 1 }
