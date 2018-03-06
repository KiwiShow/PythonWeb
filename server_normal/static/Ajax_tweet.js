// <button class="tweet-delete" data-href="/tweet/delete?id={{ t.id }}">delete</button>
// <button class="tweet-edit" data-href="/tweet/edit?id={{ t.id }}">edit</button>

let tweetUpdateFormTemplate = function () {
    let tem = `
        <div class="tweet-update-form">
            <input class="tweet-update-input">
            <button class="tweet-update">更新</button>
    `
    return tem
}

//id title created_time updated_time
let tweetTemplate = function (tweet) {
    let id = tweet.id
    let content = tweet.content
    let user_id = tweet.user_id
    let tem = `
        <div class="tweet-cell" data-id="${id}">
            <span>通过ajax获得</span>
            <span class="tweet-content">${content}</span>
            <span class="tweet-user_id">from---${user_id}</span>
            <button class="tweet-delete" data-id="${id}">删除</button>
            <button class="tweet-edit" data-id="${id}">编辑</button>
        </div> 
        <h6>评论</h6>
        <div class="comment-list">
        </div>   
    `
    return tem
}

let commentTemplate = function (comment) {
    let id = comment.id
    let content = comment.content
    let user_id = comment.user_id
    let tweet_id = comment.tweet_id
    let tem = `
        <div class="comment-cell" data-id="${id}">
            <span>通过ajax获得</span>
            <span class="comment-user_id">${user_id}</span>
            <span class="comment-content">${content}</span>
            <button class="comment-delete" data-id="${id}">删除</button>
            <button class="comment-edit" data-id="${id}">编辑</button>
        </div>    
    `
    return tem
}

let insertTweet = function (tweet) {
    let tweetCell = tweetTemplate(tweet)
    let tweetList = e('.tweet-list')
    tweetList.insertAdjacentHTML('beforeend', tweetCell)
}

let insertComment = function (comments) {
    let commentCell = commentTemplate(comments)
    let commentList = e('.comment-list')
    commentList.insertAdjacentHTML('beforeend', commentCell)
}

let allTweets = function () {
    ajaxTweetIndex(function (r) {
        let tweets = JSON.parse(r)
        for (let i = 0; i < tweets.length; i++) {
            let tweet = tweets[i]
            insertTweet(tweet)
            // 输入每个Tweet的comment
            ajaxCommentIndex(tweet.id, function (r) {
                let comments = JSON.parse(r)
                for (let i = 0; i < comments.length; i++) {
                    let comment = comments[i]
                    insertComment(comment)
                }
            })
        }
    })

}


let bindEventTweetAdd = function () {
    let b = e('#id-button-add')
    b.addEventListener('click', function () {
        let input = e('#id-input-tweet')
        let content = input.value
        let form = {
            content: content,
        }
        ajaxTweetAdd(form, function (r) {
            let tweet = JSON.parse(r)
            insertTweet(tweet)
        })

    })

}

// 事件委托
let bindEventTweetDelete = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('tweet-delete')) {// 这里没有点符号
            let tweetId = self.dataset.id
            ajaxTweetDelete(tweetId, function (r) {
                self.parentElement.remove()
            })
        }

    })

}

let bindEventTweetEdit = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('tweet-edit')) {
            let t = tweetUpdateFormTemplate()
            // 有个bug是每次点击都会出现input
            // 更好的做法是用CSS实现一个input框
            self.parentElement.insertAdjacentHTML('beforeend', t)
            // self.parentElement.innerHTML += t
        }
    })
}

let bindEventTweetUpdate = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('tweet-update')) {
            let tweetCell = self.closest('.tweet-cell')
            let input = tweetCell.querySelector('.tweet-update-input')
            let id = tweetCell.dataset.id
            let form = {
                id: id,
                content: input.value,
            }
            ajaxTweetUpdate(form, function(r){
                let updateForm = self.closest('.tweet-update-form')
                updateForm.remove()
                let tweet = JSON.parse(r)
                let  content = tweetCell.querySelector('.tweet-content')
                content.innerHTML = tweet.content
                // title.value = tweet.title
            })
        }
    })
}

let bindEventTweetComTrue = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('tweet-finished')) {
            let tweetCell = self.closest('.tweet-cell')
            let id = tweetCell.dataset.id
            ajaxTweetSwitch(id, 'True', function(r){
                let status = tweetCell.querySelector('.tweet-status')
                status.innerHTML = 'True'

            })
        }
    })
}

let bindEventTweetComFalse = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('tweet-unfinished')) {
            let tweetCell = self.closest('.tweet-cell')
            let id = tweetCell.dataset.id
            ajaxTweetSwitch(id, 'False', function(r){
                let status = tweetCell.querySelector('.tweet-status')
                status.innerHTML = 'False'
            })
        }
    })
}

let bindEvents = function() {
    bindEventTweetAdd()
    bindEventTweetDelete()
    bindEventTweetEdit()
    bindEventTweetUpdate()
}

let __main = function() {
    bindEvents()
    allTweets()
}

__main()
