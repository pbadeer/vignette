# A Mac OS taskbar app: Vignette
## Helps you focus by applying a vignette overlay to your mac

### Setup

1. Install uv and make
1. `uv sync`
1. `make run` or `uv run python vignette.py`

### Fish Terminal Alias

1. Install tmux
1. Modify "~/GitHub/vignette/" in vig.fish to be the path to this repo
1. Copy your modified vig.fish to `~/.config/fish/functions/`
1. Restart your terminal
1. Run `vig` to start, quit the python app to close.