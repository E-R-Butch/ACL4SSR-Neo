import os
import pathlib
import sys
import time

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROVIDERS_DIR = REPO_ROOT / "Rules/Generated/Providers"
RULESET_PROVIDERS_DIR = PROVIDERS_DIR / "Ruleset"

TOP_LEVEL_MAPPINGS = {
    "BanAD.yaml": REPO_ROOT / "Rules/Ingredients/AdBlock/BanAD.list",
    "BanEasyList.yaml": REPO_ROOT / "Rules/Ingredients/AdBlock/BanEasyList.list",
    "BanEasyListChina.yaml": REPO_ROOT / "Rules/Ingredients/AdBlock/BanEasyListChina.list",
    "BanProgramAD.yaml": REPO_ROOT / "Rules/Ingredients/AdBlock/BanProgramAD.list",
    "ChinaCompanyIp.yaml": REPO_ROOT / "Rules/Ingredients/China/ChinaCompanyIp.list",
    "ChinaDomain.yaml": REPO_ROOT / "Rules/Ingredients/China/ChinaDomain.list",
    "ChinaIp.yaml": REPO_ROOT / "Rules/Ingredients/China/ChinaIp.list",
    "LocalAreaNetwork.yaml": REPO_ROOT / "Rules/Core/LocalAreaNetwork.list",
    "ProxyGFWlist.yaml": REPO_ROOT / "Rules/Core/ProxyGFWlist.list",
    "ProxyMedia.yaml": REPO_ROOT / "Rules/Ruleset/ProxyMedia.list",
    "UnBan.yaml": REPO_ROOT / "Rules/Core/UnBan.list",
}

RULESET_SOURCES_DIR = REPO_ROOT / "Rules/Ruleset"


def log(message):
    print(f"[*] {message}", flush=True)


def render_provider(source_path):
    header = [
        "# Auto-generated provider file",
        f"# Source: {source_path.relative_to(REPO_ROOT)}",
        f"# Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "payload:",
    ]
    payload = []

    for raw_line in source_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            payload.append(f"  {stripped}")
            continue
        payload.append(f"  - {stripped}")

    return "\n".join(header + payload + [""])


def write_provider(output_path, source_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_provider(source_path), encoding="utf-8")
    log(f"Generated {output_path.relative_to(REPO_ROOT)} from {source_path.relative_to(REPO_ROOT)}")


def remove_stale_top_level_providers():
    active_names = set(TOP_LEVEL_MAPPINGS)
    for path in PROVIDERS_DIR.glob("*.yaml"):
        if path.name not in active_names:
            path.unlink()
            log(f"Removed stale provider {path.relative_to(REPO_ROOT)}")


def build_top_level_providers():
    for output_name, source_path in TOP_LEVEL_MAPPINGS.items():
        if not source_path.exists():
            raise FileNotFoundError(f"Missing provider source: {source_path}")
        write_provider(PROVIDERS_DIR / output_name, source_path)


def build_ruleset_providers():
    active_rule_outputs = set()
    for source_path in sorted(RULESET_SOURCES_DIR.glob("*.list")):
        output_name = f"{source_path.stem}.yaml"
        active_rule_outputs.add(output_name)
        write_provider(RULESET_PROVIDERS_DIR / output_name, source_path)

    for path in RULESET_PROVIDERS_DIR.glob("*.yaml"):
        if path.name not in active_rule_outputs:
            path.unlink()
            log(f"Removed stale ruleset provider {path.relative_to(REPO_ROOT)}")


def main():
    log("Building provider assets from active list sources...")
    remove_stale_top_level_providers()
    build_top_level_providers()
    build_ruleset_providers()
    log("Provider build completed")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log(f"Fatal Error: {exc}")
        sys.exit(1)
