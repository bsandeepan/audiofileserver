from src import create_app

if __name__=="__main__":
    # Set Values
    HOST="127.0.0.1"
    PORT=5050
    # create app and run
    app = create_app()
    app.run(host=HOST, port=PORT, debug=True)