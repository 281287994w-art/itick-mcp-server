"""快速配置工具 - 生成各平台 MCP 配置文件"""

import json
import os
import sys
from pathlib import Path


def get_user_input(prompt: str, default: str = "") -> str:
    """获取用户输入，支持默认值"""
    try:
        value = input(prompt).strip()
        return value if value else default
    except (EOFError, KeyboardInterrupt):
        print("\n")
        return default


def check_token_in_env() -> str:
    """检查环境变量中的 token"""
    return os.environ.get("ITICK_TOKEN", "")


def generate_cursor_config(token: str, use_path: bool = False, project_path: str = "") -> dict:
    """生成 Cursor 配置文件"""
    if use_path and project_path:
        return {
            "mcpServers": {
                "itick": {
                    "command": "python3",
                    "args": ["-m", "itick_mcp_server"],
                    "cwd": project_path,
                    "env": {
                        "ITICK_TOKEN": token
                    }
                }
            }
        }
    else:
        return {
            "mcpServers": {
                "itick": {
                    "command": "itick-mcp",
                    "env": {
                        "ITICK_TOKEN": token
                    }
                }
            }
        }


def generate_claude_desktop_config(token: str, use_path: bool = False, project_path: str = "") -> dict:
    """生成 Claude Desktop 配置文件"""
    # Claude Desktop 配置与 Cursor 格式相同
    return generate_cursor_config(token, use_path, project_path)


def generate_opencode_config(token: str, use_path: bool = False, project_path: str = "") -> dict:
    """生成 OpenCode 配置文件"""
    if use_path and project_path:
        return {
            "$schema": "https://opencode.ai/config.json",
            "mcp": {
                "itick": {
                    "type": "local",
                    "command": ["python3", "-m", "itick_mcp_server"],
                    "enabled": True,
                    "environment": {
                        "ITICK_TOKEN": token
                    },
                    "cwd": project_path
                }
            }
        }
    else:
        return {
            "$schema": "https://opencode.ai/config.json",
            "mcp": {
                "itick": {
                    "type": "local",
                    "command": ["itick-mcp"],
                    "enabled": True,
                    "environment": {
                        "ITICK_TOKEN": token
                    }
                }
            }
        }


def save_config(config: dict, filepath: str) -> None:
    """保存配置文件"""
    filepath = Path(filepath).expanduser()
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 配置文件已保存：{filepath}")


def main():
    """主函数"""
    print("=" * 60)
    print("iTick MCP Server 快速配置工具")
    print("=" * 60)
    print()
    
    # 获取 Token
    env_token = check_token_in_env()
    if env_token:
        print(f"✓ 检测到环境变量 ITICK_TOKEN")
        token = get_user_input(f"使用环境变量中的 Token (Y/n): ", "Y")
        if token.lower() != 'y':
            env_token = ""
    
    if not env_token:
        token = get_user_input("请输入您的 iTick Token: ")
        while not token:
            print("⚠️  Token 不能为空")
            token = get_user_input("请重新输入 iTick Token: ")
    else:
        token = env_token
    
    print()
    
    # 选择配置的平台
    print("请选择要配置的平台 (可多选，用逗号分隔):")
    print("1. Cursor")
    print("2. Claude Desktop")
    print("3. OpenCode")
    print("4. 全部")
    print()
    
    choice = get_user_input("请输入选项 (默认：4): ", "4")
    
    # 询问是否使用路径方式（未安装到系统 PATH 时）
    print()
    use_path = get_user_input("是否已安装 itick-mcp 到系统 PATH？(Y/n): ", "Y").lower()
    use_path_cmd = (use_path != 'y' and use_path != 'yes')
    
    project_path = ""
    if use_path_cmd:
        project_path = os.path.abspath(os.path.dirname(__file__))
        print(f"✓ 将使用项目路径模式：{project_path}")
    
    # 生成配置
    platforms = []
    if choice == "1":
        platforms = ["cursor"]
    elif choice == "2":
        platforms = ["claude"]
    elif choice == "3":
        platforms = ["opencode"]
    else:
        platforms = ["cursor", "claude", "opencode"]
    
    print()
    print("正在生成配置...")
    print()
    
    # Cursor 配置
    if "cursor" in platforms:
        cursor_config = generate_cursor_config(token, use_path_cmd, project_path)
        cursor_path = Path.home() / ".cursor" / "mcp.json"
        save_config(cursor_config, str(cursor_path))
    
    # Claude Desktop 配置
    if "claude" in platforms:
        claude_config = generate_claude_desktop_config(token, use_path_cmd, project_path)
        claude_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
        save_config(claude_config, str(claude_path))
    
    # OpenCode 配置
    if "opencode" in platforms:
        opencode_config = generate_opencode_config(token, use_path_cmd, project_path)
        opencode_path = Path.cwd() / "opencode.json"
        save_config(opencode_config, str(opencode_path))
    
    print()
    print("=" * 60)
    print("🎉 配置完成！")
    print("=" * 60)
    print()
    print("下一步:")
    if "cursor" in platforms:
        print("• Cursor 配置已生成，请重启 Cursor 使其生效")
    if "claude" in platforms:
        print("• Claude Desktop 配置已生成，请重启 Claude Desktop 使其生效")
    if "opencode" in platforms:
        print("• OpenCode 配置文件已生成在当前目录")
    
    print()
    print("💡 如需修改配置，可编辑生成的 JSON 文件")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n配置已取消")
        sys.exit(0)
