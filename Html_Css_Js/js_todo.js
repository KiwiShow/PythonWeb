let log = function () {
    console.log.apply(console, arguments)
}

log('loading script success')

let e = function (sel) {
    return document.querySelector(sel)
}

let input_box = e('#id-todo-input')
log(input_box)
let input_button = e('#id-todo-button')
log(input_button)
let todo_list = e('.class-todo-list-div')
log(todo_list)


let template_todo = function (todo_value) {
    return`<div class="class-todo-item-div">
        <text class="class-todo-content-text">${todo_value}</text>
        <button class="class-todo-delete-text">delete</button>
    </div>`
}

let insert_todo = function (todo_html) {
    todo_list.insertAdjacentHTML('beforeend', todo_html)
}

let on_input_clicked = function () {
    let input_value = input_box.value
    let todo_html = template_todo(input_value)
    insert_todo(todo_html)
}

let on_todo_list_clicked = function (sender) {
    log(sender)
    let target = sender.target
    if (target.classList.contains('class-todo-delete-text')){
        target.parentNode.remove()
    }
    else{
        log('on_todo_list_clicked ERROR')
    }
}

input_button.addEventListener('click', on_input_clicked)
todo_list.addEventListener('click', on_todo_list_clicked)


// 检查用户名是否符合如下规则
// 1，第一位是字母
// 2，最小长度2
// 3，只能字母或数字结尾
// 4，最大长度10
// 5，只能包含字母、数字、下划线
//
// <h3></h3> 标签
// 如果符合规则 设置标签的内容为 '检查合格'
// 如果不符合, 设置标签的内容为 '用户名错误'
// 当检查不符合规则后, 清空用户输入的内容

let name_node = e('#id-name-input')
let login_node = e('#id-login-button')
let result_node = e('#id-show-result')

let max_len = function (l) {
    return l >= 2 && l <= 10
}

let first_AZ = function (name) {
    return (name[0] >= 'a' && name[0] <= 'z') || (name[0] >= 'A' && name[0] <= 'Z')
}

let endRight = function(name, l){
	r = (name[l-1] >= 'a' && name[l-1] <= 'z') ||
        (name[l-1] >= 'A' && name[l-1] <= 'Z') ||
        (name[l-1] >= '0' && name[l-1] <= '9')
	return r
}

let isOnlyA_1 = function(name, l){
	let m = 0
	for (let i = 0; i < l; i++){
		if ((name[i] >='a'&& name[i]<='z')||
            (name[i]>='A'&&name[i]<='Z')||
            (name[i]>='0'&&name[i]<='9')||
            name[i]=='_'){
		m = m + 1
		}
	}
	return m === l
}

let check_login = function () {
    let name = name_node.value
    let l = name.length
	if (max_len(l) &&
        first_AZ(name) &&
        endRight(name, l) &&
        isOnlyA_1(name, l)){
		// result_node.innerHTML = 'ok'
        result_node.insertAdjacentHTML('beforeend', 'ok')
	}
	else{
		// result_node.innerHTML = 'error'
        result_node.insertAdjacentHTML('beforeend', 'error')
        name_node.value = ''

	}
}
// insertAdjacentHTML() 将指定的文本解析为HTML或XML，
// 并将结果节点插入到DOM树中的指定位置。
// 它不会重新解析它正在使用的元素，因此它不会破坏元素内的现有元素。
// 这避免了额外的序列化步骤，使其比直接innerHTML操作更快。
login_node.addEventListener('click', check_login)
