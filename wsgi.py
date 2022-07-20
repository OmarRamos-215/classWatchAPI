from app.main import app

if __name__== '__main__':
    #app.run(load_dotenv=True)
    app.run(load_dotenv=True, port=8080)