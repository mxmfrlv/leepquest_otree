# Define the folder name
$folderName = "leepquest"

# Check if an argument is provided
if (-not $args[0]) {
  Write-Host "Warning: No argument provided. Please provide a new folder name."
  exit 1
}

# Assign the argument to a variable
$newFolderName = $args[0]

# Check if the leepquest folder exists
if (-not (Test-Path -Path $folderName)) {
  Write-Host "Warning: The folder '$folderName' does not exist."
  exit 1
}

# Check if the __init__.py file exists and contains the NAME_IN_URL line
$initFile = Join-Path -Path $folderName -ChildPath "__init__.py"
if (-not (Test-Path -Path $initFile) -or (-not (Get-Content -Path $initFile | Where-Object { $_ -match "NAME_IN_URL = '$folderName'" }))) {
  Write-Host "Warning: The file '$initFile' does not exist or does not contain the line 'NAME_IN_URL = '$folderName'."
  exit 1
}

# Copy the folder
Copy-Item -Path $folderName -Destination $newFolderName -Recurse

# Rename the excel file
Rename-Item -Path "$newFolderName\$folderName.xlsx" -NewName "$newFolderName.xlsx"

# Replace the NAME_IN_URL in the new __init__.py file
$initFilePath = Join-Path -Path $newFolderName -ChildPath "__init__.py"
$lines = Get-Content -Path $initFilePath
$lines = $lines -replace "NAME_IN_URL = '$folderName'", "NAME_IN_URL = '$newFolderName'"
Set-Content -Path $initFilePath -Value $lines

Write-Host "Folder copied and updated successfully."