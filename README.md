motty
=====

SharePoint、JIRA、NAS上の共有フォルダ、Confluence、他のMCPサーバーを横断して検索し、
自然言語の質問に対してチャットボット的に結果を返すツールです。

## セットアップ

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

## 設定ファイル例 (`config.json`)

```json
{
  "max_results_per_source": 5,
  "connectors": {
    "jira": [
      {
        "base_url": "https://your-domain.atlassian.net",
        "email": "you@example.com",
        "api_token": "your-token"
      }
    ],
    "confluence": [
      {
        "base_url": "https://your-domain.atlassian.net/wiki",
        "email": "you@example.com",
        "api_token": "your-token"
      }
    ],
    "sharepoint": [
      {
        "tenant_id": "your-tenant-id",
        "client_id": "your-client-id",
        "client_secret": "your-client-secret"
      }
    ],
    "nas": [
      {
        "root_path": "/mnt/shared"
      }
    ],
    "mcp": [
      {
        "base_url": "https://mcp.example.com",
        "api_key": "optional-api-key"
      }
    ]
  }
}
```

## 使い方

```bash
motty "リリースノートについて教えて"
```

```bash
motty "機能Xの障害状況" --config config.json
```
