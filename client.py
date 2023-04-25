from src.client import application

def main():
    app = application.ChatClient()
    app.run()

if __name__ == '__main__':
    main()