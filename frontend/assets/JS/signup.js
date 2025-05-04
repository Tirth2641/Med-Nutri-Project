// document.getElementById("signupForm").addEventListener("submit", function (event) {
//     event.preventDefault();

//     const name = document.getElementById("name").value;
//     const email = document.getElementById("email").value;
//     const mobile = document.getElementById("mobile").value;
//     const password = document.getElementById("password").value;
//     const userType = document.getElementById("userType").value;
//     const age = document.getElementById("age").value || null;
//     const gender = document.getElementById("gender").value || null;

//     const data = {
//         name,
//         email,
//         mobile,
//         password,
//         user_type: userType,
//         age: age ? parseInt(age) : null,
//         gender: gender || null
//     };

//     fetch("http://127.0.0.1:5000/auth/signup/", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             window.location.href = userType === "patient" ? "Redirect_bot.html" : "Homepage.html";
//         } else {
//             alert("Signup failed: " + data.message);
//         }
//     })
//     .catch(error => console.error("Error:", error));
// });
function togglePatientFields() {
    const userType = document.getElementById("userType").value;
    document.getElementById("patientFields").style.display = userType === "patient" ? "block" : "none";
}

document.getElementById("signupForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const userType = document.getElementById("userType").value;
    const ageValue = document.getElementById("age").value;
    const genderValue = document.getElementById("gender").value;

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        mobile: document.getElementById("mobile").value,
        password: document.getElementById("password").value,
        user_type: userType,
        age: userType === "patient" && ageValue ? parseInt(ageValue) : null,
        gender: userType === "patient" && genderValue ? genderValue : null
    };

    fetch("http://127.0.0.1:7000/auth/signup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = userType === "patient" ? "Redirect_bot.html" : "Homepage.html";
        } else {
            alert("Signup failed: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));
});
        
