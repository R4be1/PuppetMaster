# PuppetMaster:
Linux反向shell中控平台，主体0第三方依赖及轻量化异步
![20240719](https://github.com/user-attachments/assets/7420c565-2a48-4e4c-943b-b87729db554f)

# Help:
### Master Console:
- BATCH-EXECUTE  ： 批量命令执行（目前只支持全部批量，部分批量有待考量）
- sessions ： 列出所有会话
- use      ： 使用指定会话（tab键补全）可使用远程连接的地址如(1.1.1.1:12345)

### Session:
- sessions ： 列出所有会话
- execute  ： 命令执行（execute ps -ef）
- shell    ： 交互式Shell
- bg       ： 会话/shell中可回退且不关闭会话

# Todo:
- 社区版
  - [x] 无加密通用TCP反弹Shell
  - [x] Openssl加密反弹Shell
  - [x] 多反弹Shell接收
  - [x] Session Hash（唯一权限避免重复）
  - [x] 基础deamon进程权限维持
  - [x] Linux反向Shell-release（SSLShell elf二进制文件但不包含免杀对抗）
  - [x] 批量执行命令
- 商业版
  - [x] 社区版所有功能及部分优化
  - [ ] 用户态/内核态Rootkit
  - [ ] Linux植入物免杀
  - [ ] 多用户支持（多人协作）
  
