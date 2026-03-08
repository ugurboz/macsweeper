// Wait for pywebview to be ready
window.addEventListener('pywebviewready', function () {
    initApp();
});

// For local testing if pywebview isn't injected yet (dev mock)
if (window.location.protocol === "file:" && !window.pywebview) {
    // We are likely in a local browser not pywebview, mock data can be written here if needed
}

// Localization mappings
const locales = {
    en: {
        "nav.clean": "CLEAN",
        "nav.apps": "Applications",
        "nav.orphans": "Orphaned Files",
        "nav.scan": "SCAN",
        "nav.system": "System Junk",
        "nav.large": "Large Files",
        "nav.dev": "Developer Junk",
        "nav.trash": "System Trash",
        "app.installed": "installed",
        "detail.total": "Total Found",
        "detail.files": "Files",
        "detail.leftovers": "Leftover Files",
        "detail.btn.clean": "Clean Selected",
        "msg.loading": "Scanning deeply...",
        "msg.apps_loading": "Loading applications...",
        "msg.apps_loaded": "{count} apps loaded.",
        "msg.icons_loading": "Loading icons {done}/{total}...",
        "msg.icons_ready": "Applications are ready.",
        "msg.apps_loading_failed": "Could not load applications.",
        "msg.scanning": "Scanning...",
        "msg.try_again": "Try Again",
        "msg.scan_completed": "Scan Completed",
        "msg.unknown_bundle": "Unknown Bundle ID",
        "msg.no_apps": "No apps found.",
        "msg.load_apps_failed": "Failed to load apps.",
        "msg.error.scan_app": "Error scanning app.",
        "msg.error.scan_orphans": "Error scanning orphans.",
        "msg.error.scan_generic": "Error during scan.",
        "msg.error.cleanup": "Cleanup error: {error}",
        "msg.error.generic": "Error: {error}",
        "msg.error.clean_files": "Error cleaning files: {error}",
        "msg.empty.leftovers": "No leftover files found.",
        "msg.empty.orphans": "No orphaned files found! Your Mac is clean.",
        "msg.empty.sys": "Your system caches & logs are totally clean!",
        "msg.empty.large": "No large files found (>250MB) in your home folders.",
        "msg.empty.dev": "No Developer Junk found!",
        "msg.empty.trash": "Trash is already empty!",
        "btn.scan_orphans": "Find Orphans",
        "btn.scan_sys": "Scan System",
        "btn.scan_large": "Scan Large Files",
        "btn.scan_dev": "Scan Developer Junk",
        "btn.scan_trash": "Scan Trash",
        "btn.clean_all": "Clean Selection",
        "btn.delete_all": "Permanently Delete",
        "btn.open_location": "Open",
        "btn.undo": "Undo",
        "btn.completed": "Scan Completed",
        "btn.cleaning": "Cleaning...",
        "alert.select_one": "Select at least one file to clean.",
        "alert.clean_success": "Cleaned {count} files ({size})",
        "alert.clean_none": "No items were deleted.",
        "alert.undo_success": "Restored {count} item(s).",
        "alert.undo_none": "Nothing to undo.",
        "alert.undo_partial": "Restored {ok}, failed {failed} item(s).",
        "alert.failed_items": "Some items could not be deleted:\n{paths}",
        "prompt.confirm": "Are you sure you want to move {count} items to Trash?",
        "prompt.confirm_delete": "Are you sure you want to permanently delete {count} items? This cannot be undone.",
        "prompt.risky_confirm": "{count} selected item(s) are risky (Preferences/App Support/System). Continue anyway?",
        "nav.preferences": "PREFERENCES",
        "nav.settings": "Settings",
        "settings.desc": "Configure MacSweeper preferences",
        "settings.theme": "Theme",
        "settings.theme.system": "System",
        "settings.theme.light": "Light",
        "settings.theme.dark": "Dark",
        "settings.theme_desc": "System mode follows your Mac appearance automatically.",
        "settings.lang": "Language",
        "settings.large_limit": "Large Files Minimum Size",
        "settings.large_desc": "Files smaller than this threshold will be ignored during scans.",
        "settings.startup": "Open at login",
        "settings.startup_desc": "Launch MacSweeper automatically when your Mac starts.",
        "settings.startup_failed": "Could not change startup setting.",
        "settings.safe_mode": "Safe Mode",
        "settings.safe_mode_desc": "Prevents risky files from being auto-selected and asks for extra confirmation.",
        "detail.associated": "Associated Files",
        "btn.select_all": "Select All",
        "selection.none": "No files selected",
        "selection.summary": "Selected: {count} item(s) • {size}",
        "selection.cleaning": "Cleaning: {count} item(s) • {size}",
        "app.search_placeholder": "Search applications...",
        "detail.empty.title": "No Application Selected",
        "detail.empty.desc": "Select an app from the list to view its files and clean them safely.",
        "detail.stats.total_size": "Total Size",
        "detail.stats.files_found": "Files Found",
        "hero.orphans.title": "Leftover Intelligence",
        "hero.orphans.desc": "Find traces of applications you've already dragged to the Trash.",
        "hero.orphans.btn": "Start Deep Scan",
        "hero.system.title": "System Junk & Caches",
        "hero.system.desc": "Analyze your macOS logs and application caches taking up useless space.",
        "hero.system.btn": "Analyze System Junk",
        "hero.large.title": "Large Files (>250MB)",
        "hero.large.desc": "Discover huge files hiding in Downloads, Documents or Movies.",
        "hero.large.btn": "Find Large Files",
        "hero.dev.title": "Developer Junk",
        "hero.dev.desc": "Clear out huge Xcode Derived Data, Archives, and iOS Backups.",
        "hero.dev.btn": "Scan Developer Junk",
        "hero.trash.title": "System Trash",
        "hero.trash.desc": "Analyze and empty macOS Trash securely.",
        "hero.trash.btn": "Scan Trash",
        "meta.total_found": "Total found",
        "meta.items": "items",
        "msg.all_clean": "All clean!",
        "alert.delete_failed": "Could not delete {count} item(s). You might need to grant Full Disk Access in System Settings."
    },
    tr: {
        "nav.clean": "TEMİZLİK",
        "nav.apps": "Uygulamalar",
        "nav.orphans": "Artık Dosyalar",
        "nav.scan": "TARAMA",
        "nav.system": "Sistem Çöpleri",
        "nav.large": "Büyük Dosyalar",
        "nav.dev": "Geliştirici Çöpleri",
        "nav.trash": "Sistem Çöpü",
        "app.installed": "yüklü",
        "detail.total": "Toplam Boyut",
        "detail.files": "Dosya",
        "detail.leftovers": "Uygulama Kalıntıları",
        "detail.btn.clean": "Seçilenleri Sil",
        "msg.loading": "Kapsamlı taranıyor...",
        "msg.apps_loading": "Uygulamalar yükleniyor...",
        "msg.apps_loaded": "{count} uygulama yüklendi.",
        "msg.icons_loading": "İkonlar yükleniyor {done}/{total}...",
        "msg.icons_ready": "Uygulamalar hazır.",
        "msg.apps_loading_failed": "Uygulamalar yüklenemedi.",
        "msg.scanning": "Taranıyor...",
        "msg.try_again": "Tekrar Dene",
        "msg.scan_completed": "Tarama Tamamlandı",
        "msg.unknown_bundle": "Bilinmeyen Bundle ID",
        "msg.no_apps": "Uygulama bulunamadı.",
        "msg.load_apps_failed": "Uygulamalar yüklenemedi.",
        "msg.error.scan_app": "Uygulama taranırken hata oluştu.",
        "msg.error.scan_orphans": "Artık dosyalar taranırken hata oluştu.",
        "msg.error.scan_generic": "Tarama sırasında hata oluştu.",
        "msg.error.cleanup": "Temizleme hatası: {error}",
        "msg.error.generic": "Hata: {error}",
        "msg.error.clean_files": "Dosyalar temizlenirken hata oluştu: {error}",
        "msg.empty.leftovers": "Kalıntı dosya bulunamadı.",
        "msg.empty.orphans": "Artık dosya yok! Mac'iniz tertemiz.",
        "msg.empty.sys": "Sistem önbellekleri pırıl pırıl!",
        "msg.empty.large": "Büyük dosya (>250MB) bulunamadı.",
        "msg.empty.dev": "Geliştirici çöpü (Xcode/iOS) bulunamadı!",
        "msg.empty.trash": "Çöp sepeti zaten boş!",
        "btn.scan_orphans": "Kalıntıları Bul",
        "btn.scan_sys": "Sistemi Tara",
        "btn.scan_large": "Büyük Dosyaları Tara",
        "btn.scan_dev": "Geliştirici Çöplerini Tara",
        "btn.scan_trash": "Çöpü Tara",
        "btn.clean_all": "Seçimi Temizle",
        "btn.delete_all": "Kalıcı Olarak Sil",
        "btn.open_location": "Aç",
        "btn.undo": "Geri Al",
        "btn.completed": "Tarama Bitti",
        "btn.cleaning": "Siliniyor...",
        "alert.select_one": "Silmek için en az bir dosya seçin.",
        "alert.clean_success": "{count} dosya temizlendi ({size})",
        "alert.clean_none": "Hiçbir öğe silinemedi.",
        "alert.undo_success": "{count} öğe geri yüklendi.",
        "alert.undo_none": "Geri alınacak işlem yok.",
        "alert.undo_partial": "{ok} öğe geri yüklendi, {failed} öğe başarısız.",
        "alert.failed_items": "Bazı öğeler silinemedi:\n{paths}",
        "prompt.confirm": "{count} öğeyi Çöp Sepetine taşımak istediğinize emin misiniz?",
        "prompt.confirm_delete": "{count} öğeyi kalıcı olarak silmek istediğinize emin misiniz? Bu işlem geri alınamaz.",
        "prompt.risky_confirm": "Seçili öğelerden {count} tanesi riskli (Tercihler/Uygulama Desteği/Sistem). Yine de devam edilsin mi?",
        "nav.preferences": "TERCİHLER",
        "nav.settings": "Ayarlar",
        "settings.desc": "MacSweeper tercihlerini yapılandırın",
        "settings.theme": "Tema",
        "settings.theme.system": "Sistem",
        "settings.theme.light": "Açık",
        "settings.theme.dark": "Koyu",
        "settings.theme_desc": "Sistem modu Mac görünümünü otomatik takip eder.",
        "settings.lang": "Dil",
        "settings.large_limit": "Büyük Dosya Minimum Boyutu",
        "settings.large_desc": "Taramalarda bu boyuttan daha küçük olan dosyalar atlanacak.",
        "settings.startup": "Açılışta aç",
        "settings.startup_desc": "Mac açıldığında MacSweeper otomatik başlasın.",
        "settings.startup_failed": "Açılış ayarı değiştirilemedi.",
        "settings.safe_mode": "Güvenli Mod",
        "settings.safe_mode_desc": "Riskli dosyaları otomatik seçmez ve silmeden önce ekstra onay ister.",
        "detail.associated": "İlişkili Dosyalar",
        "btn.select_all": "Tümünü Seç",
        "selection.none": "Dosya seçilmedi",
        "selection.summary": "Seçili: {count} öğe • {size}",
        "selection.cleaning": "Siliniyor: {count} öğe • {size}",
        "app.search_placeholder": "Uygulama ara...",
        "detail.empty.title": "Uygulama Seçilmedi",
        "detail.empty.desc": "Dosyalarını görmek ve güvenle temizlemek için listeden bir uygulama seçin.",
        "detail.stats.total_size": "Toplam Boyut",
        "detail.stats.files_found": "Bulunan Dosya",
        "hero.orphans.title": "Artık Dosya Analizi",
        "hero.orphans.desc": "Çöp Sepeti'ne taşıdığınız uygulamalardan kalan izleri bulun.",
        "hero.orphans.btn": "Derin Taramayı Başlat",
        "hero.system.title": "Sistem Çöpleri ve Önbellekler",
        "hero.system.desc": "Yer kaplayan macOS günlükleri ve uygulama önbelleklerini analiz edin.",
        "hero.system.btn": "Sistem Çöplerini Analiz Et",
        "hero.large.title": "Büyük Dosyalar (>250MB)",
        "hero.large.desc": "İndirilenler, Belgeler ve Filmler klasörlerindeki büyük dosyaları bulun.",
        "hero.large.btn": "Büyük Dosyaları Bul",
        "hero.dev.title": "Geliştirici Çöpleri",
        "hero.dev.desc": "Xcode Derived Data, Archives ve iOS yedeklerini temizleyin.",
        "hero.dev.btn": "Geliştirici Çöplerini Tara",
        "hero.trash.title": "Sistem Çöpü",
        "hero.trash.desc": "macOS Çöp Sepeti'ni güvenli şekilde analiz edip boşaltın.",
        "hero.trash.btn": "Çöpü Tara",
        "meta.total_found": "Toplam bulunan",
        "meta.items": "öğe",
        "msg.all_clean": "Her şey temiz!",
        "alert.delete_failed": "{count} öğe silinemedi. Sistem Ayarları'ndan Tam Disk Erişimi vermeniz gerekebilir."
    }
};

