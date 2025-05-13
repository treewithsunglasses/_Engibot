class handle:
    def handle():
        print("init handler")

    def command(asCommand):
        match asCommand:
            case "ping":
                print(pong)
            case "pong":
                print(ping)