document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#profile').style.display = 'none'

    if (document.getElementById('following')) {
        document.getElementById('following').addEventListener('click', () => load_posts("/followed", 1))
    } else {
        document.getElementById('newPost').addEventListener('click', () => force_login())
    }

    load_posts("", 1)

    document.querySelector('form').onsubmit = create_post
})

function force_login() {
    document.getElementById('login').click()
}

function load_posts(addon, page) {
    if (addon.includes("?")) {
        addon += `&page=${page}`
    } else {
        document.querySelector('#profile').style.display = 'none'
        addon += `?page=${page}`
    }
    fetch(`/load${addon}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts)
        document.getElementById('posts').innerHTML = ''
        build_paginator(addon, page, posts.num_pages);
        posts.posts.forEach(post => {
            build_post(post)
        });
    })
}

function build_paginator(addon, page, num_pages) {
    page_list = document.getElementById('pagination')
    page_list.innerHTML = ""

    const previous = document.createElement('li')
    if(page == 1){
        previous.className = "page-item disabled"    
    } else {
        previous.className = "page-item"    
        previous.addEventListener('click', () => load_posts(addon, page-1));
    }        
    const page_a_previous = document.createElement('a')
    page_a_previous.className = "page-link"

    page_a_previous.href = "#"
    page_a_previous.innerHTML = "Previous"
    previous.append(page_a_previous)   
    page_list.append(previous)
    
    for (let item = 1; item <= num_pages; item++) {
        const page_icon = document.createElement('li')  
        if(item == page) {
            page_icon.className = "page-item active"
        } else {
            page_icon.className = "page-item"
            page_icon.addEventListener('click', () => load_posts(addon, item))
        }        
        const page_a = document.createElement('a')
        page_a.className = "page-link"
        page_a.href = "#"
        page_a.innerHTML = item
        page_icon.append(page_a)

        page_list.append(page_icon)
    }
    
    const next = document.createElement('li')        
    if(page == num_pages){
        next.className = "page-item disabled"    
    } else {
        next.className = "page-item"    
        next.addEventListener('click', () => load_posts(addon, page+1))
    }   
    const page_a_next = document.createElement('a')
    page_a_next.className = "page-link"
    page_a_next.href = "#"
    page_a_next.innerHTML = "Next"
    next.append(page_a_next)
    page_list.append(next)
}

function create_post() {
    const content = document.querySelector('#post_content').value

    fetch('/create_post', {
        method: "POST",
        headers: {
            'X-CSRFToken': getCookie("csrftoken")
        },
        body: JSON.stringify({
            post: content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message) 
    })
}

function build_post(post) {
    const post_card = document.createElement('div')
    post_card.className = "card"

    const header = document.createElement('div')
    header.className = "card-header profile"
    header.id = "post-author"
    header.innerHTML = post.author_username
    post_card.append(header)
    header.addEventListener('click', () => show_profile(post.author_id))

    const card_body = document.createElement('div')
    card_body.className = "card-body"
    card_body.id = `post_body_${post.id}`
    
    const content = document.createElement('p')
    content.className = "card-text"
    content.id = `post_content_${post.id}` 
    content.innerHTML = post.post
    card_body.append(content)
    
    const likes_row = document.createElement('div')
    likes_row.id = `likes_row_${post.id}`
    likes_row.className = "row align-items-center"

    const timestamp = document.createElement('div')
    timestamp.className = "footer col-auto text-muted"
    timestamp.innerHTML = post.date
    likes_row.append(timestamp)

    const likes = document.createElement('div')
    likes.id = `likes-amount-${post.id}`
    likes.className = "card-text likes col-auto"
    likes.innerHTML = post.likes
    likes_row.append(likes)

    const likes_text = document.createElement('div')
    likes_text.innerHTML = "like"
    likes_text.id = "likes-text"
    likes_row.append(likes_text)

    const like_button = document.createElement('button')
    like_button.id = `like-button-${post.id}`
    like_button.className = "btn btn-primary"
    if (post.liked) {
        like_button.innerHTML = "Unlike"
    } else {
        like_button.innerHTML = "Like"
    }
    likes_row.append(like_button)

    like_button.addEventListener('click', () => update_like(post))

    if (post.editable) {
        const edit = document.createElement('button')
        edit.className = "card-text col-auto btn btn-link" 
        edit.innerHTML = "Edit"
        edit.addEventListener('click', () => edit_post(post))   
        likes_row.append(edit)
    }

    card_body.append(likes_row)
    post_card.append(card_body)

    document.querySelector('#posts').append(post_card)
}

function update_like(post) {
    fetch(`/post/${post.id}/update_like`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            document.getElementById(`like-button-${post.id}`).innerHTML = "Unlike"
        } else {
            document.getElementById(`like-button-${post.id}`).innerHTML = "Like"            
        }
        document.getElementById(`likes-amount-${post.id}`).innerHTML = response.newAmount
    
        console.log(response)
    })
}

function show_profile(author_id) {
    load_posts(`?profile=${author_id}`, 1)
    document.querySelector('#profile').style.display = 'block'
    document.querySelector('#newPost').style.display = 'none'
    follow_button = document.getElementById('follow-button')
    follow_button.style.display = 'none'
    fetch(`/profile/${author_id}`)
    .then(response => response.json())
    .then(profile => {
        console.log(profile)
        document.getElementById('followers-amount').innerHTML = profile.followers
        document.getElementById('following-amount').innerHTML = profile.following
        document.getElementById('posts-amount').innerHTML = profile.posts
        document.getElementById('profile-username').innerHTML = profile.user_username
        if (profile.follow_available) {
            follow_button.style.display = 'unset'
            if (profile.currently_following) {
                follow_button.innerHTML = "Unfollow"
            } else {
                follow_button.innerHTML = "Follow"
            }
        }
        follow_button.addEventListener('click', () => update_follow(author_id))
    })
    window.scrollTo(0, 0)
}

function update_follow(author_id) {
    fetch(`/profile/${author_id}/update_follow`)
    .then(response => response.json())
    .then(response => {
        follow_button = document.getElementById('follow-button')
        if (response.newFollower) {
            follow_button.innerHTML = "Unfollow"
        } else {
            follow_button.innerHTML = "Follow"
        }
        document.getElementById('followers-amount').innerHTML = response.newAmount

        console.log(response)
    })
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function edit_post(post) {
    const content = document.getElementById(`post_content_${post.id}`)
    const likes_row = document.getElementById(`likes_row_${post.id}`)
        
    const post_body = content.parentNode
        
    const new_content_form = document.createElement('input')
    new_content_form.id = `new_content_${post.id}`
    new_content_form.type = "textarea"
    new_content_form.className = "form-control col-8"
    new_content_form.value = content.innerHTML
    post_body.append(new_content_form)

    document.getElementById(`post_content_${post.id}`).remove()
    document.getElementById(`likes_row_${post.id}`).remove()

    const save_button = document.createElement('button')
    save_button.className = "btn btn-info"
    save_button.innerHTML = "Save"
    post_body.append(save_button)

    save_button.addEventListener("click", () => {
        const new_content = document.getElementById(`new_content_${post.id}`).value
        fetch('/create_post', {
            method: "PUT",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                post_id: post.id,
                new_content: new_content
            })
        })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                content.innerHTML = new_content
            } else {
                alert("You can't edit this post!")
            }
            new_content_form.remove()
            save_button.remove()
            cancel_button.remove()
            post_body.append(content)
            post_body.append(likes_row)
        })
    })

    const cancel_button = document.createElement("button")
    cancel_button.className = "btn btn-danger"
    cancel_button.innerHTML = "Cancel"
    post_body.append(cancel_button)

    cancel_button.addEventListener('click', () => {
        new_content_form.remove()
        save_button.remove()
        cancel_button.remove()
        post_body.append(content)
        post_body.append(likes_row)
    })
}