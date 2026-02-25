#!/usr/bin/env python3
"""Rename the hello-gtk-python template to your own project."""

import os
import re
import sys


def to_snake_case(name):
    """my-cool-app -> my_cool_app"""
    return name.replace('-', '_')


def to_pascal_case(name):
    """my-cool-app -> MyCoolApp"""
    return ''.join(word.capitalize() for word in name.split('-'))


def to_title(name):
    """my-cool-app -> My Cool App"""
    return ' '.join(word.capitalize() for word in name.split('-'))


def to_path_segment(app_id):
    """com.example.MyCoolApp -> /com/example/MyCoolApp"""
    return '/' + '/'.join(app_id.split('.'))


def rename_file(filepath, old_name, new_name):
    """Rename a file if its name contains old_name."""
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    if old_name in filename:
        new_filename = filename.replace(old_name, new_name)
        new_filepath = os.path.join(directory, new_filename)
        os.rename(filepath, new_filepath)
        return new_filepath
    return filepath


def collect_files(root):
    """Collect all project files, excluding build dirs and .git."""
    skip = {'.git', 'build', 'builddir', '_build', '.flatpak-builder',
            'build-flatpak', '__pycache__', '.uv', '.venv', 'node_modules'}
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip]
        for f in filenames:
            files.append(os.path.join(dirpath, f))
    return files


def main():
    print('Hello GTK Python - Project Renamer')
    print('=' * 40)
    print()

    project_name = input('Project name (kebab-case, e.g. my-cool-app): ').strip()
    if not project_name:
        print('Error: project name is required.')
        sys.exit(1)
    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', project_name):
        print('Error: project name must be lowercase-with-hyphens (e.g. my-cool-app).')
        sys.exit(1)

    default_id = f'com.example.{to_pascal_case(project_name)}'
    app_id = input(f'Application ID [{default_id}]: ').strip() or default_id
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*(\.[a-zA-Z][a-zA-Z0-9]*)+$', app_id):
        print('Error: invalid application ID (e.g. com.mycompany.MyApp).')
        sys.exit(1)

    default_display = to_title(project_name)
    display_name = input(f'Display name [{default_display}]: ').strip() or default_display

    # Derive all naming variants
    old_app_id = 'com.example.HelloGtkPython'
    old_project = 'hello-gtk-python'
    old_module = 'hello_gtk_python'
    old_pascal = 'HelloGtkPython'
    old_display = 'Hello GTK Python'
    old_path = '/com/example/HelloGtkPython'

    new_module = to_snake_case(project_name)
    new_pascal = to_pascal_case(project_name)
    new_path = to_path_segment(app_id)

    # Order matters: replace longer/more specific strings first
    replacements = [
        (old_path, new_path),
        (old_app_id, app_id),
        (old_display, display_name),
        (old_pascal, new_pascal),
        (old_module, new_module),
        (old_project, project_name),
    ]

    # File-name replacements (app ID first since it's more specific)
    file_renames = [
        (old_app_id, app_id),
        (old_project, project_name),
    ]

    print()
    print(f'  Project name:   {project_name}')
    print(f'  Application ID: {app_id}')
    print(f'  Display name:   {display_name}')
    print(f'  Module name:    {new_module}')
    print(f'  Class prefix:   {new_pascal}')
    print()

    confirm = input('Proceed? [Y/n] ').strip().lower()
    if confirm and confirm != 'y':
        print('Aborted.')
        sys.exit(0)

    root = os.path.dirname(os.path.abspath(__file__))
    files = collect_files(root)

    # Replace file contents
    replaced_count = 0
    for filepath in files:
        if filepath == os.path.abspath(__file__):
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            continue

        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            replaced_count += 1

    # Rename files (collect fresh list after content changes)
    files = collect_files(root)
    renamed_count = 0
    for filepath in sorted(files, key=len, reverse=True):
        for old, new in file_renames:
            new_path_result = rename_file(filepath, old, new)
            if new_path_result != filepath:
                renamed_count += 1
                filepath = new_path_result

    print()
    print(f'Done! Updated content in {replaced_count} files, renamed {renamed_count} files.')
    print()
    print('You can now delete this rename.py script if you no longer need it.')


if __name__ == '__main__':
    main()
