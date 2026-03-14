#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   Macost — Оценка стоимости MacBook          ║
║   Циклы батареи • Процессор • Цена           ║
╚══════════════════════════════════════════════╝
"""

import subprocess
import re
import sys
import os
import platform
import json
import urllib.request
from datetime import datetime

# ─── Автоустановка зависимостей ─────────────────────────────────────────
try:
    import customtkinter as ctk
except ImportError:
    print("⏳ Установка customtkinter...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk


# ════════════════════════════════════════════════════════════════════════
#  ЛОКАЛИЗАЦИЯ
# ════════════════════════════════════════════════════════════════════════

LANG = {
    "ru": {
        # ── Заголовок ──
        "app_title":        "Macost — Оценка стоимости Mac",
        "subtitle":         "оценка стоимости Mac",

        # ── Устройство ──
        "device":           "💻  Устройство",
        "model":            "Модель",
        "identifier":       "Идентификатор",
        "processor":        "Процессор",
        "cores":            "Ядра",
        "memory":           "Память (RAM)",
        "storage":          "Накопитель",
        "serial":           "Серийный номер",

        # ── Система ──
        "system":           "⚙️  Система",
        "macos":            "macOS",
        "year":             "Год выпуска",

        # ── Аккумулятор ──
        "battery":          "🔋  Аккумулятор",
        "cycles":           "Циклы зарядки",
        "battery_health":   "Здоровье батареи",
        "max_capacity":     "Макс. ёмкость",
        "design_capacity":  "Заводская ёмкость",
        "condition_apple":  "Состояние (Apple)",
        "status":           "Статус",
        "health_label":     "Здоровье батареи",
        "mah":              "мАч",

        # ── Статусы зарядки ──
        "fully_charged":    "⚡ Полностью заряжен",
        "charging":         "⚡ Заряжается",
        "plugged":          "🔌 Подключён",
        "on_battery":       "🔋 От батареи",

        # ── Состояния ──
        "excellent":        "Отличное",
        "good":             "Хорошее",
        "fair":             "Среднее",
        "worn":             "Изношенное",
        "poor":             "Требует замены батареи",

        # ── Цена ──
        "price_title":      "💰  Оценка стоимости",
        "rate_prefix":      "Курс ЦБ РФ:",

        # ── Кнопки ──
        "refresh":          "🔄  Обновить",
        "copy_report":      "📋  Копировать отчёт",
        "copied_toast":     "✅  Отчёт скопирован в буфер обмена",

        # ── Футер ──
        "disclaimer":       "⚠️  Цены приблизительны и основаны на средних рыночных данных.\n"
                            "Реальная стоимость зависит от внешнего состояния, комплектации и региона.",

        # ── Отчёт ──
        "report_header":    "═══ Macost — Отчёт ═══",
        "report_model":     "Модель:",
        "report_id":        "Идентиф.:",
        "report_cpu":       "Процессор:",
        "report_cores":     "Ядра:",
        "report_memory":    "Память:",
        "report_storage":   "Накопитель:",
        "report_year":      "Год выпуска:",
        "report_macos":     "macOS:",
        "report_cycles":    "Циклы:",
        "report_health":    "Здоровье:",
        "report_condition": "Состояние:",
        "report_price_usd": "Цена (USD):",
        "report_price_rub": "Цена (RUB):",
        "report_rate":      "Курс:",
        "report_date":      "Дата:",
        "report_footer":    "══════════════════════",

        # ── Язык ──
        "lang_btn":         "🇬🇧 EN",
    },

    "en": {
        # ── Header ──
        "app_title":        "Macost — Mac Value Estimator",
        "subtitle":         "Mac value estimator",

        # ── Device ──
        "device":           "💻  Device",
        "model":            "Model",
        "identifier":       "Identifier",
        "processor":        "Processor",
        "cores":            "Cores",
        "memory":           "Memory (RAM)",
        "storage":          "Storage",
        "serial":           "Serial Number",

        # ── System ──
        "system":           "⚙️  System",
        "macos":            "macOS",
        "year":             "Year",

        # ── Battery ──
        "battery":          "🔋  Battery",
        "cycles":           "Charge Cycles",
        "battery_health":   "Battery Health",
        "max_capacity":     "Max Capacity",
        "design_capacity":  "Design Capacity",
        "condition_apple":  "Condition (Apple)",
        "status":           "Status",
        "health_label":     "Battery Health",
        "mah":              "mAh",

        # ── Charge statuses ──
        "fully_charged":    "⚡ Fully Charged",
        "charging":         "⚡ Charging",
        "plugged":          "🔌 Plugged In",
        "on_battery":       "🔋 On Battery",

        # ── Conditions ──
        "excellent":        "Excellent",
        "good":             "Good",
        "fair":             "Fair",
        "worn":             "Worn",
        "poor":             "Battery Replacement Needed",

        # ── Price ──
        "price_title":      "💰  Price Estimate",
        "rate_prefix":      "Exchange rate:",

        # ── Buttons ──
        "refresh":          "🔄  Refresh",
        "copy_report":      "📋  Copy Report",
        "copied_toast":     "✅  Report copied to clipboard",

        # ── Footer ──
        "disclaimer":       "⚠️  Prices are approximate and based on average market data.\n"
                            "Actual value depends on physical condition, accessories, and region.",

        # ── Report ──
        "report_header":    "═══ Macost — Report ═══",
        "report_model":     "Model:",
        "report_id":        "Identifier:",
        "report_cpu":       "Processor:",
        "report_cores":     "Cores:",
        "report_memory":    "Memory:",
        "report_storage":   "Storage:",
        "report_year":      "Year:",
        "report_macos":     "macOS:",
        "report_cycles":    "Cycles:",
        "report_health":    "Health:",
        "report_condition": "Condition:",
        "report_price_usd": "Price (USD):",
        "report_price_rub": "Price (RUB):",
        "report_rate":      "Rate:",
        "report_date":      "Date:",
        "report_footer":    "═══════════════════════",

        # ── Language ──
        "lang_btn":         "🇷🇺 RU",
    },
}


# ════════════════════════════════════════════════════════════════════════
#  СБОР ИНФОРМАЦИИ О СИСТЕМЕ
# ════════════════════════════════════════════════════════════════════════

class MacInfo:
    """Собирает всю информацию о Mac через системные утилиты"""

    def __init__(self):
        self.data = {}
        if platform.system() == "Darwin":
            self._collect()
        else:
            self._demo_data()

    def _cmd(self, command: str) -> str:
        try:
            env = os.environ.copy()
            env["LANG"] = "en_US.UTF-8"
            r = subprocess.run(
                command, shell=True,
                capture_output=True, text=True,
                timeout=15, env=env
            )
            return r.stdout.strip()
        except Exception:
            return ""

    def _collect(self):
        self._hardware()
        self._battery()
        self._storage()
        self._system()

    def _hardware(self):
        hw = self._cmd("system_profiler SPHardwareDataType")

        fields = {
            "model_name":   r"Model Name:\s*(.+)",
            "model_id":     r"Model Identifier:\s*(.+)",
            "chip":         r"Chip:\s*(.+)",
            "processor":    r"Processor Name:\s*(.+)",
            "cores":        r"Total Number of Cores:\s*(.+)",
            "memory":       r"Memory:\s*(.+)",
            "serial":       r"Serial Number.*?:\s*(.+)",
            "model_number": r"Model Number:\s*(.+)",
        }

        for key, pattern in fields.items():
            m = re.search(pattern, hw)
            self.data[key] = m.group(1).strip() if m else None

        self.data["cpu"] = (
            self.data.get("chip")
            or self.data.get("processor")
            or "Unknown"
        )

        mem_str = self.data.get("memory") or ""
        m = re.search(r"(\d+)\s*GB", mem_str)
        self.data["ram_gb"] = int(m.group(1)) if m else 8

    def _battery(self):
        raw = self._cmd('ioreg -r -c "AppleSmartBattery"')

        def ival(key):
            m = re.search(rf'"{key}"\s*=\s*(\d+)', raw)
            return int(m.group(1)) if m else None

        def bval(key):
            m = re.search(rf'"{key}"\s*=\s*(Yes|No)', raw)
            return m.group(1) == "Yes" if m else False

        self.data["cycles"] = ival("CycleCount") or 0

        # ── Здоровье батареи (несколько стратегий) ──────────────────

        max_cap     = ival("MaxCapacity")
        raw_max     = ival("AppleRawMaxCapacity")
        design_cap  = ival("DesignCapacity")
        nominal     = ival("NominalChargeCapacity")

        health = None

        # Стратегия 1: system_profiler (самый надёжный)
        power = self._cmd("system_profiler SPPowerDataType")
        m = re.search(r"Maximum Capacity:\s*(\d+)\s*%", power)
        if m:
            health = float(m.group(1))

        # Стратегия 2: AppleRawMaxCapacity / DesignCapacity
        if health is None and raw_max and design_cap and design_cap > 100:
            health = round(raw_max / design_cap * 100, 1)

        # Стратегия 3: NominalChargeCapacity / DesignCapacity
        if health is None and nominal and design_cap and design_cap > 100:
            health = round(nominal / design_cap * 100, 1)

        # Стратегия 4: MaxCapacity (определяем — проценты или мАч)
        if health is None and max_cap is not None:
            if design_cap and design_cap > 500 and max_cap <= 110:
                health = float(max_cap)
            elif design_cap and design_cap > 0 and max_cap > 110:
                health = round(max_cap / design_cap * 100, 1)
            else:
                health = float(max_cap) if max_cap <= 110 else 100.0

        if health is None:
            health = 100.0

        self.data["battery_health"] = min(health, 100.0)

        # Ёмкости в мАч
        actual_mah = (
            raw_max
            or nominal
            or (max_cap if max_cap and max_cap > 110 else None)
            or (round(design_cap * health / 100) if design_cap else None)
            or 0
        )
        self.data["max_capacity_mah"]     = actual_mah
        self.data["design_capacity_mah"]  = design_cap or 0
        self.data["current_capacity_mah"] = ival("CurrentCapacity") or 0

        self.data["charging"]      = bval("IsCharging")
        self.data["plugged"]       = bval("ExternalConnected")
        self.data["fully_charged"] = bval("FullyCharged")

        m = re.search(r"Condition:\s*(.+)", power)
        self.data["apple_condition"] = m.group(1).strip() if m else "N/A"

    def _storage(self):
        raw = self._cmd("diskutil info disk0")
        m = re.search(r"Disk Size:\s*([\d.]+)\s*(GB|TB)", raw)
        if m:
            size = float(m.group(1))
            unit = m.group(2)
            self.data["storage_gb"] = int(size * 1000) if unit == "TB" else int(size)
            self.data["storage_str"] = f"{m.group(1)} {unit}"
        else:
            raw2 = self._cmd("system_profiler SPStorageDataType")
            m = re.search(r"Capacity:\s*([\d.,]+)\s*(GB|TB)", raw2)
            if m:
                size = float(m.group(1).replace(",", "."))
                unit = m.group(2)
                self.data["storage_gb"] = int(size * 1000) if unit == "TB" else int(size)
                self.data["storage_str"] = f"{size:.0f} {unit}"
            else:
                self.data["storage_gb"] = 256
                self.data["storage_str"] = "N/A"

    def _system(self):
        self.data["macos_ver"]   = self._cmd("sw_vers -productVersion")
        self.data["macos_build"] = self._cmd("sw_vers -buildVersion")
        self.data["year"]        = self._detect_year()

    def _detect_year(self) -> int:
        mid = self.data.get("model_id") or ""

        TABLE = [
            ("Mac16", 2024),
            ("Mac15,12", 2024), ("Mac15,13", 2024),
            ("Mac15", 2023), ("Mac14,15", 2023),
            ("Mac14,5", 2023), ("Mac14,6", 2023),
            ("Mac14,9", 2023), ("Mac14,10", 2023),
            ("Mac14,2", 2022), ("Mac14,7", 2022),
            ("MacBookPro18", 2021),
            ("MacBookPro17", 2020), ("MacBookAir10", 2020),
            ("MacBookPro16,2", 2020), ("MacBookPro16,3", 2020),
            ("MacBookAir9", 2020),
            ("MacBookPro16", 2019), ("MacBookPro15,4", 2019),
            ("MacBookPro15", 2018), ("MacBookAir8", 2018),
            ("MacBookPro14", 2017), ("MacBookAir7", 2017),
            ("MacBookPro13", 2016),
            ("MacBookPro12", 2015), ("MacBookPro11,4", 2015),
            ("MacBookPro11,5", 2015),
            ("MacBookPro11", 2013), ("MacBookAir6", 2013),
            ("MacBookPro10", 2012),
        ]

        for prefix, year in TABLE:
            if mid.startswith(prefix):
                return year
        return 2020

    def _demo_data(self):
        self.data = {
            "model_name": "MacBook Pro",
            "model_id": "MacBookPro17,1",
            "cpu": "Apple M1",
            "chip": "Apple M1",
            "processor": None,
            "cores": "8 (4 Performance and 4 Efficiency)",
            "memory": "16 GB",
            "ram_gb": 16,
            "serial": "C02ZM1XXXXX",
            "model_number": "MYD92",
            "storage_str": "512 GB",
            "storage_gb": 512,
            "cycles": 83,
            "battery_health": 94.2,
            "max_capacity_mah": 4800,
            "design_capacity_mah": 5103,
            "current_capacity_mah": 4500,
            "apple_condition": "Normal",
            "charging": False,
            "plugged": True,
            "fully_charged": False,
            "macos_ver": "14.5",
            "macos_build": "23F79",
            "year": 2020,
        }

    def get(self, key, default="N/A"):
        v = self.data.get(key)
        return v if v is not None else default


# ════════════════════════════════════════════════════════════════════════
#  КУРС ВАЛЮТ
# ════════════════════════════════════════════════════════════════════════

def fetch_usd_rate() -> float:
    try:
        req = urllib.request.Request(
            "https://www.cbr-xml-daily.ru/daily_json.js",
            headers={"User-Agent": "Macost/1.0"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return round(data["Valute"]["USD"]["Value"], 2)
    except Exception:
        return 96.0


# ════════════════════════════════════════════════════════════════════════
#  ОЦЕНКА СТОИМОСТИ
# ════════════════════════════════════════════════════════════════════════

class PriceEstimator:

    BASE = {
        ("air", "m3", 2024): 950,
        ("air", "m2", 2023): 780, ("air", "m2", 2022): 700,
        ("air", "m1", 2020): 500,
        ("air", "intel", 2020): 350, ("air", "intel", 2019): 300,
        ("air", "intel", 2018): 250, ("air", "intel", 2017): 180,
        ("pro", "m4 max", 2024): 2200, ("pro", "m4 pro", 2024): 1600,
        ("pro", "m4", 2024): 1200,
        ("pro", "m3 max", 2023): 2000, ("pro", "m3 pro", 2023): 1400,
        ("pro", "m3", 2023): 1000,
        ("pro", "m2 max", 2023): 1600, ("pro", "m2 pro", 2023): 1200,
        ("pro", "m2", 2022): 750,
        ("pro", "m1 max", 2021): 1350, ("pro", "m1 pro", 2021): 1050,
        ("pro", "m1", 2020): 620,
        ("pro", "intel", 2020): 480, ("pro", "intel", 2019): 420,
        ("pro", "intel", 2018): 350, ("pro", "intel", 2017): 280,
        ("pro", "intel", 2016): 230, ("pro", "intel", 2015): 190,
    }

    RAM_K  = {8:1.0, 16:1.12, 18:1.15, 24:1.22, 32:1.32,
              36:1.36, 48:1.48, 64:1.65, 96:1.85, 128:2.05}
    DISK_K = {128:0.92, 256:1.0, 512:1.08, 1000:1.22,
              2000:1.40, 4000:1.65, 8000:1.90}

    def __init__(self, info: MacInfo, rate: float):
        self.info = info
        self.rate = rate

    def condition(self):
        cyc = self.info.get("cycles", 0)
        hp  = self.info.get("battery_health", 100)
        if cyc <= 100 and hp >= 95:
            return "excellent"
        if cyc <= 300 and hp >= 85:
            return "good"
        if cyc <= 600 and hp >= 75:
            return "fair"
        if cyc <= 900 and hp >= 60:
            return "worn"
        return "poor"

    def condition_color(self):
        colors = {
            "excellent": "#34C759",
            "good":      "#30D158",
            "fair":      "#FF9500",
            "worn":      "#FF6B00",
            "poor":      "#FF3B30",
        }
        return colors[self.condition()]

    def estimate(self) -> dict:
        base = self._base_price()
        cond_k = {"excellent":1.10, "good":1.0,
                  "fair":0.85, "worn":0.70, "poor":0.55}
        ck = cond_k[self.condition()]

        ram  = self.info.get("ram_gb", 8)
        disk = self.info.get("storage_gb", 256)

        price = base * ck * self._near(ram, self.RAM_K) * self._near(disk, self.DISK_K)
        usd = round(price / 10) * 10
        rub = round(usd * self.rate / 100) * 100

        return dict(
            usd=usd, rub=rub,
            usd_lo=round(usd * 0.85 / 10) * 10,
            usd_hi=round(usd * 1.15 / 10) * 10,
            rub_lo=round(usd * 0.85 * self.rate / 100) * 100,
            rub_hi=round(usd * 1.15 * self.rate / 100) * 100,
        )

    def _base_price(self) -> int:
        model = (self.info.get("model_name", "") or "").lower()
        cpu   = (self.info.get("cpu", "") or "").lower()
        year  = self.info.get("year", 2020)

        mtype = "pro" if "pro" in model else "air"

        chips = ["m4 max","m4 pro","m4","m3 max","m3 pro","m3",
                 "m2 max","m2 pro","m2","m1 max","m1 pro","m1","intel"]
        chip = "intel"
        for c in chips:
            if c in cpu:
                chip = c
                break

        for dy in [0, 1, -1, 2, -2]:
            key = (mtype, chip, year + dy)
            if key in self.BASE:
                return self.BASE[key]

        age = max(0, datetime.now().year - year)
        return max(150, (1200 if mtype == "pro" else 800) - age * 130)

    @staticmethod
    def _near(val, table):
        closest = min(table, key=lambda x: abs(x - val))
        return table[closest]


# ════════════════════════════════════════════════════════════════════════
#  ИНТЕРФЕЙС
# ════════════════════════════════════════════════════════════════════════

class MacostApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.lang = "ru"
        self.geometry("720x920")
        self.minsize(620, 700)
        self.title(self.t("app_title"))

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.info       = MacInfo()
        self.rate        = fetch_usd_rate()
        self.estimator   = PriceEstimator(self.info, self.rate)

        # Контейнер-обёртка (именно его будем уничтожать)
        self.container = None
        self.main      = None

        self._build_ui()

    # ── Перевод ─────────────────────────────────────────────────────────

    def t(self, key: str) -> str:
        return LANG.get(self.lang, LANG["en"]).get(key, key)

    # ── Полная пересборка UI ────────────────────────────────────────────

    def _build_ui(self):
        # Уничтожаем ВСЕ дочерние виджеты окна
        for widget in self.winfo_children():
            widget.destroy()

        self.title(self.t("app_title"))

        # Новый контейнер на всё окно
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Скроллируемая область внутри контейнера
        self.main = ctk.CTkScrollableFrame(
            self.container, fg_color="transparent"
        )
        self.main.pack(fill="both", expand=True, padx=24, pady=(20, 10))

        self._header()
        self._card_device()
        self._card_system()
        self._card_battery()
        self._card_price()
        self._footer()

    # ── Заголовок ───────────────────────────────────────────────────────

    def _header(self):
        fr = ctk.CTkFrame(self.main, fg_color="transparent")
        fr.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            fr, text="🍎  Macost",
            font=ctk.CTkFont(size=34, weight="bold"),
        ).pack(side="left")

        ctk.CTkLabel(
            fr, text=self.t("subtitle"),
            font=ctk.CTkFont(size=14), text_color="gray",
        ).pack(side="left", padx=(14, 0), pady=(12, 0))

        # Кнопка языка
        ctk.CTkButton(
            fr, text=self.t("lang_btn"),
            width=56, height=36, corner_radius=18,
            fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35"),
            text_color=("gray20", "gray90"),
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._toggle_lang,
        ).pack(side="right", padx=(6, 0))

        # Кнопка темы
        self.theme_btn = ctk.CTkButton(
            fr, text="🌙" if ctk.get_appearance_mode() == "Dark" else "☀️",
            width=36, height=36,
            corner_radius=18, fg_color=("gray85", "gray25"),
            hover_color=("gray75", "gray35"),
            text_color=("gray20", "gray90"),
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side="right")

    # ── Карточка «Устройство» ──────────────────────────────────────────

    def _card_device(self):
        self._section(self.t("device"), [
            (self.t("model"),       self.info.get("model_name")),
            (self.t("identifier"),  self.info.get("model_id")),
            (self.t("processor"),   self.info.get("cpu")),
            (self.t("cores"),       self.info.get("cores")),
            (self.t("memory"),      self.info.get("memory")),
            (self.t("storage"),     self.info.get("storage_str")),
            (self.t("serial"),      self._mask(self.info.get("serial", ""))),
        ])

    # ── Карточка «Система» ─────────────────────────────────────────────

    def _card_system(self):
        ver   = self.info.get("macos_ver")
        build = self.info.get("macos_build", "")
        self._section(self.t("system"), [
            (self.t("macos"), f"{ver}  ({build})" if build else ver),
            (self.t("year"),  str(self.info.get("year"))),
        ])

    # ── Карточка «Аккумулятор» ─────────────────────────────────────────

    def _card_battery(self):
        card = ctk.CTkFrame(self.main, corner_radius=16)
        card.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            card, text=self.t("battery"),
            font=ctk.CTkFont(size=18, weight="bold"), anchor="w",
        ).pack(fill="x", padx=22, pady=(16, 8))

        ctk.CTkFrame(card, height=1,
                     fg_color=("gray82", "gray28")).pack(fill="x", padx=22)

        cycles     = self.info.get("cycles", 0)
        health     = self.info.get("battery_health", 100)
        cond_key   = self.estimator.condition()
        cond_label = self.t(cond_key)
        cond_color = self.estimator.condition_color()
        apple_cond = self.info.get("apple_condition")
        mah        = self.t("mah")

        if self.info.get("fully_charged", False):
            charge_status = self.t("fully_charged")
        elif self.info.get("charging", False):
            charge_status = self.t("charging")
        elif self.info.get("plugged", False):
            charge_status = self.t("plugged")
        else:
            charge_status = self.t("on_battery")

        rows = [
            (self.t("cycles"),          str(cycles)),
            (self.t("battery_health"),  f"{health}%"),
            (self.t("max_capacity"),    f"{self.info.get('max_capacity_mah', '?')} {mah}"),
            (self.t("design_capacity"), f"{self.info.get('design_capacity_mah', '?')} {mah}"),
            (self.t("condition_apple"), apple_cond),
            (self.t("status"),          charge_status),
        ]
        for label, value in rows:
            self._row(card, label, value)

        bar_fr = ctk.CTkFrame(card, fg_color="transparent")
        bar_fr.pack(fill="x", padx=22, pady=(12, 4))

        ctk.CTkLabel(
            bar_fr, text=self.t("health_label"),
            font=ctk.CTkFont(size=12), text_color="gray",
        ).pack(anchor="w")

        bar = ctk.CTkProgressBar(
            bar_fr, height=14, corner_radius=7,
            progress_color=cond_color,
        )
        bar.pack(fill="x", pady=(4, 0))
        bar.set(min(max(health / 100, 0), 1.0))

        badge = ctk.CTkLabel(
            card, text=f"   {cond_label}   ",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=cond_color, text_color="white",
            corner_radius=10,
        )
        badge.pack(pady=(14, 18))

    # ── Карточка «Стоимость» ───────────────────────────────────────────

    def _card_price(self):
        card = ctk.CTkFrame(self.main, corner_radius=16)
        card.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            card, text=self.t("price_title"),
            font=ctk.CTkFont(size=18, weight="bold"), anchor="w",
        ).pack(fill="x", padx=22, pady=(16, 8))

        ctk.CTkFrame(card, height=1,
                     fg_color=("gray82", "gray28")).pack(fill="x", padx=22)

        p = self.estimator.estimate()

        boxes = ctk.CTkFrame(card, fg_color="transparent")
        boxes.pack(fill="x", padx=22, pady=(16, 6))
        boxes.grid_columnconfigure((0, 1), weight=1)

        self._price_box(
            boxes, col=0,
            flag="🇺🇸", currency="USD",
            main=f"$ {p['usd']:,}",
            sub=f"$ {p['usd_lo']:,}  —  $ {p['usd_hi']:,}",
            color="#34C759",
        )
        self._price_box(
            boxes, col=1,
            flag="🇷🇺", currency="RUB",
            main=f"₽ {p['rub']:,}",
            sub=f"₽ {p['rub_lo']:,}  —  ₽ {p['rub_hi']:,}",
            color="#007AFF",
        )

        ctk.CTkLabel(
            card,
            text=f"{self.t('rate_prefix')}  1 USD ≈ {self.rate} ₽   •   "
                 f"{datetime.now().strftime('%d.%m.%Y %H:%M')}",
            font=ctk.CTkFont(size=11), text_color="gray",
        ).pack(pady=(4, 16))

    # ── Футер ───────────────────────────────────────────────────────────

    def _footer(self):
        ctk.CTkLabel(
            self.main,
            text=self.t("disclaimer"),
            font=ctk.CTkFont(size=11), text_color="gray",
            justify="center",
        ).pack(pady=(8, 10))

        btn_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        btn_frame.pack(pady=(0, 16))

        ctk.CTkButton(
            btn_frame, text=self.t("refresh"),
            width=160, height=42, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._refresh,
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            btn_frame, text=self.t("copy_report"),
            width=200, height=42, corner_radius=12,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("gray78", "gray30"),
            hover_color=("gray68", "gray40"),
            text_color=("gray10", "gray95"),
            command=self._copy_report,
        ).pack(side="left", padx=6)

    # ═══════════════════════════════════════════════════════════════════
    #  ВИДЖЕТ-ПОМОЩНИКИ
    # ═══════════════════════════════════════════════════════════════════

    def _section(self, title: str, rows: list):
        card = ctk.CTkFrame(self.main, corner_radius=16)
        card.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=18, weight="bold"), anchor="w",
        ).pack(fill="x", padx=22, pady=(16, 8))

        ctk.CTkFrame(card, height=1,
                     fg_color=("gray82", "gray28")).pack(fill="x", padx=22)

        for label, value in rows:
            self._row(card, label, value)

        ctk.CTkFrame(card, height=6, fg_color="transparent").pack()

    def _row(self, parent, label: str, value: str):
        fr = ctk.CTkFrame(parent, fg_color="transparent")
        fr.pack(fill="x", padx=22, pady=(7, 0))

        ctk.CTkLabel(
            fr, text=label,
            font=ctk.CTkFont(size=13), text_color="gray", anchor="w",
        ).pack(side="left")

        ctk.CTkLabel(
            fr, text=str(value),
            font=ctk.CTkFont(size=13, weight="bold"), anchor="e",
        ).pack(side="right")

    def _price_box(self, parent, col, flag, currency, main, sub, color):
        box = ctk.CTkFrame(parent, corner_radius=14,
                           fg_color=("gray90", "gray20"))
        box.grid(row=0, column=col, sticky="nsew",
                 padx=(0 if col == 0 else 6, 6 if col == 0 else 0))

        ctk.CTkLabel(
            box, text=f"{flag}  {currency}",
            font=ctk.CTkFont(size=12), text_color="gray",
        ).pack(pady=(14, 2))

        ctk.CTkLabel(
            box, text=main,
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=color,
        ).pack()

        ctk.CTkLabel(
            box, text=sub,
            font=ctk.CTkFont(size=11), text_color="gray",
        ).pack(pady=(2, 14))

    # ═══════════════════════════════════════════════════════════════════
    #  ДЕЙСТВИЯ
    # ═══════════════════════════════════════════════════════════════════

    def _toggle_lang(self):
        self.lang = "en" if self.lang == "ru" else "ru"
        self._build_ui()

    def _refresh(self):
        self.info       = MacInfo()
        self.rate        = fetch_usd_rate()
        self.estimator   = PriceEstimator(self.info, self.rate)
        self._build_ui()

    def _toggle_theme(self):
        mode = ctk.get_appearance_mode()
        new = "Light" if mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new)
        self.theme_btn.configure(text="☀️" if new == "Light" else "🌙")

    def _copy_report(self):
        p    = self.estimator.estimate()
        cond = self.t(self.estimator.condition())

        lines = [
            self.t("report_header"),
            "",
            f"{self.t('report_model'):18s}{self.info.get('model_name')}",
            f"{self.t('report_id'):18s}{self.info.get('model_id')}",
            f"{self.t('report_cpu'):18s}{self.info.get('cpu')}",
            f"{self.t('report_cores'):18s}{self.info.get('cores')}",
            f"{self.t('report_memory'):18s}{self.info.get('memory')}",
            f"{self.t('report_storage'):18s}{self.info.get('storage_str')}",
            f"{self.t('report_year'):18s}{self.info.get('year')}",
            f"{self.t('report_macos'):18s}{self.info.get('macos_ver')}",
            "",
            f"{self.t('report_cycles'):18s}{self.info.get('cycles')}",
            f"{self.t('report_health'):18s}{self.info.get('battery_health')}%",
            f"{self.t('report_condition'):18s}{cond}",
            "",
            f"{self.t('report_price_usd'):18s}${p['usd']:,}  (${p['usd_lo']:,}–${p['usd_hi']:,})",
            f"{self.t('report_price_rub'):18s}₽{p['rub']:,}  (₽{p['rub_lo']:,}–₽{p['rub_hi']:,})",
            f"{self.t('report_rate'):18s}1 USD = {self.rate} RUB",
            "",
            f"{self.t('report_date'):18s}{datetime.now().strftime('%d.%m.%Y %H:%M')}",
            self.t("report_footer"),
        ]
        text = "\n".join(lines)

        self.clipboard_clear()
        self.clipboard_append(text)
        self._show_toast(self.t("copied_toast"))

    def _show_toast(self, text: str):
        toast = ctk.CTkLabel(
            self, text=text,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#34C759", text_color="white",
            corner_radius=12, height=40,
        )
        toast.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2000, toast.destroy)

    @staticmethod
    def _mask(serial: str) -> str:
        if not serial or serial == "N/A":
            return "N/A"
        if len(serial) > 5:
            return serial[:3] + "•" * (len(serial) - 5) + serial[-2:]
        return serial


# ════════════════════════════════════════════════════════════════════════
#  ЗАПУСК
# ════════════════════════════════════════════════════════════════════════

def main():
    if platform.system() != "Darwin":
        print("⚠️  Macost is designed for macOS.")
        print("    Running in demo mode with test data.\n")

    app = MacostApp()
    app.mainloop()


if __name__ == "__main__":
    main()
