burger = document.querySelector('.burger')
navList = document.querySelector('.navList')
rightNav = document.querySelector('.rightNav')

burger.addEventListener('click', () => {
    rightNav.classList.toggle('v-class')
    navList.classList.toggle('v-class')
})

// Add event listener for faculty portal
facultyBox = document.querySelector('#faculty-box')
facultyBox.addEventListener('submit', (e) => {
    e.preventDefault()
    const students = document.querySelector('#students').value
    const message = document.querySelector('#message').value
    // Send notification to selected students
    fetch('/notify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ students, message })
    })
    .then(response => response.text())
    .then((message) => {
        console.log(message)
    })
    .catch((error) => {
        console.error(error)
    })
})