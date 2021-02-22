def get_app_vars():
    """
    Read app configuration here and send to main app.
    In Production Environment, env vars should be read from here.
    """

    with open(".secrets",'r') as secrets:
        num = int(secrets.readline())
        app_vars = {}
        for i in range(0, num):
            line = secrets.readline().split(" ")
            app_vars[line[0]] = line[1].rstrip("\n")
        return app_vars


if __name__ == "__main__":
    to_print = get_app_vars()
    print(to_print["DB_URI"])
    print(to_print["DB_NAME"])