let currentLang = 'en';
window.largeFileLimit = 250;
let themePreference = 'system';
let systemThemeMedia = null;
let safeModeEnabled = true;

window.setLang = function (lang) {
    currentLang = lang;
    localStorage.setItem('macsweeper_lang', lang);
    document.querySelectorAll('[data-i18n]').forEach(el => {
        let key = el.getAttribute('data-i18n');
        if (locales[lang] && locales[lang][key]) {
            el.innerText = locales[lang][key];
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        let key = el.getAttribute('data-i18n-placeholder');
        if (locales[lang] && locales[lang][key]) {
            el.setAttribute('placeholder', locales[lang][key]);
        }
    });

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        let key = el.getAttribute('data-i18n-title');
        if (locales[lang] && locales[lang][key]) {
            el.setAttribute('title', locales[lang][key]);
        }
    });

    document.querySelectorAll('[data-i18n-aria-label]').forEach(el => {
        let key = el.getAttribute('data-i18n-aria-label');
        if (locales[lang] && locales[lang][key]) {
            el.setAttribute('aria-label', locales[lang][key]);
        }
    });

    // Translate dynamic buttons if they are in default state
    let btns = {
        'btn-scan-orphans': 'btn.scan_orphans',
        'btn-scan-system': 'btn.scan_sys',
        'btn-scan-large': 'btn.scan_large',
        'btn-scan-dev': 'btn.scan_dev',
        'btn-scan-trash': 'btn.scan_trash'
    };
    for (let id in btns) {
        let b = document.getElementById(id);
        if (b && !b.disabled && b.innerText !== t('msg.scanning')) b.innerText = t(btns[id]);
    }

    const langSelect = document.getElementById('settings-lang');
    if (langSelect) {
        langSelect.value = lang;
    }

    if (allApps.length > 0) renderAppList(allApps); // refresh app list texts
};

