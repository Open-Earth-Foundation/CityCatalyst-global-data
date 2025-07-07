from pathlib import Path
from state.agent_state import AgentState


def get_run_path(state: AgentState, relative_path: str) -> str:
    """
    Get a path relative to the current run directory stored in state.
    Falls back to the old hardcoded path if run_dir is not set (for backwards compatibility).
    Always returns paths with forward slashes for cross-platform compatibility.
    """
    run_dir = state.get("run_dir")
    
    # Handle case where run_dir might be the string "None" due to serialization
    if run_dir and run_dir != "None" and run_dir.strip():
        result = str(Path(run_dir) / relative_path).replace('\\', '/')
        return result
    else:
        # Fallback to old behavior for backwards compatibility
        result = f"./generated/{relative_path}"
        return result


def ensure_path_exists(file_path: str):
    """Ensure the directory for a file path exists."""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True) 