from flask import Flask, request, jsonify, send_file, Response
import supabase
import uuid
import base64
from urllib.parse import quote

supabase_url = "https://espatgyfiagrnugcyvvu.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzcGF0Z3lmaWFncm51Z2N5dnZ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODA1MDU2OTAsImV4cCI6MTk5NjA4MTY5MH0.2lvtnqoZ2e9h7OeVHAfp0CRBLUitWAB-8Xo6rJoh1Eo"
supabase_client = supabase.create_client(supabase_url, supabase_key)


app = Flask(__name__)
 


@app.route('/')

def hello_world():
    return 'Hello World'
 
@app.route('/entry', methods=['POST'])
def entry():
    id = request.form.get('user_id')
    

    table = 'entry_time'
    data = {'user_id': id}
    print(data)
    result, error = supabase_client.table(table).insert(data).execute()
    if error:
        return f'Error inserting data: {error}'
    else:
        return f'Data inserted successfully: {result}'
    

@app.route('/new_user', methods=['POST'])
def new_user():
    
    user_id = request.form.get('user_id')
    
    string1 = request.form.get('Image')
    
    
    table = 'unKnown User'
    data = {'id': user_id, 'Image': string1}
    print(data)
    result, error = supabase_client.table(table).insert(data).execute()

    if error:
        return f'Error inserting data: {error}'
    else:
        return f'Data inserted successfully: {result}'

@app.route('/get_image')
def get_image():
    table_name = 'unKnown User'
    column_names = ['id','Image']

    # Select the first row from the table
    table = supabase_client.table(table_name)
    response = table.select(', '.join(column_names)).limit(1).execute()
    
    response_string = response.json()
    
    
    print(type(response_string))
    return response_string

@app.route('/add_user', methods=['POST'])
def add_user():
    
    name = request.form.get('name')
    name = str(name)

    details = request.form.get('details')
    details = str(details)
    print('recived: '+name+' '+details)
    user_id=''
    Image=''
    image_encoding=''
    column_names = ['id','Image']
    table = supabase_client.table('unKnown User')
    response = table.select(', '.join(column_names)).limit(1).execute()
    response_string = response.json()
    
    my_list = response_string.split(",")
    u_id = str(my_list[0])
    u_id = u_id[16:-1]
    u_id=u_id[2:]
    
    creation_time = str(my_list[1])
    Image = str(my_list[-2])
    Image=Image[9:-1]
    Image=Image[2:]
    

    
       
   
        
    

    table = 'Known User'
    data = {'id': u_id, 'Image': Image,'Details':details ,'Name':name}
    
    result, error = supabase_client.table(table).insert(data).execute()

    print('success')
    result = supabase_client \
    .from_('unKnown User') \
    .delete() \
    .match({'id': u_id}) \
    .execute()
    
    if error:
        return f'Error inserting data: {error}'
    else:
        return f'Data inserted successfully: {result}'


@app.route("/get_faceencoding")
def get_faceencoding():

    table_name= 'Known User'
    column_name = 'Image'

    # Use Supabase client to query the table and column data
    response = supabase_client.from_(table_name).select(column_name).execute()
    
    
    return jsonify(response.data)


@app.route("/isUserAdded")
def isUserAdded():
    result = supabase_client.from_('unKnown User').select("*").execute()

    return jsonify(str(result))
    


if __name__ == '__main__':
 
    
    app.run()
