from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
import sys
import os
import json
import asyncio
from fastapi import Request, Form

# 修改导入路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from client.client import MCPClient
from server.Performance import execute_remote_command

# 服务器文件目录路径
SERVER_DIR = 'server'

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 初始化MCP客户端
mcp_client = MCPClient()

# 初始化模板
templates = Jinja2Templates(directory="web/templates")


# 调用server服务器
@app.on_event("startup")
async def startup_event():
    try:
        # 设置超时时间为10秒
        print("Performance.py 启动中......")
        await asyncio.wait_for(mcp_client.connect_to_server("server/Performance.py"), timeout=10.0)
        print("Performance.py 启动成功")
    except asyncio.TimeoutError:
        print("启动超时，请检查Performance.py是否正常运行")
    except Exception as e:
        print(f"启动失败: {str(e)}")


# # 调用server服务器
# @app.on_event("startup")
# async def startup_event():
#     try:
#         await mcp_client.connect_to_server("server/Performance.py")
#     except Exception as e:
#         print(f"启动性能监测服务失败: {str(e)}")

# 调用html模板
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 测试报告页面
@app.get("/report.html")
async def serve_report(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})


@app.post("/query")
async def process_query(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        return {"error": "缺少查询参数"}

    response = await mcp_client.process_query(query)
    return {"response": response}


@app.post("/execute-command")
async def execute_command(
        host: str = Form(...),
        username: str = Form(...),
        password: str = Form(...),
        command: str = Form(...)
):
    """
    在远程服务器上执行命令
    """
    try:
        result = await execute_remote_command(host, username, password, command)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# MCP服务器页面
@app.get("/mcp", response_class=HTMLResponse)
async def mcp_server(request: Request):
    return templates.TemplateResponse("mcp_server.html", {"request": request})


# 获取服务器文件列表的API端点
@app.get("/api/server-files")
async def get_server_files():
    try:
        print(f"尝试获取服务器文件列表，目录: {SERVER_DIR}")

        # 确保目录存在
        if not os.path.exists(SERVER_DIR):
            print(f"目录不存在，创建目录: {SERVER_DIR}")
            os.makedirs(SERVER_DIR)

        # 获取目录中的文件列表
        files = [f for f in os.listdir(SERVER_DIR) if os.path.isfile(os.path.join(SERVER_DIR, f))]
        print(f"找到文件: {files}")

        # 返回JSON格式的文件列表
        return {"files": files}
    except Exception as e:
        print(f"获取服务器文件列表时出错: {str(e)}")
        # 发生错误时返回错误信息
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    import uvicorn

    # 修改端口号为8084或其他未被占用的端口
    uvicorn.run(app, host="0.0.0.0", port=8084)