function populateMaterialNames(materialTypeSelectId, materialNameSelectId) {
    const materialType = document.getElementById(materialTypeSelectId).value;
    fetch(`/get_raw_materials/${materialType}`)
        .then(response => response.json())
        .then(materials => {
            const materialNameSelect = document.getElementById(materialNameSelectId);
            materialNameSelect.innerHTML = ''; // Clear previous options
            materials.forEach(name => {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                materialNameSelect.appendChild(option);
            });
        });
}

function calculateTotalRate() {
    const materialFields = document.querySelectorAll('.materialField');
    let totalRate = 0;
    let materials = [];

    materialFields.forEach((field, index) => {
        const materialName = document.getElementById(`materialName${index + 1}`).value;
        const quantity = parseInt(document.getElementById(`quantity${index + 1}`).value);
        materials.push({ name: materialName, quantity: quantity });

        // Sample rate calculation logic (replace with your actual rate calculation logic)
        const ratePerUnit = 2.5; // Assuming a rate of $2.5 per unit for demonstration
        const rate = quantity * ratePerUnit;
        totalRate += rate;
    });

    document.getElementById('result').innerHTML = `The total calculated rate is: $${totalRate.toFixed(2)}`;

    // Update quantities in the database
    fetch('/update_quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ materials: materials })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Quantities updated successfully!');
        }
    });
}
