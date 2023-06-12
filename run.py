from app import create_app

app = create_app()
app.run(host='localhost', port=8080, debug=True)