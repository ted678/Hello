function sendQuery() {
    const input = document.getElementById('query');
    const chat = document.getElementById('chat');
    
    // 检查输入内容
    if (!input.value.trim()) return;
    
    // 添加用户消息
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerHTML = `
        <div class="content">${input.value}</div>
    `;
    chat.appendChild(userMessage);
    
    // 发送请求到后端
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: input.value })
    })
    .then(response => response.json())
    .then(data => {
        // 检查响应内容
        if (data.response) {
            // 添加AI回复
            const aiMessage = document.createElement('div');
            aiMessage.className = 'message';
            aiMessage.innerHTML = `
                <div class="content">${data.response}</div>
            `;
            chat.appendChild(aiMessage);
            
            // 滚动到底部
            chat.scrollTop = chat.scrollHeight;
        }
    })
    .catch(error => console.error('Error:', error));
    
    // 清空输入框
    input.value = '';
}

// 添加回车键事件监听
document.getElementById('query').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // 阻止默认的回车换行行为
        sendQuery();
    }
});

// 在文件末尾添加
document.querySelector('button').addEventListener('click', sendQuery);

// 绑定所有侧边栏项目的点击事件
document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', function() {
        window.location.href = this.dataset.link;
    });
});