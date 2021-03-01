let homeColor = null
let visitorColor = null

const homeTeam = document.getElementById('event-home-team')
const visitorTeam = document.getElementById('event-visiting-team')

function homeColorSelector(button, color){
    Array.from(document.getElementsByClassName('home')).forEach(btn => {
        btn.classList.remove('selected')
    })

    button.classList.add('selected')

    homeColor = color

    return false
}

function visitorColorSelector(button, color){
    Array.from(document.getElementsByClassName('visitor')).forEach(btn => {
        btn.classList.remove('selected')
    })

    button.classList.add('selected')

    visitorColor = color

    return false
}

function validateSetup() {
    let valid = true

    homeTeam.labels[0].classList.remove('red')
    if (homeColor == null) {
        valid = false
        homeTeam.labels[0].classList.add('red')
    }

    if (homeTeam.value.length == 0) {
        valid = false
        homeTeam.labels[0].classList.add('red')
    }

    visitorTeam.labels[0].classList.remove('red')
    if (visitorColor == null) {
        valid = false
        visitorTeam.labels[0].classList.add('red')
    }

    if (visitorTeam.value.length == 0) {
        valid = false
        visitorTeam.labels[0].classList.add('red')
    }

    return valid
}

function setup(e) {
    e.preventDefault()
    if (validateSetup()) {
        payload = new FormData()

        payload.append('home_team', homeTeam.value)
        payload.append('visitor_team', visitorTeam.value)

        payload.append('home_color', homeColor)
        payload.append('visitor_color', visitorColor)

        fetch('/init', {
            method: 'POST',
            cache: 'no-cache',
            body: payload
        }).then(res => {
            console.log(res)
        })
    }
}

document.getElementById('event-form').onsubmit = setup