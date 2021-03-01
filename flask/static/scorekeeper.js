window.gameState = null

const status = document.getElementById('status')

const visitor = document.getElementById('visitor')
const home = document.getElementById('home')

const visitorScore = document.getElementById('visitor-score')
const visitorMinus = document.getElementById('visitor-minus')
const visitorPlus = document.getElementById('visitor-plus')

const homeScore = document.getElementById('home-score')
const homeMinus = document.getElementById('home-minus')
const homePlus = document.getElementById('home-plus')

const inning = document.getElementById('inning')
const inningMinus = document.getElementById('inning-minus')
const inningPlus = document.getElementById('inning-plus')

const inningTop = document.getElementById('inning-top')
const inningMid = document.getElementById('inning-mid')
const inningBot = document.getElementById('inning-bot')
const inningEnd = document.getElementById('inning-end')

const base1 = document.getElementById('base-1')
const base2 = document.getElementById('base-2')
const base3 = document.getElementById('base-3')
const baseReset = document.getElementById('base-reset')

const outs = document.getElementById('outs')
const outReset = document.getElementById('out-reset')
const outBtn = document.getElementById('out-btn')

const balls = document.getElementById('balls')
const ballBtn = document.getElementById('ball-btn')
const strikes = document.getElementById('strikes')
const strikeBtn = document.getElementById('strike-btn')
const countReset = document.getElementById('count-reset')

function updateTeams() {
    visitor.innerText = window.gameState.visitor_team
    visitorScore.innerText = window.gameState.visitor_score

    visitorMinus.disabled = true
    visitorPlus.disabled = true

    home.innerText = window.gameState.home_team
    homeScore.innerText = window.gameState.home_score

    homeMinus.disabled = true
    homePlus.disabled = true
}

function updateInnings() {
    inning.innerText = window.gameState.inning

    if (window.gameState.inning <= 1) {
        inningMinus.disabled = true
    }
    else {
        inningMinus.disabled = false
    }

    Array.from(document.getElementsByClassName('inning-btn')).forEach(btn => {
        btn.classList.remove('checked')
    })

    switch (window.gameState.inning_mode) {
        case 'top':
            inningTop.classList.add('checked')
            visitorPlus.disabled = false
            if (window.gameState.visitor_score > 0) {
                visitorMinus.disabled = false
            }
            setAtBats(false)
            break
        case 'mid':
            inningMid.classList.add('checked')
            setAtBats(true)
            break
        case 'bot':
            inningBot.classList.add('checked')
            homePlus.disabled = false
            if (window.gameState.home_score > 0) {
                homeMinus.disabled = false
            }
            setAtBats(false)
            break
        case 'end':
            inningEnd.classList.add('checked')
            setAtBats(true)
            break
        default:
            console.log('Unknown Inning Mode')
    }

}

function updateBases() {
    if (window.gameState.base_1) {
        base1.classList.add('on')
    }
    else {
        base1.classList.remove('on')
    }

    if (window.gameState.base_2) {
        base2.classList.add('on')
    }
    else {
        base2.classList.remove('on')
    }

    if (window.gameState.base_3) {
        base3.classList.add('on')
    }
    else {
        base3.classList.remove('on')
    }
}

function updateAtBat() {
    outs.innerText = window.gameState.outs
    balls.innerText = window.gameState.balls
    strikes.innerText = window.gameState.strikes
}

function updateGameState() {
    updateTeams()
    updateInnings()
    updateBases()
    updateAtBat()
}

function setAtBats(state) {
    base1.disabled = state
    base2.disabled = state
    base3.disabled = state

    baseReset.disabled = state

    outBtn.disabled = state
    outReset.disabled = state
    ballBtn.disabled = state
    strikeBtn.disabled = state
    countReset.disabled = state
}

const socket = io()

socket.on('connect', () => {
    socket.emit('event-request', 'update')
})

socket.on('disconnect', () => {
    status.innerText = 'DISCONNECTED'
    status.classList.add('error')
})

socket.on('event-reset', payload => {
    console.log(payload)
    status.innerText = 'CONNECTED'
    status.classList.remove('error')

    window.gameState = payload
    updateGameState()
})

function adjustScore(team, operation) {
    let payload = null
    if (team == 'home') {
        if (operation == 'add') {
            payload = {
                team: 'home',
                score: window.gameState.home_score + 1
            }
        }
        else {
            payload = {
                team: 'home',
                score: window.gameState.home_score - 1
            }
        }
    }
    else {
        if (operation == 'add') {
            payload = {
                team: 'visitor',
                score: window.gameState.visitor_score + 1
            }
        }
        else {
            payload = {
                team: 'visitor',
                score: window.gameState.visitor_score - 1
            }
        }
    }

    socket.emit('score-update', payload)
}

visitorMinus.onclick = () => {adjustScore('visitor', 'minus')}
visitorPlus.onclick = () => {adjustScore('visitor', 'add')}

homeMinus.onclick = () => {adjustScore('home', 'minus')}
homePlus.onclick = () => {adjustScore('home', 'add')}

function changeInningMode(mode) {
    socket.emit('inning-mode-update', mode)
}

inningTop.onclick = () => {changeInningMode('top')}
inningMid.onclick = () => {changeInningMode('mid')}
inningBot.onclick = () => {changeInningMode('bot')}
inningEnd.onclick = () => {changeInningMode('end')}

function adjustInning(operation) {
    if (operation == 'add') {
        socket.emit('inning-update', window.gameState.inning + 1)
    }
    else {
        socket.emit('inning-update', window.gameState.inning - 1)
    }
}

inningMinus.onclick = () => {adjustInning('minus')}
inningPlus.onclick = () => {adjustInning('add')}

function changeBase(base) {
    let payload = null
    switch (base) {
        case 1:
            payload = {
                base: 1,
                state: !(window.gameState.base_1)
            }
            break
        case 2:
            payload = {
                base: 2,
                state: !(window.gameState.base_2)
            }
            break
        case 3:
            payload = {
                base: 3,
                state: !(window.gameState.base_3)
            }
            break
        default:
            console.log('Unknown Base')
    }

    socket.emit('base-update', payload)
}

base1.onclick = () => {changeBase(1)}
base2.onclick = () => {changeBase(2)}
base3.onclick = () => {changeBase(3)}

baseReset.onclick = () => {socket.emit('base-reset', 'reset')}

outBtn.onclick = () => {socket.emit('out-update', window.gameState.outs + 1)}
outReset.onclick = () => {socket.emit('out-reset', 'reset')}

strikeBtn.onclick = () => {socket.emit('strike-update', window.gameState.strikes + 1)}
ballBtn.onclick = () => {socket.emit('ball-update', window.gameState.balls + 1)}
countReset.onclick = () => {socket.emit('count-reset', 'reset')}