from app.config import ApplicationConfiguration
from app.cli import CLIConsole

if __name__ == '__main__':
    app_config = ApplicationConfiguration()
    with CLIConsole(app_config.config) as cli:
        cli.run()