function t(key, params = {}) {
    let str = (locales[currentLang] && locales[currentLang][key]) ? locales[currentLang][key] : key;
    for (let k in params) {
        str = str.replace(`{${k}}`, params[k]);
    }
    return str;
}

function localizeCategory(category) {
    if (currentLang !== 'tr') return category;

    const map = {
        'Application': 'Uygulama',
        'Preferences': 'Tercihler',
        'Home Dotfile': 'Ana Dizin Gizli Dosyası',
        'Receipt': 'Makbuz',
        'Crash Report': 'Çökme Raporu',
        'Crash Reports': 'Çökme Raporları',
        'User Cache': 'Kullanıcı Önbelleği',
        'System Cache': 'Sistem Önbelleği',
        'User Log': 'Kullanıcı Günlüğü',
        'System Log': 'Sistem Günlüğü',
        'System Trash': 'Sistem Çöpü',
        'Xcode Derived Data': 'Xcode Türetilmiş Veriler',
        'Xcode Archives': 'Xcode Arşivleri',
        'iOS Backup': 'iOS Yedeği',
        'Large File': 'Büyük Dosya',
        'Large App': 'Büyük Uygulama',
    };

    if (map[category]) return map[category];
    if (category.startsWith('Trash (') && category.endsWith(')')) {
        return category.replace('Trash (', 'Çöp (');
    }

    return category;
}

function formatBytes(bytes) {
    if (bytes < 1000) return `${bytes} B`;
    if (bytes < 1_000_000) return `${(bytes / 1000).toFixed(1)} KB`;
    if (bytes < 1_000_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
    return `${(bytes / 1_000_000_000).toFixed(2)} GB`;
}

const RISKY_CATEGORY_KEYWORDS = [
    'preference', 'app support', 'application support', 'launch',
    'framework', 'helper', 'startup', 'receipt', 'home dotfile',
    'system preference', 'group container', 'container', 'app script'
];

const RISKY_PATH_SEGMENTS = [
    '/library/preferences/',
    '/library/application support/',
    '/library/launchagents/',
    '/library/launchdaemons/',
    '/library/frameworks/',
    '/library/privilegedhelpertools/',
    '/private/var/db/receipts/'
];

function isRiskyFile(fileObj) {
    if (!fileObj) return false;
    const category = String(fileObj.category || '').toLowerCase();
    const path = String(fileObj.path || '').toLowerCase();
    if (RISKY_CATEGORY_KEYWORDS.some(k => category.includes(k))) return true;
    return RISKY_PATH_SEGMENTS.some(seg => path.includes(seg));
}

function shouldAutoSelectFile(fileObj) {
    if (!safeModeEnabled) return true;
    return !isRiskyFile(fileObj);
}

function getRiskyCount(files) {
    return files.filter(isRiskyFile).length;
}

function confirmCleanup(files, isPermanentDelete = false) {
    const firstPrompt = isPermanentDelete
        ? t('prompt.confirm_delete', { count: files.length })
        : t('prompt.confirm', { count: files.length });
    if (!confirm(firstPrompt)) return false;

    if (!safeModeEnabled) return true;

    const riskyCount = getRiskyCount(files);
    if (riskyCount > 0) {
        return confirm(t('prompt.risky_confirm', { count: riskyCount }));
    }
    return true;
}

window.openFileLocation = async function (path, event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }

    if (!path || !window.pywebview?.api?.reveal_path) {
        return;
    }

    try {
        await window.pywebview.api.reveal_path(path);
    } catch (e) {
        console.error('Failed to open location:', e);
    }
};

function getSelectedCurrentAppFiles() {
    const selected = [];
    document.querySelectorAll('.file-checkbox:checked').forEach(chk => {
        const gIdx = Number(chk.getAttribute('data-gidx'));
        const fIdx = Number(chk.getAttribute('data-fidx'));
        const fileObj = currentLeftoversGroups?.[gIdx]?.files?.[fIdx];
        if (fileObj) selected.push(fileObj);
    });
    return selected;
}

function updateCurrentSelectionStatus(customText = null) {
    const statusEl = document.getElementById('selection-status');
    if (!statusEl) return;

    if (customText) {
        statusEl.textContent = customText;
        statusEl.classList.add('is-active');
        return;
    }

    const selected = getSelectedCurrentAppFiles();
    if (selected.length === 0) {
        statusEl.textContent = t('selection.none');
        statusEl.classList.remove('is-active');
        return;
    }

    const total = selected.reduce((acc, f) => acc + (f.size_bytes || 0), 0);
    statusEl.textContent = t('selection.summary', {
        count: selected.length,
        size: formatBytes(total),
    });
    statusEl.classList.add('is-active');
}

function applyThemeFromPreference() {
    const root = document.documentElement;
    if (themePreference === 'light') {
        root.setAttribute('data-theme', 'light');
        return;
    }
    if (themePreference === 'dark') {
        root.setAttribute('data-theme', 'dark');
        return;
    }

    const isDark = systemThemeMedia && systemThemeMedia.matches;
    root.setAttribute('data-theme', isDark ? 'dark' : 'light');
}

window.setThemePreference = function (theme) {
    themePreference = theme;
    localStorage.setItem('macsweeper_theme', theme);
    applyThemeFromPreference();

    const themeSelect = document.getElementById('settings-theme');
    if (themeSelect) {
        themeSelect.value = theme;
    }
};

window.toggleSafeMode = function (enabled) {
    safeModeEnabled = !!enabled;
    localStorage.setItem('macsweeper_safe_mode', safeModeEnabled ? '1' : '0');
};

