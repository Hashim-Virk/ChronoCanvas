# PowerShell AWS SAM Build & Deployment Script for ChronoCanvas Agent
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Building & Deploying ChronoCanvas Agent to AWS Stack... " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$StackName = "chronocanvas-agent-stack"
$Region = "us-east-1"

# Check if AWS CLI & SAM CLI are installed
if (Get-Command sam -ErrorAction SilentlyContinue) {
    Write-Host "[1/3] Building SAM application..." -ForegroundColor Green
    sam build --template-file aws/template.yaml

    Write-Host "[2/3] Deploying SAM application to AWS..." -ForegroundColor Green
    sam deploy --stack-name $StackName --region $Region --resolve-s3 --capabilities CAPABILITY_IAM --no-confirm-changeset
} else {
    Write-Host "[Note] AWS SAM CLI not detected in local path. To deploy to your AWS account:" -ForegroundColor Yellow
    Write-Host "1. Install AWS CLI & SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html" -ForegroundColor Yellow
    Write-Host "2. Run: sam build --template-file aws/template.yaml" -ForegroundColor Yellow
    Write-Host "3. Run: sam deploy --guided" -ForegroundColor Yellow
}

Write-Host "`nDeployment script finished." -ForegroundColor Cyan
