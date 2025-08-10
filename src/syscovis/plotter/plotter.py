from pathlib import Path

from rich.console import Console

console = Console()


class Plotter:
    def __init__(
        self, save=True, show=True, name="", root_indicator="toml", plot_dir="/plots"
    ):
        self.save: bool = save
        self.show: bool = show
        self.root_indicator: str = root_indicator
        self.project_root_dir = Plotter.find_project_root()
        self.plot_dir: Path = self.create_plot_dir(plot_dir)
        self.task_name: str = name
        console.print("plotter is ready to plot...", style="bold cyan blink")

    @staticmethod
    def find_project_root(indicator="toml") -> Path:
        """
        Find project root for relative paths
        """
        # TODO: make indicator to enum
        root_indicators = {
            "toml": "pyproject.toml",
            "git": ".git",
            "venv": ".venv",
        }
        # select indicator, use pyproject.toml as default
        indicator_path = root_indicators.get(indicator, "pyproject.toml")
        # set current location as start
        run_dir = Path.cwd()
        current_dir = run_dir
        # follow the path backwards
        while current_dir != current_dir.parent:
            if (current_dir / indicator_path).exists():
                break
            current_dir = current_dir.parent
        if current_dir != Path("/"):
            console.print("Project root found!", style="green")
            return current_dir
        else:
            console.print("Project root not found!", style="red bold")
            console.print(f"Set [cwd = {run_dir}] as project root", style="yellow")
            return run_dir

    def create_plot_dir(self, plot_dir: str) -> Path:
        path = self.project_root_dir / plot_dir
        path.mkdir(parents=True, exist_ok=True)
        return path
