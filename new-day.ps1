# Script: CreateDirectoryAndFiles.ps1

# Check if a command-line argument is provided
if ($args.Count -eq 0) {
    Write-Host "Please provide a number as a command-line argument." -ForegroundColor Red
    exit
}

# Get the number from the command-line argument
$number = $args[0]

# Define the directory name based on the input
$directory = "$number"

# Check if the directory already exists
if (-Not (Test-Path -Path $directory)) {
    # Create the directory
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    Write-Host "Directory '$directory' created."

    # Define file names
    $files = @("first_part.py", "second_part.py", "my.txt", "text.txt")

    # Create the files inside the directory
    foreach ($file in $files) {
        New-Item -ItemType File -Path (Join-Path -Path $directory -ChildPath $file) -Force | Out-Null
        Write-Host "File '$file' created in directory '$directory'."
    }
} else {
    Write-Host "Directory '$directory' already exists. No changes made."
}
