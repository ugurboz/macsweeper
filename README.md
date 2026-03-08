# MacSweeper Pro

MacSweeper Pro, macOS uygulamalarını kaldırdıktan sonra kalan dosyaları tarayan ve güvenli temizlik yapmayı kolaylaştıran bir araçtır.

## Neden Bu Projeyi Yaptık

macOS için çıkan temizleyici uygulamaların büyük kısmı ücretli veya abonelik modelinde. MacSweeper Pro'yu, herkesin kullanabilecegi, inceleyebilecegi ve gelistirebilecegi pratik bir alternatif sunmak icin yaptik.

Bu projeyi acik kaynak tutarak toplulugun su katkilarini hedefliyoruz:

- temel temizlik ozelliklerine ucretsiz erisim
- temizleme mantiginin seffaf sekilde incelenebilmesi
- guvenlik kontrolleri ve yeni ozellikler icin topluluk katkisi

## Ozellikler

- Secilen bir `.app` paketi icin kalan dosyalari tarama
- Sonuclari kategoriye gore gruplama (Cache, Preferences, Logs vb.)
- Dosyalari kalici silmek yerine Cop'e tasima
- Son temizlik islemine geri alma (Cop'ten geri yukleme)
- Sistem temizlik modulleri:
  - Sistem/Kullanici onbellek ve log taramasi
  - Buyuk dosya taramasi
  - Gelistirici artiklari taramasi (Xcode, iOS backup)
  - Cop taramasi ve Cop'u bosaltma
- `pywebview` tabanli arayuz
- Hizli test icin CLI modu

## Gereksinimler

- macOS
- Python 3.10+

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Calistirma

Arayuz modu:

```bash
python3 main.py
```

CLI modu:

```bash
python3 main.py --cli
python3 main.py /Applications/Safari.app
```

## Testler

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## Paketleme

### py2app ile `.app` olusturma

```bash
python3 setup.py py2app
```

### PyInstaller ile `.app` olusturma

```bash
./scripts/build_macos.sh
```

### DMG olusturma

```bash
./build_dmg.sh
```

## Hazir DMG (Dogrudan Dagitim)

Repoda dogrudan kurulum icin hazir bir DMG dosyasi tutulur:

- `MacSweeper_Pro_Installer.dmg`

Bu dosyayi olusturmak/guncellemek icin:

```bash
./build_dmg.sh
```

## GitHub Push Notlari

`.gitignore` dosyasi gereksiz dosyalarin repoya gitmesini engeller:

- `build/`, `dist/`, `DMG_Temp/`
- `__pycache__/`, `*.pyc`
- sanal ortamlar (`.venv/`, `venv/`)
- uretilen paketler (`*.app`, `*.spec`)

Eger bu dosyalardan baziari daha once track edildiyse bir kez untrack et:

```bash
git rm -r --cached build dist DMG_Temp __pycache__ .venv venv
```

Sonra normal sekilde commit al:

```bash
git add .
git commit -m "README ve gitignore guncellendi"
```