window.toggleOpenAtLogin = async function (enabled) {
    if (!window.pywebview || !window.pywebview.api || !window.pywebview.api.set_open_at_login) {
        return;
    }

    const toggle = document.getElementById('settings-open-at-login');
    if (toggle) toggle.disabled = true;

    try {
        const result = await window.pywebview.api.set_open_at_login(enabled);
        if (!result || !result.ok) {
            throw new Error('startup setting failed');
        }
    } catch (_e) {
        if (toggle) toggle.checked = !enabled;
        alert(t('settings.startup_failed'));
    } finally {
        if (toggle) toggle.disabled = false;
    }
};

async function initializePreferences() {
    const savedLang = localStorage.getItem('macsweeper_lang') || 'tr';
    setLang(savedLang);

    const savedTheme = localStorage.getItem('macsweeper_theme') || 'system';
    themePreference = savedTheme;
    const themeSelect = document.getElementById('settings-theme');
    if (themeSelect) themeSelect.value = savedTheme;

    systemThemeMedia = window.matchMedia('(prefers-color-scheme: dark)');
    applyThemeFromPreference();
    const onThemeChange = () => {
        if (themePreference === 'system') {
            applyThemeFromPreference();
        }
    };
    if (systemThemeMedia.addEventListener) {
        systemThemeMedia.addEventListener('change', onThemeChange);
    } else if (systemThemeMedia.addListener) {
        systemThemeMedia.addListener(onThemeChange);
    }

    const limitSelect = document.getElementById('settings-large-limit');
    if (limitSelect) {
        const savedLimit = localStorage.getItem('macsweeper_large_limit');
        if (savedLimit) {
            limitSelect.value = savedLimit;
        }
        window.largeFileLimit = parseInt(limitSelect.value || '250', 10);
    }

    const savedSafeMode = localStorage.getItem('macsweeper_safe_mode');
    safeModeEnabled = savedSafeMode !== '0';
    const safeModeToggle = document.getElementById('settings-safe-mode');
    if (safeModeToggle) {
        safeModeToggle.checked = safeModeEnabled;
    }

    const startupToggle = document.getElementById('settings-open-at-login');
    if (startupToggle && window.pywebview?.api?.get_open_at_login_status) {
        try {
            const status = await window.pywebview.api.get_open_at_login_status();
            startupToggle.checked = !!(status && status.enabled);
        } catch (_e) {
            startupToggle.checked = false;
        }
    }
}

let allApps = [];
let selectedAppObj = null;
let currentLeftovers = null;
let currentLeftoversGroups = null; // Storing references by indices
let _listenersAttached = false;
const appIconCache = new Map();
let iconLoadToken = 0;
let appLoadStatusTimer = null;
let undoAvailable = false;

function setUndoAvailable(enabled) {
    undoAvailable = !!enabled;
    const btn = document.getElementById('btn-undo-last-clean');
    if (!btn) return;
    btn.classList.toggle('hidden', !undoAvailable);
}

function summarizeFailedItems(res) {
    const paths = Array.isArray(res?.failed_paths) ? res.failed_paths : [];
    if (paths.length === 0) return '';
    const shown = paths.slice(0, 3).join('\n');
    const suffix = paths.length > 3 ? `\n+${paths.length - 3} more` : '';
    return t('alert.failed_items', { paths: shown + suffix });
}

window.undoLastCleanup = async function () {
    if (!window.pywebview?.api?.undo_last_cleanup) {
        alert(t('alert.undo_none'));
        return;
    }

    try {
        const res = await window.pywebview.api.undo_last_cleanup();

        if (res.success_count > 0 && res.failed_count === 0) {
            showToast(t('alert.undo_success', { count: res.success_count }));
        } else if (res.success_count > 0) {
            alert(t('alert.undo_partial', { ok: res.success_count, failed: res.failed_count }));
        } else {
            alert(t('alert.undo_none'));
        }

        setUndoAvailable(!!res.undo_available);

        if (selectedAppObj) {
            const selectedEl = document.querySelector('.app-item.selected');
            if (selectedEl) {
                await selectApp(selectedAppObj, selectedEl);
            }
        }
    } catch (e) {
        console.error(e);
        alert(t('msg.error.generic', { error: e }));
    }
};

function setAppLoadStatus(message, kind = 'loading', autoHideMs = 0) {
    const statusEl = document.getElementById('app-load-status');
    if (!statusEl) return;

    if (appLoadStatusTimer) {
        clearTimeout(appLoadStatusTimer);
        appLoadStatusTimer = null;
    }

    const textEl = statusEl.querySelector('.status-text');
    if (textEl) {
        textEl.textContent = message;
    }

    statusEl.classList.remove('hidden', 'is-loading', 'is-ready', 'is-done', 'is-error');
    statusEl.classList.add(`is-${kind}`);

    if (autoHideMs > 0) {
        appLoadStatusTimer = setTimeout(() => {
            statusEl.classList.add('hidden');
        }, autoHideMs);
    }
}

function initApp() {
    if (!_listenersAttached) {
        setupEventListeners();
        _listenersAttached = true;
    }
    initializePreferences();
    loadApps();
}

function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-links li[data-view]').forEach(item => {
        item.addEventListener('click', (e) => {
            document.querySelectorAll('.nav-links li').forEach(l => l.classList.remove('active'));
            item.classList.add('active');

            const viewId = item.getAttribute('data-view');
            document.querySelectorAll('.main-content > div').forEach(v => v.classList.add('hidden'));
            document.getElementById('view-' + viewId).classList.remove('hidden');

            // Auto-scan on first visit to scan-based views
            const autoScanMap = {
                'system': { btnId: 'btn-scan-system', resId: 'system-results', fn: scanSystemJunk },
                'large': { btnId: 'btn-scan-large', resId: 'large-results', fn: scanLargeFiles },
                'dev': { btnId: 'btn-scan-dev', resId: 'dev-results', fn: scanDevJunk },
                'trash': { btnId: 'btn-scan-trash', resId: 'trash-results', fn: scanTrash },
                'orphans': { btnId: 'btn-scan-orphans', resId: 'orphans-results', fn: scanOrphans },
            };
            const scanInfo = autoScanMap[viewId];
            if (scanInfo) {
                const resDiv = document.getElementById(scanInfo.resId);
                const btn = document.getElementById(scanInfo.btnId);
                // Auto-scan if results area hasn't been populated yet (still hidden or empty)
                if (resDiv && resDiv.classList.contains('hidden') && btn && !btn.disabled) {
                    scanInfo.fn();
                }
            }
        });
    });

    // Search
    document.getElementById('app-search').addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const filtered = allApps.filter(a => a.name.toLowerCase().includes(query));
        renderAppList(filtered);
    });

    // Clean Button
    document.getElementById('btn-clean').addEventListener('click', cleanCurrentApp);

    // Scan Orphans
    document.getElementById('btn-scan-orphans').addEventListener('click', scanOrphans);
    document.getElementById('btn-scan-system').addEventListener('click', scanSystemJunk);
    document.getElementById('btn-scan-large').addEventListener('click', scanLargeFiles);
    document.getElementById('btn-scan-dev').addEventListener('click', scanDevJunk);
    document.getElementById('btn-scan-trash').addEventListener('click', scanTrash);
}

