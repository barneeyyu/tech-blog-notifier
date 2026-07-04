from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    BroadcastRequest,
    TextMessage,
)

def format_message(
    name: str,
    emoji: str,
    zh_title: str,
    original_title: str,
    zh_summary: str,
    url: str,
) -> str:
    lines = [
        f"{emoji} {name}",
        "",
        f"📌 {zh_title}",
        f"Original: {original_title}",
        "",
    ]
    if zh_summary:
        lines += [f"📝 {zh_summary}", ""]
    lines.append(f"🔗 {url}")
    return "\n".join(lines)

def broadcast_article(
    token: str,
    name: str,
    emoji: str,
    zh_title: str,
    original_title: str,
    zh_summary: str,
    url: str,
) -> None:
    text = format_message(
        name=name,
        emoji=emoji,
        zh_title=zh_title,
        original_title=original_title,
        zh_summary=zh_summary,
        url=url,
    )
    configuration = Configuration(access_token=token)
    with ApiClient(configuration) as api_client:
        api = MessagingApi(api_client)
        api.broadcast(BroadcastRequest(messages=[TextMessage(type="text", text=text)]))
