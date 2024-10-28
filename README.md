# PuppetMaster（Linux C2）:
Linux反向shell中控平台，主体0第三方依赖及轻量化异步，默认自带无限制持久化，防止任何服务端意外导致权限丢失。

声明：本项目仅用于交流分享及合法授权活动，一切用户行为与作者无关且不负任何责任。

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

### Tips：
可以在执行命令前加上sleep 123;使执行结果在123秒后再回传给C2,但实际上tcp连接还是保持的。

# Todo:
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
- 商业版
  - [x] 社区版所有功能及部分优化
  - [ ] 用户态/内核态Rootkit
  - [ ] Linux植入物反沙箱动静态免杀对抗
  - [x] 多用户支持（多人协作）
  - [ ] HTTPS/ICMP/SSH加密内网隧道
  - [x] 多用户Web控制端
  - [ ] 白名单死点解析
  - [ ] 类beacons效果
  - [x] 自定义Webshell兼容PHP/JSP/ASP/ASPX/CMDSHELL/....
