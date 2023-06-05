var formArchive = document.querySelectorAll('.form_archive')
var btnreset = document.querySelectorAll('.btnreset')
var btnremove = document.querySelectorAll('.btnremove')
console.log(formArchive)

for (let i = 0; i < formArchive.length; i++) {
    formArchive[i].onsubmit = (e) => {
        e.preventDefault()
        let formdata = new FormData(formArchive[i])
        fetch('http://127.0.0.1:5000/archive_remove', { method: 'POST', body: formdata })
            .then(res => console.log(res))
        btnreset[i].remove()
        btnremove[i].innerHTML += `<h5 class="text-danger m-2">Removed from Archive</h5>`
    }
}