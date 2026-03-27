from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import Template, Context
from django.views.decorators.csrf import csrf_exempt

tarefas_db = []

@csrf_exempt
def home(request):
    if request.method == 'POST':
        item = request.POST.get('tarefa')
        if item:
            tarefas_db.append({'id': len(tarefas_db) + 1, 'texto': item, 'concluida': False})
        return redirect('/')

    html_layout = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>To-Do List | Klayton e Yasmin</title>
        <link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            body { 
                font-family: 'Lato', sans-serif; 
                background-color: #efffcd;
                margin: 0; display: flex; flex-direction: column; 
                min-height: 100vh; align-items: center; 
            }
            .container { 
                background: #ffffff; padding: 40px; border-radius: 20px; 
                box-shadow: 0 10px 25px rgba(46, 38, 51, 0.1); 
                width: 700px; margin-top: 60px; flex-grow: 1; 
                border: 2px solid #dce9be;
            }
            h2 { 
                text-align: center; color: #2e2633;
                font-family: 'Abril Fatface', cursive; 
                font-size: 48px; margin-bottom: 30px; 
            }
            form { display: flex; gap: 12px; margin-bottom: 40px; }
            input { 
                flex: 1; padding: 18px; border: 2px solid #dce9be; border-radius: 12px; 
                outline: none; font-size: 16px; font-family: 'Lato', sans-serif;
                background-color: #fdfdfd; color: #555152;
            }
            input:focus { border-color: #99173c; }
            button { 
                background: #2e2633; 
                color: #efffcd;
                border: none; padding: 0 35px; 
                border-radius: 12px; cursor: pointer; font-weight: 700; 
                font-family: 'Lato', sans-serif; transition: 0.3s;
            }
            button:hover { background: #99173c; transform: scale(1.02); }
            ul { list-style: none; padding: 0; }
            li { 
                background: #fff; margin-bottom: 15px; padding: 20px; 
                border-radius: 12px; display: flex; justify-content: space-between; 
                align-items: center; border-bottom: 3px solid #dce9be;
                transition: 0.3s;
            }
            li:hover { transform: translateX(5px); border-color: #99173c; }
            .texto-tarefa { flex-grow: 1; font-size: 19px; color: #555152; }
            .riscado { text-decoration: line-through; color: #dce9be; font-weight: 300; }
            .acoes { display: flex; gap: 20px; }
            .check { color: #dce9be; text-decoration: none; font-size: 22px; transition: 0.3s; }
            .check:hover { color: #99173c; }
            .del { color: #99173c; text-decoration: none; font-weight: bold; font-size: 20px; }
            footer { 
                background: #2e2633;
                color: #dce9be;
                width: 100%; text-align: center; 
                padding: 25px 0; font-family: 'Lato', sans-serif;
                font-size: 14px; letter-spacing: 2px;
            }
            footer b { font-family: 'Abril Fatface', cursive; color: #efffcd; font-weight: normal; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Minhas Tarefas</h2>
            <form method="POST">
                <input type="text" name="tarefa" placeholder="Digite uma nova tarefa..." required>
                <button type="submit">ADICIONAR</button>
            </form>
            <ul>
                {% for t in lista %}
                <li>
                    <span class="texto-tarefa {% if t.concluida %}riscado{% endif %}">
                        {{ t.texto }}
                    </span>
                    <div class="acoes">
                        <a href="/concluir/{{ t.id }}/" class="check">✔</a>
                        <a href="/deletar/{{ t.id }}/" class="del">✕</a>
                    </div>
                </li>
                {% endfor %}
            </ul>
        </div>
        <footer>
            PROJETO ACADÊMICO &nbsp;|&nbsp; <b>Klayton e Yasmin</b>
        </footer>
    </body>
    </html>
    """
    t = Template(html_layout)
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
    path('', home, name='home'),
    path('concluir/<int:id>/', concluir, name='concluir'),
    path('deletar/<int:id>/', deletar, name='deletar'),
]