<h1 align="center" style="color: black">Update Framework</h1>
<div align="center">
    <img src="https://raw.githubusercontent.com/Raghav67816/UpdateFramework/main/icon.png">
</div>


Hello devs! You are the right spot to make take your software distribution and maintainance to another level with the Update Framework, a cross-platform tool to update your application without needing your users to download newer releases and replace the older one. Specially, if you publish an application on Linux based systems outside of apt repositories.

## Features
- Easy-to-Setup
- Templates for backend
- Light-weight
- Compatible with all types of applications

## Installation
Step 1: Download the release file from [here](https://github.com/Raghav67816/UpdateFramework).

Step 2: Extract the file.
Step 3: Locate and execute the **cli.bin** file, for testing only.


!!! info
    You may wonder why the size of the executable is large, this is due to the libraries shipped with it. When we will be having multiple executable like update tool, logger etc. They will use these libraries with some other. So, don't worry about the size of final version of Unified Software

## Usage
The CLI requires two options:
 - request_endpoint - The endpoint to make get request.
 - products_file - Path to JSON file containing information about the installed products/software.

```bash
./cli.bin <REQUEST_ENDPOINT> <PATH_TO_JSON_FILE>
```

## Example

As discussed above, this tool can be used with any of your application. For example, you have an application written in Python. To integrate, this tool use `os module` to call execute command and read the exit codes.

```py
from os import command

command("cli.bin <REQUEST_ENDPOINT> <PATH_TO_JSON>")
```

Please note that it is a minimal example.

## API Response Structure
The tool follows a particular structure of response from API which is given below.

```json
{
  "filename": "UpdateFilename.tar.xz",
  "release_date": "YYYY-MM-DD",
  "release_link": "URL_TO_FILE",
  "version": "1"
}
```

This means that you should return the `filename` i.e the name of the file with which it is uploaded, `release_date` (optional) - The date of release, `release_link` - Url to file, `version` - The latest version available.

Similarly, a specific JSON structure is followed for the file containing information of the installed products.

```json
{
    "xyz_product": {
        "name": "xyz_product",
        "version": "CURRENT_VERSION",
        "path": "INSTALLATION_DIR"
    }
}
```

