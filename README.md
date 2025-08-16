# PuppetMaster: 专注Linux C2商业定制版研发 
# PuppetMaster: Focus on customized business Linux-C2

**Contact To: r4be1@foxmail.com**

仅支持定制并不打算广泛销售，不同客户的方案和植入物都不同，保证互不影响及稳定可靠性。

_It only supports customization and is not intended for widespread sales. Different customers have different plans and implants to ensure no mutual impact and stable reliability._

一切一切的前提是合法合规！若非国内红队大厂单位使用，上线地区严格写死 **禁止大陆港澳地区** 不支持一切形式的黑灰产活动！购买前请向公安机关或有关单位备案，一经发现违规使用将主动上报公安或相关单位，积极配合调查。关于这点可能会有猜忌说变相偷权限，格局大点吧偷权限都十年前前辈们玩剩的了，对这种事情一点兴趣没有也绝对不会做出这种事情，如若发现全额退款主动销号。

_Note: The only limitation is that you cannot control the Machine/Puppet from China._

## Bypass：
- [x] Kaspersky EDR +NDR +KATA
<img width="1102" height="1077" alt="2c2" src="https://github.com/user-attachments/assets/dd6a0b34-3e81-42dd-8a1b-2b59cabcaf48" />


## 商业版可选功能模块（打勾必选）：
- [x] 基础功能（命令执行 命令限制绕过 文件管理 静默 自启动等）
- [x] 反沙箱 反调试 按需保障免杀效果
- [ ] 反向内网隧道
- [ ] 多人协作
- [ ] WebUI / GUI / TUI
- [ ] 白名单死点解析
- [ ] 高置信第三方接口流量（如Google/Dropbox/Github/OneDrive等）
- [ ] 智能研判提权
- [ ] 明文密码窃取
- [ ] 非系统文件 数据库 gitlab等 导出
- [ ] 进程或整个系统 内存导出
- [ ] 自动化痕迹清除
- [ ] 自动寻找可利用的凭据并可选内网自动化尝试利用（合法流量）
- [ ] 进程名伪装，杀软/EDR进程识别
- [ ] 内存加载驱动
- [ ] 用户态Rootkit
- [ ] 内核态Rootkit（内核模块实现，需向乙方提交内核版本信息，托管编译）
- [ ] 实时威胁情报分析
- [ ] 容器/云厂商识别及自动化尝试docker逃逸
- [ ] 流量隐藏/复用/修改，内网流量伪装
- [ ] 按需同步前沿或未公开的权限维持手法
- [ ] 自研Webshell管理器按需保障webshell免杀效果

关于服务器，高置信第三方接口账号/apikey，驱动托管编译，上线托管提醒，前端对接需求 之类的问题，都可协助/购买/搭建/部署等。

注：开源部分内容与商业版关系不大。

联系：r4be1@foxmail.com

---


---









# PuppetMaster（Linux C2）开源部分:
Linux反向shell/python-shell中控平台，主体0第三方依赖及轻量化异步，默认自带无限制持久化，防止任何服务端意外导致权限丢失。

声明：本项目开源部分仅用于交流分享及合法授权活动，一切用户行为与作者无关且不负任何责任。

**第一次使用注意修改Master主程序中的host变量，把127.0.0.1改为你的服务器公网ip,否则默认持久化命令会将权限持续反弹到127上。**

![图片](https://github.com/user-attachments/assets/5bebaee8-cf2e-4480-ad96-7b81690d9abf)

硬性Windows平台用户注意：Windows报错缺少readline库是因为Windows版的Python官方库中不包含readline,在Windows上pip install readline也会报错，如果一定要在Windows平台上跑的话可以把import readline改成第三方库或直接注释readline相关的行（就三行，但会缺少补全功能）

# Help:
### Master Console:
- BATCH-EXECUTE  ： 批量命令执行（目前只支持全部批量，部分批量有待考量）
- sessions ： 列出所有在线会话
- quiet    ： 安静模式（关闭重复上线的提示）
- use      ： 使用指定会话（tab键补全）可使用hash或远程连接的地址如(1.1.1.1:12345)

### Session:
- sessions ： 列出所有会话
- execute  ： 命令执行（execute ps -ef）
- shell    ： 交互式Shell
- close    ： 关闭当前会话（不会杀掉持久化进程）
- history  ： 输出完整的执行记录，包括执行的命令及回显
- bg       ： 会话/shell中可回退且不关闭会话

### Make Implant:
修改服务端IP：
![图片](https://github.com/user-attachments/assets/69d8a14d-652a-47f8-9c75-a68efad433f1)

cd SSL-shell && make linux 即可，而后会生成sslshell这个文件。

### DingDing Webhook:
将webhook url填入而后关键词设置为Puppet即可：
![图片](https://github.com/user-attachments/assets/7623cfbb-6d6d-4f34-bfa1-f78305e77650)


- 社区版
  - [x] 无加密通用TCP反弹Shell
  - [x] Openssl加密反弹Shell
  - [x] 多反弹Shell接收
  - [x] Session Hash（唯一权限避免重复）
  - [x] 基础deamon进程权限维持
  - [x] Linux反向Shell-release（SSLShell elf二进制文件但不包含免杀对抗，目前2024/7月社区版VT全过）
  - [x] 批量执行命令
  - [x] 钉钉/邮箱上线提示
  - [x] 安静模式（不在终端输出上线信息）
  - [x] 命令执行结果history（主要是批量命令执行回显记录）
