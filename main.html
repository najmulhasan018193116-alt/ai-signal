
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Login Register</title>

<style>
body{
font-family:Arial;
background:#f5f5f5;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
}

.container{
width:350px;
background:white;
padding:20px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,0.1);
}

.tabs{
display:flex;
justify-content:space-around;
margin-bottom:20px;
}

.tabs button{
background:none;
border:none;
font-size:18px;
cursor:pointer;
}

input{
width:100%;
padding:10px;
margin:8px 0;
border-radius:5px;
border:1px solid #ccc;
}

button.main{
width:100%;
padding:12px;
border:none;
border-radius:20px;
background:#f5b400;
color:white;
font-size:16px;
}

.hidden{
display:none;
}
</style>
</head>

<body>

<div class="container">

<div class="tabs">
<button onclick="showLogin()">Login</button>
<button onclick="showRegister()">Register</button>
</div>

<!-- LOGIN -->
<div id="loginPage">

<input id="loginPhone" placeholder="Phone number">

<input type="password" id="loginPass" placeholder="Password">

<button class="main" onclick="loginUser()">Login</button>

<p onclick="showReset()" style="cursor:pointer">Forgot password</p>

</div>

<!-- REGISTER -->
<div id="registerPage" class="hidden">

<input id="regPhone" placeholder="Phone number">

<input type="password" id="regPass" placeholder="Password">

<input type="password" id="regConfirm" placeholder="Confirm Password">

<input id="refCode" placeholder="Referral Code">

<label>
<input type="checkbox" id="agree"> I agree privacy
</label>

<button class="main" onclick="registerUser()">Register</button>

</div>

<!-- RESET PASSWORD -->
<div id="resetPage" class="hidden">

<input id="resetPhone" placeholder="Phone number">

<button onclick="sendOTP()">Send Code</button>

<input id="otpInput" placeholder="Enter OTP">

<input type="password" id="newPass" placeholder="New Password">

<button onclick="resetPassword()">Change Password</button>

</div>

</div>

<script>

let otp="";

function showRegister(){
document.getElementById("loginPage").style.display="none";
document.getElementById("registerPage").style.display="block";
document.getElementById("resetPage").style.display="none";
}

function showLogin(){
document.getElementById("loginPage").style.display="block";
document.getElementById("registerPage").style.display="none";
document.getElementById("resetPage").style.display="none";
}

function showReset(){
document.getElementById("loginPage").style.display="none";
document.getElementById("registerPage").style.display="none";
document.getElementById("resetPage").style.display="block";
}

function registerUser(){

let phone=document.getElementById("regPhone").value;
let pass=document.getElementById("regPass").value;
let confirm=document.getElementById("regConfirm").value;
let ref=document.getElementById("refCode").value;
let agree=document.getElementById("agree").checked;

if(phone.length!=11){
alert("Phone number must be 11 digits");
return;
}

if(pass==""){
alert("Password required");
return;
}

if(confirm==""){
alert("Confirm password required");
return;
}

if(pass!=confirm){
alert("Password not match");
return;
}

if(ref==""){
alert("Referral code required");
return;
}

if(!agree){
alert("Please agree privacy");
return;
}

localStorage.setItem("phone",phone);
localStorage.setItem("pass",pass);

alert("Registration successful");

showLogin();

}

function loginUser(){

let phone=document.getElementById("loginPhone").value;
let pass=document.getElementById("loginPass").value;

let savedPhone=localStorage.getItem("phone");
let savedPass=localStorage.getItem("pass");

if(phone==savedPhone && pass==savedPass){
alert("Login success");
}else{
alert("Wrong phone or password");
}

}

function sendOTP(){

let phone=document.getElementById("resetPhone").value;
let savedPhone=localStorage.getItem("phone");

if(phone!=savedPhone){
alert("Phone not registered");
return;
}

otp=Math.floor(1000+Math.random()*9000);

alert("OTP Code: "+otp);

}

function resetPassword(){

let input=document.getElementById("otpInput").value;
let newPass=document.getElementById("newPass").value;

if(input!=otp){
alert("Wrong OTP");
return;
}

localStorage.setItem("pass",newPass);

alert("Password changed");

showLogin();

}

</script>

</body>
</html>
