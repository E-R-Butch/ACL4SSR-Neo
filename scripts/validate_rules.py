import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG_FILE = REPO_ROOT / "Config/ACL4SSR_Online_Full.ini"

LIST_DIRS = [
    REPO_ROOT / "Rules/Core",
    REPO_ROOT / "Rules/Ingredients/China",
    REPO_ROOT / "Rules/Ingredients/AdBlock",
    REPO_ROOT / "Rules/Outputs",
    REPO_ROOT / "Rules/Ruleset",
]

ALLOWED_SPECIAL_GROUPS = {"DIRECT", "REJECT"}
RULE_TOKEN_RE = re.compile(r"^[A-Z0-9-]+$")
GROUP_REF_RE = re.compile(r"\[\]([^`\n]+)")


def log(message):
    print(f"[*] {message}", flush=True)


def fail(message):
    print(f"[!] {message}", flush=True)


def parse_custom_groups(lines):
    groups = set()
    for line in lines:
        if line.startswith("custom_proxy_group="):
            body = line.split("=", 1)[1]
            group_name = body.split("`", 1)[0].strip()
            if group_name:
                groups.add(group_name)
    return groups


def validate_ini(config_path):
    errors = []
    lines = config_path.read_text(encoding="utf-8").splitlines()
    groups = parse_custom_groups(lines)

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(";"):
            continue

        if stripped.startswith("surge_ruleset="):
            body = stripped.split("=", 1)[1]
            target = body.split(",", 1)[0].strip()
            if target not in groups:
                errors.append(f"{config_path}:{lineno} ruleset target '{target}' has no matching custom_proxy_group")

        if stripped.startswith("custom_proxy_group="):
            body = stripped.split("=", 1)[1]
            group_name, _, definition = body.partition("`")
            if not group_name:
                errors.append(f"{config_path}:{lineno} custom_proxy_group is missing a group name")
                continue

            for ref in GROUP_REF_RE.findall(definition):
                ref = ref.strip()
                if ref in ALLOWED_SPECIAL_GROUPS:
                    continue
                if ref not in groups:
                    errors.append(f"{config_path}:{lineno} group '{group_name}' references undefined group '{ref}'")

    return errors


def validate_list_file(path):
    errors = []
    non_comment_rules = 0

    for lineno, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        non_comment_rules += 1
        if "," not in line:
            errors.append(f"{path}:{lineno} missing comma-separated rule format")
            continue

        token, remainder = line.split(",", 1)
        if not RULE_TOKEN_RE.fullmatch(token):
            errors.append(f"{path}:{lineno} invalid rule token '{token}'")
        if not remainder.strip():
            errors.append(f"{path}:{lineno} empty rule payload")

    if non_comment_rules == 0:
        errors.append(f"{path} contains no effective rules")

    return errors


def main():
    errors = []

    log(f"Validating config: {CONFIG_FILE}")
    errors.extend(validate_ini(CONFIG_FILE))

    for list_dir in LIST_DIRS:
        for path in sorted(list_dir.glob("*.list")):
            log(f"Checking list file: {path.relative_to(REPO_ROOT)}")
            errors.extend(validate_list_file(path))

    if errors:
        for error in errors:
            fail(error)
        fail(f"Validation failed with {len(errors)} issue(s)")
        sys.exit(1)

    log("Validation completed successfully!")


if __name__ == "__main__":
    main()
