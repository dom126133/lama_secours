from flask import Blueprint, request, current_app
from markupsafe import escape

blueprint_index = Blueprint('hello_world', __name__)

@blueprint_index.route('/', methods=['GET'])
def create_index_blueprint():
    #name = request.args.get("name", "World")
    return f'<h1>Vigogne</h1>'\
           f'<p>A substitute to LAMA</p>'\
           f'<h2>Downloaded json zip file</h2>'\
           f'<p>Use the following end point in order to download a '\
           f'json zip file: <a href="{request.base_url[:-4]}/v2/uploadedfile">'\
           f'{request.base_url[:-4]}/v2/uploadedfile</a>'\
           f'<h2>Download a json file</h2>'\
           f'<p>In a shell, use curl to post the zip file.</p>'\
           f'<p>Example:</p>'\
           f'<code style="display:inline-block;margin-left:3em;">'\
           f"curl -X 'POST' \\</br>"\
           f"'http://127.0.0.1:8000/v2/uploadzip/' \\</br>"\
           f"-H 'accept: application/json' \\</br>"\
           f"-H 'Content-Type: multipart/form-data' \\</br>"\
           f"-F 'file=@shift-definitions_04-01-2024_12-17-06.zip;type=application/zip'"\
           f'</code>'\
           f'<p>Replace <code>shift-definitions_04-01-2024_12-17-06.zip</code> with the name of your zipfile.'
           