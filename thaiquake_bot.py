from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv
import os
import json

# Pegando o token do telegram
load_dotenv()
token_tel = os.getenv("token_telegram")

# Armazenar IDs do usuarios
USER_FILE = os.getenv("users_json")



# Função para carregar os usuários salvos
def carregar_users():
    try:
        with open(USER_FILE, "r") as f:
            user_list =  set(json.load(f))
            return set(user_list)
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

# Função para salvar os usuários no arquivo
def salvar_users():
    with open(USER_FILE, "w") as f:
        json.dump(list(users), f)


# Carregar usuários ao iniciar
users = carregar_users()

# Iniando o bot do telegram (start)
async def iniciando(update: Update, context: CallbackContext):
    # pegando o id do usuario e colocando no users
    chat_id = update.message.chat_id
    users.add(chat_id)
    salvar_users()
    user = update.effective_user

    # Mensagem com lista de comandos disponíveis
    mensagem_inicio = (
        f"Olá {user.first_name}! Eu sou o ThaiQuakeBot e você foi registrado para receber avisos de terremotos na região da Tailandia!.\n\n Aqui estão os comandos disponíveis:\n"
        "/iniciar - Registra você para receber alertas de terremotos.\n"
        "/sair - Remove você da lista de alertas de terremotos.\n"
    )

    await update.message.reply_text(mensagem_inicio)


# Respondendo um comando no telegram
async def mensagem(update: Update, context):
    texto = update.message.text
    await update.message.reply_text(f"Você disse: {texto}\n Infelizmente eu não posso te responder.")


async def notificar_todos(mensagem):
    if not users:
        print("Nenhum usuário registrado para receber mensagens.")
        return
    
    try:
        for id_user in users:
            await app.bot.send_message(chat_id=id_user, text=mensagem)
        print(f'Mensagens enviadas!')
    except Exception as e:
        print(f'Erro ao enviar mensagem: {e}')


# Função para remover um usuário da lista de registrados
async def deletar_user(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in users:
        users.remove(chat_id)
        salvar_users() # Aqui estou atualizando o json com id do usuario excluido
        await update.message.reply_text("Você foi removido da lista de alertas!")
    else:
        await update.message.reply_text("Você não estava na lista de alertas!")


# Criando e iniciando o but
app = Application.builder().token(token_tel).build()

# Associando as funções
app.add_handler(CommandHandler("iniciar", iniciando))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensagem))
app.add_handler(CommandHandler("sair", deletar_user))

print("Bot configurado e pronto para ser iniciado")
