const {WebSocketServer} = require('ws')
const dotenv = require('dotenv')

dotenv.config()
 
const wss = new WebSocketServer({port: process.env.PORT || 8080})
 
wss.on('connection', (ws) => {
    ws.on('erro', console.error)
 
    ws.on('message', (data) => {
        wss.clients.forEach((client) => client.send(data.toString()))/// linha para enviar menseagem no servidor para todos
    })
   
    console.log('Pessoa conectada')
})