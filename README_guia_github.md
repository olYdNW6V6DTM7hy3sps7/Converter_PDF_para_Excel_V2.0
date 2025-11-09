Guia Simples: Sincronizando seu Projeto com o GitHub

Este guia ensinará como usar o Git (uma ferramenta de controle de versão) para conectar sua pasta local (onde está o PixelPath) a um repositório online no GitHub.

⚠️ 0. Pré-requisitos

Conta no GitHub: Você precisa ter uma conta gratuita no GitHub.

Git Instalado: Você precisa instalar o programa Git no seu computador. (Procure por "Download Git" no Google.)

Terminal/Prompt de Comando: Você fará tudo usando a linha de comando.

🚀 1ª Parte: Configurando o Repositório

Passo 1.1: Criar um Repositório Vazio no GitHub

Acesse o seu GitHub e clique no botão "New" (Novo) para criar um novo repositório.

Dê um nome ao seu projeto (ex: PixelPath-Otimizado).

Mantenha a opção "Public" (Público) ou "Private" (Privado) como preferir.

Muito Importante: Deixe todas as outras caixas (README, gitignore, license) DESMARCADAS. O repositório deve estar completamente vazio.

Clique em "Create repository" (Criar repositório).

Passo 1.2: Copiar o Link do Repositório

Após a criação, o GitHub mostrará uma página com instruções. Procure e copie o link que termina em .git.

Exemplo: https://github.com/SeuUsuario/PixelPath-Otimizado.git

💻 2ª Parte: Conectando sua Pasta Local

Abra o seu Terminal/Prompt de Comando e navegue até a pasta principal do seu projeto PixelPath (aquela que contém o create_project.py, o requirements.txt e a pasta pixelpath/).

Passo 2.1: Inicializar o Git

Este comando diz ao seu computador para começar a rastrear a pasta como um projeto Git.

git init


Passo 2.2: Adicionar Todos os Arquivos

Este comando prepara todos os arquivos e pastas para serem enviados ao GitHub.

git add .


Passo 2.3: Registrar a Primeira Versão (Commit)

O "commit" é como tirar uma foto do estado atual dos seus arquivos. Você precisa dar uma mensagem descrevendo o que foi feito.

git commit -m "Primeiro commit do projeto PixelPath otimizado"


Passo 2.4: Conectar ao GitHub

Este comando usa o link que você copiou no Passo 1.2 e nomeia a conexão como origin.

git remote add origin SEU_LINK_DO_REPOSITÓRIO
# Exemplo: git remote add origin [https://github.com/SeuUsuario/PixelPath-Otimizado.git](https://github.com/SeuUsuario/PixelPath-Otimizado.git)


Passo 2.5: Enviar para o GitHub (Push)

Este é o comando final que envia seus arquivos locais para o servidor do GitHub.

git push -u origin master


Se for a primeira vez, pode ser que o Terminal peça seu nome de usuário e senha do GitHub.

Pronto! Seus arquivos agora estão no GitHub!

🔄 3ª Parte: Atualizando o Repositório (Sincronizando)

Sempre que você fizer mudanças nos arquivos (como no README.md ou nos códigos Python) e quiser salvar essas mudanças no GitHub, siga estes três passos:

Adicionar: Prepare as novas alterações para o registro.

git add .


Registrar (Commit): Crie a nova "foto" das alterações, com uma mensagem descritiva (ex: "Atualizei a lógica do CCL").

git commit -m "Descreva aqui suas alterações"


Enviar (Push): Envie as alterações registradas para o GitHub.

git push
