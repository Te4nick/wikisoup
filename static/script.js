const api_addr = "http://127.0.0.1:8000/"
const api_article_url = api_addr + "article/url"

const matrixSizeContainer = document.getElementById('matrixSizeContainer')
const matrixContainer = document.getElementById('matrixContainer')
const operandContainer = document.getElementById('operandContainer')

const reURL = new RegExp("^https://..\.wikipedia.org/wiki/.+")

async function apiFetchJSON(data, path, method) {
    let req = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    }
    if (data != null) req.body = JSON.stringify(data);

    const response = await fetch(path, req);
    return await response.json();
}

function api_article_element(id) {
    return api_addr + "article/" + id + "/element"
}

function inputClamp(elementId, min, max) {
    const val = Number(document.getElementById(elementId).value);
    if (val < min || val > max) {
        document.getElementById(elementId).value = min
        alert("Size must be between 2 and 10.");
        return null;
    }
    return val
}


function submitURL() {
    
    const url = document.getElementById('wikipediaArticle').value
    if (!url.match(reURL)) {
        alert("URL must be the WIKIPEDIA ARTICLE.\nExample: https://en.wikipedia.org/wiki/Python_(programming_language)")
        return
    }

    apiFetchJSON({"url": url}, api_article_url, 'POST')
    .then(data => setArticleTitleInfobox(data.id))
    .catch(error => console.error('Error:', error));
}

function deleteArticle(articleId) {
    return function () {
        apiFetchJSON(null, api_article_url + "?id=" + articleId, 'Delete')
            .then(setArticlesPage())
            .catch(setArticlesPage());
    }
}

function setArticleTitleInfobox(articleId) {
    return function () {
        apiFetchJSON(null, api_article_element(articleId), 'GET')
            .then(data => document.getElementById("articleTitleContainer").innerHTML = data.html)
            .catch(error => console.error('Error:', error));
        apiFetchJSON({"class_string": "infobox vevent"}, api_article_element(articleId), 'POST')
            .then(data => document.getElementById("articleTitleContainer").innerHTML += data.html)
            .catch(error => console.error('Error:', error));
    }
}


// !!!
// !!! PAGE CHANGE SECTION !!!
// !!!
var currentPageNumber = 1
var totalArticles = 0
const articlesContainer = document.getElementById('articlesContainer')
const pageNumberInput = document.getElementById("pageNumber")

function changePage(next) {
    const pageNumberInput = document.getElementById("pageNumber")
    pageNumber = Number(pageNumberInput.value)
    if (!Number.isInteger(pageNumber)) {
        return
    }
    if (!next) {
        if (pageNumber == 1) return
        pageNumberInput.value = pageNumber - 1
        setArticlesPage()
        return
    } else {
        if (10*pageNumber >= totalArticles) return
        pageNumberInput.value = pageNumber + 1
        setArticlesPage()
        return
    }
}

function setArticlesPage() {
    let newPageNumber = Number(document.getElementById("pageNumber").value)
    apiFetchJSON(null, api_article_url + "?page=" + newPageNumber, "GET")
    .then(data => {
        articlesContainer.innerHTML = ''; // Clear previous page
        totalArticles = Number(data.total)
        const table = document.createElement('table');
        const tbody = document.createElement('tbody');
    
        for (article of data.articles) {
            const tr = document.createElement('tr');
            
            const tdUrl = document.createElement('td');
            tdUrl.textContent = article.url.toString()
            tdUrl.onclick = setArticleTitleInfobox(article.id.toString())
            tr.appendChild(tdUrl);

            const tdDel = document.createElement('td');
            const buttonDel = document.createElement('button')
            buttonDel.textContent = "Delete"
            buttonDel.onclick = deleteArticle(article.id.toString())
            tdDel.appendChild(buttonDel)
            tr.appendChild(tdDel);

            tbody.appendChild(tr);
        }
    
        table.appendChild(tbody);
        articlesContainer.appendChild(table);
        currentPageNumber = newPageNumber
    })
    
}

window.onload = setArticlesPage