# Convert .docx files to PDF with Microsoft Word. Usage: to_pdf.ps1 a.docx [b.docx ...]
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Paths)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
  foreach ($p in $Paths) {
    $full = (Resolve-Path $p).Path
    $doc = $word.Documents.Open($full, $false, $true)
    $pages = $doc.ComputeStatistics(2)
    $doc.SaveAs([ref]([IO.Path]::ChangeExtension($full, '.pdf')), [ref]17)
    $doc.Close($false)
    Write-Output "$p`tpages=$pages"
  }
} finally { $word.Quit() }
