import json
import random
import string
import argparse
from pathlib import Path

STORE_FILE = Path("password_store.json")


def load_store():
    if not STORE_FILE.exists():
        return {}
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_store(store):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


def generate_password(length=16, numbers=True, symbols=True, uppercase=True):
    chars = list(string.ascii_lowercase)

    if uppercase:
        chars.extend(string.ascii_uppercase)
    if numbers:
        chars.extend(string.digits)
    if symbols:
        chars.extend("!@#$%^&*")

    if len(chars) == 0:
        print("至少需要选择一种字符类型。")
        return None

    password = "".join(random.choices(chars, k=length))
    return password


def check_password_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if len(password) >= 16:
        score += 1

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*" for c in password):
        score += 1

    if score <= 3:
        return "弱"
    elif score <= 5:
        return "中"
    elif score <= 6:
        return "强"
    else:
        return "很强"


def save_account(name, password, remark=""):
    store = load_store()

    if name in store:
        print(f"账号 [{name}] 已存在。")
        return

    store[name] = {
        "password": password,
        "remark": remark
    }

    save_store(store)
    print(f"已保存账号：{name}")


def list_accounts():
    store = load_store()

    if not store:
        print("暂无保存记录。")
        return

    print("\n=== 账号记录 ===")
    for name, item in store.items():
        print(f"\n账号：{name}")
        print(f"密码：{item['password']}")
        print(f"备注：{item.get('remark', '无')}")


def delete_account(name):
    store = load_store()

    if name not in store:
        print(f"账号 [{name}] 不存在。")
        return

    confirm = input(f"确定删除账号 [{name}]？(y/n)：")
    if confirm.lower() != "y":
        print("已取消删除。")
        return

    del store[name]
    save_store(store)
    print(f"已删除账号：{name}")


def main():
    parser = argparse.ArgumentParser(description="密码生成与管理工具")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser("generate", help="生成密码")
    generate_parser.add_argument("--length", type=int, default=16, help="密码长度")
    generate_parser.add_argument("--numbers", action="store_true", help="包含数字")
    generate_parser.add_argument("--symbols", action="store_true", help="包含符号")
    generate_parser.add_argument("--uppercase", action="store_true", help="包含大写字母")

    check_parser = subparsers.add_parser("check", help="检查密码强度")
    check_parser.add_argument("password", help="待检查密码")

    save_parser = subparsers.add_parser("save", help="保存账号记录")
    save_parser.add_argument("name", help="账号名称")
    save_parser.add_argument("password", help="密码")
    save_parser.add_argument("remark", nargs="?", default="", help="备注")

    subparsers.add_parser("list", help="查看所有账号记录")

    delete_parser = subparsers.add_parser("delete", help="删除账号记录")
    delete_parser.add_argument("name", help="账号名称")

    args = parser.parse_args()

    if args.command == "generate":
        password = generate_password(
            length=args.length,
            numbers=args.numbers,
            symbols=args.symbols,
            uppercase=args.uppercase
        )
        if password:
            print(f"生成密码：{password}")
            print(f"强度：{check_password_strength(password)}")

    elif args.command == "check":
        level = check_password_strength(args.password)
        print(f"密码强度：{level}")

    elif args.command == "save":
        save_account(args.name, args.password, args.remark)

    elif args.command == "list":
        list_accounts()

    elif args.command == "delete":
        delete_account(args.name)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
