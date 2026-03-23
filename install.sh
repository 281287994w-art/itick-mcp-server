#!/bin/bash

# iTick MCP Server 一键安装脚本
# 自动完成环境检查、依赖安装和基础配置

set -e

echo "🚀 开始安装 iTick MCP Server..."

# 检查 Python 版本
echo "📋 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 错误：未找到 Python，请先安装 Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ 检测到 Python $PYTHON_VERSION"

# 检查 Python 版本是否 >= 3.10
REQUIRED_VERSION="3.10"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ 错误：需要 Python 3.10+，当前版本为 $PYTHON_VERSION"
    exit 1
fi

# 检查 pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ 错误：未找到 pip，请先安装 pip"
    exit 1
fi

echo "✓ pip 检查通过"

# 创建虚拟环境（可选，如果用户想要全局安装可跳过）
echo ""
read -p "是否创建虚拟环境？(推荐，y/n): " create_venv
create_venv=${create_venv:-y}

if [ "$create_venv" = "y" ]; then
    if [ ! -d "venv" ]; then
        echo "📦 创建虚拟环境..."
        $PYTHON_CMD -m venv venv
        echo "✓ 虚拟环境创建成功"
        
        # 激活虚拟环境
        source venv/bin/activate
        echo "✓ 虚拟环境已激活"
    else
        echo "✓ 虚拟环境已存在，激活中..."
        source venv/bin/activate
    fi
fi

# 安装依赖
echo ""
echo "📦 安装依赖包..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -e .

echo "✓ 依赖安装完成"

# 配置环境变量
echo ""
echo "⚙️  配置环境变量..."
read -p "请输入您的 iTick Token: " itick_token
itick_token=${itick_token:-}

if [ -z "$itick_token" ]; then
    echo "⚠️  警告：未输入 Token，后续需要手动配置 ITICK_TOKEN 环境变量"
else
    # 写入 .env 文件
    cat > .env << EOF
# iTick MCP Server 环境变量配置
ITICK_TOKEN="$itick_token"
# ITICK_API_BASE="https://api.itick.org"
EOF
    echo "✓ 环境变量已保存到 .env 文件"
    
    # 询问是否添加到 shell 配置
    read -p "是否将环境变量添加到 shell 配置文件？(y/n): " add_to_shell
    add_to_shell=${add_to_shell:-n}
    
    if [ "$add_to_shell" = "y" ]; then
        SHELL_CONFIG=""
        if [[ "$SHELL" == *"zsh"* ]]; then
            SHELL_CONFIG="$HOME/.zshrc"
        elif [[ "$SHELL" == *"bash"* ]]; then
            if [ -f "$HOME/.bashrc" ]; then
                SHELL_CONFIG="$HOME/.bashrc"
            elif [ -f "$HOME/.bash_profile" ]; then
                SHELL_CONFIG="$HOME/.bash_profile"
            fi
        fi
        
        if [ -n "$SHELL_CONFIG" ]; then
            echo "" >> "$SHELL_CONFIG"
            echo "# iTick MCP Server 环境变量" >> "$SHELL_CONFIG"
            echo "export ITICK_TOKEN=\"$itick_token\"" >> "$SHELL_CONFIG"
            echo "✓ 环境变量已添加到 $SHELL_CONFIG"
            echo "💡 提示：请运行 'source $SHELL_CONFIG' 使配置生效"
        else
            echo "⚠️  未找到合适的 shell 配置文件，请手动配置"
        fi
    fi
fi

# 验证安装
echo ""
echo "🔍 验证安装..."
if command -v itick-mcp &> /dev/null; then
    echo "✓ itick-mcp 命令已可用"
else
    echo "⚠️  itick-mcp 命令未在 PATH 中找到"
    if [ "$create_venv" = "y" ]; then
        echo "💡 提示：请先激活虚拟环境：source venv/bin/activate"
    fi
fi

# 完成提示
echo ""
echo "=========================================="
echo "🎉 安装完成！"
echo "=========================================="
echo ""
echo "下一步操作："
echo "1. 如果创建了虚拟环境，使用前请激活："
echo "   source venv/bin/activate"
echo ""
echo "2. 确保环境变量已配置："
echo "   - 已添加到 shell 配置：重启终端或运行 source 命令"
echo "   - 或使用 .env 文件：在启动时加载"
echo ""
echo "3. 启动服务："
echo "   itick-mcp"
echo ""
echo "4. 配置到 Cursor/Claude Desktop："
echo "   参考 README.md 中的配置示例"
echo ""
echo "💡 更多帮助信息请查看：README.md"
echo ""
