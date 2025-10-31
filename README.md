# TesteCadastro

Projeto simples de cadastro de usuários com:
- Frontend: HTML/CSS/JS (abrir frontend/index.html)
- Backend: Python + Flask (backend/app.py)
- Banco: MySQL (configurado automaticamente ao iniciar o backend)

Credenciais MySQL usadas (conforme informado):
- usuário: root
- senha: 35272114

### Como rodar
1. Certifique-se que MySQL está rodando localmente.
2. No terminal, instale dependências (recomendado criar um virtualenv):
   ```
   pip install -r backend/requirements.txt
   ```
3. Inicie o backend:
   ```
   python backend/app.py
   ```
   O backend irá criar o banco `cadastro_db` e a tabela `usuarios` automaticamente, caso não existam.
4. Abra o arquivo `frontend/index.html` no navegador (ou use Live Server no VS Code).
5. Cadastre usuários pelo formulário. O frontend comunica com o backend em http://127.0.0.1:5000

