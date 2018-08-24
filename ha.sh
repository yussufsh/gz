until python groundzeroapis.py; do
    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done
