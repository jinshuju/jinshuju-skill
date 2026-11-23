#!/usr/bin/env python3
"""
金数据 MCP Skill 安装辅助脚本

这是一个 MCP 类型的 Skill —— 实际能力由远端 MCP Server 提供，
无需在本地安装任何 Python / Node 依赖。

脚本作用：打印 / 生成 MCP 连接配置片段，方便粘贴到 AI 客户端。

用法：
    python3 setup.py                         # 打印配置说明
    python3 setup.py --print-json [TOKEN]    # 输出带 Bearer 访问令牌的 mcp.json
"""

from __future__ import annotations

import argparse
import json
import sys

MCP_NAME = "jinshuju-form"
MCP_URL = "https://jinshuju.net/mcp"
PERSONAL_TOKEN_URL = "https://next.jinshuju.net/profile/api"
ACCOUNT_TOKEN_URL = "https://next.jinshuju.net/system/api_licence"


def build_snippet(token: str = "YOUR_ACCESS_TOKEN") -> dict:
    return {
        "mcpServers": {
            MCP_NAME: {
                "url": MCP_URL,
                "headers": {
                    "Authorization": f"Bearer {token}",
                },
            }
        }
    }


def print_banner() -> None:
    print("=" * 60)
    print("  金数据 MCP Skill · 安装辅助")
    print("=" * 60)


def print_setup_instructions() -> None:
    print_banner()
    print()
    print(f"MCP 地址：{MCP_URL}")
    print()
    print("金数据 MCP 支持两种认证方式，由用户自行选择：")
    print()
    print("─" * 60)
    print(" 方式 A · OAuth 2.0（推荐）")
    print("─" * 60)
    print()
    print("  1. 打开 AI 客户端的连接器 / Connectors 管理入口")
    print("  2. 选择「添加连接器 (Add custom connector)」")
    print(f"  3. Name = {MCP_NAME}，URL = {MCP_URL}")
    print("  4. 点击 Add，弹出金数据登录页，登录并点「允许」")
    print("  5. 连接器状态变成 ✅ 即完成，无需手动管理凭证")
    print()
    print("─" * 60)
    print(" 方式 B · 访问令牌（Bearer）")
    print("─" * 60)
    print()
    print("第 1 步：创建访问令牌：")
    print(f"         个人访问令牌：{PERSONAL_TOKEN_URL}")
    print(f"         账户访问令牌：{ACCOUNT_TOKEN_URL}")
    print()
    print("第 2 步：在 AI 客户端（Claude Desktop / Cursor / WorkBuddy 等）中添加 MCP 连接器。")
    print()
    print(f"  名称       ：{MCP_NAME}")
    print(f"  地址 (URL) ：{MCP_URL}")
    print("  请求头     ：Authorization: Bearer YOUR_ACCESS_TOKEN")
    print()
    print("或把以下片段粘贴到客户端的 MCP 配置：")
    print()
    print(json.dumps(build_snippet(), indent=2, ensure_ascii=False))
    print()
    print("旧的 API Key / Secret（HTTP Basic）凭证已不再支持，请改用以上两种方式。")
    print()
    print("─" * 60)
    print()
    print("添加完成后，在对话里发送 '列一下我金数据里的表单' 即可验证。")
    print()
    print("其它命令：")
    print("  python3 setup.py --print-json TOKEN   # 生成可直接粘贴的 mcp.json")


def main() -> int:
    parser = argparse.ArgumentParser(description="金数据 MCP Skill 安装辅助")
    parser.add_argument("--print-json", nargs="?", const="YOUR_ACCESS_TOKEN", metavar="TOKEN",
                        help="输出带 Authorization: Bearer 头的 mcp.json 片段；不带 TOKEN 则保留占位符")
    args = parser.parse_args()

    if args.print_json is not None:
        print(json.dumps(build_snippet(args.print_json), indent=2, ensure_ascii=False))
        return 0

    print_setup_instructions()
    return 0


if __name__ == "__main__":
    sys.exit(main())
