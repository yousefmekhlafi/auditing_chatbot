import os
import pathlib

# Project root directory name
PROJECT_NAME = "auditing_chatbot"

# Define the structure: List of relative paths (files) from the project root
# Directories will be created automatically when files within them are created.
# We explicitly list __init__.py for packages and .gitkeep for potentially empty dirs.
STRUCTURE = [
    ".vscode/launch.json",
    ".vscode/settings.json",
    "src/__init__.py",
    "src/core/__init__.py",
    "src/core/rag_pipeline.py",
    "src/core/agent_hooks.py",
    "src/data_ingestion/__init__.py",
    "src/data_ingestion/loaders/__init__.py",
    "src/data_ingestion/loaders/pdf_loader.py",
    "src/data_ingestion/loaders/base_loader.py",
    "src/data_ingestion/data_source.py",
    "src/parsing/__init__.py",
    "src/parsing/document_parser.py",
    "src/parsing/text_extractor.py",
    "src/parsing/table_extractor.py",
    "src/parsing/image_extractor.py",
    "src/parsing/layout_analyzer.py",
    "src/parsing/models.py",
    "src/chunking/__init__.py",
    "src/chunking/chunker.py",
    "src/chunking/strategies.py",
    "src/embedding/__init__.py",
    "src/embedding/embedder_clients/__init__.py",
    "src/embedding/embedder_clients/sentence_transformer_client.py",
    "src/embedding/embedder_clients/openai_client.py",
    "src/embedding/embedder_clients/multimodal_client.py",
    "src/embedding/embedder_clients/base_client.py",
    "src/embedding/embedder.py",
    "src/vector_store/__init__.py",
    "src/vector_store/vector_db_clients/__init__.py",
    "src/vector_store/vector_db_clients/chroma_client.py",
    "src/vector_store/vector_db_clients/faiss_client.py",
    "src/vector_store/vector_db_clients/base_client.py",
    "src/vector_store/vector_store_manager.py",
    "src/retrieval/__init__.py",
    "src/retrieval/retriever.py",
    "src/generation/__init__.py",
    "src/generation/llm_clients/__init__.py",
    "src/generation/llm_clients/openai_client.py",
    "src/generation/llm_clients/huggingface_client.py",
    "src/generation/llm_clients/base_client.py",
    "src/generation/prompt_templates.py",
    "src/generation/generator.py",
    "src/api/__init__.py",
    "src/api/main.py",
    "src/api/routers/__init__.py",
    "src/api/routers/chat.py",
    "src/api/schemas.py",
    "src/ui/__init__.py",
    "src/ui/app.py",
    "src/utils/__init__.py",
    "src/utils/config_manager.py",
    "src/utils/logging_config.py",
    "src/utils/helpers.py",
    "config/config.yaml",
    "config/.env",
    "data/raw/.gitkeep", # .gitkeep ensures Git tracks the empty directory
    "data/processed/.gitkeep",
    "notebooks/.gitkeep",
    "notebooks/01_data_loading_parsing_test.ipynb",
    "notebooks/02_embedding_vectorstore_test.ipynb",
    "notebooks/03_rag_pipeline_test.ipynb",
    "scripts/ingest_data.py",
    "tests/__init__.py",
    "tests/test_parsing.py",
    "tests/test_retrieval.py",
    ".gitignore",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "README.md"
]

# Content for .gitignore
GITIGNORE_CONTENT = """
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
# Usually these files are written by a CI, but they should be ignored by default.
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# VS Code
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json

# Docker
docker-compose.override.yml

# Data files & sensitive config
data/
*.sqlite
*.db
config/.env

# Notebook checkpoints
.ipynb_checkpoints

# Temporary files
*.log
*.tmp
*~
"""

def create_structure(base_path, structure_list):
    """Creates the directory structure and placeholder files."""
    base_path = pathlib.Path(base_path)
    print(f"Creating project structure at: {base_path.resolve()}")

    # Create the root directory
    base_path.mkdir(exist_ok=True)
    print(f"Created: {base_path}/")

    for item_path in structure_list:
        full_path = base_path / item_path
        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Create the file
        full_path.touch(exist_ok=True)
        print(f"Created: {full_path}")

        # Add default content to .gitignore
        if full_path.name == ".gitignore":
            try:
                with open(full_path, 'w') as f:
                    f.write(GITIGNORE_CONTENT)
                print(f"  -> Added default content to .gitignore")
            except IOError as e:
                print(f"  -> Error writing to .gitignore: {e}")
        elif full_path.name == "README.md":
             try:
                with open(full_path, 'w') as f:
                    f.write(f"# {PROJECT_NAME}\n\nProject description goes here.")
                print(f"  -> Added default title to README.md")
             except IOError as e:
                print(f"  -> Error writing to README.md: {e}")


if __name__ == "__main__":
    create_structure(PROJECT_NAME, STRUCTURE)
    print("\nProject structure created successfully!")
    print(f"Navigate into the project directory: cd {PROJECT_NAME}")