Set-ExecutionPolicy Unrestricted -Force

$apiUrl = "https://store.rg-adguard.net/api/GetFiles"

# Prompt the user for the download folder location
$downloadFolder = Read-Host "Please enter the download folder location (e.g. C:\Users\Username\Downloads)"

if (!(Test-Path $downloadFolder -PathType Container)) {
    New-Item $downloadFolder -ItemType Directory -Force
}

$productUrl = Read-Host "Please enter the Microsoft Store product URL"

$body = @{
    type = 'url'
    url  = $productUrl
    ring = 'RP'
    lang = 'en-US'
}

$response = Invoke-RestMethod -Method Post -Uri $apiUrl -ContentType 'application/x-www-form-urlencoded' -Body $body

$regex = '<tr style.*<a href=\"(?<url>.*)"\s.*>(?<text>.*)<\/a>'
$fileLinks = $response | Select-String $regex -AllMatches | ForEach-Object { $_.Matches } | ForEach-Object {
    $url = $_.Groups[1].Value
    $text = $_.Groups[2].Value

    if ($text -match "_(x86|x64|neutral).*appx(|bundle)$") {
        $downloadFile = Join-Path $downloadFolder $text
        if (!(Test-Path $downloadFile)) {
            [PSCustomObject]@{
                Url = $url
                File = $downloadFile
                Name = $text
            }
        }
    }
}

if ($fileLinks.Count -eq 0) {
    Write-Host "No files found to download."
} else {
    foreach ($file in $fileLinks) {
        $downloadOption = Read-Host "Do you want to download $($file.Name)? (Y/N)"
        if ($downloadOption -eq "Y") {
            Invoke-WebRequest -Uri $file.Url -OutFile $file.File                
        } else {
            Write-Host "$($file.Name) will not be downloaded."
            continue
        }

        $installOption = Read-Host "Do you want to install $($file.Name)? (Y/N)"
        if ($installOption -eq "Y") {
            Add-AppxPackage -Path $file.File
        } else {
            Write-Host "$($file.Name) will not be installed."
        }
    }
}
