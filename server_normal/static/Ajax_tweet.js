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

let commentUpdateFormTemplate = function () {
    let tem = `
        <div class="comment-update-form">
            <input class="comment-update-input">
            <button class="comment-update">更新</button>
    `
    return tem
}

//id title created_time updated_time
let tweetTemplate = function (tweet) {
    let id = tweet.id
    let content = tweet.content
    let user_id = tweet.user_id
    let user_name = tweet.user_name
    let ct = tweet.created_time
    let ut = tweet.updated_time
    let tem = `
        <div class="tweet-cell" data-id="${id}">
            <div class="tweet-pure-cell" data-id="${id}">
                <span class="tweet-content">${content}</span>
                <span class="tweet-user_id">from ${user_name}</span>
                <span class="tweet-ct">ct@${ct}</span>
                <span class="tweet-ut">ut@${ut}</span>
                <button class="tweet-delete" data-id="${id}">删除</button>
                <button class="tweet-edit" data-id="${id}">编辑</button>
            </div>
            <div class="comment-form" data-id="${id}">
                <h6>评论</h6>
                <div class="comment-list" data-id="${id}">
                    <!--comment-list goes here-->
                </div>
                <input type="hidden" name="tweet_id" value="${id}">
                <input class="comment-add-input" name="content">
                <br>
                <button class="comment-add" data-id="${id}">添加评论</button>
            </div>  
        </div> 
    `
    return tem
}

let commentTemplate = function (comment) {
    let id = comment.id
    let content = comment.content
    let user_id = comment.user_id
    let user_name = comment.user_name
    let tweet_id = comment.tweet_id
    let ct = comment.created_time
    let ut = comment.updated_time
    let tem = `
        <div class="comment-cell" data-id="${id}">
            <span class="comment-user_id">${user_name}: </span>
            <span class="comment-content">${content}</span>
            <span class="comment-ct">ct@${ct}</span>
            <span class="comment-ut">ut@${ut}</span>
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
                self.parentElement.parentElement.remove()
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
        // log(event.target)
        let self = event.target
        if (self.classList.contains('tweet-update')) {
            let tweetCell = self.closest('.tweet-pure-cell')
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
                let  tweet_ct = tweetCell.querySelector('.tweet-ct')
                let  tweet_ut = tweetCell.querySelector('.tweet-ut')
                content.innerHTML = tweet.content
                tweet_ct.innerHTML = tweet.created_time
                tweet_ut.innerHTML = tweet.updated_time
                // title.value = tweet.title
            })
        }
    })
}

// todo 搞懂self event target
// 出现的问题是a用户不管在http://localhost:3000/tweet/index?user_id=3
// 的情况下ajax交互界面显示依然a的tweet及其command。
// 试图通过go-to-user-input获得user_id传给ajaxapi，但是不成功。
// 因为每次go-to-user-button每次submit之后页面会重新渲染
// 所以如果go-to-user-input没有默认值则ajax没有数据显示，
// 有默认值则ajax一直显示默认user_id的数据😢
let bindEventCommentAdd = function () {
    let b = e('.tweet-list')
    b.addEventListener('click', function (event) {
        let self = event.target
        // log(self)
        // log(self.classList)
        if(self.classList.contains('comment-add')) {
            let commentForm = self.closest('.comment-form')
            let tweetId = commentForm.dataset.id
            let content = commentForm.querySelector('.comment-add-input').value
            let form = {
                tweet_id: tweetId,
                content: content,
            }
            ajaxCommentAdd(form, function(r) {
                // 收到返回的数据, 插入到页面中
                let comment = JSON.parse(r)
//                insertComment(comment)
                let input = commentForm.querySelector('.comment-add-input')
                input.value = ''
                insertComment(comment)

            })
        }

    })

}

let bindEventCommentDelete = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('comment-delete')) {
            let commentId = self.dataset.id
            ajaxCommentDelete(commentId, function (r) {
                self.parentElement.remove()
            })
        }

    })

}

let bindEventCommentEdit = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('comment-edit')) {
            let t = commentUpdateFormTemplate()
            // 有个bug是每次点击都会出现input
            // 更好的做法是用CSS实现一个input框
            self.parentElement.insertAdjacentHTML('beforeend', t)
            // self.parentElement.innerHTML += t
        }
    })
}

let bindEventCommentUpdate = function () {
    let tweetList = e('.tweet-list')
    tweetList.addEventListener('click', function (event) {
        // log(event.target)
        let self = event.target
        if (self.classList.contains('comment-update')) {
            let commentCell = self.closest('.comment-cell')
            let input = commentCell.querySelector('.comment-update-input')
            let id = commentCell.dataset.id
            let form = {
                id: id,
                content: input.value,
            }
            ajaxCommentUpdate(form, function(r){
                let updateForm = self.closest('.comment-update-form')
                updateForm.remove()
                let comment = JSON.parse(r)
                let  content = commentCell.querySelector('.comment-content')
                let  comment_ct = commentCell.querySelector('.comment-ct')
                let  comment_ut = commentCell.querySelector('.comment-ut')
                content.innerHTML = comment.content
                comment_ct.innerHTML = comment.created_time
                comment_ut.innerHTML = comment.updated_time
                // title.value = tweet.title
            })
        }
    })
}

let bindEvents = function() {
    bindEventTweetAdd()
    bindEventTweetDelete()
    bindEventTweetEdit()
    bindEventTweetUpdate()
    bindEventCommentAdd()
    bindEventCommentDelete()
    bindEventCommentEdit()
    bindEventCommentUpdate()
}

let __main = function() {
    allTweets()
    bindEvents()

}

__main()
