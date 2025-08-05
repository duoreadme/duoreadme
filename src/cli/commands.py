"""
CLI命令模块

提供各种CLI命令的实现。
"""

import click
from pathlib import Path
from ..core.translator import Translator
from ..core.parser import Parser
from ..core.generator import Generator
from ..utils.config import Config
from ..utils.logger import enable_debug, info, debug


@click.command()
@click.option('--project-path', default='.', help='项目路径，默认为当前目录')
@click.option('--languages', help='要翻译的语言，用逗号分隔，如：zh,en,ja')
@click.option('--config', help='配置文件路径')
@click.option('--verbose', is_flag=True, help='显示详细输出')
@click.option('--debug', 'debug_mode', is_flag=True, help='启用调试模式，输出 DEBUG 级别日志')
def translate_command(project_path, languages, config, verbose, debug_mode):
    """翻译项目并生成多语言README"""
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
        click.echo("🚀 多语言 README 生成工具")
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
        
        click.echo("\n🎉 所有任务完成！")
        
    except Exception as e:
        click.echo(f"❌ 执行失败: {e}", err=True)
        if verbose or debug_mode:
            import traceback
            traceback.print_exc()


def run_translation_workflow(
    translator: Translator,
    parser_obj: Parser,
    generator: Generator,
    project_path: str,
    languages: list = None,
    verbose: bool = False
):
    """执行翻译工作流程"""
    click.echo("📖 步骤 1: 运行翻译脚本")
    debug(f"开始翻译项目: {project_path}")
    
    # 翻译项目内容
    translation_response = translator.translate_project(project_path, languages)
    
    if not translation_response.success:
        click.echo(f"❌ 翻译失败: {translation_response.error}", err=True)
        debug(f"翻译失败详情: {translation_response.error}")
        return
    
    click.echo("✅ 翻译完成")
    debug("翻译响应处理完成")
    
    # 解析多语言README
    parsed_readme = parser_obj.parse_multilingual_content(
        translation_response.content, 
        languages
    )
    debug("多语言内容解析完成")
    
    # 生成README文件
    click.echo("\n🔍 步骤 2: 生成README文件")
    generation_result = generator.generate_readme_files(
        parsed_readme, 
        translation_response.raw_response
    )
    debug("README文件生成完成")
    
    # 生成总结报告
    click.echo("\n📊 步骤 3: 生成总结报告")
    summary = generator.generate_summary(generation_result)
    click.echo(summary)
    debug("总结报告生成完成")


@click.command()
@click.option('--config', help='配置文件路径')
@click.option('--debug', 'debug_mode', is_flag=True, help='启用调试模式，输出 DEBUG 级别日志')
def config_command(config, debug_mode):
    """显示配置信息"""
    try:
        # 根据 --debug 参数设置日志级别
        if debug_mode:
            enable_debug()
            debug("调试模式已启用")
        
        config_obj = Config(config)
        debug(f"配置文件路径: {config}")
        
        click.echo("当前配置:")
        click.echo("=" * 30)
        
        for section, values in config_obj.get_all().items():
            click.echo(f"\n[{section}]")
            for key, value in values.items():
                if isinstance(value, str) and len(value) > 50:
                    # 隐藏敏感信息
                    display_value = value[:10] + "..." if key in ['secret_id', 'secret_key', 'bot_app_key'] else value
                else:
                    display_value = value
                click.echo(f"  {key}: {display_value}")
                debug(f"配置项: [{section}].{key} = {display_value}")
        
    except Exception as e:
        click.echo(f"❌ 获取配置失败: {e}", err=True)
        if debug_mode:
            import traceback
            traceback.print_exc()





 