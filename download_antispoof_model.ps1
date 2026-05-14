$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ModelDir = Join-Path $ProjectRoot "backend\models\antispoof"
$ModelPath = Join-Path $ModelDir "minifasnet_v2.onnx"
$LicensePath = Join-Path $ModelDir "LICENSE.upstream.txt"
$ReadmePath = Join-Path $ModelDir "README.model.txt"
$ExpectedSha256 = "D7B3CD9BA8A7CEB13BAA8C4720902E27CA3112EFF52F926C08804AF6B6EECC7B"

$ModelUrl = "https://huggingface.co/garciafido/minifasnet-v2-anti-spoofing-onnx/resolve/main/minifasnet_v2.onnx"
$LicenseUrl = "https://huggingface.co/garciafido/minifasnet-v2-anti-spoofing-onnx/resolve/main/LICENSE"
$ReadmeUrl = "https://huggingface.co/garciafido/minifasnet-v2-anti-spoofing-onnx/resolve/main/README.md"

function Write-Step {
    param([string]$Message)
    Write-Host "[download-antispoof] $Message"
}

function Download-File {
    param(
        [Parameter(Mandatory = $true)][string]$Url,
        [Parameter(Mandatory = $true)][string]$OutFile
    )

    Write-Step "Downloading $(Split-Path -Leaf $OutFile)"
    Invoke-WebRequest -Uri $Url -OutFile $OutFile
}

function Ensure-Directory {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        Write-Step "Creating directory: $Path"
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
    }
}

function Verify-Hash {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Expected
    )

    $hash = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToUpperInvariant()
    Write-Step "Model SHA256: $hash"
    if ($hash -ne $Expected.ToUpperInvariant()) {
        throw "SHA256 mismatch for $Path. Expected: $Expected ; Actual: $hash"
    }
}

Ensure-Directory -Path $ModelDir

Download-File -Url $ModelUrl -OutFile $ModelPath
Download-File -Url $LicenseUrl -OutFile $LicensePath
Download-File -Url $ReadmeUrl -OutFile $ReadmePath

Verify-Hash -Path $ModelPath -Expected $ExpectedSha256

Write-Step "Done."
Write-Step "Model path: $ModelPath"
