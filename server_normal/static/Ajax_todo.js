
//id title created_time updated_time
let todoTemplate = function (todo) {
    log('in todoTemplate')
    let id = todo.id
    let title = todo.title
    let ct = todo.created_time
    let ut = todo.updated_time
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
    log('in insertTodo')
    let todoCell = todoTemplate(todo)
    let todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

let allTodos = function () {
    log('in allTodos')
    ajaxTodoIndex(function (r) {
        let todos = JSON.parse(r)
        for (let i = 0; i < todos.length; i++) {
            let todo = todos[i]
            insertTodo(todo)
        }
    })

}


let __main = function() {
    allTodos()
}

__main()
