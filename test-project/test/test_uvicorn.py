

async def app_ws(scope, receive, send):
    assert scope['type'] == 'websocket'
    await receive()
    await send({
        'type': 'websocket.accept',
        'subprotocol': None,
    })
    while True:
        body = await receive()
        print(body)
        await send({
            'type': 'websocket.send',
            'bytes': body['text']
        })
        if body['text'] == 'exit':
            break


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    print(scope)
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world',
        'more_body': True,
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world',
        'more_body': False,
    })


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app_ws)
