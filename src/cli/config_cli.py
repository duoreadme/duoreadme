"""
配置CLI命令模块

提供配置查看命令。
"""

import click
from ..utils.config import Config
from ..utils.logger import enable_debug, debug


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
        click.echo(f"获取配置失败: {e}", err=True)
        if debug_mode:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    config_command() 