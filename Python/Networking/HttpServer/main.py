from http.server import HTTPServer, BaseHTTPRequestHandler
from collections import Counter
from io import BytesIO
import json


class RequestHandler(BaseHTTPRequestHandler):
    """
        Example addresses:
        localhost:8000/
        localhost:8000/1
        localhost:8000/2
        localhost:8000/5
        localhost:8000/1_5
        localhost:8000/3_2
    """

    DATA_PATH = "data.json"

    def __init__(self, *args, **kwargs):
        try:
            self.data = RequestHandler.load_data()
        except FileNotFoundError:
            print("[ERROR]:Data file not found.")
            self.data = []

        super().__init__(*args, **kwargs)

    @staticmethod
    def load_data(path=DATA_PATH):
        with open(path) as file:
            data = json.load(file)
        return data

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        params = self.parse_path(self.path)
        self.handle_request(params)

    @staticmethod
    def parse_path(path):
        print("PATH:", path)
        path = path[1:]
        params = path.split(sep="_")
        for index, n in reversed(list(enumerate(params))):
            try:
                params[index] = int(n)
            except ValueError:
                del params[index]
                print("Incorrect parameter:", n)
        print("PARAMS:", params)
        return params

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

    def handle_request(self, params):
        if not self.data:
            self.wfile.write(b"Data file not found :(")
            return

        if not params:
            params = [1, 2, 3, 4, 5]

        summary = Counter()
        for index, storage in enumerate(self.data):
            if (index + 1) in params:
                for item, number in self.data[storage].items():
                    summary[item] += number

        html = "<table><tr><th>Item</th><th>Number</th></tr>"
        for item, number in summary.items():
            html += "<tr>"
            html += "<td>" + str(item) + "</td>"
            html += "<td>" + str(number) + "</td>"
            html += "</tr>"
        html += "</table>"

        html = html.encode()
        self.wfile.write(html)


def main():
    httpd = HTTPServer(('localhost', 8000), RequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
