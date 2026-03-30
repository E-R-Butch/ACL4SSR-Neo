# ACL4SSR-Neo 🚀

> 基于 [ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) 规则深度定制的 Clash 分流规则集，整合了多家优质去广告规则源，更精简、更干净。

---

## ✨ 特性

- 🎯 **精细分流**：按服务类型独立分组，国内直连 / 国外代理 / 媒体解锁开箱即用
- 🛑 **超强去广告**：整合 ACL4SSR + ConnersHua + lhie1 三大规则源，严格去重合并，拦截效果非常好
- 🎮 **游戏优化**：游戏运行与游戏下载独立分组，可自由切换，避免浪费代理流量
- 🗺️ **智能区域路由**：自动按节点名称匹配🇭🇰港 / 🇨🇳台 / 🇸🇬新 / 🇯🇵日 / 🇺🇲美 / 🇰🇷韩，自动测速选最优
- ✏️ **自定义直连表**：`CustomDirect.list` 优先级最高，可随时追加你自己的直连域名
- 🔒 **运营商劫持屏蔽**：涵盖 ConnersHua `Hijacking.list`，有效防御 DNS 劫持与中间人注入

---

## 📁 新版项目结构 (Ingredient-First Architecture)

```text
Clash/
├── Core/                # 🟢 核心翻墙及直连代理规则 (CustomDirect, ProxyGFWlist 等)
├── Ingredients/         # 📦 原始“食材”素材库 (AdBlock 去广告源、China 国内特色源等)
├── Ruleset/             # 🔵 具体应用级别细化分流规则 (Apple, Netflix 等 100+ 项)
├── Outputs/             # 🍲 加工后的成品列表 (如三源深度去重合并的 MergedADBan)
├── Providers/           # 🟡 yaml 格式的 Rule Providers 规则库
└── config/              # 📖 点菜单/主配置 (包含 ACL4SSR_Online_Full.ini)
```

---

## 🚀 快速使用

配合 [Subconverter](https://github.com/tindy2013/subconverter) 在线订阅转换工具使用：

将以下地址作为「远程配置」粘贴到转换面板的配置文件栏：

```
https://raw.githubusercontent.com/E-R-Butch/ACL4SSR-Neo/master/Clash/config/ACL4SSR_Online_Full.ini
```

然后填入你的节点订阅地址，即可生成完整 Clash 配置。

---

## 🗂️ 策略组一览

| 策略组 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| 🚀 节点选择 | select | DIRECT | 主出口，统筹全局 |
| 🚀 手动切换 | select | — | 手动节点全量列表 |
| ♻️ 自动选择 | url-test | — | 全节点自动测速 |
| 🇭🇰 香港节点 | url-test | — | 按名自动归类 |
| 🇨🇳 台湾节点 | url-test | — | 按名自动归类 |
| 🇸🇬 狮城节点 | url-test | — | 按名自动归类 |
| 🇯🇵 日本节点 | url-test | — | 按名自动归类 |
| 🇺🇲 美国节点 | url-test | — | 按名自动归类 |
| 🇰🇷 韩国节点 | url-test | — | 按名自动归类 |
| 🎥 奈飞节点 | select | — | 支持 Netflix 解锁的节点单独归类 |
| 📹 油管视频 | select | 节点选择 | YouTube |
| 🎥 奈飞视频 | select | 奈飞节点 | Netflix |
| 📺 巴哈姆特 | select | 台湾节点 | 台湾网络才能访问 |
| 🌍 国外媒体 | select | 节点选择 | Spotify、Disney+ 等 |
| 🌏 国内媒体 | select | DIRECT | 爱奇艺、优酷等 |
| 📲 电报消息 | select | 节点选择 | Telegram |
| 🍎 苹果服务 | select | DIRECT | Apple 相关服务 |
| Ⓜ️ 微软云盘 | select | DIRECT | OneDrive |
| 🎮 游戏平台 | select | **DIRECT** | 避免走代理导致延迟 |
| 🎮 游戏下载 | select | **DIRECT** | 避免浪费代理流量 |
| 🛑 广告拦截 | select | REJECT | 三方合并超强去广告 |
| 🎯 全球直连 | select | DIRECT | 国内 / 自定义直连 |
| 🐟 漏网之鱼 | select | DIRECT | 未匹配规则兜底 |

---

## 📜 规则来源致谢

| 规则源 | 说明 |
|--------|------|
| [ACL4SSR/ACL4SSR](https://github.com/ACL4SSR/ACL4SSR) | 本项目基础规则集 |
| [ConnersHua/Profiles](https://github.com/ConnersHua/Profiles) | 广告/劫持拦截规则 |
| [lhie1/Rules](https://github.com/lhie1/Rules) | 广告拦截规则（归档） |
| [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script) | lhie1 归档的社区维护版 |

---

## 📝 许可证

本项目基于 [GNU General Public License v3.0](./LICENCE) 开源。
