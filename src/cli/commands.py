"""
CLI commands module

Provides implementations for various CLI commands.
"""

import click
from pathlib import Path
from ..core.translator import Translator
from ..core.parser import Parser
from ..core.generator import Generator
from ..utils.config import Config
from ..utils.logger import enable_debug, info, debug


@click.command()
@click.option('--project-path', default='.', help='Project path, defaults to current directory')
@click.option('--languages', help='Languages to generate, comma-separated, e.g.: zh-Hans,en,ja')
@click.option('--config', help='Configuration file path')
@click.option('--verbose', is_flag=True, help='Show detailed output')
@click.option('--debug', 'debug_mode', is_flag=True, help='Enable debug mode, output DEBUG level logs')
def gen_command(project_path, languages, config, verbose, debug_mode):
    """Generate multi-language README"""
    try:
        # Set log level based on --debug parameter
        if debug_mode:
            enable_debug()
            debug("Debug mode enabled")
        
        # Load configuration
        config_obj = Config(config)
        debug(f"Configuration file path: {config}")
        
        # Validate configuration
        if not config_obj.validate():
            click.echo("Error: Configuration validation failed", err=True)
            return
        
        # Create core components
        translator = Translator(config_obj)
        parser_obj = Parser()
        generator = Generator()
        debug("Core components initialized")
        
        # Display start information
        click.echo("=" * 50)
        
        # Process language parameters
        language_list = None
        if languages:
            language_list = [lang.strip() for lang in languages.split(',')]
            debug(f"Target languages: {language_list}")
        
        # Execute generation workflow
        run_translation_workflow(
            translator=translator,
            parser_obj=parser_obj,
            generator=generator,
            project_path=project_path,
            languages=language_list,
            verbose=verbose
        )
        
        click.echo("\nAll tasks completed!")
        
    except Exception as e:
        click.echo(f"❌ Execution failed: {e}", err=True)
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
    """Execute generation workflow"""
    debug(f"Starting project generation: {project_path}")
    
    # Generate project content
    translation_response = translator.translate_project(project_path, languages)
    
    if not translation_response.success:
        click.echo(f"❌ Generation failed: {translation_response.error}", err=True)
        debug(f"Generation failure details: {translation_response.error}")
        return
    
    debug("Generation response processing completed")
    
    # Parse multi-language README
    parsed_readme = parser_obj.parse_multilingual_content(
        translation_response.content, 
        languages
    )
    debug("Multi-language content parsing completed")
    
    # Generate README files
    click.echo("\nGenerating README files")
    generation_result = generator.generate_readme_files(
        parsed_readme, 
        translation_response.raw_response
    )
    debug("README file generation completed")
    
    # Generate summary report
    summary = generator.generate_summary(generation_result)
    click.echo(summary)
    debug("Summary report generation completed")


@click.command()
@click.option('--project-path', default='.', help='Project path, defaults to current directory')
@click.option('--languages', help='Languages to translate, comma-separated, e.g.: zh-Hans,en,ja')
@click.option('--config', help='Configuration file path')
@click.option('--verbose', is_flag=True, help='Show detailed output')
@click.option('--debug', 'debug_mode', is_flag=True, help='Enable debug mode, output DEBUG level logs')
def trans_command(project_path, languages, config, verbose, debug_mode):
    """Pure text translation function - translate README file in project root directory"""
    try:
        # Set log level based on --debug parameter
        if debug_mode:
            enable_debug()
            debug("Debug mode enabled")
        
        # Load configuration
        config_obj = Config(config)
        debug(f"Configuration file path: {config}")
        
        # Validate configuration
        if not config_obj.validate():
            click.echo("Error: Configuration validation failed", err=True)
            return
        
        # Create core components
        translator = Translator(config_obj)
        parser_obj = Parser()
        generator = Generator()
        debug("Core components initialized")
        
        # Display start information
        click.echo("=" * 50)
        click.echo("Starting pure text translation")
        click.echo("=" * 50)
        
        # Process language parameters
        language_list = None
        if languages:
            language_list = [lang.strip() for lang in languages.split(',')]
            debug(f"Target languages: {language_list}")
        
        # Execute translation workflow
        run_text_translation_workflow(
            translator=translator,
            parser_obj=parser_obj,
            generator=generator,
            project_path=project_path,
            languages=language_list,
            verbose=verbose
        )
        
        click.echo("\nTranslation completed!")
        
    except Exception as e:
        click.echo(f"❌ Translation failed: {e}", err=True)
        if verbose or debug_mode:
            import traceback
            traceback.print_exc()


def run_text_translation_workflow(
    translator: Translator,
    parser_obj: Parser,
    generator: Generator,
    project_path: str,
    languages: list = None,
    verbose: bool = False
):
    """Execute pure text translation workflow"""
    debug(f"Starting project translation: {project_path}")
    
    # Read README file in project root directory
    readme_content = translator._read_readme_file(project_path)
    
    if not readme_content:
        click.echo("❌ README file not found or read failed", err=True)
        return
    
    debug(f"Successfully read README file, length: {len(readme_content)} characters")
    
    # Execute pure text translation
    translation_response = translator.translate_text_only(readme_content, languages)
    
    if not translation_response.success:
        click.echo(f"❌ Translation failed: {translation_response.error}", err=True)
        debug(f"Translation failure details: {translation_response.error}")
        return
    
    debug("Translation response processing completed")
    
    # Parse multi-language README (same processing as gen command)
    parsed_readme = parser_obj.parse_multilingual_content(
        translation_response.content, 
        languages
    )
    debug("Multi-language content parsing completed")
    
    # Generate README files (same processing as gen command)
    click.echo("\nGenerating README files")
    generation_result = generator.generate_readme_files(
        parsed_readme, 
        translation_response.raw_response
    )
    debug("README file generation completed")
    
    # Generate summary report (same processing as gen command)
    summary = generator.generate_summary(generation_result)
    click.echo(summary)
    debug("Summary report generation completed")


@click.command()
@click.option('--config', help='Configuration file path')
@click.option('--debug', 'debug_mode', is_flag=True, help='Enable debug mode, output DEBUG level logs')
def config_command(config, debug_mode):
    """Display configuration information"""
    try:
        # Set log level based on --debug parameter
        if debug_mode:
            enable_debug()
            debug("Debug mode enabled")
        
        config_obj = Config(config)
        debug(f"Configuration file path: {config}")
        
        click.echo("Current configuration:")
        click.echo("=" * 30)
        
        for section, values in config_obj.get_all().items():
            click.echo(f"\n[{section}]")
            for key, value in values.items():
                if isinstance(value, str) and len(value) > 50:
                    # Hide sensitive information
                    display_value = value[:10] + "..." if key in ['secret_id', 'secret_key', 'bot_app_key'] else value
                else:
                    display_value = value
                click.echo(f"  {key}: {display_value}")
                debug(f"Configuration item: [{section}].{key} = {display_value}")
        
    except Exception as e:
        click.echo(f"❌ Failed to get configuration: {e}", err=True)
        if debug_mode:
            import traceback
            traceback.print_exc()
