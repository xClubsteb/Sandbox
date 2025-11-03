let q1Buttons = document.querySelectorAll("#question1 .btn");
let q2Buttons = document.querySelectorAll("#question2 .btn");

let response = document.getElementById("response_section");
let user_input = document.getElementById("user_input");
let submitBtn = document.getElementById("submit");

q1Buttons.forEach(button => {
    button.addEventListener("click", () => {

        console.log(button.id);

        q1Buttons.forEach(btn => {
            btn.style.backgroundColor = "";
        });

        const correct = "q1-btn3";
        if (correct == button.id){
            document.getElementById(button.id).style.backgroundColor = "#6abb61"
            document.getElementById("q1-p").textContent = "Correct!";
        }
        else{
            document.getElementById(button.id).style.backgroundColor = "#d67b7b"
            document.getElementById("q1-p").textContent = "Incorrect!";
        }
    });
});

q2Buttons.forEach(button => {
    button.addEventListener("click", () => {

        console.log(button.id);

        q2Buttons.forEach(btn => {
            btn.style.backgroundColor = "";
        });

        const correct = "q2-btn1";
        if (correct == button.id){
            document.getElementById(button.id).style.backgroundColor = "#6abb61"
            document.getElementById("q2-p").textContent = "Correct!";
        }
        else{
            document.getElementById(button.id).style.backgroundColor = "#d67b7b"
            document.getElementById("q2-p").textContent = "Incorrect!";
        }
    });
});

submitBtn.addEventListener("click", () => {
    const answer = user_input.value.trim().toLowerCase();
    const correct_answer = "africa";
    let display_text = document.getElementById("p-response");
    
    console.log(answer);
    if (correct_answer == answer){
        user_input.style.backgroundColor = "#6abb61";
        display_text.textContent = "Correct!";
    }
    else{
        user_input.style.backgroundColor = "#d67b7b";
        display_text.textContent = "Incorrect!";
    }
});