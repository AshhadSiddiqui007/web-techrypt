@echo off
echo Copying server files to functions folder...
cd %~dp0

echo Creating server directory structure...
if not exist "functions\server\config" mkdir "functions\server\config"
if not exist "functions\server\controllers" mkdir "functions\server\controllers"
if not exist "functions\server\middlewares" mkdir "functions\server\middlewares"
if not exist "functions\server\models" mkdir "functions\server\models"
if not exist "functions\server\routes" mkdir "functions\server\routes"
if not exist "functions\server\utils" mkdir "functions\server\utils"

echo Copying config files...
xcopy /Y "..\server\config\*" "functions\server\config\"

echo Copying controller files...
xcopy /Y "..\server\controllers\*" "functions\server\controllers\"

echo Copying middleware files...
xcopy /Y "..\server\middlewares\*" "functions\server\middlewares\"

echo Copying model files...
xcopy /Y "..\server\models\*" "functions\server\models\"

echo Copying route files...
xcopy /Y "..\server\routes\*" "functions\server\routes\"

echo Copying utility files...
xcopy /Y "..\server\utils\*" "functions\server\utils\"

echo Copying .env files...
xcopy /Y "..\.env" "functions\"
if exist "..\.env.production" xcopy /Y "..\.env.production" "functions\"

echo Server files successfully copied to functions folder!
echo You can now deploy the full app to Firebase.
pause
