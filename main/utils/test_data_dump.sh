for app in core llm_test; do
    echo "Running data dump for $app"
    sh "apps/$app/tests/data_dump.sh"
done
