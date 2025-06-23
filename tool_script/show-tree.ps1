function Show-Tree {
    param (
        [string]$Path = ".",
        [string]$Prefix = ""
    )
    Get-ChildItem -LiteralPath $Path -Force | Where-Object {
        $_.Name -ne ".venv" -and $_.Name -ne ".git" -and $_.Name -ne "__pycache__"
    } | ForEach-Object {
        Write-Output "$Prefix|- $_"
        if ($_.PSIsContainer) {
            Show-Tree -Path $_.FullName -Prefix "$Prefix  "
        }
    }
}

Show-Tree
