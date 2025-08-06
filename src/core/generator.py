"""
文档生成器模块

负责生成和保存多语言README文件。
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from ..utils.file_utils import FileUtils
from ..models.types import ParsedReadme, GenerationResult
from ..utils.logger import debug, info, warning, error


class Generator:
    """文档生成器类，负责生成和保存多语言README文件"""
    
    def __init__(self):
        """
        初始化生成器
        """
        self.output_dir = Path("docs")
        self.file_utils = FileUtils()
        debug("文档生成器初始化完成")
        
    def generate_readme_files(self, parsed_readme: ParsedReadme, raw_content: str = "") -> GenerationResult:
        """
        生成多语言README文件
        
        Args:
            parsed_readme: 解析后的README对象
            raw_content: 原始响应内容（不再保存）
            
        Returns:
            GenerationResult: 生成结果对象
        """
        debug(f"开始生成多语言README文件，共 {len(parsed_readme.content)} 种语言")
        
        # 确保输出目录存在
        self._ensure_output_directory()
        
        saved_files = []
        failed_files = []
        
        # 保存各语言的README文件
        for lang, content in parsed_readme.content.items():
            try:
                debug(f"正在生成 {lang} 语言的README文件")
                
                # 英文README放在根目录下
                if lang == "English" or lang == "en":
                    filename = "README.md"
                    filepath = Path(filename)
                    # 在英文README开头添加多语言说明
                    language_note = "> This is the English README. For other language versions, please see the [docs](./docs) directory.\n\n"
                    content = language_note + content
                    debug("英文README将保存到根目录")
                else:
                    # 其他语言放在docs目录下
                    filename = self._get_filename_for_language(lang)
                    filepath = self.output_dir / filename
                    debug(f"{lang} README将保存到: {filepath}")
                
                self.file_utils.write_text_file(filepath, content)
                saved_files.append({
                    "language": lang,
                    "filename": filename,
                    "filepath": str(filepath),
                    "size": len(content)
                })
                debug(f"✅ 成功保存 {lang} README文件 ({len(content)} 字符)")
            except Exception as e:
                failed_files.append({
                    "language": lang,
                    "filename": filename,
                    "error": str(e)
                })
                error(f"❌ 保存 {lang} README 失败: {e}")
                debug(f"保存失败详情: {e}")
        

        
        debug(f"README文件生成完成: 成功 {len(saved_files)} 个，失败 {len(failed_files)} 个")
        return GenerationResult(
            saved_files=saved_files,
            failed_files=failed_files,
            total_saved=len(saved_files),
            total_failed=len(failed_files)
        )
    
    def _ensure_output_directory(self):
        """确保输出目录存在"""
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
            debug(f"创建输出目录: {self.output_dir}")
        else:
            debug(f"输出目录已存在: {self.output_dir}")
    
    def _get_filename_for_language(self, language: str) -> str:
        """
        获取指定语言对应的文件名
        
        Args:
            language: 语言名称
            
        Returns:
            str: 对应的文件名
        """
        filename_map = {
            # 语言名称映射
            "中文": "README.zh.md",
            "繁體中文": "README.zh-Hant.md",
            "English": "README.md",  # 英文README放在根目录
            "en": "README.md",       # 支持简写形式
            "日本語": "README.ja.md",
            "한국어": "README.ko.md",
            "Français": "README.fr.md",
            "Deutsch": "README.de.md",
            "Español": "README.es.md",
            "Italiano": "README.it.md",
            "Português": "README.pt.md",
            "Português (Portugal)": "README.pt-PT.md",
            "Русский": "README.ru.md",
            "Tiếng Việt": "README.vi.md",
            "ไทย": "README.th.md",
            "हिन्दी": "README.hi.md",
            "العربية": "README.ar.md",
            "Türkçe": "README.tr.md",
            "Polski": "README.pl.md",
            "Nederlands": "README.nl.md",
            "Svenska": "README.sv.md",
            "Dansk": "README.da.md",
            "Norsk": "README.no.md",
            "Norsk Bokmål": "README.nb.md",
            "Suomi": "README.fi.md",
            "Čeština": "README.cs.md",
            "Slovenčina": "README.sk.md",
            "Magyar": "README.hu.md",
            "Română": "README.ro.md",
            "български": "README.bg.md",
            "Hrvatski": "README.hr.md",
            "Slovenščina": "README.sl.md",
            "Eesti": "README.et.md",
            "Latviešu": "README.lv.md",
            "Lietuvių": "README.lt.md",
            "Malti": "README.mt.md",
            "Ελληνικά": "README.el.md",
            "Català": "README.ca.md",
            "Euskara": "README.eu.md",
            "Galego": "README.gl.md",
            "Afrikaans": "README.af.md",
            "IsiZulu": "README.zu.md",
            "isiXhosa": "README.xh.md",
            "Sesotho": "README.st.md",
            "Kiswahili": "README.sw.md",
            "Èdè Yorùbá": "README.yo.md",
            "Asụsụ Igbo": "README.ig.md",
            "Hausa": "README.ha.md",
            "አማርኛ": "README.am.md",
            "ଓଡ଼ିଆ": "README.or.md",
            "বাংলা": "README.bn.md",
            "ગુજરાતી": "README.gu.md",
            "ਪੰਜਾਬੀ": "README.pa.md",
            "తెలుగు": "README.te.md",
            "ಕನ್ನಡ": "README.kn.md",
            "മലയാളം": "README.ml.md",
            "தமிழ்": "README.ta.md",
            "සිංහල": "README.si.md",
            "မြန်မာဘာသာ": "README.my.md",
            "ភាសាខ្មែរ": "README.km.md",
            "ລາວ": "README.lo.md",
            "नेपाली": "README.ne.md",
            "اردو": "README.ur.md",
            "فارسی": "README.fa.md",
            "پښتو": "README.ps.md",
            "سنڌي": "README.sd.md",
            "עברית": "README.he.md",
            "粵語": "README.yue.md",
            # 语言代码映射
            "zh": "README.zh.md",
            "zh-Hans": "README.zh.md",
            "zh-Hant": "README.zh-Hant.md",
            "ja": "README.ja.md",
            "ko": "README.ko.md",
            "fr": "README.fr.md",
            "de": "README.de.md",
            "es": "README.es.md",
            "it": "README.it.md",
            "pt": "README.pt.md",
            "pt-PT": "README.pt-PT.md",
            "ru": "README.ru.md",
            "th": "README.th.md",
            "vi": "README.vi.md",
            "hi": "README.hi.md",
            "ar": "README.ar.md",
            "tr": "README.tr.md",
            "pl": "README.pl.md",
            "nl": "README.nl.md",
            "sv": "README.sv.md",
            "da": "README.da.md",
            "no": "README.no.md",
            "nb": "README.nb.md",
            "fi": "README.fi.md",
            "cs": "README.cs.md",
            "sk": "README.sk.md",
            "hu": "README.hu.md",
            "ro": "README.ro.md",
            "bg": "README.bg.md",
            "hr": "README.hr.md",
            "sl": "README.sl.md",
            "et": "README.et.md",
            "lv": "README.lv.md",
            "lt": "README.lt.md",
            "mt": "README.mt.md",
            "el": "README.el.md",
            "ca": "README.ca.md",
            "eu": "README.eu.md",
            "gl": "README.gl.md",
            "af": "README.af.md",
            "zu": "README.zu.md",
            "xh": "README.xh.md",
            "st": "README.st.md",
            "sw": "README.sw.md",
            "yo": "README.yo.md",
            "ig": "README.ig.md",
            "ha": "README.ha.md",
            "am": "README.am.md",
            "or": "README.or.md",
            "bn": "README.bn.md",
            "gu": "README.gu.md",
            "pa": "README.pa.md",
            "te": "README.te.md",
            "kn": "README.kn.md",
            "ml": "README.ml.md",
            "ta": "README.ta.md",
            "si": "README.si.md",
            "my": "README.my.md",
            "km": "README.km.md",
            "lo": "README.lo.md",
            "ne": "README.ne.md",
            "ur": "README.ur.md",
            "fa": "README.fa.md",
            "ps": "README.ps.md",
            "sd": "README.sd.md",
            "he": "README.he.md",
            "yue": "README.yue.md"
        }
        
        return filename_map.get(language, f"README.{language.lower()}.md")
    
    def generate_summary(self, generation_result: GenerationResult) -> str:
        """
        生成总结报告
        
        Args:
            generation_result: 生成结果对象
            
        Returns:
            str: 总结报告文本
        """
        summary_lines = [
            "=" * 60,
            "项目生成和解析完成总结",
            "=" * 60,
            f"✓ {self.output_dir} 目录已创建",
            "生成的文件:"
        ]
        
        # 添加生成的文件信息
        for file_info in generation_result.saved_files:
            if file_info["language"] != "raw":
                location = "根目录" if file_info["filename"] == "README.md" else f"{self.output_dir}目录"
                summary_lines.append(f"  - {file_info['filename']} ({file_info['size']} bytes) - {location}")
        
        # 添加原始响应文件
        raw_files = [f for f in generation_result.saved_files if f["language"] == "raw"]
        for file_info in raw_files:
            summary_lines.append(f"  - {file_info['filename']} ({file_info['size']} bytes)")
        
        # 添加成功生成的语言列表
        languages = [f["language"] for f in generation_result.saved_files if f["language"] != "raw"]
        if languages:
            summary_lines.append(f"✓ 成功生成了 {len(languages)} 种语言的 README:")
            for lang in languages:
                summary_lines.append(f"  - {lang}")
        
        # 添加失败信息
        if generation_result.failed_files:
            summary_lines.append("失败的文件:")
            for file_info in generation_result.failed_files:
                summary_lines.append(f"  - {file_info['filename']}: {file_info['error']}")
        
        summary_lines.extend([
            "=" * 60,
            "任务完成！",
            "=" * 60
        ])
        
        return "\n".join(summary_lines)
    
    def cleanup_old_files(self, keep_languages: Optional[List[str]] = None):
        """
        清理旧的文件
        
        Args:
            keep_languages: 要保留的语言列表，如果为None则保留所有
        """
        if keep_languages is None:
            return
        
        # 获取要删除的文件
        files_to_delete = []
        for file_path in self.output_dir.glob("README.*.md"):
            lang = self._get_language_from_filename(file_path.name)
            if lang and lang not in keep_languages:
                files_to_delete.append(file_path)
        
        # 删除文件
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                print(f"已删除旧文件: {file_path}")
            except Exception as e:
                print(f"删除文件失败 {file_path}: {e}")
    
    def _get_language_from_filename(self, filename: str) -> Optional[str]:
        """
        从文件名获取语言
        
        Args:
            filename: 文件名
            
        Returns:
            Optional[str]: 语言名称，如果无法识别则返回None
        """
        filename_map = {
            "README.md": "English",      # 根目录的README.md是英文
            "README.zh.md": "中文",
            "README.zh-Hant.md": "繁體中文",
            "README.en.md": "English",   # 兼容旧格式
            "README.ja.md": "日本語",
            "README.ko.md": "한국어",
            "README.fr.md": "Français",
            "README.de.md": "Deutsch",
            "README.es.md": "Español",
            "README.it.md": "Italiano",
            "README.pt.md": "Português",
            "README.pt-PT.md": "Português (Portugal)",
            "README.ru.md": "Русский",
            "README.th.md": "ไทย",
            "README.vi.md": "Tiếng Việt",
            "README.hi.md": "हिन्दी",
            "README.ar.md": "العربية",
            "README.tr.md": "Türkçe",
            "README.pl.md": "Polski",
            "README.nl.md": "Nederlands",
            "README.sv.md": "Svenska",
            "README.da.md": "Dansk",
            "README.no.md": "Norsk",
            "README.nb.md": "Norsk Bokmål",
            "README.fi.md": "Suomi",
            "README.cs.md": "Čeština",
            "README.sk.md": "Slovenčina",
            "README.hu.md": "Magyar",
            "README.ro.md": "Română",
            "README.bg.md": "български",
            "README.hr.md": "Hrvatski",
            "README.sl.md": "Slovenščina",
            "README.et.md": "Eesti",
            "README.lv.md": "Latviešu",
            "README.lt.md": "Lietuvių",
            "README.mt.md": "Malti",
            "README.el.md": "Ελληνικά",
            "README.ca.md": "Català",
            "README.eu.md": "Euskara",
            "README.gl.md": "Galego",
            "README.af.md": "Afrikaans",
            "README.zu.md": "IsiZulu",
            "README.xh.md": "isiXhosa",
            "README.st.md": "Sesotho",
            "README.sw.md": "Kiswahili",
            "README.yo.md": "Èdè Yorùbá",
            "README.ig.md": "Asụsụ Igbo",
            "README.ha.md": "Hausa",
            "README.am.md": "አማርኛ",
            "README.or.md": "ଓଡ଼ିଆ",
            "README.bn.md": "বাংলা",
            "README.gu.md": "ગુજરાતી",
            "README.pa.md": "ਪੰਜਾਬੀ",
            "README.te.md": "తెలుగు",
            "README.kn.md": "ಕನ್ನಡ",
            "README.ml.md": "മലയാളം",
            "README.ta.md": "தமிழ்",
            "README.si.md": "සිංහල",
            "README.my.md": "မြန်မာဘာသာ",
            "README.km.md": "ភាសាខ្មែរ",
            "README.lo.md": "ລາວ",
            "README.ne.md": "नेपाली",
            "README.ur.md": "اردو",
            "README.fa.md": "فارسی",
            "README.ps.md": "پښتو",
            "README.sd.md": "سنڌي",
            "README.he.md": "עברית",
            "README.yue.md": "粵語"
        }
        
        return filename_map.get(filename) 