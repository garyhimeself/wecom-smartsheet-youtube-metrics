$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$envPath = Join-Path (Split-Path -Parent $PSScriptRoot) '.env'

$form = New-Object System.Windows.Forms.Form
$form.Text = '配置 YouTube API Key'
$form.Size = New-Object System.Drawing.Size(480, 220)
$form.StartPosition = 'CenterScreen'
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$form.MinimizeBox = $false

$label = New-Object System.Windows.Forms.Label
$label.Text = '粘贴你的 YouTube Data API Key。它只会保存在本机，不会显示或上传。'
$label.AutoSize = $true
$label.Location = New-Object System.Drawing.Point(20, 24)
$form.Controls.Add($label)

$keyInput = New-Object System.Windows.Forms.TextBox
$keyInput.Location = New-Object System.Drawing.Point(20, 62)
$keyInput.Size = New-Object System.Drawing.Size(424, 28)
$keyInput.UseSystemPasswordChar = $true
$form.Controls.Add($keyInput)

$saveButton = New-Object System.Windows.Forms.Button
$saveButton.Text = '保存'
$saveButton.Location = New-Object System.Drawing.Point(284, 118)
$saveButton.Size = New-Object System.Drawing.Size(75, 30)
$saveButton.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.Controls.Add($saveButton)

$cancelButton = New-Object System.Windows.Forms.Button
$cancelButton.Text = '取消'
$cancelButton.Location = New-Object System.Drawing.Point(369, 118)
$cancelButton.Size = New-Object System.Drawing.Size(75, 30)
$cancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
$form.Controls.Add($cancelButton)

$form.AcceptButton = $saveButton
$form.CancelButton = $cancelButton

if ($form.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
    exit 0
}

$apiKey = $keyInput.Text.Trim()
if ([string]::IsNullOrWhiteSpace($apiKey)) {
    [System.Windows.Forms.MessageBox]::Show('未填写 API Key，未保存任何内容。', '未完成') | Out-Null
    exit 1
}

if (Test-Path -LiteralPath $envPath) {
    $replace = [System.Windows.Forms.MessageBox]::Show(
        '本机已经存在 .env。是否替换其中的配置？',
        '确认替换',
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Warning
    )
    if ($replace -ne [System.Windows.Forms.DialogResult]::Yes) {
        exit 0
    }
}

Set-Content -LiteralPath $envPath -Value "YOUTUBE_API_KEY=$apiKey" -NoNewline -Encoding utf8
[System.Windows.Forms.MessageBox]::Show('配置已保存到本机。现在可以开始读取和更新智能表格。', '完成') | Out-Null
