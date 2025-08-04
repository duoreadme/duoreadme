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


@click.command()
@click.option('--project-path', default='.', help='项目路径，默认为当前目录')
@click.option('--languages', help='要翻译的语言，用逗号分隔，如：zh,en,ja')


@click.option('--config', help='配置文件路径')
@click.option('--verbose', is_flag=True, help='显示详细输出')
def translate_command(project_path, languages, config, verbose):
    """翻译项目并生成多语言README"""
    try:
        # 加载配置
        config_obj = Config(config)
        
        # 验证配置
        if not config_obj.validate():
            click.echo("错误: 配置验证失败", err=True)
            return
        
        # 创建核心组件
        translator = Translator(config_obj)
        parser_obj = Parser()
        generator = Generator()
        
        # 显示开始信息
        click.echo("🚀 多语言 README 生成工具")
        click.echo("=" * 50)
        
        # 处理语言参数
        language_list = None
        if languages:
            language_list = [lang.strip() for lang in languages.split(',')]
        
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
        if verbose:
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
    
    # 翻译项目内容
    translation_response = translator.translate_project(project_path, languages)
    
    if not translation_response.success:
        click.echo(f"❌ 翻译失败: {translation_response.error}", err=True)
        return
    
    click.echo("✅ 翻译完成")
    
    # 解析多语言README
    click.echo("正在解析多语言 README...")
    parsed_readme = parser_obj.parse_multilingual_content(
        translation_response.content, 
        languages
    )
    
    if parsed_readme.total_count == 0:
        click.echo("⚠️  未能解析到多语言 README 内容")
    
    # 生成README文件
    click.echo("\n🔍 步骤 2: 生成README文件")
    generation_result = generator.generate_readme_files(
        parsed_readme, 
        translation_response.raw_response
    )
    
    # 生成总结报告
    click.echo("\n📊 步骤 3: 生成总结报告")
    summary = generator.generate_summary(generation_result)
    click.echo(summary)


@click.command()
@click.option('--config', help='配置文件路径')
def config_command(config):
    """显示配置信息"""
    try:
        config_obj = Config(config)
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
        
    except Exception as e:
        click.echo(f"❌ 获取配置失败: {e}", err=True)





 