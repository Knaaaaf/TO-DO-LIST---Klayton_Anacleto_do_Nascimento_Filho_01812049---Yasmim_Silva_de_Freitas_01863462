from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

# Lista na memória (apaga se reiniciar o servidor)
tarefas_db = []

@csrf_exempt
def home(request):
    if request.method == 'POST':
        item = request.POST.get('tarefa')
        if item:
            tarefas_db.append({'id': len(tarefas_db) + 1, 'texto': item, 'concluida': False})
        return redirect('/')

    html_pronto = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>To-Do List | Klayton e Yasmin</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background-color: #ffffff; 
                margin: 0; 
                display: flex; 
                flex-direction: column; 
                min-height: 100vh; 
                align-items: center; 
            }
            .container { 
                background: #ffffff; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.05); 
                width: 700px; 
                margin-top: 60px; 
                flex-grow: 1; 
                border: 1px solid #eee;
            }
            h2 { text-align: center; color: #222; font-size: 32px; margin-bottom: 30px; }
            form { display: flex; gap: 10px; margin-bottom: 30px; }
            input { 
                flex: 1; padding: 15px; border: 2px solid #eee; 
                border-radius: 8px; outline: none; font-size: 16px;
            }
            button { 
                background: #28a745; color: white; border: none; 
                padding: 0 30px; border-radius: 8px; cursor: pointer; 
                font-weight: bold; font-size: 16px;
            }
            ul { list-style: none; padding: 0; }
            li { 
                background: #fff; margin-bottom: 12px; padding: 15px; 
                border-radius: 8px; display: flex; justify-content: space-between; 
                align-items: center; border: 1px solid #f0f0f0;
            }
            .texto-tarefa { flex-grow: 1; font-size: 18px; color: #333; }
            .riscado { text-decoration: line-through; color: #bbb; }
            .acoes { display: flex; gap: 20px; }
            .check { color: #28a745; text-decoration: none; font-size: 20px; font-weight: bold; }
            .del { color: #d32f2f; text-decoration: none; font-weight: bold; font-size: 18px; }
            footer { 
                background: #fff; color: #777; width: 100%; text-align: center; 
                padding: 25px 0; font-size: 14px; border-top: 1px solid #eee; margin-top: 40px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Lista de Tarefas</h2>
            <form method="POST">
                <input type="text" name="tarefa" placeholder="O que você vai fazer hoje?" required>
                <button type="submit">Adicionar</button>
            </form>
            <ul>
                {% for t in lista %}
                <li>
                    <span class="texto-tarefa {% if t.concluida %}riscado{% endif %}">
                        {{ t.texto }}
                    </span>
                    <div class="acoes">
                        <a href="/concluir/{{ t.id }}" class="check" title="Marcar como concluída">✔</a>
                        <a href="/deletar/{{ t.id }}" class="del" title="Excluir tarefa">✕</a>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
        <footer>
            To-Do List Acadêmico &nbsp;|&nbsp; <b>Klayton e Yasmin</b>
        </footer>
    </body>
    </html>
    """
    t = Template(html_pronto)
    c = Context({'lista': tarefas_db})
    return HttpResponse(t.render(c))

def concluir(request, id):
    global tarefas_db
    for t in tarefas_db:
        if t['id'] == id:
            t['concluida'] = not t['concluida']
            break
    return redirect('/')

def deletar(request, id):
    global tarefas_db
    tarefas_db = [t for t in tarefas_db if t['id'] != id]
    return redirect('/')

urlpatterns = [
    path('', home),
    path('concluir/<int:id>', concluir),
    path('deletar/<int:id>', deletar),
]