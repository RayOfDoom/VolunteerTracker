from website import create_app

app = create_app()

# only if we run this file, not import this file
if __name__ == '__main__':
    app.run(debug=True)
