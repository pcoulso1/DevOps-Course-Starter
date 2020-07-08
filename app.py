from flask import Flask, render_template, request, redirect, url_for
import trello_items as item_store

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', items=item_store.get_items())


@app.route('/update/<id>/<new_status>', methods=['POST'])
def update(id, new_status):
    item_store.update_item(id, new_status)
    return redirect("/")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if 'add' in request.form:
            item_store.add_item(
                request.form.get('new_todo_title'),
                request.form.get('new_todo_description'),
                request.form.get('new_todo_due'))
        return redirect("/")

    return render_template('add.html', items=item_store.get_items())


@app.route('/delete/<id>', methods=['POST'])
@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    if request.method == 'POST':
        if 'delete' in request.form:
            item_store.remove_item(id)
        return redirect("/")

    return render_template('delete.html', item=item_store.get_item(id))


if __name__ == '__main__':
    app.run(debug=True)
