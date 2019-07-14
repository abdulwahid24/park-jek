from app.config import ApplicationConfiguration
from app.cli import CLIConsole

if __name__ == '__main__':
    config = ApplicationConfiguration()
    with CLIConsole(config) as cli:
        cli.run()