import httpx
import json

# 正在运行的 FastAPI 应用的 URL
url = "http://127.0.0.1:8001/analyse"

# 要发送到 API 的查询
payload = {
    "query": "中国老龄化社会的未来"
    # "query": "以色列什么时候停战"
   # "query": "特朗普上台，发布货币紧缩政策"
}

print("正在向服务器发送请求...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    # 发送 POST 请求 (设置一个较长的超时时间，因为 LLM 可能响应较慢)
    with httpx.Client(timeout=300.0) as client:
        response = client.post(url, json=payload)

        # 检查请求是否成功
        response.raise_for_status()

        # 打印服务器的响应
        print("\n--- 服务器响应 ---")
        try:
            # 尝试以 JSON 格式美化打印
            response_data = response.json()
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            # 如果不是 JSON，则作为文本打印
            print(response.text)

except httpx.HTTPStatusError as e:
    print(f"\n--- 错误 ---")
    print(f"发生 HTTP 错误: {e}")
    print(f"响应内容: {e.response.text}")
except httpx.RequestError as e:
    print(f"\n--- 错误 ---")
    print(f"请求 {e.request.url!r} 时发生错误。")
    print("请确保 FastAPI 服务器正在 http://127.0.0.1:8000 上运行。")