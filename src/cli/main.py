"""
主CLI入口模块

提供命令行界面的主入口。
"""

import click
from .commands import translate_command, config_command


@click.command()
@click.version_option(version="1.0.0", prog_name="DuoReadme")
@click.option('--project-path', default='.', help='项目路径，默认为当前目录')
@click.option('--languages', help='要翻译的语言，用逗号分隔，如：zh,en,ja')
@click.option('--config', help='配置文件路径')
@click.option('--verbose', is_flag=True, help='显示详细输出')
@click.option('--debug', 'debug_mode', is_flag=True, help='启用调试模式，输出 DEBUG 级别日志')
def cli(project_path, languages, config, verbose, debug_mode):
    """
    DuoReadme - 多语言 README 生成工具
    
    一个强大的CLI工具，用于将项目代码和README自动翻译成多种语言并生成规范化的多语言文档。
    """
    # 直接调用 translate 命令的逻辑
    from .commands import run_translation_workflow
    from ..core.translator import Translator
    from ..core.parser import Parser
    from ..core.generator import Generator
    from ..utils.config import Config
    from ..utils.logger import enable_debug, debug
    
    try:
        # 根据 --debug 参数设置日志级别
        if debug_mode:
            enable_debug()
            debug("调试模式已启用")
        
        # 加载配置
        config_obj = Config(config)
        debug(f"配置文件路径: {config}")
        
        # 验证配置
        if not config_obj.validate():
            click.echo("错误: 配置验证失败", err=True)
            return
        
        # 创建核心组件
        translator = Translator(config_obj)
        parser_obj = Parser()
        generator = Generator()
        debug("核心组件初始化完成")
        
        # 显示开始信息
        click.echo("多语言 README 生成工具")
        click.echo("=" * 50)
        
        # 处理语言参数
        language_list = None
        if languages:
            language_list = [lang.strip() for lang in languages.split(',')]
            debug(f"目标语言: {language_list}")
        
        # 执行翻译流程
        run_translation_workflow(
            translator=translator,
            parser_obj=parser_obj,
            generator=generator,
            project_path=project_path,
            languages=language_list,
            verbose=verbose
        )
        
        click.echo("\n所有任务完成！")
        
    except Exception as e:
        click.echo(f"执行失败: {e}", err=True)
        if verbose or debug_mode:
            import traceback
            traceback.print_exc()


def main():
    """主函数 - CLI入口点"""
    cli()


if __name__ == "__main__":
    main() 