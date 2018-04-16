// 自己编写的一些基本函数

// 输出函数
let log = function () {
    console.log.apply(console, arguments)
}

// 单选函数
let e = function (sel) {
    return document.querySelector(sel)
}

// 多选函数
let es = function (sel) {
    return document.querySelectorAll(sel)
}

// 对时间进行注释 并且 定时刷新时间
let createTimer = function () {
    setInterval(function () {
        let times = es('.time')
        for (let i = 0; i < times.length; i++) {
            let t = times[i]
            let time = Number(t.id) * 1000
            // let now = Math.floor(new Date() / 1000)
            // let delta = now - time
            //
            // day = Math.floor(delta / 86400)
            // hour = Math.floor((delta % 86400) / 3600)
            // minute = Math.floor((delta % 3600) / 60)
            //
            // let s = delta + ' 秒前'
            // let ss = day + ' 天前' + hour + ' 小时前' + minute + ' 分前'
            ss = moment(time).fromNow()
            t.innerHTML = t.dataset.type + ss
        }
    }, 1000)

}

// 对文本进行Markdown包装
let markContents = function () {
    let contentDivs = es('.markdown-text')
    for (let i = 0; i < contentDivs.length; i++) {
        let contentDiv = contentDivs[i]
        let content = marked(contentDiv.innerHTML)
        contentDiv.innerHTML = content
    }
}

//编辑器 初始化
let new_edit = function () {
    let editor = new Editor()
    editor.render($('.editor')[0])
}
