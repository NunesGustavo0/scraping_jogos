# 🎮 Scraping Jogos

> Coleta automatizada de dados de jogos via web scraping, com agendamento por cron e containerização Docker.

---

## 📋 Sobre o Projeto

O **Scraping Jogos** é uma aplicação Python que realiza a extração automatizada de dados de jogos a partir de fontes web. O projeto é totalmente containerizado com Docker e possui agendamento automático de execução via crontab, tornando a coleta de dados periódica e sem necessidade de intervenção manual.

---

## 🗂️ Estrutura do Projeto

```
scraping_jogos/
├── src/                  # Código-fonte principal
├── Dockerfile            # Imagem Docker da aplicação
├── docker-compose.yml    # Orquestração dos containers
├── crontab               # Configuração do agendamento automático
├── requirements.txt      # Dependências Python
└── .gitignore
```

---

## 🚀 Tecnologias Utilizadas

- **Python** — Linguagem principal
- **Docker / Docker Compose** — Containerização e orquestração
- **Crontab** — Agendamento automático de execuções
- **Bibliotecas Python** — Definidas em `requirements.txt`

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Docker](https://www.docker.com/) (versão 20+)
- [Docker Compose](https://docs.docker.com/compose/) (versão 2+)

---

## 🛠️ Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/NunesGustavo0/scraping_jogos.git
cd scraping_jogos
```

### 2. Suba os containers com Docker Compose

```bash
docker-compose up --build
```

O container irá iniciar a aplicação e o cron configurado passará a executar o scraping automaticamente nos intervalos definidos.

### 3. Execução manual (opcional)

Para rodar o scraping manualmente sem esperar o cron:

```bash
docker-compose run --rm app python src/main.py
```

> **Nota:** Substitua `src/main.py` pelo script de entrada correto, se necessário.

---

## 🕐 Agendamento (Crontab)

O arquivo `crontab` define a frequência de execução automática do scraper. Para alterar o intervalo, edite o arquivo antes de subir os containers.

Exemplo de entrada cron:
```
0 * * * * python /app/src/main.py   # Executa a cada hora
```

---

## 📦 Dependências

As dependências do projeto estão listadas em `requirements.txt`. Para instalar localmente (fora do Docker):

```bash
pip install -r requirements.txt
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Commit suas alterações (`git commit -m 'feat: adiciona minha feature'`)
4. Faça o push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

## 👤 Autor

**Gustavo Nunes**

- GitHub: [@NunesGustavo0](https://github.com/NunesGustavo0)