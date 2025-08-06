"""
Language code mapping module

Provides mapping for all supported language codes and corresponding language names.
"""

# Language code to language name mapping
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

# Common language codes (recommended for use)
COMMON_LANGUAGES = [
    "zh-Hans",  # Chinese (Simplified)
    "en",       # English
    "ja",       # Japanese
    "ko",       # Korean
    "fr",       # French
    "de",       # German
    "es",       # Spanish
    "it",       # Italian
    "pt",       # Portuguese (Brazil)
    "ru",       # Russian
    "ar",       # Arabic
    "hi",       # Hindi
    "th",       # Thai
    "vi",       # Vietnamese
    "tr",       # Turkish
    "pl",       # Polish
    "nl",       # Dutch
    "sv",       # Swedish
    "da",       # Danish
    "no"        # Norwegian
]

def get_language_name(code: str) -> str:
    """
    Get language name corresponding to language code
    
    Args:
        code: Language code
        
    Returns:
        Language name, returns the code itself if code doesn't exist
    """
    return LANGUAGE_CODES.get(code, code)

def get_all_language_codes() -> list:
    """
    Get all supported language codes
    
    Returns:
        List of language codes
    """
    return list(LANGUAGE_CODES.keys())

def get_common_language_codes() -> list:
    """
    Get common language codes
    
    Returns:
        List of common language codes
    """
    return COMMON_LANGUAGES.copy()

def is_valid_language_code(code: str) -> bool:
    """
    Check if language code is valid
    
    Args:
        code: Language code
        
    Returns:
        Whether it's valid
    """
    return code in LANGUAGE_CODES 