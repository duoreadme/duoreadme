"""
主CLI入口模块

提供命令行界面的主入口。
"""

import click
from .commands import translate_command, config_command


@click.group()
@click.version_option(version="1.0.0", prog_name="DuoReadme")
def cli():
    """
    DuoReadme - 多语言 README 生成工具
    
    一个强大的CLI工具，用于将项目代码和README自动翻译成多种语言并生成规范化的多语言文档。
    """
    pass


# 添加所有子命令
cli.add_command(translate_command, name="translate")
cli.add_command(config_command, name="config")


def main():
    """主函数 - CLI入口点"""
    cli()


if __name__ == "__main__":
    main() 