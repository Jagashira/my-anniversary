# 📘 Photo Album PDF Generator

A lightweight Python tool that converts a folder of photos into **high-quality PDF albums**.  
Two PDFs are automatically generated:

- **A4 Album:** Each photo placed on its own A4 page, centered and scaled to fit
- **Original-Size Album:** Pages sized exactly to each image (見開き対応)

Perfect for creating travel albums, anniversary albums, printed photo books, or digital archives.

---

## 🚀 Features

### 🖼 A4 Album

- 1 ページに 1 枚だけ写真を配置
- 写真は A4 サイズ内に最大フィット
- 表紙と中身で縮尺が統一された綺麗な仕上がり
- 印刷用のアルバムとして最適

### 📖 Original-Size Album (見開き)

- ページサイズ＝写真の元のピクセルサイズ
- 2 枚ずつ横に並べて見開きページを作成  
  （奇数の場合は最後の 1 枚だけ単独）
- 高解像度アーカイブに最適

### ⚡ Additional Features

- **tqdm による進捗バー表示**
- **requirements.txt を自動生成**
- **画像を RGB 変換して PDF 互換性を保証**
- **連番ソートで安定したページ順**
- **dist/<フォルダ名>/ に全出力を自動生成**

---

## 📂 Project Structure

```
make_album/
├── make_album.py
├── exporter.py
├── image_loader.py
├── layout.py
├── utils.py
└── dist/
```

---

## 🛠 Installation

### 1. Clone the project

```bash
git clone <your-repo-url>
cd make_album
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install Pillow reportlab tqdm
```

初回実行時には `requirements.txt` が自動生成されます。

---

## 📸 Usage

### 1. Prepare your images

```
photos/
 ├── 1.png
 ├── 2.jpg
 ├── 3.jpeg
 └── ...
```

### 2. Generate PDFs

```bash
python make_album.py photos
```

### 3. Output files

```
dist/photos/
 ├── album_A4.pdf
 └── album_original.pdf
```

---

## 📝 PDF Output Details

### A4 Album

- サイズ：A4 縦固定
- 最大フィットした写真を中央に 1 ページ 1 枚
- 写真のアスペクト比は完全維持

### Original-Size Album

- 元の写真サイズをそのまま利用
- 見開き構成（2 枚）
- 高解像度の保存・配布用

---

## 💻 Example Progress Output

```
A4版 作成中:  45%|█████████▍        | 5/11
原寸版 見開き作成中:  33%|█████▎      | 2/6
```

---

## 🔧 Internal Modules Overview

### image_loader.py

- フォルダ内の png/jpg/jpeg を読み込み
- ファイル名の数字順にソート
- RGB に変換して PDF 互換

### layout.py

- A4 フィット計算
- 高品質 LANCZOS リサイズ

### exporter.py

- A4 版 → 1 ページ 1 枚
- 原寸版 → 見開き構成

### utils.py

- requirements.txt をプロジェクトルートに生成

---

## 🤝 Contributing

Issues や Pull Requests は歓迎します！  
新機能の提案や改善点もぜひ。

---
