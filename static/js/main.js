document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".record-form input, .record-form select, .record-form textarea")
        .forEach((field) => {
            if (!["checkbox", "hidden", "submit"].includes(field.type)) {
                field.classList.add("form-control");
            }
        });
});
