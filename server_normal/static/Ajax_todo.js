let todoUpdateFormTemplate = function () {
    let tem = `
        <div class="todo-update-form">
            <input class="todo-update-input">
            <button class="todo-update">更新</button>
    `
    return tem
}

//id title created_time updated_time
let todoTemplate = function (todo) {
    let id = todo.id
    let title = todo.title
    let ct = todo.created_time
    let ut = todo.updated_time
    // data-* 是 HTML5 新增的自定义标签属性的方法
    // data-id="1" 获取属性的方式是  .dataset.id
    let tem = `
        <div class="todo-cell" data-id="${id}">
            <span>通过ajax获得</span>
            <span class="todo-id">${id}</span>
            <span class="todo-title">${title}</span>
            <span>created@${ct}</span>
            <span>updated@${ut}</span>
            <button class="todo-edit" data-id="${id}">编辑</button>
            <button class="todo-delete" data-id="${id}">删除</button>
        </div>    
    `
    return tem
}

let insertTodo = function (todo) {
    let todoCell = todoTemplate(todo)
    let todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

let allTodos = function () {
    ajaxTodoIndex(function (r) {
        let todos = JSON.parse(r)
        for (let i = 0; i < todos.length; i++) {
            let todo = todos[i]
            insertTodo(todo)
        }
    })

}

let bindEventTodoAdd = function () {
    let b = e('#id-button-add')
    b.addEventListener('click', function () {
        let input = e('#id-input-todo')
        let title = input.value
        let form = {
            title: title,
        }
        ajaxTodoAdd(form, function (r) {
            let todo = JSON.parse(r)
            insertTodo(todo)
        })

    })

}

// 事件委托
let bindEventTodoDelete = function () {
    let todoList = e('.todo-list')
    todoList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('todo-delete')) {// 这里没有点符号
            let todoId = self.dataset.id
            ajaxTodoDelete(todoId, function (r) {
                self.parentElement.remove()
            })
        }

    })

}

let bindEventTodoEdit = function () {
    let todoList = e('.todo-list')
    todoList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('todo-edit')) {
            let t = todoUpdateFormTemplate()
            // 有个bug是每次点击都会出现input
            // 更好的做法是用CSS实现一个input框
            self.parentElement.insertAdjacentHTML('beforeend', t)
            // self.parentElement.innerHTML += t
        }
    })
}

let bindEventTodoUpdate = function () {
    let todoList = e('.todo-list')
    todoList.addEventListener('click', function (event) {
        let self = event.target
        if (self.classList.contains('todo-update')) {
            let todoCell = self.closest('.todo-cell')
            let input = todoCell.querySelector('.todo-update-input')
            let id = todoCell.dataset.id
            let form = {
                id: id,
                title: input.value,
            }
            ajaxTodoUpdate(form, function(r){
                let updateForm = self.closest('.todo-update-form')
                updateForm.remove()
                let todo = JSON.parse(r)
                let title = todoCell.querySelector('.todo-title')
                title.innerHTML = todo.title
                // title.value = todo.title
            })
        }
    })
}

let bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}


let __main = function() {
    bindEvents()
    allTodos()
}

__main()
