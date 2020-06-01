from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    return render_template('index.html', items=session.get_items())

@app.route('/update/<id>')
def update(id):
    session.update_item(id)
    return redirect("/")

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        if 'add' in request.form:
            session.add_item(request.form.get('new_todo'))
        return redirect("/")

    return render_template('add.html', items=session.get_items())

@app.route('/delete', methods=['POST'], defaults={'id': None})
@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    if request.method == 'POST':
        if 'delete' in request.form:
            session.remove_item(request.form.get('id'))
        return redirect("/")

    return render_template('delete.html', item=session.get_item(id))
 
if __name__ == '__main__':
    app.run(debug=True)
