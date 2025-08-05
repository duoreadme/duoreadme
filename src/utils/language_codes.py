"""
语言代码映射模块

提供所有支持的语言代码和对应的语言名称映射。
"""

# 语言代码到语言名称的映射
LANGUAGE_CODES = {
    "af": "Afrikaans",
    "am": "አማርኛ",
    "ar": "العربية",
    "as": "অসমীয়া",
    "az": "Azərbaycanca",
    "ba": "Bashkir",
    "bg": "български",
    "bho": "Bhojpuri",
    "bn": "বাংলা",
    "bo": "བོད་ཡིག",
    "brx": "বড়ো",
    "bs": "Bosnian",
    "ca": "Català",
    "cs": "Čeština",
    "cy": "Cymraeg",
    "da": "Dansk",
    "de": "Deutsch",
    "doi": "Dogri",
    "dsb": "Dolnoserbski",
    "dv": "ދިވެހި",
    "el": "Ελληνικά",
    "en": "English",
    "es": "Español",
    "et": "Eesti",
    "eu": "Euskara",
    "fa": "فارسی",
    "fi": "Suomi",
    "fil": "Filipino",
    "fj": "Na Vosa Vakaviti",
    "fo": "Føroyskt",
    "fr": "Français",
    "fr-CA": "Français (Canada)",
    "ga": "Gaeilge",
    "gl": "Galego",
    "gom": "Konkani",
    "gu": "ગુજરાતી",
    "ha": "Hausa",
    "he": "עברית",
    "hi": "हिन्दी",
    "hne": "Chhattisgarhi",
    "hr": "Hrvatski",
    "hsb": "Hornjoserbsce",
    "ht": "Haitian Creole",
    "hu": "Magyar",
    "hy": "Հայերեն",
    "id": "Indonesia",
    "ig": "Asụsụ Igbo",
    "ikt": "Inuinnaqtun",
    "is": "Íslenska",
    "it": "Italiano",
    "iu": "ᐃᓄᒃᑎᑐᑦ",
    "iu-Latin": "Inuktitut (Latin)",
    "ja": "日本語",
    "ka": "ქართული",
    "kk": "Қазақ Тілі",
    "km": "ភាសាខ្មែរ",
    "kmr": "Kurdî (Bakur)",
    "kn": "ಕನ್ನಡ",
    "ko": "한국어",
    "ks": "कश्मीरी",
    "ku": "Kurdî (Navîn)",
    "ky": "Кыргызча",
    "ln": "Lingála",
    "lo": "ລາວ",
    "lt": "Lietuvių",
    "lug": "Ganda",
    "lv": "Latviešu",
    "lzh": "中文 (文言文)",
    "mai": "Maithili",
    "mg": "Malagasy",
    "mi": "Te Reo Māori",
    "mk": "македонски",
    "ml": "മലയാളം",
    "mn-Cyrl": "Mongolian (Cyrillic)",
    "mn-Mong": "монгол (Монгол)",
    "mni": "মণিপুরী",
    "mr": "मराठी",
    "ms": "Melayu",
    "mt": "Malti",
    "mww": "Hmong Daw",
    "my": "မြန်မာဘာသာ",
    "nb": "Norsk Bokmål",
    "ne": "नेपाली",
    "nl": "Nederlands",
    "nso": "Sesotho sa Leboa",
    "nya": "Nyanja",
    "or": "ଓଡ଼ିଆ",
    "otq": "Hãhãhũ",
    "pa": "ਪੰਜਾਬੀ",
    "pl": "Polski",
    "prs": "دری",
    "ps": "پښتو",
    "pt": "Português (Brasil)",
    "pt-PT": "Português (Portugal)",
    "ro": "Română",
    "ru": "Русский",
    "run": "Rundi",
    "rw": "Kinyarwanda",
    "sd": "سنڌي",
    "si": "සිංහල",
    "sk": "Slovenčina",
    "sl": "Slovenščina",
    "sm": "Gagana Samoa",
    "sn": "chiShona",
    "so": "Soomaali",
    "sq": "Shqip",
    "sr-Cyrl": "Српски (ћирилица)",
    "sr-Latin": "Srpski (latinica)",
    "st": "Sesotho",
    "sv": "Svenska",
    "sw": "Kiswahili",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "th": "ไทย",
    "ti": "ትግርኛ",
    "tk": "Türkmen Dili",
    "tlh-Latin": "Klingon (Latin)",
    "tlh-Piqd": "Klingon (pIqaD)",
    "tn": "Setswana",
    "to": "Lea Fakatonga",
    "tr": "Türkçe",
    "tt": "Татарча",
    "ty": "Reo Tahiti",
    "ug": "ئۇيغۇرچە",
    "uk": "Українська",
    "ur": "اردو",
    "uz": "Uzbek (Latin)",
    "vi": "Tiếng Việt",
    "xh": "isiXhosa",
    "yo": "Èdè Yorùbá",
    "yua": "Yucatec Maya",
    "yue": "粵語 (繁體)",
    "zh-Hans": "中文 (简体)",
    "zh-Hant": "繁體中文 (繁體)",
    "zu": "IsiZulu"
}

# 常用语言代码（推荐使用）
COMMON_LANGUAGES = [
    "zh-Hans",  # 中文 (简体)
    "en",       # English
    "ja",       # 日本語
    "ko",       # 한국어
    "fr",       # Français
    "de",       # Deutsch
    "es",       # Español
    "it",       # Italiano
    "pt",       # Português (Brasil)
    "ru",       # Русский
    "ar",       # العربية
    "hi",       # हिन्दी
    "th",       # ไทย
    "vi",       # Tiếng Việt
    "tr",       # Türkçe
    "pl",       # Polski
    "nl",       # Nederlands
    "sv",       # Svenska
    "da",       # Dansk
    "no"        # Norsk
]

def get_language_name(code: str) -> str:
    """
    获取语言代码对应的语言名称
    
    Args:
        code: 语言代码
        
    Returns:
        语言名称，如果代码不存在则返回代码本身
    """
    return LANGUAGE_CODES.get(code, code)

def get_all_language_codes() -> list:
    """
    获取所有支持的语言代码
    
    Returns:
        语言代码列表
    """
    return list(LANGUAGE_CODES.keys())

def get_common_language_codes() -> list:
    """
    获取常用语言代码
    
    Returns:
        常用语言代码列表
    """
    return COMMON_LANGUAGES.copy()

def is_valid_language_code(code: str) -> bool:
    """
    检查语言代码是否有效
    
    Args:
        code: 语言代码
        
    Returns:
        是否有效
    """
    return code in LANGUAGE_CODES 