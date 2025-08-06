"""
Document generator module

Responsible for generating and saving multi-language README files.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from ..utils.file_utils import FileUtils
from ..models.types import ParsedReadme, GenerationResult
from ..utils.logger import debug, info, warning, error


class Generator:
    """Document generator class, responsible for generating and saving multi-language README files"""
    
    def __init__(self):
        """
        Initialize generator
        """
        self.output_dir = Path("docs")
        self.file_utils = FileUtils()
        debug("Document generator initialized")
        
    def generate_readme_files(self, parsed_readme: ParsedReadme, raw_content: str = "") -> GenerationResult:
        """
        Generate multi-language README files
        
        Args:
            parsed_readme: Parsed README object
            raw_content: Original response content (no longer saved)
            
        Returns:
            GenerationResult: Generation result object
        """
        debug(f"Starting to generate multi-language README files, {len(parsed_readme.content)} languages total")
        
        # Ensure output directory exists
        self._ensure_output_directory()
        
        saved_files = []
        failed_files = []
        
        # Save README files for each language
        for lang, content in parsed_readme.content.items():
            try:
                debug(f"Generating README file for {lang} language")
                
                # English README goes in root directory
                if lang == "English" or lang == "en":
                    filename = "README.md"
                    filepath = Path(filename)
                    # Add multi-language note at the beginning of English README
                    language_note = "> This is the English README. For other language versions, please see the [docs](./docs) directory.\n\n"
                    content = language_note + content
                    debug("English README will be saved to root directory")
                else:
                    # Other languages go in docs directory
                    filename = self._get_filename_for_language(lang)
                    filepath = self.output_dir / filename
                    debug(f"{lang} README will be saved to: {filepath}")
                
                self.file_utils.write_text_file(filepath, content)
                saved_files.append({
                    "language": lang,
                    "filename": filename,
                    "filepath": str(filepath),
                    "size": len(content)
                })
                debug(f"✅ Successfully saved {lang} README file ({len(content)} characters)")
            except Exception as e:
                failed_files.append({
                    "language": lang,
                    "filename": filename,
                    "error": str(e)
                })
                error(f"❌ Failed to save {lang} README: {e}")
                debug(f"Save failure details: {e}")
        

        
        debug(f"README file generation completed: {len(saved_files)} successful, {len(failed_files)} failed")
        return GenerationResult(
            saved_files=saved_files,
            failed_files=failed_files,
            total_saved=len(saved_files),
            total_failed=len(failed_files)
        )
    
    def _ensure_output_directory(self):
        """Ensure output directory exists"""
        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True)
            debug(f"Created output directory: {self.output_dir}")
        else:
            debug(f"Output directory already exists: {self.output_dir}")
    
    def _get_filename_for_language(self, language: str) -> str:
        """
        Get filename for specified language
        
        Args:
            language: Language name
            
        Returns:
            str: Corresponding filename
        """
        filename_map = {
            # Language name mapping
            "中文": "README.zh.md",
            "繁體中文": "README.zh-Hant.md",
            "English": "README.md",  # English README goes in root directory
            "en": "README.md",       # Support abbreviated form
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
            # Language code mapping
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
        Generate summary report
        
        Args:
            generation_result: Generation result object
            
        Returns:
            str: Summary report text
        """
        summary_lines = [
            "=" * 60,
            "Project generation and parsing completion summary",
            "=" * 60,
            f"✓ {self.output_dir} directory created",
            "Generated files:"
        ]
        
        # Add generated file information
        for file_info in generation_result.saved_files:
            if file_info["language"] != "raw":
                location = "root directory" if file_info["filename"] == "README.md" else f"{self.output_dir} directory"
                summary_lines.append(f"  - {file_info['filename']} ({file_info['size']} bytes) - {location}")
        
        # Add original response file
        raw_files = [f for f in generation_result.saved_files if f["language"] == "raw"]
        for file_info in raw_files:
            summary_lines.append(f"  - {file_info['filename']} ({file_info['size']} bytes)")
        
        # Add successfully generated language list
        languages = [f["language"] for f in generation_result.saved_files if f["language"] != "raw"]
        if languages:
            summary_lines.append(f"✓ Successfully generated README in {len(languages)} languages:")
            for lang in languages:
                summary_lines.append(f"  - {lang}")
        
        # Add failure information
        if generation_result.failed_files:
            summary_lines.append("Failed files:")
            for file_info in generation_result.failed_files:
                summary_lines.append(f"  - {file_info['filename']}: {file_info['error']}")
        
        summary_lines.extend([
            "=" * 60,
            "Task completed!",
            "=" * 60
        ])
        
        return "\n".join(summary_lines)
    
    def cleanup_old_files(self, keep_languages: Optional[List[str]] = None):
        """
        Clean up old files
        
        Args:
            keep_languages: List of languages to keep, if None then keep all
        """
        if keep_languages is None:
            return
        
        # Get files to delete
        files_to_delete = []
        for file_path in self.output_dir.glob("README.*.md"):
            lang = self._get_language_from_filename(file_path.name)
            if lang and lang not in keep_languages:
                files_to_delete.append(file_path)
        
        # Delete files
        for file_path in files_to_delete:
            try:
                file_path.unlink()
                print(f"Deleted old file: {file_path}")
            except Exception as e:
                print(f"Failed to delete file {file_path}: {e}")
    
    def _get_language_from_filename(self, filename: str) -> Optional[str]:
        """
        Get language from filename
        
        Args:
            filename: Filename
            
        Returns:
            Optional[str]: Language name, returns None if unrecognizable
        """
        filename_map = {
            "README.md": "English",      # README.md in root directory is English
            "README.zh.md": "中文",
            "README.zh-Hant.md": "繁體中文",
            "README.en.md": "English",   # Compatible with old format
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