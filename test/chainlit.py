import chainlit as cl 

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hello, world!").send()

@cl.on_message
async def on_message(input_message: str):
    print(f"입력된 메시지: {input_message}")
    new_message = cl.Message(content="input_message")
    print(new_message.content)
    await cl.Message(content="You said something!").send()