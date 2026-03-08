# jepx-data-analytics-platform
## 1. 全体アーキテクチャ

```mermaid
flowchart TD
    A[Windows Task Scheduler / cron] --> B[main.py]
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

## 2. ETLの流れ

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

## 3. ディレクトリ構成と責務

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

### 各ファイルの責務

- `main.py`  
  全体の実行制御を担当するエントリポイント

- `config.py`  
  URL、保存先、DB名など設定値を管理する

- `downloader.py`  
  JEPXデータの取得と raw 保存を担当する

- `processor.py`  
  生データの整形、列整理、型変換、必要列抽出を担当する

- `database.py`  
  SQLiteへの保存、テーブル作成、重複制御を担当する

- `logger.py`  
  ログ出力設定を担当する

---

## 4. Phase A の実行フロー（Windowsローカル）

```mermaid
sequenceDiagram
    participant S as Task Scheduler
    participant M as main.py
    participant D as downloader.py
    participant P as processor.py
    participant DB as SQLite

    S->>M: 定期実行
    M->>D: JEPXデータ取得開始
    D->>D: 公開データダウンロード
    D->>M: raw保存完了
    M->>P: データ整形依頼
    P->>P: 列整理・型変換・必要列抽出
    P->>M: processed保存完了
    M->>DB: SQLiteへ保存
    DB->>M: 保存完了
    M->>M: ログ出力
```

---

## 5. Phase C の実行フロー（ミニPC + Linux）

```mermaid
sequenceDiagram
    participant C as cron
    participant M as main.py
    participant D as downloader.py
    participant P as processor.py
    participant DB as SQLite/PostgreSQL
    participant LOG as logs/

    C->>M: 毎日定時実行
    M->>D: JEPXデータ取得
    D->>M: raw保存
    M->>P: データ整形
    P->>M: processed保存
    M->>DB: DB保存
    M->>LOG: 実行ログ出力
```

---

## 6. 長期研究アーキテクチャ

```mermaid
flowchart TD
    A[JEPX価格データ蓄積] --> B[時系列DB / SQLite]
    B --> C[スパイク検出]
    C --> D[極値分布フィッティング]
    D --> E[臨界現象との比較]
    E --> F[電力需給モデル構築]
```

---

## 7. 将来拡張アーキテクチャ

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

    L[AWS Lambda / EC2] -. 将来移行 .-> B
    M[S3 / PostgreSQL] -. 将来移行 .-> E
```

---

## 8. アーキテクチャ設計方針

このプロジェクトでは以下の設計方針を採用する。

1. **責務分離**  
   取得、整形、保存、分析を分離する

2. **ローカル完結で開始**  
   まずはWindowsローカルで完成させる

3. **Linux移植を前提に設計**  
   `pathlib`、設定分離、ログ管理により移植性を高める

4. **将来のクラウド化を阻害しない**  
   スケジューラとアプリ本体を分離し、保存先も差し替え可能にする

5. **研究基盤として育てる**  
   単なる取得ツールではなく、スパイク検出・極値統計・臨界現象解析につながる基盤とする