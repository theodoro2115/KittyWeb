// Elementos do Login
const login = document.querySelector(".login")
const loginForm = document.querySelector(".login_form")
const loginInput = document.querySelector(".login_form")
 
 
// Elementos do Chat
const chat = document.querySelector(".chat")
const chatForm = document.querySelector(".chat_form")
const chatInput = document.querySelector(".chat_form")
 
const colores = [
    "cadetblue",
    "darkgoldenrod",
    "cornflowerblue",
    "darkkhaki",
    "hotpink",
    "darkolivegreen"
]
 
const user = {id: "", name: "", color: "" }/// padrão para receber as informações
 
let websocket
 
const createMessageSelfElement = (content) => {
    const div = document.createElement("div")
}
 
const getRandomColor = () => {/// para gerar cores aleatórias
    const randomIndex = Math.floor(Math.random() * colors.length)
    return colors[randomIndex]
}
const processMensagem = ({data}) => {/// processar as mensagens
    const {userId, userName, userColor, content} = JSON.parse(data)/// para transformar as informações
}
const handleLogin = (event) => {
}
 
const sendMensagem = (event) => {
    event.preventDefault()
 
    const mensagem = { /// informações que seram do usuário
        userId: user.id,
        userName: user.name,
        userColor: user.color,
        content: chatInput.value
    }
 
    websocket.send(JSON.stringify(mensagem))/// para enviar a informaçõa
 
    chatInput.value = "" /// para apagar a imagem após ser enviada
}
 
loginForm.addEventListener("submit", handleSubmit) /// evento para o login
chatForm.addEventListener("submit", handleSubmit) /// evento para o chat