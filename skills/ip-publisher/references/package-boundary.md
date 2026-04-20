# Package Boundary

这个已发布的 `ip-publisher` skill 包，默认只包含当前 skill 目录中的说明文件与参考文件。它的默认职责是：围绕用户给定的话题，生成 Xiaohongshu、WeChat Official Account 和 Zhihu 三个平台版本，并整理成一份可审阅的发布包说明。

为了避免能力误解，需要明确区分两类资产。

| 资产类型 | 是否属于当前已安装 skill 包 | 说明 |
| --- | --- | --- |
| `SKILL.md`、`prompt.md`、`references/*` | 是 | 属于当前 skill 包，安装后即可读取 |
| 仓库根目录下的 `scripts/*.py` | 否 | 它们属于 companion repo 资源，不应被默认假设为当前 skill 包自带资产 |
| 用户本地配置文件 | 否 | 不属于 skill 包内容；默认也不应被读取或写入 |
| 第三方发布工具、浏览器插件、平台账号 | 否 | 不属于当前 skill 包，也不是默认依赖 |

如果用户明确要求使用仓库脚本、本地配置文件或外部发布工具，应该先说明这已经进入 **companion repo mode** 或外部工具模式，而不是当前已安装 skill 的默认运行边界。
