// script.js

// Function to fetch data from the API
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}

// Populate table dropdown
fetchData('http://localhost:5000/tables').then(tableNames => {
    const tableDropdown = document.getElementById('tableDropdown');
    tableNames.forEach(tableName => {
        const option = document.createElement('option');
        option.text = tableName;
        tableDropdown.add(option);
    });
    updateTable();
});

// Function to update table
function updateTable() {
    const tableName = document.getElementById('tableDropdown').value;
    fetchData(`http://localhost:5000/table/${tableName}`).then(data => {
        // Clear table
        const dataTable = document.getElementById('dataTable');
        dataTable.innerHTML = '';

        // Add headers
        const headerRow = dataTable.insertRow();
        for (const column in data[0]) {
            const headerCell = document.createElement('th');
            headerCell.textContent = column;
            headerRow.appendChild(headerCell);
        }

        // Add data rows
        data.forEach(row => {
            const dataRow = dataTable.insertRow();
            for (const column in row) {
                const dataCell = dataRow.insertCell();
                dataCell.textContent = row[column];
            }
        });
    });
}

// Update table when a new table is selected from the dropdown
document.getElementById('tableDropdown').addEventListener('change', updateTable);

// Mock functions for add, edit, and delete buttons
document.getElementById('addButton').addEventListener('click', function () {
    alert('Add button clicked');
});
document.getElementById('editButton').addEventListener('click', function () {
    alert('Edit button clicked');
});
document.getElementById('deleteButton').addEventListener('click', function () {
    alert('Delete button clicked');
});