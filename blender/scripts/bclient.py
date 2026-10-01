"""Minimal client for the Blender MCP addon socket (127.0.0.1:9876)."""
import json
import socket
import sys

HOST, PORT = "127.0.0.1", 9876


def send_command(cmd, timeout=180):
    """Send one command dict, return parsed response dict."""
    payload = json.dumps(cmd).encode("utf-8")
    s = socket.create_connection((HOST, PORT), timeout=30)
    s.settimeout(timeout)
    try:
        s.sendall(payload)
        buf = b""
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
            try:
                return json.loads(buf.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
    finally:
        s.close()
    raise RuntimeError("No response / connection closed")


def exec_code(code, timeout=180):
    resp = send_command({"type": "execute_code", "params": {"code": code}}, timeout)
    return resp


if __name__ == "__main__":
    # Usage: bclient.py ping | sceneinfo | exec <file_with_code>
    mode = sys.argv[1] if len(sys.argv) > 1 else "ping"
    if mode == "ping":
        print(json.dumps(send_command({"type": "ping"}), indent=1)[:500])
    elif mode == "sceneinfo":
        print(json.dumps(send_command({"type": "get_scene_info"}), indent=1)[:4000])
    elif mode == "exec":
        with open(sys.argv[2]) as f:
            code = f.read()
        resp = exec_code(code)
        print(json.dumps(resp, indent=1)[:6000])
