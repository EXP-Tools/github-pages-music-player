// 登录总开关
var showLogin = true;
if (mkPlayer.debug) {
    showLogin = false;
}

// Get the loginPanel and the musicContent div
var loginPanel = document.getElementById("loginPanel");
var musicContent = document.getElementById("musicContent");

// Display the loginPanel
window.onload = function (event) {
    if (showLogin) {
        loginPanel.style.display = "block";
    } else {
        loginPanel.style.display = "none";
        musicContent.style.display = "block";
    }
}

async function getCredentials() {
    try {
        const response = await fetch("static/pwd");
        const text = await response.text();
        const [username, passwordHash] = text.split(":");

        return {
            username,
            passwordHash
        };
    } catch (error) {
        console.error("Error fetching credentials:", error);
    }
}

async function checkAuthentication(event) {
    event.preventDefault();  // 阻止默认行为，避免刷新页面

    const credentials = await getCredentials();
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;

    // Hash the password entered by the user
    const passwordHash = await hashPassword(pass);

    if (credentials && user == credentials.username && passwordHash == credentials.passwordHash) {
        // alert("登陆成功");
        loginPanel.style.display = "none";
        musicContent.style.display = "block"; // 显示内容
    } else {
        alert("账号或密码错误");
    }
}

async function hashPassword(password) {
    // Encode the password as UTF-8
    const encoder = new TextEncoder();
    const data = encoder.encode(password);

    // Hash the password
    const hash = await window.crypto.subtle.digest('SHA-256', data);

    // Convert the hash to a hexadecimal string
    let hashArray = Array.from(new Uint8Array(hash));
    let hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

    return hashHex;
}