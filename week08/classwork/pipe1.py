import multiprocessing as mp
import string
import queue

def sender(conn):
    """Sends messages through the pipe."""
    messages = string.ascii_lowercase
    for msg in messages:
        conn.send(msg)
        print(f"Sent: {msg}")
    conn.send(None)  # Send a termination signal
    conn.close()

def receiver(conn):
    """Receives messages from the pipe."""
    while True:
        msg = conn.recv()
        if msg is None:  # Stop condition
            break
        print(f"Received: {msg}")

def main():
    """Sets up multiprocessing communication."""
    parent_conn, child_conn = mp.Pipe()  # Create a pipe with two connection endpoints


    q = queue.Queue()
    # Ensure "args" (plural) is used and arguments are passed as a tuple
    p_sender = mp.Process(target=sender, args=(parent_conn,))
    p_receiver = mp.Process(target=receiver, args=(child_conn,))

    # Start both processes
    p_sender.start()
    p_receiver.start()

    # Wait for processes to finish
    p_sender.join()
    p_receiver.join()

if __name__ == "__main__":
    main()
