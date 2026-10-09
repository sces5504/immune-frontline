# 免疫前線｜Immune Frontline

醫學系 clerk 可閱讀的像素免疫策略遊戲。每回合一個指令，等待時只有動畫，不會自行推進感染。

- [直接遊玩最新版](https://sces5504.github.io/immune-frontline/)
- [版本檔案室：每版皆可獨立遊玩](https://sces5504.github.io/immune-frontline/versions/)

## 版本與還原

所有發布版本均有獨立 HTML 備份、SHA-256 雜湊、變更說明與 Git 標籤。舊版不會被覆寫。

要把網站暫時切到舊版：開啟 **Actions → Deploy game to GitHub Pages → Run workflow**，在版本欄填入例如 `1.0.0`（留空代表最新來源）。這不會刪除或重設任何程式歷史。下次推送 `main` 會重新部署最新來源。

要永久把主要來源還原，可請 Codex 還原指定版本；還原會以一個新的版本發布，保留其他版本。

## 修改與發布

遊戲唯一來源是 `outputs/immune-frontline.html`。修改完成後：

1. 更新遊戲內的版本號。
2. 執行 `node scripts/check_game.cjs`。
3. 執行 `python3 scripts/release.py --version X.Y.Z --title '版本名稱' --notes '變更說明'`。
4. 提交改動，新增相同的 `vX.Y.Z` 標籤，再推送到 `main`。GitHub Actions 自動發布最新遊戲及全部備份。

本遊戲將細胞反應時間和戰場數量簡化。科普重點在免疫功能分工，不代表臨床處置。