async function loadApps() {
    const listEl = document.getElementById('app-list');
    setAppLoadStatus(t('msg.apps_loading'), 'loading');
    renderAppSkeletons(8);

    try {
        // Call Python Backend
        allApps = await window.pywebview.api.get_apps();
        // Sort alphabetically
        allApps.sort((a, b) => a.name.localeCompare(b.name));
        setAppLoadStatus(t('msg.apps_loaded', { count: allApps.length }), 'ready');
        renderAppList(allApps, { trackLoadStatus: true });
    } catch (e) {
        console.error(e);
        setAppLoadStatus(t('msg.apps_loading_failed'), 'error');
        listEl.innerHTML = `<p style="padding:20px; color:var(--danger)">${t('msg.load_apps_failed')}</p>`;
    }
}

function renderAppSkeletons(count = 8) {
    const listEl = document.getElementById('app-list');
    if (!listEl) return;

    listEl.innerHTML = '';
    for (let i = 0; i < count; i += 1) {
        const li = document.createElement('li');
        li.className = 'app-item app-item-skeleton';
        li.innerHTML = `
            <div class="app-icon skeleton-block"></div>
            <div class="app-info-skeleton">
                <div class="skeleton-line skeleton-line-main"></div>
                <div class="skeleton-line skeleton-line-sub"></div>
            </div>
        `;
        listEl.appendChild(li);
    }
}

function renderAppList(apps, options = {}) {
    const trackLoadStatus = !!options.trackLoadStatus;
    const listEl = document.getElementById('app-list');
    listEl.innerHTML = '';

    if (apps.length === 0) {
        listEl.innerHTML = `<p style="padding: 20px; text-align: center; color: var(--text-muted)">${t('msg.no_apps')}</p>`;
        return;
    }

    apps.forEach(app => {
        const li = document.createElement('li');
        li.className = 'app-item';
        li.dataset.iconKey = encodeURIComponent(app.path);

        // Initial letter as icon
        const initial = app.name.charAt(0).toUpperCase();
        li.innerHTML = `
            <div class="app-icon-slot"><div class="app-icon">${initial}</div></div>
            <div class="app-info">
                <h4>${app.name}</h4>
                <p>${t('app.installed')}</p>
            </div>
        `;

        const cachedIcon = appIconCache.get(app.path) || app.icon_base64;
        if (cachedIcon) {
            applyIconToListItem(li, cachedIcon);
            appIconCache.set(app.path, cachedIcon);
        }

        li.addEventListener('click', () => selectApp(app, li));
        listEl.appendChild(li);
    });

    loadAppIconsInBackground(apps, { trackLoadStatus });
}

function applyIconToListItem(li, iconBase64) {
    const slot = li.querySelector('.app-icon-slot');
    if (!slot || !iconBase64) return;
    slot.innerHTML = `<img src="${iconBase64}" class="app-icon" style="width:32px; height:32px; border-radius:8px; object-fit:contain; background: transparent; padding:0;">`;
}

function applyIconByKey(iconKey, iconBase64) {
    if (!iconBase64) return;
    document.querySelectorAll(`.app-item[data-icon-key="${iconKey}"]`).forEach(li => {
        applyIconToListItem(li, iconBase64);
    });
}

async function loadAppIconsInBackground(apps, options = {}) {
    const trackLoadStatus = !!options.trackLoadStatus;

    if (!window.pywebview?.api?.get_app_icon) {
        if (trackLoadStatus) {
            setAppLoadStatus(t('msg.icons_ready'), 'done', 1400);
        }
        return;
    }

    const token = ++iconLoadToken;
    const missing = apps.filter(app => !appIconCache.has(app.path)).slice(0, 80);
    const batchSize = 6;
    let processed = 0;

    if (trackLoadStatus) {
        if (missing.length === 0) {
            setAppLoadStatus(t('msg.icons_ready'), 'done', 1200);
            return;
        }
        setAppLoadStatus(t('msg.icons_loading', { done: 0, total: missing.length }), 'loading');
    }

    for (let i = 0; i < missing.length; i += batchSize) {
        if (token !== iconLoadToken) return;
        const batch = missing.slice(i, i + batchSize);

        await Promise.all(batch.map(async app => {
            try {
                const res = await window.pywebview.api.get_app_icon(app.path);
                const icon = res && res.icon_base64 ? res.icon_base64 : '';
                if (!icon) return;

                appIconCache.set(app.path, icon);
                applyIconByKey(encodeURIComponent(app.path), icon);
            } catch (_e) {
                // Keep fallback initials when icon extraction fails.
            } finally {
                processed += 1;
            }
        }));

        if (trackLoadStatus && token === iconLoadToken) {
            setAppLoadStatus(t('msg.icons_loading', { done: processed, total: missing.length }), 'loading');
        }

        await new Promise(resolve => setTimeout(resolve, 0));
    }

    if (trackLoadStatus && token === iconLoadToken) {
        setAppLoadStatus(t('msg.icons_ready'), 'done', 1400);
    }
}

async function selectApp(app, liElement) {
    // UI Selection state
    document.querySelectorAll('.app-item').forEach(el => el.classList.remove('selected'));
    liElement.classList.add('selected');

    selectedAppObj = app;

    // Toggle panels
    document.getElementById('detail-empty').classList.add('hidden');
    const content = document.getElementById('detail-content');
    content.classList.remove('hidden');

    // Loading State
    document.getElementById('detail-app-name').innerText = app.name;
    document.getElementById('detail-bundle-id').innerText = app.bundle_id || t('msg.unknown_bundle');
    document.getElementById('detail-total-size').innerText = t('msg.scanning');
    document.getElementById('detail-file-count').innerText = '-';

    const fileListEl = document.getElementById('detail-file-list');
    fileListEl.innerHTML = '<div class="loading-spinner"></div>';
    document.getElementById('btn-clean').disabled = true;
    updateCurrentSelectionStatus(t('msg.scanning'));

    try {
        // Trigger Python scan
        const result = await window.pywebview.api.scan_app_leftovers(app.path);

        let allFiles = [];
        result.groups.forEach(g => {
            allFiles = allFiles.concat(g.files);
        });
        currentLeftovers = allFiles;
        currentLeftoversGroups = result.groups;

        document.getElementById('detail-total-size').innerText = result.total_size;
        document.getElementById('detail-file-count').innerText = currentLeftovers.length;

        renderFileTree(result.groups);

        if (currentLeftovers.length > 0) {
            document.getElementById('btn-clean').disabled = false;
            document.getElementById('btn-clean').innerText = t('detail.btn.clean');
            updateCurrentSelectionStatus();
        } else {
            fileListEl.innerHTML = `<p style="padding: 10px; color: var(--text-muted)">${t('msg.empty.leftovers')}</p>`;
            updateCurrentSelectionStatus(t('selection.none'));
        }
    } catch (e) {
        console.error(e);
        fileListEl.innerHTML = `<p style="padding:10px; color:var(--danger)">${t('msg.error.scan_app')}</p>`;
    }
}

