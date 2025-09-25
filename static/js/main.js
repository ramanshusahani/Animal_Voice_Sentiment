document.addEventListener('DOMContentLoaded', function() {
    const animalSelect = document.getElementById('animal-select');
    const soundSelect = document.getElementById('sound-select');
    const form = document.getElementById('animal-sound-form');
    const resultDisplay = document.getElementById('result-display');

    // Event listener for animal dropdown change
    animalSelect.addEventListener('change', function() {
        const selectedAnimal = this.value;
        
        if (selectedAnimal) {
            // Clear and disable sound dropdown while loading
            soundSelect.innerHTML = '<option value="">Loading sounds...</option>';
            soundSelect.disabled = true;
            
            // Fetch sounds for the selected animal
            fetch(`/get_sounds/${encodeURIComponent(selectedAnimal)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Clear the sound dropdown
                    soundSelect.innerHTML = '<option value="">-- Select a Sound --</option>';
                    
                    // Populate with new sounds
                    if (data.sounds && data.sounds.length > 0) {
                        data.sounds.forEach(sound => {
                            const option = document.createElement('option');
                            option.value = sound;
                            option.textContent = sound;
                            soundSelect.appendChild(option);
                        });
                        soundSelect.disabled = false;
                    } else {
                        soundSelect.innerHTML = '<option value="">No sounds available</option>';
                        soundSelect.disabled = true;
                    }
                })
                .catch(error => {
                    console.error('Error fetching sounds:', error);
                    soundSelect.innerHTML = '<option value="">Error loading sounds</option>';
                    soundSelect.disabled = true;
                });
        } else {
            // Reset sound dropdown if no animal is selected
            soundSelect.innerHTML = '<option value="">Select an animal first</option>';
            soundSelect.disabled = true;
        }
        
        // Hide previous results
        resultDisplay.classList.remove('result-visible');
    });

    // Event listener for form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent page reload
        
        const selectedAnimal = animalSelect.value;
        const selectedSound = soundSelect.value;
        
        // Validate selections
        if (!selectedAnimal || !selectedSound) {
            showResult('Please select both an animal and a sound.', 'error');
            return;
        }
        
        // Show loading message
        showResult('Loading...', 'loading');
        
        // Prepare data for POST request
        const requestData = {
            animal: selectedAnimal,
            sound: selectedSound
        };
        
        // Make POST request to get the "Call For" information
        fetch('/get_call_for', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.call_for) {
                const resultText = `🔍 <strong>${selectedAnimal}</strong> make a <strong>"${selectedSound}"</strong> sound for: <br><br>📢 ${data.call_for}`;
                showResult(resultText, 'success');
            } else {
                showResult('No information found for this combination.', 'error');
            }
        })
        .catch(error => {
            console.error('Error getting call for information:', error);
            showResult('Sorry, there was an error processing your request. Please try again.', 'error');
        });
    });

    // Helper function to display results
    function showResult(message, type) {
        resultDisplay.innerHTML = message;
        resultDisplay.className = type === 'error' ? 'error' : (type === 'loading' ? 'loading' : '');
        resultDisplay.classList.add('result-visible');
    }
});