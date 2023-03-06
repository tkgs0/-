#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
环境要求: Python3.8 以上
安装依赖: pip install -U httpx tqdm
"""

import asyncio, httpx
from pathlib import Path


# 文件目录
dirPath: str = "./人教版2019/数学B/必修4"

# 页数
pages: int = 142

# 文件名
fileName: str = "{i}.jpg"

# 文件链接
url: str = "https://book.pep.com.cn/1421001137201/files/mobile/{i}.jpg"

# 请求参数
params: dict = {}

# 请求头
headers: dict = {
    "User-Agent": "Mozilla/5.0 (Linux; arm64; Android 12; SM-S9080) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 YaBrowser/23.0.0.00.00 SA/3 Mobile Safari/537.36",
}

# 饼干
cookies: dict = {}

# 超时期限 (秒)
timeout: int = 120


async def dload(sem, name: str, fileurl: str) -> None:
    filePath: Path = (
        Path(dirPath.strip()) / name.strip()
        if dirPath.strip()
        else Path(__file__) / name.strip()
    )
    filePath.parent.mkdir(parents=True, exist_ok=True)
    async with sem:
        async with httpx.AsyncClient().stream(
            'GET', url=fileurl.strip(),
            params=params, headers=headers, cookies=cookies,
            follow_redirects=True,
            timeout=timeout,
        ) as resp:
            with open(filePath, 'wb') as fd:
                async for chunk in resp.aiter_bytes(1024):
                    fd.write(chunk)
    print(f"{name}: Done.")


async def run() -> None:
    down: list = []
    sem = asyncio.Semaphore(5)
    for x in range(pages):
        down.append(dload(sem, fileName.format(i=x+1), url.format(i=x+1)))
    await asyncio.gather(*down)


if __name__ == '__main__':
    asyncio.run(run())
