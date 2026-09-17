# 企业微信智能表格 YouTube 数据读取与写入

让营销人员在企业微信智能表格中，根据公开视频链接更新 YouTube 播放量、点赞数和发布时间。

## 能做什么

- 从指定智能表格读取 YouTube 链接。
- 使用 YouTube 官方 Data API 批量查询公开指标。
- 先显示逐行更新预览；只有明确确认后才写回。
- 写入后重新读取核验结果。

不抓取 YouTube 网页；不保存或上传任何 API Key、机器人凭证、Webhook 地址或企业内部表格链接。

## 一次性初始化

1. 安装 Node.js 18 或更新版本。
2. 安装并授权企业微信命令行工具：

   ```text
   npm install -g @wecom/cli
   npx skills add WeComTeam/wecom-cli -y -g
   wecom-cli auth init
   ```

3. 在 Google Cloud 项目中启用 YouTube Data API v3，并创建 API Key。
4. 不需要手动寻找或创建 `.env`。在 Skill 文件夹中运行：

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\setup-local-config.ps1
   ```

   会出现一个本地密码遮罩弹窗。粘贴 Key 后按 Enter 或点击“保存”；脚本会自动创建本机 `.env`。如果已有配置，弹窗会要求再次确认才会替换。

5. 不要将自动生成的 `.env` 发给任何人或上传到 GitHub。

## 表格准备

至少准备两列：

| 用途 | 建议字段类型 | 示例字段名 |
| --- | --- | --- |
| 视频链接 | 超链接 | 视频链接 |
| 播放量 | 数字 | 播放量 |

可选增加“点赞数”（数字）和“发布时间”（日期/文本）。首次运行时，Skill 会读取字段并请你确认实际映射，绝不按名称猜测。

## 日常使用

在 Codex 中提供目标智能表格链接，并说：

```text
更新这个智能表格中 YouTube 链接对应的播放量、点赞数和发布时间；先给我预览，确认后再写入。
```

Skill 会处理读取、预览、确认和核验。没有链接、非 YouTube 链接、私密或不可用视频会列为异常，并保持原数据不变。

## Webhook 说明

默认使用企业微信 CLI 更新现有记录。只有 CLI 返回权限限制时才考虑 Webhook；Webhook 地址是敏感写入凭证，而且不能可靠更新人工创建的历史记录。

## 本地验证

```text
python -m unittest tests/test_youtube_metrics.py -v
```
