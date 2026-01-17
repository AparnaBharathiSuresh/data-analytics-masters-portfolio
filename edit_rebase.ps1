$file = $args[0]; $content = Get-Content $file; $content = $content -replace '^pick 3571402', 'edit 3571402'; Set-Content $file $content
