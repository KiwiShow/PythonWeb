let log = function () {
    console.log.apply(console, arguments)
}

let e = function (sel) {
    return document.querySelector(sel)
}

// ajax函数
let ajax = function (method, path, data, responseCallback) {
    let r = new XMLHttpRequest()
    r.open(method, path, true)
    r.setRequestHeader('Content-Type', 'application/json')
    r.onreadystatechange = function () {
        if (r.readyState === 4) {
            responseCallback(r.response)
        }
    }
    data = JSON.stringify(data)
    r.send(data)
}


// Refused to execute script from
// 'http://localhost:3000/static?file=Ajax_base.js'
// because its MIME type ('image/gif') is not executable.
// todo的AjaxAPI
let ajaxTodoIndex = function (callback) {
    let path = '/ajax/todo/index'
    ajax('GET', path, '', callback)
}

let ajaxTodoAdd = function (form, callback) {
    let path = '/ajax/todo/add'
    ajax('POST', path, form, callback)
}

let ajaxTodoDelete = function (id, callback) {
    let path = '/ajax/todo/delete?id=' + id
    ajax('GET', path, '', callback)
}


