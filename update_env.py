import argparse
import os
import sys

TARGET_VARS = {
    "ELASTIC_OTLP_ENDPOINT",
    "ELASTICSEARCH_URL",
    "KIBANA_URL",
    "ELASTIC_API_KEY",
    "ELASTIC_OTLP_API_KEY",
}


def update_env_file(filepath: str) -> None:
    if not os.path.isfile(filepath):
        print(f"Erreur : le fichier '{filepath}' est introuvable.", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        stripped = line.strip()

        # Conserver les commentaires, les lignes vides et les lignes sans '='
        if not stripped or stripped.startswith("#") or "=" not in line:
            updated_lines.append(line)
            continue

        # Séparer uniquement sur le premier '=' (important pour les clés Base64 finissant par '==')
        key, _ = line.split("=", 1)
        key_clean = key.strip()

        if key_clean in TARGET_VARS:
            env_val = os.environ.get(key_clean)
            if env_val is not None:
                newline = "\n" if line.endswith("\n") else ""
                updated_lines.append(f"{key}={env_val}{newline}")
            else:
                print(
                    f"Avertissement : '{key_clean}' n'est pas définie dans l'environnement. Valeur actuelle conservée.",
                    file=sys.stderr,
                )
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"Fichier '{filepath}' mis à jour.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remplace les valeurs des variables Elastic par celles de l'environnement."
    )
    parser.add_argument("fichier", help="Chemin du fichier à modifier (ex: .env)")
    args = parser.parse_args()

    update_env_file(args.fichier)
