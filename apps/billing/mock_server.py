import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()


class MockSageX3Server(BaseHTTPRequestHandler):
    def initialize_server(self):
        try:
            base = getattr(settings, "BASE_DIR")
            os.sys(f"poetry run python -m {base}/apps/billing/mock_server.py")
            return True
        except Exception as e:
            raise e

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"response": "document_id"}).encode("utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.send_header("Access-Control-Allow-Origin", "*")
        self.wfile.write(json.dumps({"response": "document_id"}).encode("utf-8"))


def run_mock_server(server_class=HTTPServer, handler_class=MockSageX3Server) -> tuple[HTTPServer, Thread]:
    host = ""
    setattr(settings, "TRANSACTION_PROCESSOR_URL", f"http://{host}:8001")
    server_address = (host, 8001)
    mock_server = server_class(server_address, handler_class)
    thread = Thread(None, mock_server.serve_forever)
    thread.start()
    return mock_server, thread
