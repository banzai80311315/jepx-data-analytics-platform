# jepx-data-analytics-platform

JEPX（日本卸電力取引所）の電力価格データを収集・蓄積・分析し、  
電力価格スパイクの統計的性質を研究するためのデータ分析基盤。

最終的な研究テーマ：

```
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

本プロジェクトは **Windowsホスト + Ubuntu VM** 上で開発する。

```mermaid
flowchart TD
    A[Windows Host]
    A --> B[VirtualBox]
    B --> C[Ubuntu VM]
    C --> D[Python Environment]
    D --> E[JEPX Data Analytics Platform]
```

この構成により以下を実現する。

- Linuxサーバー環境での開発
- cronベースのバッチ処理
- 将来のLinuxサーバー・クラウド移行

---

# 2. 全体アーキテクチャ

```mermaid
flowchart TD
    A[cron Scheduler] --> B[main.py]
    B --> C[downloader.py]
    C --> D[JEPX公開データ取得]
    C --> E[data/raw/ に生データ保存]

    B --> F[processor.py]
    E --> F
    F --> G[列名整理・型変換・必要列抽出]
    G --> H[data/processed/ に整形済みデータ保存]

    B --> I[database.py]
    H --> I
    I --> J[(SQLite Database)]

    B --> K[analysis scripts]
    J --> K
    K --> L[スパイク検出]
    K --> M[時系列分析]
    K --> N[極値分布解析]
    K --> O[臨界現象との比較]
    K --> P[電力需給モデル]
```

---

# 3. ETLの流れ

```mermaid
flowchart LR
    A[JEPXデータ] --> B[Extract: downloader.py]
    B --> C[Raw保存]
    C --> D[Transform: processor.py]
    D --> E[Processed保存]
    E --> F[Load: database.py]
    F --> G[(SQLite)]
    G --> H[Analysis]
```

---

# 4. ディレクトリ構成と責務

```mermaid
flowchart TD
    A[jepx_project/] --> B[app/]
    A --> C[data/]
    A --> D[logs/]
    A --> E[requirements.txt]
    A --> F[README.md]

    B --> B1[main.py]
    B --> B2[config.py]
    B --> B3[downloader.py]
    B --> B4[processor.py]
    B --> B5[database.py]
    B --> B6[logger.py]

    C --> C1[raw/]
    C --> C2[processed/]
    C --> C3[jepx.sqlite3]
```

---

## 各ファイルの責務

### main.py
全体の実行制御を担当するエントリポイント

### config.py
URL、保存先、DB名など設定値を管理

### downloader.py
JEPXデータの取得と raw 保存

### processor.py
生データ整形

- 列整理
- 型変換
- 必要列抽出

### database.py
SQLite保存処理

- テーブル作成
- 重複制御

### logger.py
ログ設定

---

# 5. Phase A 実行フロー（Ubuntu VM）

```mermaid
sequenceDiagram
    participant C as cron
    participant M as main.py
    participant D as downloader.py
    participant P as processor.py
    participant DB as SQLite
    participant LOG as logs/

    C->>M: 定期実行
    M->>D: JEPXデータ取得開始
    D->>D: 公開データダウンロード
    D->>M: raw保存
    M->>P: データ整形
    P->>M: processed保存
    M->>DB: SQLite保存
    M->>LOG: ログ出力
```

---

# 6. 将来の運用アーキテクチャ

Ubuntu VMで完成したシステムを  
**ミニPC Linux サーバーへ移植する。**

```mermaid
flowchart TD
    A[Ubuntu VM 開発環境]
    A --> B[Linux Mini Server]
    B --> C[cron Scheduler]
    C --> D[JEPX Downloader]
    D --> E[Database]
    E --> F[Analysis]
```

---

# 7. 長期研究アーキテクチャ

```mermaid
flowchart TD
    A[JEPX価格データ蓄積] --> B[時系列DB / SQLite]
    B --> C[スパイク検出]
    C --> D[極値分布フィッティング]
    D --> E[臨界現象との比較]
    E --> F[電力需給モデル構築]
```

---

# 8. 将来拡張アーキテクチャ

```mermaid
flowchart TD
    A[Scheduler] --> B[Python ETL]
    B --> C[Raw Storage]
    B --> D[Processed Storage]
    D --> E[(Database)]

    E --> F[Analysis API / FastAPI]
    F --> G[Web Dashboard]

    E --> H[統計分析]
    H --> I[極値分布]
    H --> J[相関分析]
    H --> K[需給モデル]

    L[AWS EC2 / Lambda] -. 将来移行 .-> B
    M[S3 / PostgreSQL] -. 将来移行 .-> E
```

---

# 9. アーキテクチャ設計方針

本プロジェクトでは以下の設計原則を採用する。

### 1. 責務分離
取得・整形・保存・分析を分離する

### 2. Linuxサーバー前提設計
開発環境は Ubuntu VM を使用

### 3. cronベースのバッチ処理
定期実行は Linux cron で制御

### 4. 移植性を重視
将来的に

```
Ubuntu VM
↓
Linuxミニサーバー
↓
クラウド
```

へ移行可能な設計とする。

### 5. 研究基盤として設計
単なる取得ツールではなく

- スパイク検出
- 極値統計
- 臨界現象解析

につながるデータ基盤として設計する。