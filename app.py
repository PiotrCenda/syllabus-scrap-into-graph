from flask import Flask, flash, render_template, request, redirect
from wtforms import Form, StringField, SelectField
from flask_table import Table, Col
from neo import query, Neo4jConnection


app = Flask(__name__)
conn = Neo4jConnection(uri="bolt://localhost:7687", user="admin", pwd="admin")

class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')

class SearchForm(Form):
    search = StringField('')


def edit_description(descriptions):
    final_desc = ''
    for desc in descriptions:
        for key in desc.keys():
            final_desc += ((key).replace("'", "").replace('[', '').replace(']', '') + '\n').replace('_', ' ').lower().capitalize()
            for k in desc[key].keys():
                k_str = k.capitalize().replace('_', ' ') + ': '
                if k != 'name':
                    desc_str = desc[key][k].capitalize().replace('_', ' ')
                else:
                    desc_str = desc[key][k].replace('_', ' ')
                final_desc += (k_str + desc_str + '\n')
            final_desc += '\n'
        final_desc += '\n'
    
    print(final_desc)
    return final_desc
    
def create_table(query):
    item_list = []
    names = {}

    print(type(query))
    for q in query:
        try:
            
            curr_q = dict(q)
            node_a = dict(curr_q['a'])
            label_a = str(curr_q['labels(a)'])
            node_b = dict(curr_q['b'])
            label_b = str(curr_q['labels(b)'])
            relationship = dict(curr_q['r'])
            label_r = str(curr_q['TYPE(r)'])
            print(node_a['name'])
            
            # desc = str(label_a) + str(node_a) + str(label_r) + str(relationship) +str(label_b) + str(node_b)
            # item_list.append(Item(node_a['name'], desc))
            try:
                names[node_a['name']].extend([{label_r: relationship}, {label_b: node_b}])
            except KeyError as ke:
                names[node_a['name']] =[{label_a: node_a}, {label_r: relationship}, {label_b: node_b}]
            # print(names.keys())
        except Exception as e:
            print(e)
            print('FAILED')
    for key in names.keys():    
        # edit_description(names[key])
        item_list.append(Item(key, edit_description(names[key])))

    return item_list

@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)


@app.route('/results')
def search_results(search):
    search_string = search.data['search']
    q = query(search_input=search_string, connection=conn)
    table = create_table(query=q)

    items = [Item('Name1', search_string + '1'),
         Item('Name2', search_string + '15'),
         Item('Name3', search_string + '2')]
    
    table = ItemTable(table)
    table.border = True
    return render_template('results.html', table=table)

if __name__ == '__main__':
    app.run()