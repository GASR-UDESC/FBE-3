#!/bin/bash

OUTPUT_DIR="src"

mkdir -p "$OUTPUT_DIR"

glib-compile-resources \
    --sourcedir=src \
    --target="$OUTPUT_DIR/fbe.gresource" \
    src/fbe.gresource.xml

echo "Resources compiled to $OUTPUT_DIR/fbe.gresource"
