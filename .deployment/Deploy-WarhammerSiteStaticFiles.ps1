function Deploy-WarhammerSiteStaticFiles {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory = $True)]
        [pscredential]
        $Credential
    )

    $date = Get-Date -Format 'MM-dd-yyyy_hh-mm'

    if (!(Get-Module -Name Posh-SSH)) {
        Import-Module Posh-SSH
    }

    if (!(Get-Module -Name "logging")) {
        Import-Module "$env:userprofile\OneDrive\Dev\!powershell\Logging\logging.psm1"
    }
    Initialize-Log -OutputChannels @("Screen", "File") -FilePath "$env:userprofile\OneDrive\Dev\_sites\_deployment\logs\warhammer_deploy_$date.txt"

    $web01IP = "10.0.30.6"
    $archiveFilePath = "$env:userprofile\OneDrive\Dev\_sites\_archive\warhammer.darkwebwarlocks.com_$date.zip"

    New-LogEntry -Severity "INFO" -Message "Creating archive for Warhammer site..."
    try {
        Compress-Archive -Path "$env:UserProfile\OneDrive\Dev\_sites\warhammer.darkwebwarlocks.com" -DestinationPath $archiveFilePath -CompressionLevel Optimal
        New-LogEntry -Severity "SUCCESS" -Message "Site archive successfully created:`n$archiveFilePath"
    }
    catch {
        New-LogEntry -Severity "FAIL" -Message "An error occured creating the site archive:`n$_"
    }

    New-LogEntry -Severity "INFO" -Message "Attempting to create a new SFTP session to Web01"
    try {
        $SFTPSession = New-SFTPSession -ComputerName $web01IP -Credential $Credential
        New-LogEntry -Severity "SUCCESS" -Message "Session created!"
    }
    catch {
        New-LogEntry -Severity "FAIL" -Message "An error occured connecting:`n$_"
    }

    Write-Host "Copying images folder..."
    try {
        Set-SFTPItem -SessionId $SFTPSession.SessionId -Path "$env:Userprofile\OneDrive\Dev\_sites\warhammer.darkwebwarlocks.com\static\images" -Destination "/var/www/warhammer.darkwebwarlocks.com" -Force        
        New-LogEntry -Severity "SUCCESS" -Message "Static files copied!"
    }
    catch {
        New-LogEntry -Severity "FAIL" -Message "An error occured copying the 'images' folder`n:$_"
    }

    Write-Host "Pulling files from Git..."
    try {
        $sshSession = New-SSHSession -ComputerName $web01IP -Credential $Credential
        $result = Invoke-ssHCommand -Command "cd /var/www/warhammer.darkwebwarlocks.com && git pull" -SessionId $sshSession.SessionId
        New-LogEntry -Severity "SUCCESS" -Message "Git pull initiated! Output: $($result.Output)"
    }
    catch {
        New-LogEntry -Severity "FAIL" -Message "An error occured invoking a Git pull`n:$_"
    }

    Send-Log
}