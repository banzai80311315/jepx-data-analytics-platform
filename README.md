# jepx-data-analytics-platform

JEPX（日本卸電力取引所）の電力価格データを分析する  
インタラクティブ分析アプリケーション。

JEPXが公開している年度CSVデータを読み込み、

- 任意期間
- エリア
- 分析手法

を指定して、ブラウザ上から電力価格分析を行う。

本アプリは、電力価格スパイクの統計的性質を研究するための  
**分析プラットフォーム**として設計している。

---

# 研究テーマ

最終的な研究テーマ：

```text
JEPX価格
↓
スパイク検出
↓
極値分布
↓
臨界現象
↓
電力需給モデル
```

---

# 1. 開発環境アーキテクチャ

本プロジェクトは **Windowsホストで開発し、Ubuntu VM を実行環境として使用する。**  
コード編集は **VS Code + Remote SSH** を用いて、Ubuntu VM 上のプロジェクトを直接編集する。

```mermaid
flowchart TD
    A[Windows Host]
    A --> B[VS Code]
    A --> C[Browser]
    A --> D[Git]
    A --> E[VirtualBox]

    B -->|Remote SSH| F[Ubuntu VM]
    E --> F

    F --> G[Python Environment]
    G --> H[Streamlit App]
```

この構成により以下を実現する。

- Windows上の快適な開発環境
- Linuxサーバー環境での実行
- VS Code から Ubuntu VM への直接開発
- Streamlit によるローカル分析アプリ
- 将来の Linux サーバー・クラウド移行

---

# 2. 開発フロー

本プロジェクトの基本的な開発フローは以下である。

```mermaid
flowchart LR
    A[Windows VS Code] -->|Remote SSH| B[Ubuntu VM]
    B --> C[コード編集]
    C --> D[streamlit run app.py]
    D --> E[ブラウザで分析]
```

実務イメージとしては次に近い。

```text
開発PC
↓
SSH
↓
Linuxサーバー
↓
アプリ実行
```

---

# 3. 全体アーキテクチャ

```mermaid
flowchart TD
    A[Browser] --> B[Streamlit UI]

    B --> C[Analysis Controller]

    C --> D[CSV Loader]
    D --> E[JEPX CSV Dataset]

    C --> F[Data Processor]
    F --> G[Clean Data]

    C --> H[Analysis Modules]

    H --> I[時系列分析]
    H --> J[分布分析]
    H --> K[スパイク検出]
    H --> L[極値解析]
```

---

# 4. データ分析フロー

```mermaid
flowchart LR
    A[JEPX CSV] --> B[Load]
    B --> C[Preprocess]
    C --> D[Analysis]
    D --> E[Visualization]
```

---

# 5. ディレクトリ構成と責務

```mermaid
flowchart TD
    A[jepx-data-analytics-platform/] --> B[app/]
    A --> C[data/]
    A --> D[logs/]
    A --> E[requirements.txt]
    A --> F[README.md]
    A --> G[notebooks/]

    B --> B1[app.py]
    B --> B2[loader.py]
    B --> B3[processor.py]
    B --> B4[analyzer.py]
    B --> B5[visualizer.py]
    B --> B6[config.py]

    C --> C1[raw CSV]
    C --> C2[processed data]
```

---

## 各ファイルの責務

### app.py
Streamlitアプリ本体  
UIと分析実行を管理

---

### loader.py
JEPX CSV読み込み

- CSVロード
- pandas DataFrame化

---

### processor.py
データ整形

- 列整理
- 日付変換
- 欠損処理

---

### analyzer.py
分析ロジック

- 時系列分析
- 分布分析
- スパイク検出
- 極値解析

---

### visualizer.py
グラフ描画

- matplotlib / plotly

---

### config.py
設定管理

---

# 6. アプリ実行フロー

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant S as Streamlit
    participant A as Analyzer
    participant D as Dataset

    U->>B: 分析条件入力
    B->>S: Streamlit UI
    S->>A: 分析実行
    A->>D: CSVデータ読み込み
    A->>S: 分析結果
    S->>B: グラフ表示
```

---

# 7. 将来の運用アーキテクチャ

Ubuntu VMで開発したアプリを  
**ミニPC Linux サーバーへ移植する。**

```mermaid
flowchart TD
    A[Windows + VS Code]
    A -->|Remote SSH| B[Ubuntu VM]

    B --> C[Streamlit App]

    C --> D[Browser]

    B --> E[Linux Mini Server]
```

---

# 8. 長期研究アーキテクチャ

```mermaid
flowchart TD
    A[JEPX価格データ] --> B[時系列分析]
    B --> C[スパイク検出]
    C --> D[極値分布フィッティング]
    D --> E[臨界現象との比較]
    E --> F[電力需給モデル構築]
```

---

# 9. 将来拡張アーキテクチャ

```mermaid
flowchart TD
    A[Streamlit App] --> B[Analysis Modules]
    B --> C[統計分析]
    B --> D[極値分布]
    B --> E[相関分析]
    B --> F[需給モデル]

    G[FastAPI] -. 将来拡張 .-> A
    H[Web Dashboard] -. 将来拡張 .-> A
```

---

# 10. アーキテクチャ設計方針

本プロジェクトでは以下の設計原則を採用する。

### 1. 責務分離
データ読み込み・整形・分析・可視化を分離する

### 2. 開発環境と実行環境の分離
Windows を開発母艦、Ubuntu VM を実行環境とする

### 3. Streamlitによる分析アプリ
Pythonコードを書かずに分析可能なUIを提供する

### 4. Remote SSH による開発
VS Code から Ubuntu VM に接続し、Linux 上のファイルを直接編集する

### 5. 移植性を重視
将来的に

```text
Ubuntu VM
↓
Linuxミニサーバー
↓
クラウド
```

へ移行可能な設計とする。

### 6. 研究基盤として設計
単なる分析ツールではなく

- スパイク検出
- 極値統計
- 臨界現象解析

につながる分析基盤とする。