function renderFileTree(groups) {
    const fileListEl = document.getElementById('detail-file-list');
    fileListEl.innerHTML = '';

    groups.forEach((g, gIdx) => {
        let groupBytes = g.files.reduce((acc, f) => acc + f.size_bytes, 0);
        let groupDisplaySize = formatBytes(groupBytes);
        const allCheckedInGroup = g.files.length > 0 && g.files.every(shouldAutoSelectFile);
        const groupCheckedAttr = allCheckedInGroup ? 'checked' : '';

        const groupEl = document.createElement('div');
        groupEl.className = 'tree-group expanded';

        groupEl.innerHTML = `
            <div class="tree-header" onclick="this.parentElement.classList.toggle('expanded')">
                <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
                <input type="checkbox" class="custom-checkbox group-checkbox" ${groupCheckedAttr} onclick="event.stopPropagation(); toggleGroup(${gIdx}, this.checked)">
                <div style="flex:1; margin-left:8px;">${localizeCategory(g.category).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
                <div style="color:var(--text-muted); font-size:12px;">${g.files.length} ${t('meta.items')}</div>
                <div style="color:var(--text-main); font-weight:600">${groupDisplaySize}</div>
            </div>
            <div class="tree-content" id="gcv_${gIdx}"></div>
        `;

        const contentEl = groupEl.querySelector('.tree-content');

        g.files.forEach((f, fIdx) => {
            const safePath = f.path.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const escapedPath = JSON.stringify(f.path).replace(/"/g, '&quot;');
            const fileCheckedAttr = shouldAutoSelectFile(f) ? 'checked' : '';
            const fileItem = document.createElement('div');
            fileItem.className = 'file-item';
            fileItem.innerHTML = `
                <input type="checkbox" class="custom-checkbox file-checkbox" ${fileCheckedAttr} data-gidx="${gIdx}" data-fidx="${fIdx}">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="var(--text-muted)" stroke-width="2" fill="none"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"></path><polyline points="13 2 13 9 20 9"></polyline></svg>
                <div class="file-path" title="${safePath}" style="font-size:12px; opacity:0.9">${safePath}</div>
                <div class="file-size" style="font-size:12px; white-space:nowrap; color:var(--text-muted)">${f.display_size}</div>
                <button class="icon-btn file-open-btn" title="${t('btn.open_location')}" onclick="openFileLocation(${escapedPath}, event)">${t('btn.open_location')}</button>
            `;
            fileItem.style.cursor = 'pointer';
            fileItem.addEventListener('click', (e) => {
                if (e.target.tagName === 'INPUT' || e.target.closest('.file-open-btn')) return;
                const chk = fileItem.querySelector('.file-checkbox');
                if (chk) { chk.checked = !chk.checked; updateCurrentSelectionStatus(); }
            });
            contentEl.appendChild(fileItem);
        });

        fileListEl.appendChild(groupEl);
    });

    document.querySelectorAll('.file-checkbox, .group-checkbox').forEach(chk => {
        chk.addEventListener('change', () => updateCurrentSelectionStatus());
    });
    updateCurrentSelectionStatus();
}

window.toggleGroup = function (gIdx, isChecked) {
    const content = document.getElementById('gcv_' + gIdx);
    if (!content) return;
    const checkboxes = content.querySelectorAll('.file-checkbox');
    checkboxes.forEach(chk => chk.checked = isChecked);
    updateCurrentSelectionStatus();
};

async function cleanCurrentApp() {
    let toClean = getSelectedCurrentAppFiles();

    if (toClean.length === 0) {
        alert(t('alert.select_one'));
        return;
    }

    if (!confirmCleanup(toClean, false)) {
        return;
    }

    const btn = document.getElementById('btn-clean');
    const originalText = btn.innerHTML;
    btn.innerHTML = `<span class="loading-spinner" style="width:14px;height:14px;border-width:2px;margin:0;display:inline-block"></span> ${t('btn.cleaning')}`;
    btn.disabled = true;

    const totalToClean = toClean.reduce((acc, f) => acc + (f.size_bytes || 0), 0);
    updateCurrentSelectionStatus(
        t('selection.cleaning', { count: toClean.length, size: formatBytes(totalToClean) }),
    );

    try {
        const res = await window.pywebview.api.clean_files(toClean);
        setUndoAvailable(!!res.undo_available);

        // Refresh scan
        await selectApp(selectedAppObj, document.querySelector('.app-item.selected'));

        if (res.success_count > 0) {
            showToast(t('alert.clean_success', { count: res.success_count, size: res.freed_display }));
        }
        if (res.failed_count > 0) {
            alert(t('alert.delete_failed', { count: res.failed_count }));
            const details = summarizeFailedItems(res);
            if (details) alert(details);
        } else if (res.success_count === 0) {
            alert(t('alert.clean_none'));
        }
    } catch (e) {
        alert(t('msg.error.cleanup', { error: e }));
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.querySelector('.toast-message').innerText = message;
    toast.classList.remove('hidden');
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.classList.add('hidden'), 500);
    }, 3000);
}

