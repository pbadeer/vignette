function vig
    tmux new-session -d -s vignette-session 'cd ~/GitHub/vignette/ && uv run python vignette.py; tmux kill-session -t vignette-session'
end

