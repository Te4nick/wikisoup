const api_addr = "http://127.0.0.1/"
const api_article_url = api_addr + "article/url"
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
    if (response.headers.get("content-length") == 0) return response
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
    .then(data => {
        setArticlesPage()
        setArticleTitleInfobox(data.id)()
    })
    .catch(error => console.error('Error:', error));
}

function deleteArticle(articleId) {
    return function () {
        apiFetchJSON(null, api_article_url + "?id=" + articleId, 'Delete')
        setArticlesPage()
    }
}

function setArticleTitleInfobox(articleId) {
    return function () {
        apiFetchJSON(null, api_article_element(articleId), 'GET')
            .then(data => document.getElementById("articleTitleContainer").innerHTML = data.html)
            .catch(error => console.error('Error:', error));
        apiFetchJSON({"class_string": "infobox"}, api_article_element(articleId), 'POST')
            .then(data => document.getElementById("articleTitleContainer").innerHTML += data.html)
            .catch(error => console.error('Error:', error));
    }
}


// !!!
// !!! PAGE CHANGE SECTION !!!
// !!!
var currentPageNumber = 1
var totalArticles = 0
var pageSize = 0

function changePage(next) {
    const pageNumberInput = document.getElementById("pageNumber")
    pageNumber = Number(pageNumberInput.value)
    if (!Number.isInteger(pageNumber)) {
        return
    }
    if (!next) {
        if (pageNumber == 1) return
        currentPageNumber = pageNumber - 1
        pageNumberInput.value = currentPageNumber
        setArticlesPage()
        return
    } else {
        if (pageSize*pageNumber >= totalArticles) return
        currentPageNumber = pageNumber + 1
        pageNumberInput.value = currentPageNumber
        setArticlesPage()
        return
    }
}

function setHistoryFooter() {
    const historyFooter = document.getElementById("historyFooter")
    const articlesContainer = document.getElementById("articlesContainer")
    if (!articlesContainer) {
        historyFooter.innerHTML = '' +
        '<div id="articlesContainer"></div>' +
        '<label for="pageNumber">Page: </label>' +
        '<button for="pageNumber" onclick="changePage(false)" type="submit">&lt;</button>' +
        '<input id="pageNumber" name="pageNumber" type="text" value="1" disabled>' +
        '<button for="pageNumber" onclick="changePage(true)" type="submit">&gt;</button>'
        setArticlesPage()
    } else {
        historyFooter.innerHTML = ''
    }
}

function setArticlesPage() {
    const articlesContainer = document.getElementById("articlesContainer")
    if (!articlesContainer) return
    apiFetchJSON(null, api_article_url + "?page=" + currentPageNumber, "GET")
    .then(data => {
        articlesContainer.innerHTML = ''; // Clear previous page
        totalArticles = Number(data.total)
        pageSize = Number(data.page_size)
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
    })
    
}

// window.onload = setArticlesPage