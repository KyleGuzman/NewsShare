var date = new Date(Date.now());
var month = new Date(date.setMonth(date.getMonth() - 1))
var lastMonth = month.getFullYear() + "-" + (month.getMonth() + 1) + "-" + month.getDate()
var mainPic = document.querySelector('#mainpic')
var newsFeed = document.querySelector('#newsfeed')






function search() {
    var search = document.querySelector('#search').value
    // console.log(search)
    newsFeed.innerHTML = ""
    fetch("https://newsapi.org/v2/everything?q=" + search + "&from=" + lastMonth + "&sortBy=publishedAt&apiKey=aed9f20fe4f54ce4ba78e1c546e31c61")
        // fetch("https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=aed9f20fe4f54ce4ba78e1c546e31c61")
        .then((res) => { return (res.json()) })
        .then((data) => {
            mainPic.remove()
            for (let article of data.articles) {
                var publishDate = new Date(article.publishedAt)
                var displayDate = (publishDate.getMonth() + 1) + "/" + publishDate.getDate() + "/" + publishDate.getFullYear()
                var formDate = publishDate.getFullYear() + "-" + (publishDate.getMonth() + 1) + "-" + publishDate.getDate()
                // console.log(article.title)
                newsFeed.innerHTML += `<form id='mainpic' class="mb-5 test">
                                            <div class="card">
                                                <img src="${article.urlToImage}" class="card-img-top" alt="${article.title}">
                                                <div class="card-body">
                                                    <h5 class="card-title">${article.title}</h5>
                                                    <h6 class="card-subtitle mb-2 text-muted">Source: ${article.source.name}</h6>
                                                    <h6 class="card-subtitle mb-2 text-muted">${article.description}</h6>
                                                    <h6 class="card-subtitle mb-2 text-muted"><a href="${article.url}">Link to original article</a></h6>
                                                    <h6 class="card-subtitle mb-2 text-muted"> Published on: ${displayDate}</h6>
                                                </div>
                                            </div>
                                            <input type="hidden" name="title" value="${article.title}">
                                            <input type="hidden" name="source" value="${article.source.name}">
                                            <input type="hidden" name="description" value="${article.description}">
                                            <input type="hidden" name="content" value="${article.content}">
                                            <input type="hidden" name="url" value="${article.url}">
                                            <input type="hidden" name="image" value="${article.urlToImage}">
                                            <input type="hidden" name="published_date" value="${formDate}">
                                            <div class="form-group m-3 btnsaved">
                                                <button type="submit" class="btn btn-primary btntest">Save and read later</button>
                                            </div>
                                        </form>`
            }
            var articleForm = document.querySelectorAll('.test')
            var btnreset = document.querySelectorAll('.btntest')
            var btnsave = document.querySelectorAll('.btnsaved')
            for (let i = 0; i < articleForm.length; i++) {
                articleForm[i].onsubmit = (e) => {
                    e.preventDefault()
                    let formdata = new FormData(articleForm[i])
                    fetch('http://127.0.0.1:5000/save_news', { method: 'POST', body: formdata })
                        .then(res => console.log(res))
                    btnreset[i].remove()
                    btnsave[i].innerHTML += `<h5 class="text-danger">Saved!</h5>`
                }
            }
        })
}