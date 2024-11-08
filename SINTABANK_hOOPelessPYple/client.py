import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("localhost", 10000))
    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running.")
        return
    except Exception as e:
        print(f"Unable to connect to the server: {e}")
        return

    while True:
        try:
            # Receive and send username
            message = client.recv(1024).decode()
            if not message:
                break
            username = input(message)
            client.send(username.encode())

            # Receive and send password
            message = client.recv(1024).decode()
            if not message:
                break
            password = input(message)
            client.send(password.encode())

            # Receive and print login response
            response = client.recv(1024).decode()
            if not response:
                break
            print(response)

            # Continue interaction or close
            continue_interaction = input("Do you want to continue? (yes/no): ").strip().lower()
            if continue_interaction != "yes":
                break
        except KeyboardInterrupt:
            print("\nKeyboard Interrupt. Closing connection.")
            break
        except ConnectionError:
            print("\nConnection closed unexpectedly.")
            break

    client.close()
    print("Client disconnected.")

if __name__ == "__main__":
    main()
