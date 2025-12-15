import os
import socket
import time

def env_int(name: str) -> int:
    val = os.getenv(name)
    if val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    try:
        x = int(val)
    except ValueError:
        raise RuntimeError(f"Env var {name} must be an integer, got: {val!r}")
    return x

def recv_all(conn: socket.socket, max_bytes: int = 4096) -> str:
    data = b""
    while len(data) < max_bytes:
        chunk = conn.recv(256)
        if not chunk:
            break
        data += chunk
        if b"\n" in data:
            break
    return data.decode("utf-8", errors="replace").strip()

def main() -> None:
    N = env_int("COLLATZ_COUNT")
    if N <= 0:
        raise RuntimeError("COLLATZ_COUNT must be > 0")

    host = os.getenv("SERVER_HOST", "server")
    port = int(os.getenv("SERVER_PORT", "9000"))

    deadline = time.time() + 30 
    last_err = None

    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=5) as conn:
                msg = f"{N}\n".encode("utf-8")
                conn.sendall(msg)
                resp = recv_all(conn)
                print(resp)
                return
        except Exception as e:
            last_err = e
            time.sleep(1)

    raise RuntimeError(f"Could not connect to server at {host}:{port}. Last error: {last_err}")

if __name__ == "__main__":
    main()
