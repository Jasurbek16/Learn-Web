from main_flask import create_app
# ^ get from the __init__

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
