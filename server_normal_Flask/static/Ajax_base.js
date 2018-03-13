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
    let path = '/ajax/todo/delete/' + id
    ajax('GET', path, '', callback)
}

let ajaxTodoUpdate = function (form, callback) {
    let path = '/ajax/todo/update'
    ajax('POST', path, form, callback)
}

let ajaxTodoSwitch = function (id, status, callback) {
    let path = '/ajax/todo/status_switch/' + id + '?status=' + status
    ajax('GET', path, '', callback)
}


// tweet的AjaxAPI
let ajaxTweetIndex = function (callback) {
    let path = '/ajax/tweet/index'
    ajax('GET', path, '', callback)
}

let ajaxTweetAdd = function (form, callback) {
    let path = '/ajax/tweet/add'
    ajax('POST', path, form, callback)
}

let ajaxTweetDelete = function (id, callback) {
    let path = '/ajax/tweet/delete?id=' + id
    ajax('GET', path, '', callback)
}

let ajaxTweetUpdate = function (form, callback) {
    let path = '/ajax/tweet/update'
    ajax('POST', path, form, callback)
}

let ajaxCommentIndex = function (tweet_id, callback) {
    let path = '/ajax/comment/index?tweet_id=' + tweet_id
    ajax('GET', path, '', callback)
}

let ajaxCommentAdd = function (form, callback) {
    let path = '/ajax/comment/add'
    ajax('POST', path, form, callback)
}

let ajaxCommentDelete = function (id, callback) {
    let path = '/ajax/comment/delete?id=' + id
    ajax('GET', path, '', callback)
}

let ajaxCommentUpdate = function (form, callback) {
    let path = '/ajax/comment/update'
    ajax('POST', path, form, callback)
}


