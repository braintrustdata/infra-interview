import http.server
import socketserver
import os
import datetime
import argparse
from urllib.parse import urlparse, unquote

# Get environment variables with defaults
DEFAULT_PORT = int(os.environ.get("PORT", 8000))
DEFAULT_DIRECTORY = os.environ.get("DIRECTORY", ".")


class FileDetailsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        # Only allow root path
        if self.path != "/":
            self.send_error(403, "Only root directory listing is allowed")
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        current_dir = os.getcwd()
        port_value = os.environ.get("PORT", "default")
        dir_value = os.environ.get("DIRECTORY", "default")

        # HTML header with some basic styling
        html = f"""
        <html>
        <head>
            <title>File Details</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                tr:hover {{ background-color: #f5f5f5; }}
            </style>
        </head>
        <body>
            <h2>Files in Directory: {current_dir}</h2>
            <p><small>Server configured with PORT={port_value} and DIRECTORY={dir_value}</small></p>
            <table>
                <tr>
                    <th>File Name</th>
                    <th>Size</th>
                    <th>Last Modified</th>
                </tr>
        """

        try:
            # List files in current directory
            for filename in os.listdir("."):
                file_stats = os.stat(filename)
                size = file_stats.st_size
                # Format size
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"

                # Format modification time
                mod_time = datetime.datetime.fromtimestamp(
                    file_stats.st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S")

                html += f"""
                <tr>
                    <td>{filename}</td>
                    <td>{size_str}</td>
                    <td>{mod_time}</td>
                </tr>
                """

            html += """
            </table>
        </body>
        </html>
        """

            self.wfile.write(html.encode())
        except Exception as e:
            self.send_error(500, f"Error listing directory: {str(e)}")


def run_server(port, directory):
    # Change to the specified directory
    os.chdir(directory)

    handler = FileDetailsHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Configuration:")
        print(
            f"  - Port: {port} (from {'environment' if port == DEFAULT_PORT else 'command line'})"
        )
        print(
            f"  - Directory: {os.path.abspath(directory)} (from {'environment' if directory == DEFAULT_DIRECTORY else 'command line'})"
        )
        print(f"\nServer running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simple HTTP server that lists files in a directory. "
        "Can be configured via command line arguments or environment variables (PORT, DIRECTORY)"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to run the server on (default: {DEFAULT_PORT}, can also use PORT env var)",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=DEFAULT_DIRECTORY,
        help=f"Directory to list files from (default: {DEFAULT_DIRECTORY}, can also use DIRECTORY env var)",
    )

    args = parser.parse_args()

    # Verify directory exists
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist")
        exit(1)

    # Convert to absolute path
    directory = os.path.abspath(args.directory)

    run_server(args.port, directory)
