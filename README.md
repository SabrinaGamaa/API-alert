# Sistema de Alerta de Terremotos na Tailândia

Este projeto é composto por dois scripts principais que monitoram e alertam sobre terremotos detectados na Tailândia, enviando notificações tanto por Telegram quanto via SMS usando Twilio. O sistema é dividido em duas partes:

- **Monitoramento de Terremotos**: Verifica se houve terremotos na região da Tailândia e envia o alerta.
- **Bot Telegram**: Permite que os usuários se registrem para receber notificações sobre terremotos.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `twilio`
  - `python-telegram-bot`
  - `dotenv`
  - `json`
  - `threading`
  - `asyncio`
  - `datetime`

## Como Usar

### Configuração Inicial

1. **Configuração do Twilio**:
   - Crie uma conta no [Twilio](https://www.twilio.com/) e obtenha um SID de conta, token de autenticação e SID de serviço de mensagens.
   - Armazene essas credenciais no arquivo `.env` como mostrado abaixo:

    ```env
    account_sid=seu_account_sid
    token=seu_token
    service_sid=seu_service_sid
    para=seu_numero_telefone
    terremotos_alertados=terremotos_alertados.json
    users_json=users.json
    token_telegram=seu_token_telegram
    ```

2. **Instalação das dependências**:

    ```bash
    pip install requests twilio python-telegram-bot python-dotenv
    ```

3. **Executando o sistema**:

   Para rodar o sistema de monitoramento e o bot do Telegram, basta executar o script principal:

   ```bash
   python alert.py

### Arquivos do Projeto

    `alert.py`
    <p>
        Este script é responsável pelo monitoramento de terremotos na região da Tailândia. Ele faz requisições para a API de terremotos da USGS e, ao encontrar um terremoto com magnitude superior a 3.0, envia uma notificação para os usuários registrados via SMS (Twilio) e Telegram.
    </p>

### Funções principais:

    - executar_alerta(): Verifica os terremotos e envia alertas.

    - enviar_mensagem(): Envia a mensagem de alerta via Twilio.

    - monitoramento(): Monitora terremotos em intervalos regulares de 2 minutos.

**thaiquakebot.py**
    <p>
        Este script é responsável pelo bot de Telegram que permite aos usuários se registrarem para receber alertas de terremotos e se desregistrarem, caso desejem.
    </p>

    - Funções principais:

    iniciando(): Registra o usuário no bot quando ele envia o comando /iniciar.

    deletar_user(): Remove o usuário da lista de alertas quando ele envia o comando /sair.

    notificar_todos(): Envia notificações de terremotos para todos os usuários registrados.

    Como Funciona
    Monitoramento de Terremotos
    O sistema consulta a API da USGS para detectar terremotos na região da Tailândia. Ele analisa eventos ocorridos nos últimos 4 dias e, se a magnitude do evento for superior a 3.0, envia um alerta.

    Notificações via Twilio
    Quando um terremoto é detectado, o sistema envia uma mensagem SMS usando o Twilio com os detalhes do evento (local, magnitude, link de mais informações).

    Bot Telegram
    O bot Telegram permite que os usuários se registrem para receber notificações. Eles podem interagir com o bot usando comandos simples como /iniciar para começar a receber alertas ou /sair para parar de receber as notificações.

    Como Funciona o Histórico de Eventos
    Os eventos detectados são salvos em um arquivo JSON (terremotos_alertados.json). Isso evita o envio de múltiplas notificações para o mesmo evento. O histórico é carregado ao iniciar o sistema e atualizado sempre que um novo terremoto é detectado.

    Comandos do Bot Telegram
    /iniciar: Registra o usuário para começar a receber notificações de terremotos.

    /sair: Remove o usuário da lista de alertas.

**Execução Simultânea**
    O sistema de monitoramento e o bot Telegram são executados simultaneamente, usando threads e asyncio. O monitoramento acontece em segundo plano e o bot responde aos comandos do usuário sem bloquear o processo de monitoramento.

### Exemplos de Mensagens de Alerta
    - Quando um terremoto é detectado, a mensagem de alerta enviada será parecida com a seguinte:
    ``` yaml
        🚨 TERREMOTO DETECTADO! 🚨

        📍 Local: 100km E de Chiang Mai, Tailândia
        📅 Data e Hora: 2025-04-01 10:45:00 UTC
        💥 Magnitude: 4.5
        🔗 Mais informações: https://earthquake.usgs.gov/earthquakes/eventpage/us7000y5a
    ```
    IMAGEM

### Contribuições
    Sinta-se à vontade para fazer contribuições, melhorias ou correções! Se você encontrar algum bug ou tiver sugestões, por favor, abra uma issue ou envie um pull request.

### Licença
    Este projeto está licenciado sob a MIT License.