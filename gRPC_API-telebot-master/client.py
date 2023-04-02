import grpc
import todo_pb2
import todo_pb2_grpc
import telegram
from telegram.ext import CommandHandler, Updater, PicklePersistence

# Inisialisasi bot telegram
bot = telegram.Bot(token='YOUR_TELEBOT_TOKEN')
updater = Updater(token='YOUR_TELEBOT_TOKEN', use_context=True)
dispatcher = updater.dispatcher

# Inisialisasi client untuk mengakses TodoService
import grpc
import todo_pb2
import todo_pb2_grpc

class TodoServiceClient:

    def __init__(self, host='localhost', port=50051):
        # Membuat insecure channel ke TodoService
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = todo_pb2_grpc.TodoServiceStub(self.channel)

    def Create(self, title):
        # Membuat request untuk operasi Create
        request = todo_pb2.CreateRequest(title=title)
        # Memanggil RPC Create dari TodoService
        return self.stub.Create(request)

    def Read(self, id):
        # Membuat request untuk operasi Read
        request = todo_pb2.ReadRequest(id=id)
        # Memanggil RPC Read dari TodoService
        return self.stub.Read(request)

    def Update(self, id, title):
        # Membuat request untuk operasi Update
        request = todo_pb2.UpdateRequest(id=id, title=title)
        # Memanggil RPC Update dari TodoService
        return self.stub.Update(request)

    def Delete(self, id):
        # Membuat request untuk operasi Delete
        request = todo_pb2.DeleteRequest(id=id)
        # Memanggil RPC Delete dari TodoService
        return self.stub.Delete(request)

    def List(self):
        # Membuat request untuk operasi List
        request = todo_pb2.ListRequest()
        # Memanggil RPC List dari TodoService
        return self.stub.List(request)

# Membuat instance TodoServiceClient dan menyimpannya ke dalam bot_data
todo_service = TodoServiceClient('localhost:50051')
dispatcher.bot_data['todo_service'] = todo_service

# Menambahkan command-handler ke dalam bot
def start(update, context):
    # Menampilkan pesan untuk command /start
    message = "Halo! Gunakan daftar command berikut untuk menggunakan Aplikasi\n\n"
    message += "Berikut adalah daftar command yang tersedia:\n"
    message += "/add <judul todo> - untuk menambahkan todo list\n"
    message += "/read <id todo> - untuk membaca todo list\n"
    message += "/update <id todo> <judul baru> - untuk mengubah todo list\n"
    message += "/delete <id todo> - untuk menghapus todo list\n"
    message += "/list - untuk melihat semua todo list"
    # Mengirim pesan ke chat
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def add(update, context):
    # Mendapatkan judul dari command argument
    title = context.args[0]
    # Memanggil RPC Create dari TodoService menggunakan insecure channel
    response = todo_service.Create(title)
    # Mengirim pesan ke chat
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response.message)

def read(update, context):
    # Mendapatkan ID dari command argument
    id = context.args[0]
    try:
        # Memanggil RPC Read dari TodoService menggunakan insecure channel
        response = todo_service.Read(id)
        # Mengirim pesan ke chat
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=response.todo.title)
    except grpc.RpcError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=str(e))

def update(update, context):
    # Mendapatkan ID dan judul baru dari command argument
    id = context.args[0]
    title = context.args[1]
    # Memanggil RPC Update dari TodoService menggunakan insecure channel
    try:
        response = todo_service.Update(id, title)
        # Mengirim pesan ke chat
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=response.message)
    except grpc.RpcError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))

def delete(update, context):
    # Mendapatkan ID dari command argument
    id = context.args[0]
    # Memanggil RPC Delete dari TodoService menggunakan insecure channel
    try:
        response = todo_service.Delete(id)
        # Mengirim pesan ke chat
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=response.message)
    except grpc.RpcError as e:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=str(e))

def list(update, context):
    try:
        # Memanggil RPC List dari TodoService menggunakan insecure channel
        response = todo_service.List()
        todo_list = response.todos
        if not todo_list:
            # Mengirim pesan ke chat jika tidak ada todo list
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Tidak ada todo list")
            return
        # Mengirim pesan ke chat dengan daftar todo list
        message = 'Todo list:\n'
        for todo in todo_list:
            message += f"- {todo.title} (ID: {todo.id})\n"
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=message)
    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Gagal mengambil todo list")

# Menambahkan command-handler ke dalam bot
start_handler = CommandHandler('start', start)
add_handler = CommandHandler('add', add)
read_handler = CommandHandler('read', read)
update_handler = CommandHandler('update', update)
delete_handler = CommandHandler('delete', delete)
list_handler = CommandHandler('list', list)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(read_handler)
dispatcher.add_handler(update_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(list_handler)

# Memulai polling untuk telegram bot
updater.start_polling()
