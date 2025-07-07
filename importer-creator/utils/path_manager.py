import os
import glob
from pathlib import Path


class PathManager:
    """Manages paths for importer-creator runs with automatic directory creation."""
    
    def __init__(self, base_dir="./generated"):
        self.base_dir = Path(base_dir)
        self.current_run_dir = None
        
    def get_next_run_number(self):
        """Get the next run number by finding existing run directories."""
        if not self.base_dir.exists():
            return 1
            
        existing_runs = glob.glob(str(self.base_dir / "run_*"))
        if not existing_runs:
            return 1
            
        run_numbers = []
        for run_dir in existing_runs:
            try:
                run_num = int(Path(run_dir).name.split('_')[1])
                run_numbers.append(run_num)
            except (ValueError, IndexError):
                continue
                
        return max(run_numbers) + 1 if run_numbers else 1
    
    def create_run_directory(self):
        """Create a new run directory and return its path."""
        run_number = self.get_next_run_number()
        self.current_run_dir = self.base_dir / f"run_{run_number}"
        
        # Create the run directory and all subdirectories
        subdirs = [
            "initial_script/steps",
            "initial_script/final", 
            "step_2/steps",
            "step_2/final",
            "step_3/steps", 
            "step_3/final",
            "step_4/steps",
            "step_4/final"
        ]
        
        for subdir in subdirs:
            (self.current_run_dir / subdir).mkdir(parents=True, exist_ok=True)
            
        print(f"Created run directory: {self.current_run_dir}")
        return str(self.current_run_dir)
    
    def get_path(self, relative_path):
        """Get a path relative to the current run directory."""
        if self.current_run_dir is None:
            raise ValueError("No run directory created. Call create_run_directory() first.")
        return str(self.current_run_dir / relative_path)
    
    def ensure_dir_exists(self, file_path):
        """Ensure the directory for a file path exists."""
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)


# Global instance
path_manager = PathManager() 