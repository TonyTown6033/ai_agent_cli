#!/usr/bin/env python3
import sys
import os  # 新增导入 os 模块
import click
from openai import OpenAI
from typing import List, Dict
import base64
from PIL import Image
import io

@click.group()
@click.option('--model', default='gpt-4o-mini', show_default=True,
              help='选择语言模型 (deepseek/gpt-4o-mini)')
@click.option('--temperature', type=float, default=0.7,
              help='生成结果的随机性 (0-2)')
@click.pass_context
def cli(ctx, model, temperature):
    """\b
    OpenAI多轮对话CLI工具
    支持持续对话上下文记忆
    支持管道输入
    """
    ctx.ensure_object(dict)

    # 从环境变量中加载 API 密钥
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        click.secho("错误: 未找到环境变量 'OPENAI_API_KEY'，请设置您的 API 密钥！", fg='red', err=True)
        raise click.Abort()

    ctx.obj.update({
        'client': OpenAI(
            base_url='https://api.openai-proxy.org/v1',
            api_key=api_key  # 使用环境变量中的密钥
        ),
        'model': model,
        'temperature': temperature,
        'history': []
    })

def _update_history(history: List[Dict], role: str, content: str) -> List[Dict]:
    """维护最近5轮对话上下文"""
    history.append({"role": role, "content": content})
    return history[-10:]  # 保留最近5轮对话（10条消息）

@cli.command()
@click.option('-q', '--question', default=None, help='直接输入问题并获取回答')
@click.pass_context
def chat(ctx, question):
    """启动交互式对话"""
    config = ctx.obj
    system_prompt = {"role": "system", "content": "你是有问必答的智能助手, 使用中文回答问题"}
    config['history'] = _update_history(config['history'], **system_prompt)

    # 检查是否通过管道输入
    if not question and not sys.stdin.isatty():
        question = sys.stdin.read().strip()

    if question:
        # 如果提供了问题或管道输入，直接处理
        config['history'] = _update_history(config['history'], "user", question)
        try:
            response = config['client'].chat.completions.create(
                messages=config['history'],
                model=config['model'],
                temperature=config['temperature']
            )
            ai_reply = response.choices[0].message.content
            click.secho(f"AI => {ai_reply}", fg='blue')
        except Exception as e:
            click.secho(f"错误: {str(e)}", fg='red', err=True)
        return

    click.secho("已进入对话模式（输入 q 退出）", fg='green')

    while True:
        try:
            user_input = click.prompt('You', type=str, prompt_suffix=' => ')
            if user_input.lower() in ('q', 'quit'):
                break

            # 更新对话历史
            config['history'] = _update_history(
                config['history'], "user", user_input)

            # 调用API
            response = config['client'].chat.completions.create(
                messages=config['history'],
                model=config['model'],
                temperature=config['temperature']
            )
            
            # 处理响应
            ai_reply = response.choices[0].message.content
            click.secho(f"AI => {ai_reply}", fg='blue')
            
            # 更新助手回复
            config['history'] = _update_history(
                config['history'], "assistant", ai_reply)

        except KeyboardInterrupt:
            click.secho("\n对话已终止", fg='red')
            break
        except Exception as e:
            click.secho(f"错误: {str(e)}", fg='red', err=True)
            raise click.Abort()

@cli.command()
@click.option('-i', '--image', type=click.Path(exists=True), help='输入图片路径并获取AI处理结果')
@click.pass_context
def process_image(ctx, image):
    """处理图片并获取AI的结果"""
    config = ctx.obj

    if not image:
        click.secho("请提供图片路径！", fg='red', err=True)
        return

    try:
        # 打开图片并转换为Base64
        with open(image, "rb") as img_file:
            img_data = img_file.read()
            encoded_image = base64.b64encode(img_data).decode('utf-8')

        # 构造请求消息，包含图片的 Base64 数据
        image_prompt = [
            {"type": "text", "text": "描述这张图片"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
        ]
        config['history'] = _update_history(config['history'], "user", image_prompt)

        # 调用API
        response = config['client'].chat.completions.create(
            messages=config['history'],
            model=config['model'],
            temperature=config['temperature']
        )

        # 处理响应
        ai_reply = response.choices[0].message.content
        click.secho(f"AI => {ai_reply}", fg='blue')

    except Exception as e:
        click.secho(f"处理图片时出错: {str(e)}", fg='red', err=True)

if __name__ == '__main__':
    cli(obj={})