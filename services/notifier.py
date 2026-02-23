# -*- coding: utf-8 -*-
"""
通用通知服务模块

基于 notify.py 提供统一的消息推送功能，支持钉钉、飞书、Bark、Telegram、
企业微信、邮件等多种推送渠道。具体渠道通过 notify.py 中的 push_config 或
环境变量进行配置。
"""

import asyncio
import logging
from datetime import datetime

import notify


class Notifier:
    """
    通用通知客户端

    封装 notify.py 的 send() 函数，提供与业务逻辑解耦的通知接口。
    """

    # 通知级别常量
    LEVEL_INFO = "INFO"
    LEVEL_WARNING = "WARNING"
    LEVEL_ERROR = "ERROR"

    # 级别对应的emoji
    LEVEL_EMOJI = {
        "INFO": "✅",
        "WARNING": "⚠️",
        "ERROR": "❌",
    }

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info("通用通知服务已初始化")

    async def _send(self, title: str, content: str) -> bool:
        """
        异步发送通知（内部方法）

        Args:
            title: 通知标题
            content: 通知内容

        Returns:
            bool: 发送成功返回True
        """
        try:
            await asyncio.to_thread(notify.send, title, content)
            return True
        except Exception as e:
            self.logger.error(f"发送通知异常: {e}")
            return False

    async def send_card_message(
        self, influencer: str, platform: str, markdown_content: str
    ) -> bool:
        """
        发送动态通知

        Args:
            influencer: 博主名称
            platform: 平台名称
            markdown_content: Markdown格式的内容

        Returns:
            bool: 发送成功返回True
        """
        title = f"【{platform}】{influencer}"
        success = await self._send(title, markdown_content)
        if success:
            self.logger.info(f"通知发送成功: {influencer} - {platform}")
        else:
            self.logger.error(f"通知发送失败: {influencer} - {platform}")
        return success

    async def send_system_notification(
        self, level: str, title: str, content: str
    ) -> bool:
        """
        发送系统状态通知

        Args:
            level: 通知级别 (INFO/WARNING/ERROR)
            title: 通知标题
            content: 通知内容

        Returns:
            bool: 发送成功返回True
        """
        emoji = self.LEVEL_EMOJI.get(level, "📢")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        formatted_title = f"{emoji} {level} - {title}"
        formatted_content = f"{content}\n\n---\n时间: {timestamp}"

        return await self._send(formatted_title, formatted_content)