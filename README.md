# WinAppxAIO
This script is a PowerShell script that prompts the user for a download folder location and a Microsoft Store product URL. It then uses an API from store.rg-adguard.net to retrieve downloadable appx files from the Microsoft Store, filters the results for x86, x64, or neutral architecture files, and offers to download and install them based on user input.

To break it down step-by-step:

1. The script sets the API endpoint URL and prompts the user for a download folder location.
2. If the specified download folder does not exist, the script creates it.
3. The user is prompted for a Microsoft Store product URL.
4. The script builds a POST request body with the product URL and other parameters, and sends the request to the API endpoint.
5. The API returns HTML content, which the script searches for links matching a regular expression that identifies appx files for x86, x64, or neutral architectures.
6. For each matching link, the script creates an object with properties for the URL, downloaded file path, and file name.
7. If there are no matches, the script informs the user and exits. Otherwise, it prompts the user to confirm each download and installation.
8. If the user confirms a download, the script downloads the file using Invoke-WebRequest and saves it to the specified download folder.
9. If the user confirms an installation, the script installs the downloaded appx package using Add-AppxPackage.

Overall, this script automates the process of downloading and installing appx packages from the Microsoft Store and provides a user-friendly interface for selecting which packages to download and install.
