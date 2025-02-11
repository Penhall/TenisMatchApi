@echo off
echo Inicializando repositório Git...

:: Inicializar repositório
git init

:: Adicionar arquivos
git add .

:: Criar primeiro commit
git commit -m "Initial commit: Project structure setup"

:: Configurar branch principal como 'main'
git branch -M main

echo Para conectar com o GitHub:
echo 1. Crie um novo repositório no GitHub
echo 2. Execute: git remote add origin https://github.com/Penhall/TenisMatchApi.git
echo 3. Execute: git push -u origin main