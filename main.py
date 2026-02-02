from db import conectar
from auth import Login
from ui import App

if __name__ == "__main__":
    conn, cursor = conectar()
    Login(cursor, conn, App).mainloop()
