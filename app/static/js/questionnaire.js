document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.querySelector('#student-form button');
    const errorMessage = document.getElementById('error-message');
    const statementContainer = document.getElementById('statement-container');
    const statementNumber = document.getElementById('statement-number');
    const choicesContainer = document.getElementById('choices-container');
    let currentStatement = null;

    startButton.addEventListener('click', checkStudent);

    async function checkStudent() {
        const studentNumber = document.getElementById('student_number').value;
        if (!studentNumber) {
            errorMessage.textContent = 'Voer een studentnummer in';
            return;
        }

        try {
            const response = await fetch(`/api/student/${studentNumber}/statement`);
            const data = await response.json();

            if (!response.ok) {
                errorMessage.textContent = data.error || 'Er is een fout opgetreden';
                return;
            }

            if (data.message === 'Alle stellingen voltooid') {
                errorMessage.textContent = data.message;
                return;
            }

            document.getElementById('student-form').classList.add('hidden');
            statementContainer.classList.remove('hidden');

            displayStatement(data);
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Er is een fout opgetreden bij het ophalen van de stelling';
        }
    }

    function displayStatement(statement) {
        currentStatement = statement;
        statementNumber.textContent = statement.statement_number;
        choicesContainer.innerHTML = '';

        statement.statement_choices.forEach(choice => {
            const button = document.createElement('button');
            button.className = 'choice-button';
            button.textContent = choice.choice_text;
            button.onclick = () => submitChoice(choice.choice_number);
            choicesContainer.appendChild(button);
        });
    }

    async function submitChoice(choiceNumber) {
        if (!currentStatement) return;

        const studentNumber = document.getElementById('student_number').value;
        try {
            const response = await fetch(`/api/student/${studentNumber}/statement/${currentStatement.statement_number}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    statement_choice: choiceNumber
                })
            });

            const data = await response.json();

            if (!response.ok) {
                errorMessage.textContent = data.error || 'Er is een fout opgetreden';
                return;
            }

            const nextResponse = await fetch(`/api/student/${studentNumber}/statement`);
            const nextData = await nextResponse.json();

            if (nextData.message === 'Alle stellingen voltooid') {
                statementContainer.innerHTML = `
                    <h2>Bedankt!</h2>
                    <p>Je hebt alle stellingen beantwoord.</p>
                    ${data.action_type ? `<p>Jouw Action Type is: ${data.action_type}</p>` : ''}
                `;
                return;
            }

            displayStatement(nextData);
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Er is een fout opgetreden bij het opslaan van je antwoord';
        }
    }
});