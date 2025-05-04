function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = "none";
    });
    document.getElementById(sectionId).style.display = "block";
}

function addDoctor() {
    alert("Functionality to add doctors will be implemented.");
}

// Sample Data
const doctors = [
    { id: 1, name: "Dr. John Doe", email: "johndoe@example.com" },
    { id: 2, name: "Dr. Jane Smith", email: "janesmith@example.com" }
];

const patients = [
    { id: 101, name: "Alice Johnson", age: 32, gender: "Female" },
    { id: 102, name: "Bob Williams", age: 45, gender: "Male" }
];

// Load Data
function loadDoctors() {
    const doctorList = document.getElementById("doctorList");
    doctors.forEach(doctor => {
        const row = `<tr>
            <td>${doctor.id}</td>
            <td>${doctor.name}</td>
            <td>${doctor.email}</td>
            <td><button class="btn btn-danger btn-sm">Remove</button></td>
        </tr>`;
        doctorList.innerHTML += row;
    });
}

function loadPatients() {
    const patientList = document.getElementById("patientList");
    patients.forEach(patient => {
        const row = `<tr>
            <td>${patient.id}</td>
            <td>${patient.name}</td>
            <td>${patient.age}</td>
            <td>${patient.gender}</td>
            <td><button class="btn btn-danger btn-sm">Remove</button></td>
        </tr>`;
        patientList.innerHTML += row;
    });
}

window.onload = function() {
    loadDoctors();
    loadPatients();
};