async function scanOrphans() {
    const btn = document.getElementById('btn-scan-orphans');
    btn.innerText = t('msg.scanning');
    btn.disabled = true;

    const resDiv = document.getElementById('orphans-results');
    resDiv.classList.remove('hidden');
    resDiv.innerHTML = '<div class="loading-spinner"></div>';

    try {
        const groups = await window.pywebview.api.get_orphans();

        if (groups.length === 0) {
            resDiv.innerHTML = `<div class="empty-state"><p>${t('msg.empty.orphans')}</p></div>`;
            btn.innerText = t('msg.scan_completed');
            return;
        }

        window.orphansDataGroups = groups;
        let cumulativeSize = 0;
        const allOrphanFiles = groups.flatMap(g => g.files || []);
        const allOrphansChecked = allOrphanFiles.length > 0 && allOrphanFiles.every(shouldAutoSelectFile);
        const allOrphansCheckedAttr = allOrphansChecked ? 'checked' : '';

        let html = `<div style="padding: 20px">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid var(--border)">
                <h2>${t('meta.total_found')}: <span style="color:var(--danger)" id="orphans_total_size">0 MB</span></h2>
                <div style="display:flex; gap:16px; align-items:center;">
                    <label style="cursor:pointer; display:flex; align-items:center; gap:6px;">
                        <input type="checkbox" ${allOrphansCheckedAttr} onchange="toggleAllGlobalOrphans(this.checked)" style="accent-color:var(--danger)">
                        ${t('btn.select_all')}
                    </label>
                    <button onclick="cleanOrphansAction()" class="btn-primary" style="background:var(--danger)">${t('btn.clean_all')}</button>
                </div>
            </div>`;

        groups.forEach((g, gIdx) => {
            let totalBytes = g.files.reduce((acc, f) => acc + f.size_bytes, 0);
            cumulativeSize += totalBytes;
            let displaySize = (totalBytes / (1024 * 1024)).toFixed(1) + " MB";
            const groupChecked = g.files.length > 0 && g.files.every(shouldAutoSelectFile);
            const groupCheckedAttr = groupChecked ? 'checked' : '';

            html += `<div style="background: var(--bg-surface-alt); padding: 16px; border-radius: 12px; margin-bottom: 16px;">
                <h3 style="margin-bottom: 8px">
                    <input type="checkbox" ${groupCheckedAttr} onclick="event.stopPropagation(); toggleOrphanGroup(${gIdx}, this.checked)" style="margin-right:12px; accent-color:var(--danger)" class="custom-checkbox">
                    ${g.app_name} <span style="float:right; color:var(--accent)">${displaySize}</span>
                </h3>
                <ul class="file-list" style="margin-bottom: 16px" id="orphans_gcv_${gIdx}">`;

            g.files.forEach((f, fIdx) => {
                const escapedPath = JSON.stringify(f.path).replace(/"/g, '&quot;');
                const fileCheckedAttr = shouldAutoSelectFile(f) ? 'checked' : '';
                html += `<li class="file-item file-row-toggle" style="padding: 8px; cursor: pointer">
                    <input type="checkbox" ${fileCheckedAttr} data-gidx="${gIdx}" data-fidx="${fIdx}" class="custom-checkbox orphan-checkbox" style="margin-right:12px; accent-color:var(--danger)">
                    <span class="file-path">${f.path}</span>
                    <span class="file-size">${localizeCategory(f.category)}</span>
                    <button class="icon-btn file-open-btn" title="${t('btn.open_location')}" onclick="openFileLocation(${escapedPath}, event)">${t('btn.open_location')}</button>
                </li>`;
            });

            html += `</ul></div>`;
        });
        html += '</div>';

        resDiv.innerHTML = html;
        document.getElementById('orphans_total_size').innerText = (cumulativeSize / (1024 * 1024)).toFixed(1) + " MB";
        resDiv.querySelectorAll('.file-row-toggle').forEach(row => {
            row.addEventListener('click', (e) => {
                if (e.target.tagName === 'INPUT' || e.target.closest('.file-open-btn')) return;
                const chk = row.querySelector('input[type="checkbox"]');
                if (chk) chk.checked = !chk.checked;
            });
        });
        btn.innerText = t('btn.completed');
        btn.disabled = false;
    } catch (e) {
        console.error(e);
        resDiv.innerHTML = `<p>${t('msg.error.scan_orphans')}</p>`;
        btn.innerText = t('msg.try_again');
        btn.disabled = false;
    }
}

window.toggleOrphanGroup = function (gIdx, isChecked) {
    const list = document.getElementById('orphans_gcv_' + gIdx);
    if (list) {
        list.querySelectorAll('.orphan-checkbox').forEach(chk => chk.checked = isChecked);
    }
};

window.cleanOrphansAction = async function () {
    let toClean = [];
    document.querySelectorAll('.orphan-checkbox:checked').forEach(chk => {
        let gIdx = chk.getAttribute('data-gidx');
        let fIdx = chk.getAttribute('data-fidx');
        if (window.orphansDataGroups && window.orphansDataGroups[gIdx]) {
            let fileObj = window.orphansDataGroups[gIdx].files[fIdx];
            if (fileObj) toClean.push(fileObj);
        }
    });

    if (toClean.length === 0) {
        alert(t('alert.select_one')); return;
    }
    if (!confirmCleanup(toClean, false)) return;

    try {
        const res = await window.pywebview.api.clean_files(toClean);
        setUndoAvailable(!!res.undo_available);
        if (res.success_count > 0) {
            showToast(t('alert.clean_success', { count: res.success_count, size: res.freed_display }));
        }
        if (res.failed_count > 0) {
            alert(t('alert.delete_failed', { count: res.failed_count }));
            const details = summarizeFailedItems(res);
            if (details) alert(details);
        } else if (res.success_count === 0) {
            alert(t('alert.clean_none'));
        }

        const successSet = new Set(res.success_paths || []);

        // Remove only successfully cleaned items from DOM
        document.querySelectorAll('.orphan-checkbox:checked').forEach(chk => {
            let gIdx = chk.getAttribute('data-gidx');
            let fIdx = chk.getAttribute('data-fidx');
            if (window.orphansDataGroups && window.orphansDataGroups[gIdx]) {
                let fileObj = window.orphansDataGroups[gIdx].files[fIdx];
                if (fileObj && successSet.has(fileObj.path)) {
                    const li = chk.closest('.file-item');
                    if (li) li.remove();
                }
            }
        });

        // If no orphan items remain, show empty state
        const remaining = document.querySelectorAll('.orphan-checkbox');
        if (remaining.length === 0) {
            document.getElementById('orphans-results').innerHTML = `<div class="empty-state"><h3>✅ ${t('msg.all_clean')}</h3></div>`;
        }
    } catch (e) {
        alert(t('msg.error.generic', { error: e }));
    }
};

async function renderGenericList(btnId, resDivId, apiFunc, emptyMsg, isTrash = false) {
    const btn = document.getElementById(btnId);
    btn.innerText = t('msg.scanning');
    btn.disabled = true;

    const resDiv = document.getElementById(resDivId);
    resDiv.classList.remove('hidden');
    resDiv.innerHTML = `
        <div class="radar-scan">
            <div class="radar-ring"></div>
            <div class="radar-ring"></div>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
        </div>
        <p style="text-align:center; color:var(--accent); font-weight:600; margin-top:20px;">${t('msg.loading')}</p>
    `;

    try {
        let files;
        if (apiFunc === 'get_large_files') {
            files = await window.pywebview.api.get_large_files(window.largeFileLimit);
        } else {
            files = await window.pywebview.api[apiFunc]();
        }

        if (files.length === 0) {
            resDiv.innerHTML = `<div class="empty-state"><p>${t(emptyMsg)}</p></div>`;
            btn.innerText = t('btn.completed');
            return;
        }

        let totalBytes = files.reduce((acc, f) => acc + f.size_bytes, 0);
        let displaySize = (totalBytes / (1024 * 1024)).toFixed(1) + " MB";
        const allGenericChecked = files.length > 0 && files.every(shouldAutoSelectFile);
        const allGenericCheckedAttr = allGenericChecked ? 'checked' : '';

        // Generate distinct top-level clean button
        let html = `<div style="padding: 20px">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 1px solid var(--border)">
                <h2>${t('meta.total_found')}: <span style="color:var(--danger)">${displaySize}</span></h2>
                <div style="display:flex; gap:16px; align-items:center;">
                    <label style="cursor:pointer; display:flex; align-items:center; gap:6px;">
                        <input type="checkbox" ${allGenericCheckedAttr} onchange="toggleAllGenericList('${resDivId}', this.checked)" style="accent-color:var(--danger)">
                        ${t('btn.select_all')}
                    </label>
                    <button onclick="cleanGenericList('${resDivId}')" class="btn-primary" style="background:var(--danger)">${isTrash ? t('btn.delete_all') : t('btn.clean_all')}</button>
                </div>
            </div>
            <ul class="file-list" id="${resDivId}-list">`;

        // Store files data globally for cleaning later
        window[resDivId + "_data"] = files;
        window[resDivId + "_isTrash"] = isTrash;

        files.forEach((f, index) => {
            const safePath = f.path.replace(/</g, "&lt;").replace(/>/g, "&gt;");
            const escapedPath = JSON.stringify(f.path).replace(/"/g, '&quot;');
            const fileCheckedAttr = shouldAutoSelectFile(f) ? 'checked' : '';
            html += `<li class="file-item file-row-toggle" style="padding: 12px 16px; margin-bottom: 8px; cursor: pointer">
                <div style="flex:1; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;">
                    <input type="checkbox" id="chk_${resDivId}_${index}" ${fileCheckedAttr} style="margin-right: 12px; accent-color: var(--danger)">
                    <span class="file-path" title="${safePath}">${safePath}</span>
                </div>
                <div class="file-meta">
                    <span class="file-category">${localizeCategory(f.category)}</span>
                    <span class="file-size">${f.display_size}</span>
                    <button class="icon-btn file-open-btn" title="${t('btn.open_location')}" onclick="openFileLocation(${escapedPath}, event)">${t('btn.open_location')}</button>
                </div>
            </li>`;
        });

        html += `</ul></div>`;
        resDiv.innerHTML = html;
        resDiv.querySelectorAll('.file-row-toggle').forEach(row => {
            row.addEventListener('click', (e) => {
                if (e.target.tagName === 'INPUT' || e.target.closest('.file-open-btn')) return;
                const chk = row.querySelector('input[type="checkbox"]');
                if (chk) chk.checked = !chk.checked;
            });
        });
        btn.innerText = t('msg.scan_completed');
        btn.disabled = false;
    } catch (e) {
        console.error(e);
        resDiv.innerHTML = `<p>${t('msg.error.scan_generic')}</p>`;
        btn.innerText = t('msg.try_again');
        btn.disabled = false;
    }
}

function scanSystemJunk() {
    renderGenericList('btn-scan-system', 'system-results', 'get_system_junk', 'msg.empty.sys');
}

function scanLargeFiles() {
    renderGenericList('btn-scan-large', 'large-results', 'get_large_files', 'msg.empty.large');
}

function scanDevJunk() {
    renderGenericList('btn-scan-dev', 'dev-results', 'get_dev_junk', 'msg.empty.dev');
}

function scanTrash() {
    renderGenericList('btn-scan-trash', 'trash-results', 'get_trash', 'msg.empty.trash', true);
}

async function cleanGenericList(resDivId) {
    const filesData = window[resDivId + "_data"];
    if (!filesData) return;
    const isTrash = window[resDivId + "_isTrash"] || false;

    // Filter out only checked
    let toClean = [];
    filesData.forEach((f, idx) => {
        let chk = document.getElementById(`chk_${resDivId}_${idx}`);
        if (chk && chk.checked) {
            toClean.push(f);
        }
    });

    if (toClean.length === 0) {
        alert(t('alert.select_one'));
        return;
    }

    if (!confirmCleanup(toClean, isTrash)) {
        return;
    }

    try {
        const apiMethod = isTrash ? 'empty_trash' : 'clean_files';
        const res = await window.pywebview.api[apiMethod](toClean);
        if (!isTrash) {
            setUndoAvailable(!!res.undo_available);
        }
        if (res.success_count > 0) {
            showToast(t('alert.clean_success', { count: res.success_count, size: res.freed_display }));
        }
        if (res.failed_count > 0) {
            alert(t('alert.delete_failed', { count: res.failed_count }));
            const details = summarizeFailedItems(res);
            if (details) alert(details);
        } else if (res.success_count === 0) {
            alert(t('alert.clean_none'));
        }

        if (isTrash) {
            // Trash permissions and stale entries can desync quickly; refresh from source.
            scanTrash();
            return;
        }

        // Remove only successfully cleaned items from UI
        const successSet = new Set(res.success_paths || []);
        const remaining = [];

        filesData.forEach((f, idx) => {
            const chk = document.getElementById(`chk_${resDivId}_${idx}`);
            const li = chk ? chk.closest('.file-item') : null;
            if (chk && chk.checked && successSet.has(f.path)) {
                // Remove the successfully cleaned item from DOM
                if (li) li.remove();
            } else {
                remaining.push(f);
            }
        });

        // Update stored data with remaining files
        window[resDivId + "_data"] = remaining;

        // Re-index checkboxes for remaining items
        const listEl = document.getElementById(`${resDivId}-list`);
        if (listEl) {
            const items = listEl.querySelectorAll('.file-item');
            items.forEach((item, newIdx) => {
                const chk = item.querySelector('input[type="checkbox"]');
                if (chk) chk.id = `chk_${resDivId}_${newIdx}`;
            });
        }

        // Show empty state only if nothing remains
        if (remaining.length === 0) {
            document.getElementById(resDivId).innerHTML = `<div class="empty-state"><h3>✅ ${t('msg.all_clean')}</h3></div>`;
        }
    } catch (e) {
        alert(t('msg.error.clean_files', { error: e }));
    }
}

window.toggleAllAppFiles = function (isChecked) {
    document.querySelectorAll('#detail-file-list .file-checkbox').forEach(chk => {
        chk.checked = isChecked;
    });
    updateCurrentSelectionStatus();
};

window.toggleAllGlobalOrphans = function (isChecked) {
    document.querySelectorAll('#orphans-results .orphan-checkbox').forEach(chk => {
        chk.checked = isChecked;
    });
    // Toggle the visible group headers as well
    document.querySelectorAll('#orphans-results .custom-checkbox').forEach(chk => {
        if (!chk.classList.contains('orphan-checkbox')) {
            chk.checked = isChecked;
        }
    });
};

window.toggleAllGenericList = function (resDivId, isChecked) {
    document.querySelectorAll('#' + resDivId + '-list input[type="checkbox"]').forEach(chk => {
        chk.checked = isChecked;
    });
};
