function openModal(content) {
  const modal = document.getElementById("planModal");
  const modalContent = document.getElementById("modalContent");
  modalContent.innerHTML = content; // Inject content into modal
  modal.style.display = "block"; // Show modal
}

function closeModal() {
  const modal = document.getElementById("planModal");
  modal.style.display = "none"; // Hide modal
}

function convertReminderToParagraph(reminder) {
  if (!reminder || typeof reminder !== "object") {
    return "No valid reminder details available.";
  }

  let paragraph = "";
  Object.entries(reminder).forEach(([medicine, details]) => {
    const { Timing, meal_timing } = details;
    const timings = Array.isArray(Timing) ? Timing.join(", ") : "Not specified";
    const mealTimingText = meal_timing ? meal_timing.toLowerCase() : "unspecified";
    paragraph += `${medicine}: Should be taken ${mealTimingText} a meal, at these times: ${timings}. `;
  });

  return paragraph.trim();
}

function convertNutritionPlanToParagraph(planStr) {
  let plan;
  try {
    // Parse the input string into a JSON object
    plan = JSON.parse(planStr);
  } catch (error) {
    // Handle invalid JSON input
    return "Invalid plan format. Please provide a valid JSON string.";
  }

  // Validate the structure of the parsed data
  if (!plan || typeof plan !== "object" || !plan.meal_plan) {
    return "Meal plan data is either missing or improperly structured.";
  }

  const { meal_plan: mealPlan } = plan;
  const day = mealPlan.day || "Single Day Meal Plan";

  // Initialize the paragraph with the day title
  let paragraph = `<p><strong>Meal Plan for:</strong> ${day}</p>`;

  // Define the order of meals
  const mealTimes = ["breakfast", "lunch", "afternoon_snack", "dinner", "evening_snack"];

  // Add details for each meal
  mealTimes.forEach(mealTime => {
    const mealDetails = mealPlan[mealTime] || {};
    const mealName = mealDetails.meal || "No meal specified";
    const description = mealDetails.description || "No description available";
    const notes = mealDetails.notes || "No notes provided";

    // Capitalize the first letter of mealTime
    const capitalizedMealTime = mealTime.charAt(0).toUpperCase() + mealTime.slice(1).replace("_", " ");

    paragraph += `<p><strong>${capitalizedMealTime}:</strong></p>`;
    paragraph += `<p>Meal: ${mealName}</p>`;
    paragraph += `<p>Description: ${description}</p>`;
    paragraph += `<p>Notes: ${notes}</p>`;
  });

  return paragraph.trim();
}


function fetchPlans() {
  fetch('http://127.0.0.1:7000/api/doctor/plans')
    .then(res => res.json())
    .then(data => {
      const medList = document.getElementById("medPlanList");
      const nutriList = document.getElementById("nutriPlanList");
      medList.innerHTML = "";
      nutriList.innerHTML = "";

      if (!data.medications?.length) {
        medList.innerHTML = "<li class='list-group-item'>No medication plans found</li>";
      }

      if (!data.nutritions?.length) {
        nutriList.innerHTML = "<li class='list-group-item'>No nutrition plans found</li>";
      }

      data.medications?.forEach(plan => {
        const fplan = convertReminderToParagraph(JSON.parse(plan.reminder));
        const approvalText = plan.approved ? 'Approved' : 'Not Approved';

        medList.innerHTML += `
              <li class="list-group-item">
                <strong>Reminder ID:</strong> ${plan.mid}<br>
                <strong>Name:</strong> ${plan.name}<br>
                <strong>Details:</strong> ${fplan}<br>
                <strong>Approval Status:</strong> <span style="color: ${plan.approved ? 'green' : 'red'};">${approvalText}</span>
                <button class="approve-btn" onclick="approvePlan('${plan.mid}', 'medication', '${plan.pid}')">Approve</button>
              </li>`;
      });

      data.nutritions?.forEach(plan => {
        const fplan = convertNutritionPlanToParagraph(plan.plan);
        const approvalText = plan.approved ? 'Approved' : 'Not Approved';

        nutriList.innerHTML += `
              <li class="list-group-item">
                <strong>Plan Name:</strong> ${plan.plan_name}<br>
                <strong>Approval Status:</strong> <span style="color: ${plan.approved ? 'green' : 'red'};">${approvalText}</span><br><br>
                <button onclick="openModal('${fplan}')" style="background-color: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">View Details</button>
               
                <button class="approve-btn" onclick="approvePlan('${plan.nid}', 'nutrition', '${plan.pid}')">Approve</button>
              </li>`;
      });
    })
    .catch(err => {
      console.error("Error fetching plans:", err);
      alert("Failed to load plans. Please try again later.");
    });
}

function approvePlan(planId, type, patientId) {
  fetch('http://127.0.0.1:7000/api/approve-plan', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plan_id: planId, plan_type: type })
  })
    .then(res => res.json())
    .then(response => {
      alert(response.message || "Plan approved successfully.");
      sendTelegramMessage(patientId, type);
      fetchPlans();
    })
    .catch(error => {
      console.error("Approval error:", error);
      alert("Failed to approve plan. Please try again later.");
    });
}


function logout() {
  fetch('http://127.0.0.1:7000/api/logout', { method: 'POST' })
    .then(() => window.location.href = 'login.html');
}

window.onload = fetchPlans;
