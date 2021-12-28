# Non-supported spotify locations 
SUPPORTED_REGIONS = ["AD", "AR", "AS", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "EC", "SV", "EE", "FI", "FR", 
                     "DE", "GR", "GT", "HN", "HU", "IS", "IN", "ID", "IE", "IL", "IT", "JP", "LV", "LI", "LT", "LU", "MY", "MT", "MX", "MC", "NL",
                     "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "RO", "RU", "SA", "SG", "SK", "ZA", "KR", "ES", "SE", "CH", "TW", "TH",
                     "TR", "AE", "UK", "US", "UY", "VN"]

# Written out for profile generation and webdriver input
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# List of email domains accessible with the Temp Mail API
DOMAINS = ['@mailkept.com', '@promail1.net', '@rcmails.com', '@relxv.com', '@folllo.com', '@fortuna7.com', '@invecra.com', '@linodg.com', '@awiners.com', '@subcaro.com']

# Webdriver information
WEBDRIVER = 'src/webdriver/chromedriver.exe'
PROXYLIST = "src/webdriver/proxy.json"
PROXYFARM = "https://proxylist.geonode.com/api/proxy-list?limit=200&page=1&sort_by=lastChecked&sort_type=desc&speed=fast"

# Sign up URLs for each country supported by Spotify
SIGN_UP_URL_AD = 'https://www.spotify.com/ad/signup'    # Andorra
SIGN_UP_URL_AR = 'https://www.spotify.com/ar/signup'    # Argentina
SIGN_UP_URL_AS = 'https://www.spotify.com/as/signup'    # Australia
SIGN_UP_URL_AT = 'https://www.spotify.com/at/signup'    # Austria
SIGN_UP_URL_BE = 'https://www.spotify.com/be/signup'    # Belgium
SIGN_UP_URL_BO = 'https://www.spotify.com/bo/signup'    # Bolivia
SIGN_UP_URL_BR = 'https://www.spotify.com/br/signup'    # Brazil
SIGN_UP_URL_BG = 'https://www.spotify.com/bg/signup'    # Bulgaria
SIGN_UP_URL_CA = 'https://www.spotify.com/ca/signup'    # Canada
SIGN_UP_URL_CL = 'https://www.spotify.com/cl/signup'    # Chile
SIGN_UP_URL_CO = 'https://www.spotify.com/co/signup'    # Colombia
SIGN_UP_URL_CR = 'https://www.spotify.com/cr/signup'    # Costa Rica
SIGN_UP_URL_CY = 'https://www.spotify.com/cy/signup'    # Cyprus
SIGN_UP_URL_CZ = 'https://www.spotify.com/cz/signup'    # Czech Republic
SIGN_UP_URL_DK = 'https://www.spotify.com/dk/signup'    # Denmark
SIGN_UP_URL_DO = 'https://www.spotify.com/do/signup'    # Dominican Republic
SIGN_UP_URL_EC = 'https://www.spotify.com/ec/signup'    # Ecuador
SIGN_UP_URL_SV = 'https://www.spotify.com/sv/signup'    # El Salvador
SIGN_UP_URL_EE = 'https://www.spotify.com/ee/signup'    # Ecuador
SIGN_UP_URL_FI = 'https://www.spotify.com/fi/signup'    # Finland
SIGN_UP_URL_FR = 'https://www.spotify.com/fr/signup'    # France
SIGN_UP_URL_DE = 'https://www.spotify.com/de/signup'    # Germany
SIGN_UP_URL_GR = 'https://www.spotify.com/gr/signup'    # Greece
SIGN_UP_URL_GT = 'https://www.spotify.com/gt/signup'    # Guatemala
SIGN_UP_URL_HN = 'https://www.spotify.com/hn/signup'    # Honduras
SIGN_UP_URL_HU = 'https://www.spotify.com/hu/signup'    # Hungary
SIGN_UP_URL_IS = 'https://www.spotify.com/is/signup'    # Iceland
SIGN_UP_URL_IN = 'https://www.spotify.com/in/signup'    # India
SIGN_UP_URL_ID = 'https://www.spotify.com/id/signup'    # Indonesia
SIGN_UP_URL_IE = 'https://www.spotify.com/ie/signup'    # Ireland
SIGN_UP_URL_IL = 'https://www.spotify.com/il/signup'    # Israel
SIGN_UP_URL_IT = 'https://www.spotify.com/it/signup'    # Italy
SIGN_UP_URL_JP = 'https://www.spotify.com/jp/signup'    # Japan
SIGN_UP_URL_LV = 'https://www.spotify.com/lv/signup'    # Latvia
SIGN_UP_URL_LI = 'https://www.spotify.com/li/signup'    # Liechtenstein
SIGN_UP_URL_LT = 'https://www.spotify.com/lt/signup'    # Lithuania
SIGN_UP_URL_LU = 'https://www.spotify.com/lu/signup'    # Luxembourg
SIGN_UP_URL_MY = 'https://www.spotify.com/my/signup'    # Malaysia
SIGN_UP_URL_MT = 'https://www.spotify.com/mt/signup'    # Malta
SIGN_UP_URL_MX = 'https://www.spotify.com/mx/signup'    # Mexico
SIGN_UP_URL_MC = 'https://www.spotify.com/mc/signup'    # Monaco
SIGN_UP_URL_NL = 'https://www.spotify.com/nl/signup'    # Netherlands
SIGN_UP_URL_NZ = 'https://www.spotify.com/nz/signup'    # New Zealand
SIGN_UP_URL_NI = 'https://www.spotify.com/ni/signup'    # Nicaragua
SIGN_UP_URL_NO = 'https://www.spotify.com/no/signup'    # Norway
SIGN_UP_URL_PA = 'https://www.spotify.com/pa/signup'    # Panama
SIGN_UP_URL_PY = 'https://www.spotify.com/py/signup'    # Paraguay
SIGN_UP_URL_PE = 'https://www.spotify.com/pe/signup'    # Peru
SIGN_UP_URL_PH = 'https://www.spotify.com/ph/signup'    # Philippines
SIGN_UP_URL_PL = 'https://www.spotify.com/pl/signup'    # Poland
SIGN_UP_URL_PT = 'https://www.spotify.com/pt/signup'    # Portugal
SIGN_UP_URL_RO = 'https://www.spotify.com/ro/signup'    # Romania
SIGN_UP_URL_RU = 'https://www.spotify.com/ru/signup'    # Russia
SIGN_UP_URL_SA = 'https://www.spotify.com/sa/signup'    # Saudi Arabia
SIGN_UP_URL_SG = 'https://www.spotify.com/sg/signup'    # Singapore
SIGN_UP_URL_SK = 'https://www.spotify.com/sk/signup'    # Slovakia
SIGN_UP_URL_ZA = 'https://www.spotify.com/za/signup'    # South Africa
SIGN_UP_URL_KR = 'https://www.spotify.com/kr/signup'    # South Korea
SIGN_UP_URL_ES = 'https://www.spotify.com/es/signup'    # Spain
SIGN_UP_URL_SE = 'https://www.spotify.com/se/signup'    # Sweden
SIGN_UP_URL_CH = 'https://www.spotify.com/ch/signup'    # Switzerland
SIGN_UP_URL_TW = 'https://www.spotify.com/tw/signup'    # Taiwan
SIGN_UP_URL_TH = 'https://www.spotify.com/th/signup'    # Thailand
SIGN_UP_URL_TR = 'https://www.spotify.com/tr/signup'    # Turkey
SIGN_UP_URL_AE = 'https://www.spotify.com/ae/signup'    # United Arab Emirates
SIGN_UP_URL_UK = 'https://www.spotify.com/uk/signup'    # United Kingdom
SIGN_UP_URL_US = 'https://www.spotify.com/us/signup'    # United States
SIGN_UP_URL_UY = 'https://www.spotify.com/uy/signup'    # Uruguay
SIGN_UP_URL_VN = 'https://www.spotify.com/vn/signup'    # Vietnam




