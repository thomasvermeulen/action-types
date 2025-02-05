document.addEventListener("DOMContentLoaded", function () {
    function toggleVisibility(buttonId, formId) {
        const button = document.getElementById(buttonId);
        const form = document.getElementById(formId);
        
        if (!button || !form) return;
        
        button.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            
            document.querySelectorAll(".side-form").forEach(f => {
                if (f !== form) f.classList.remove("show");
            });
            
            form.classList.toggle("show");
        });
    }
    
    toggleVisibility("add-student-button", "add-student-form");
    toggleVisibility("add-teacher-button", "add-teacher-form");
    
    document.querySelectorAll('.edit-student').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopImmediatePropagation();
            
            const editForm = document.getElementById('edit-student-form');
            document.getElementById('edit-student-number').value = this.dataset.studentNumber;
            document.getElementById('edit-student-name').value = this.dataset.name;
            document.getElementById('edit-student-class').value = this.dataset.class;
            document.getElementById('edit-student-team').value = this.dataset.team;
            document.getElementById('edit-student-form-action').action = `/admin/student/edit/${this.dataset.studentNumber}`;
            
            document.querySelectorAll(".side-form").forEach(f => {
                if (f !== editForm) f.classList.remove("show");
            });
            
            editForm.classList.add("show");
        });
    });
    
    function addCancelListener(cancelButtonId, formId) {
        const cancelButton = document.getElementById(cancelButtonId);
        const form = document.getElementById(formId);
        
        if (cancelButton && form) {
            cancelButton.addEventListener("click", function (e) {
                e.preventDefault();
                e.stopImmediatePropagation();
                form.classList.remove("show");
            });
        }
    }
    
    addCancelListener("cancel-student", "add-student-form");
    addCancelListener("cancel-teacher", "add-teacher-form");
    addCancelListener("cancel-edit", "edit-student-form");
    
    const classFilter = document.getElementById('class-filter');
    const teamFilter = document.getElementById('team-filter');
    
    if (classFilter) {
        classFilter.addEventListener('change', function () {
            const selectedClass = this.value;
            const selectedTeam = teamFilter.value;
            window.location.href = `?class=${selectedClass}&team=${selectedTeam}`;
        });
    }
    
    if (teamFilter) {
        teamFilter.addEventListener('change', function () {
            const selectedClass = classFilter.value;
            const selectedTeam = this.value;
            window.location.href = `?class=${selectedClass}&team=${selectedTeam}`;
        });
    }

    document.querySelectorAll(".view-statements").forEach(button => {
        button.addEventListener("click", async function () {
            const studentNumber = this.dataset.studentNumber;
            try {
                const response = await fetch(`/api/statements/${studentNumber}`);
                
                if (!response.ok) {
                    throw new Error(`API error: ${response.status}`);
                }

                const data = await response.json();
                if (!data.statements || data.statements.length === 0) {
                    document.getElementById("statements-list").innerHTML = "<li>Geen stellingen gevonden.</li>";
                } else {
                    document.getElementById("statements-list").innerHTML = 
                        data.statements.map(s => `<li>${s}</li>`).join("");
                }

                document.getElementById("statements-modal").classList.add("show");
            } catch (error) {
                console.error("Fout bij ophalen van stellingen:", error);
                document.getElementById("statements-list").innerHTML = 
                    "<li>Er is een fout opgetreden bij het ophalen van de stellingen.</li>";
                document.getElementById("statements-modal").classList.add("show");
            }
        });
    });

    document.getElementById("close-statements").addEventListener("click", function () {
        document.getElementById("statements-modal").classList.remove("show");
    });

    window.addEventListener("click", function(event) {
        const modal = document.getElementById("statements-modal");
        if (event.target === modal) {
            modal.classList.remove("show");
        }
    });
});