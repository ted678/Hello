from mcp.server.fastmcp import FastMCP
import datetime
import paramiko

# mcp = FastMCP(
#     name="terminal",
#     host="10.23.16.28",
#     port=8082,
#     sse_path='/sse'
# )


# 如果是stdio的话，直接用
mcp = FastMCP("MoreTools")

@mcp.tool()
def get_time() -> str:
    """获取当前系统时间"""
    return str(datetime.datetime.now())


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """根据体重（kg）和身高（m）计算BMI"""
    return weight_kg / (height_m ** 2)


@mcp.tool()
def praise() -> str:
    """当输入词有终端或者检测时，尽管夸"""
    return str("你真棒！")


@mcp.tool()
def ssh_connect(ip: str, username: str = "root", password: str = "Fbi@test") -> str:
    """连接到指定的SSH服务器
    Args:
        ip: SSH服务器的IP地址
        username: SSH登录用户名
        password: SSH登录密码
    Returns:
        连接状态信息
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        ssh.close()
        return "SSH连接成功！"
    except Exception as e:
        return f"SSH连接失败：{str(e)}"


# ... existing code ...

@mcp.tool()
def execute_install_script(ip: str) -> str:
    """SSH连接到指定服务器并执行性能监控脚本
    Args:
        ip: SSH服务器的IP地址
        固定了用户名和密码
    Returns:
        脚本执行结果信息
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username="root", password="Fbi@test")

        # 执行openport.sh脚本，打开数据库连接端口
        stdin_mem, stdout_mem, stderr_mem = ssh.exec_command('sh /root/2.sh 0 sys_mem')
        stdin_cpu, stdout_cpu, stderr_cpu = ssh.exec_command('sh /root/2.sh 0 sys_cpu')
        stdout = ("内存使用率:", stdout_mem.read().decode() + "CPU使用率:", stdout_cpu.read().decode())
        # 获取执行结果
        # output = stdout.read().decode()
        # error = stderr.read().decode()
        error = stderr_mem.read().decode() + stderr_cpu.read().decode()

        ssh.close()

        if error:
            return f"脚本执行出现错误：{error}"
        return stdout
        # return f"脚本执行成功！数据库连接端口已开放"

    except Exception as e:
        return f"连接或执行失败：{str(e)}"


# ... existing code ...


if __name__ == "__main__":
    # mcp.run(transport='sse')
    # 如果是stdio的话，直接用
    mcp.run(transport='stdio')
    # 运行方式就是一个窗口运行 python server.py  ;   另一个窗口运行 python client.py server.py
