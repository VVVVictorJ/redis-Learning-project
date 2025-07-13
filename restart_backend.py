#!/usr/bin/env python3
import subprocess
import sys
import os
import time


def restart_backend():
    print("正在重启后端服务...")

    # 停止现有的uvicorn进程
    try:
        subprocess.run(["pkill", "-f", "uvicorn"], check=False)
        print("已停止现有的uvicorn进程")
        time.sleep(2)
    except Exception as e:
        print(f"停止进程时出错: {e}")

    # 切换到backend目录
    backend_dir = os.path.join(os.getcwd(), "backend")

    # 启动新的uvicorn进程
    try:
        print("正在启动新的后端服务...")
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--reload",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ]

        # 在后台启动
        process = subprocess.Popen(
            cmd, cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        print(f"后端服务已启动，PID: {process.pid}")
        print("服务地址: http://localhost:8000")
        print("API文档: http://localhost:8000/docs")

        # 等待几秒钟确保服务启动
        time.sleep(3)

        # 检查进程是否还在运行
        if process.poll() is None:
            print("✅ 后端服务启动成功！")
        else:
            print("❌ 后端服务启动失败")
            stdout, stderr = process.communicate()
            print(f"stdout: {stdout.decode()}")
            print(f"stderr: {stderr.decode()}")

    except Exception as e:
        print(f"启动服务时出错: {e}")


if __name__ == "__main__":
    restart_backend()
