# Import modul-modul yang diperlukan
import grpc
import firebase_admin
from firebase_admin import credentials, firestore
import todo_pb2
import todo_pb2_grpc
from concurrent import futures

# Inisialisasi firebase menggunakan service account key
cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Membuat class TodoService yang mewarisi todo_pb2_grpc.TodoServiceServicer
class TodoService(todo_pb2_grpc.TodoServiceServicer):

    # Implementasi RPC Create
    def Create(self, request, context):
        # Membuat reference ke document baru dalam collection 'todo'
        todo_ref = db.collection('todo').document()
        # Menyimpan data baru dalam document tersebut dengan field title dari request
        todo_ref.set({'title': request.title})
        # Mengembalikan response yang berisi pesan 'Todo created'
        return todo_pb2.CreateResponse(message='Todo created')

    # Implementasi RPC Read
    def Read(self, request, context):
        try:
            # Mencari document dengan id yang diberikan dalam request
            todo_ref = db.collection('todo').document(request.id).get()
            # Jika document tidak ditemukan, membatalkan permintaan dengan error NOT_FOUND
            todo = todo_ref.to_dict()
            if not todo:
                context.abort(grpc.StatusCode.NOT_FOUND, "Todo not found")
            # Mengembalikan response yang berisi informasi mengenai todo item yang ditemukan
            return todo_pb2.ReadResponse(
                todo=todo_pb2.Todo(id=request.id, title=todo['title']))
        # Menangkap error yang terjadi dan membatalkan permintaan dengan error INTERNAL
        except Exception as e:
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    # Implementasi RPC Update
    def Update(self, request, context):
        # Mencari document dengan id yang diberikan dalam request
        todo_ref = db.collection('todo').document(request.id)
        # Jika document ditemukan, memperbarui field title dengan value dari request
        if todo_ref.get().exists:
            todo_ref.update({'title': request.title})
            # Mengembalikan response yang berisi pesan 'Todo updated'
            return todo_pb2.UpdateResponse(message='Todo updated')
        # Jika document tidak ditemukan, membatalkan permintaan dengan error NOT_FOUND
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.UpdateResponse()

    # Implementasi RPC Delete
    def Delete(self, request, context):
        # Mencari document dengan id yang diberikan dalam request
        todo_ref = db.collection('todo').document(request.id)
        # Jika document ditemukan, menghapus document tersebut
        if todo_ref.get().exists:
            todo_ref.delete()
            # Mengembalikan response yang berisi pesan 'Todo deleted'
            return todo_pb2.DeleteResponse(message='Todo deleted')
        # Jika document tidak ditemukan, membatalkan permintaan dengan error NOT_FOUND
        else:
            context.set_details('Todo not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return todo_pb2.DeleteResponse()

    # Implementasi RPC List
    def List(self, request, context):
        try:
            todos = []
            # Mendapatkan seluruh document dalam collection 'todo'
            for todo in db.collection('todo').get():
                # Mengubah setiap document menjadi dictionary
                todo_dict = todo.to_dict()
                # Menambahkan field 'id' ke dictionary yang nilainya adalah id dari document
                todo_dict['id'] = todo.id
                # Menambahkan dictionary tersebut ke dalam list todos
                todos.append(todo_dict)
            # Mengembalikan response yang berisi list todos
            return todo_pb2.ListResponse(todos=todos)
        # Menangkap error yang terjadi dan membatalkan permintaan dengan error INTERNAL
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return todo_pb2.ListResponse()


# Function untuk menjalankan server
def serve():
    # Membuat server dengan 10 worker untuk melayani request
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Menambahkan TodoService ke dalam server
    todo_pb2_grpc.add_TodoServiceServicer_to_server(TodoService(), server)
    # Mengaktifkan server pada port 50051
    server.add_insecure_port('[::]:50051')
    # Menjalankan server
    server.start()
    # Menunggu permintaan dari client
    server.wait_for_termination()


if __name__ == '__main__':
    # Jalanin server
    serve()
